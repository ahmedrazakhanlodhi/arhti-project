"""07_spatial_stats.py: Q1 spatial statistics as prespecified in D018 (weights/permutations/seed), plus labelled extras.

    .venv/bin/python -I scripts/07_spatial_stats.py      (after 06_raster_context.py)

Unit of analysis (gate, D014/D024): tehsil if administrative assignment >= 95% of rural populated mouzas, else district.
The other level is reported as a labelled MAUP comparison. Scenarios: Cholistan option A (primary) and B (sensitivity, D015).
Q1 sample: units with zero rural populated mouzas have undefined shares and are excluded (D028); n is reported everywhere.

Weights (prespecified): Queen contiguity, row-standardised (primary); kNN k=5 from GEODESIC centroid distances,
row-standardised (sensitivity, D026). 999 permutations, seed 20261031. LISA reported at p<0.05, p<0.01 and FDR(0.05).
Regression (EXPLORATORY): OLS (HC3) + spatial error model (prespecified check) + spatial lag model (POST-HOC, D019),
LM diagnostics, leave-one-out jackknife ranges (POST-HOC). No model is chosen on significance.
"""

from __future__ import annotations

import datetime as dt
import importlib.util
import sys
import warnings
from pathlib import Path

import esda
import geopandas as gpd
import numpy as np
import pandas as pd
import spreg
import statsmodels.api as sm
from libpysal.weights import Queen
from statsmodels.stats.outliers_influence import variance_inflation_factor

warnings.filterwarnings("ignore")
np.seterr(all="ignore")
ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("common", ROOT / "scripts" / "common.py")
common = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(common)

GPKG = ROOT / "data" / "processed" / "punjab_credit_context.gpkg"
OUT = ROOT / "outputs" / "tables"
SEED, PERM, ALPHA, ALPHA2, K = 20261031, 999, 0.05, 0.01, 5
GATE, PUNJAB_RP = 0.95, 23130
VINTAGE = ("Mouza Census 2020 (PBS, Jan-Mar 2020; enumerator-reported availability); ESA WorldCover 2021; "
           "MAP Accessibility to Cities 2015; OCHA COD-AB boundaries (valid_on 2022-09-09). Vintages differ")
QUAD = {1: "High-High", 2: "Low-High", 3: "Low-Low", 4: "High-Low"}
CATS = ["High-High", "Low-Low", "High-Low", "Low-High", "not significant"]
X_VARS = ["commercial_share", "ztbl_share", "onlinebank_over25km_share", "tt_city_cropw_hours", "cropland_share",
          "road_metalled_share"]
LAYERS = {("tehsil", "A"): "tehsil", ("tehsil", "B"): "tehsil_optB", ("district", "A"): "district", ("district", "B"): "district_optB"}
WNAMES = ["Queen", "kNN-5 (geodesic)"]


def load(level, scen):
    g = gpd.read_file(GPKG, layer=LAYERS[(level, scen)]).to_crs(common.CRS)
    name, pc = ("adm3_name", "adm3_pcode") if level == "tehsil" else ("adm2_name", "adm2_pcode")
    g = g.rename(columns={name: "unit", pc: "pcode"})
    g["tt_city_cropw_hours"] = g.tt_city_cropw_mean_min / 60
    excluded = g[g.arhti_share.isna()][["unit", "rp_mouzas"]]
    g = g[g.arhti_share.notna()].reset_index(drop=True)
    return g, excluded


def weights(g):
    wq = Queen.from_dataframe(g, use_index=False, silence_warnings=True)
    wk = common.geodesic_knn(g, k=K)
    info = {}
    for nm, w in zip(WNAMES, [wq, wk]):
        card = list(w.cardinalities.values())
        info[nm] = dict(n=w.n, islands=[g.unit[i] for i in w.islands], components=w.n_components,
                        min_nb=min(card), mean_nb=float(np.mean(card)), max_nb=max(card))
        w.transform = "r"
    return dict(zip(WNAMES, [wq, wk])), info


def gmoran(y, w):
    np.random.seed(SEED)
    m = esda.Moran(y, w, permutations=PERM)
    return dict(I=m.I, EI=m.EI, z_perm=m.z_sim, p_perm=m.p_sim, z_norm=m.z_norm, p_norm=m.p_norm)


def lisa(g, y, w, bv=None):
    l = (esda.Moran_Local(y, w, permutations=PERM, seed=SEED, n_jobs=1) if bv is None else
         esda.Moran_Local_BV(y, bv, w, permutations=PERM, seed=SEED, n_jobs=1))
    cut = esda.fdr(l.p_sim, ALPHA)
    # esda.fdr returns alpha/n (Bonferroni) when NO p-value passes Benjamini-Hochberg; flag that case (D036)
    n_ = len(l.p_sim)
    bh_pass = np.sort(l.p_sim)[::-1] < np.arange(n_, 0, -1) * ALPHA / n_
    fallback = not bh_pass.any()
    d = pd.DataFrame({"unit": g.unit, "pcode": g.pcode, "Ii": l.Is, "quadrant": [QUAD[q] for q in l.q], "p_sim": l.p_sim})
    d["cluster_p05"] = np.where(d.p_sim < ALPHA, d.quadrant, "not significant")
    d["cluster_p01"] = np.where(d.p_sim < ALPHA2, d.quadrant, "not significant")
    # true Benjamini-Hochberg: when no p-value passes, nothing is rejected (esda's alpha/n fallback is not used for labels)
    d["cluster_fdr05"] = np.where((d.p_sim <= cut) & (not fallback), d.quadrant, "not significant")
    d["fdr_cutoff"] = np.nan if fallback else cut
    d["bh_fallback_bonferroni"] = fallback
    return d


def counts(d):
    return pd.DataFrame({c: d[c].value_counts().reindex(CATS, fill_value=0) for c in ["cluster_p05", "cluster_p01", "cluster_fdr05"]})


def models(g, w):
    y = g.arhti_share.values
    X = g[X_VARS]
    Xc = sm.add_constant(X)
    ols = sm.OLS(y, Xc).fit(cov_type="HC3")
    ols_plain = sm.OLS(y, Xc).fit()
    vif = pd.Series([variance_inflation_factor(Xc.values, i) for i in range(1, Xc.shape[1])], index=X_VARS)
    np.random.seed(SEED)
    rm = esda.Moran(ols.resid, w, permutations=PERM)
    sp = spreg.OLS(y[:, None], X.values, w=w, spat_diag=True, moran=True)
    err = spreg.ML_Error(y[:, None], X.values, w)
    lag = spreg.ML_Lag(y[:, None], X.values, w)
    rows = []
    for t, c, s, z, p in zip(["const"] + X_VARS, ols.params, ols.bse, ols.tvalues, ols.pvalues):
        rows.append(dict(model="OLS (HC3)", term=t, coef=c, se=s, stat=z, p=p, vif=vif.get(t, np.nan)))
    for nm, m, extra in [("Spatial error (ML; prespecified check)", err, "lambda"), ("Spatial lag (ML; POST-HOC)", lag, "rho")]:
        names = ["const"] + X_VARS + [extra]
        for t, c, s, zp in zip(names, np.asarray(m.betas).ravel(), np.asarray(m.std_err).ravel(), m.z_stat):
            rows.append(dict(model=nm, term=t, coef=c, se=s, stat=zp[0], p=zp[1], vif=np.nan))
    diag = dict(n=len(y), k=Xc.shape[1], ols_r2=ols.rsquared, ols_adj_r2=ols.rsquared_adj, ols_aic=ols_plain.aic,
                ols_loglik=ols_plain.llf, resid_moran_I=rm.I, resid_moran_p_perm=rm.p_sim,
                spreg_moran_z=sp.moran_res[1], spreg_moran_p=sp.moran_res[2], LM_error=sp.lm_error[0], LM_error_p=sp.lm_error[1],
                LM_lag=sp.lm_lag[0], LM_lag_p=sp.lm_lag[1], RLM_error=sp.rlm_error[0], RLM_error_p=sp.rlm_error[1],
                RLM_lag=sp.rlm_lag[0], RLM_lag_p=sp.rlm_lag[1], sem_loglik=err.logll, sem_aic=err.aic,
                sem_lambda=float(np.asarray(err.betas).ravel()[-1]), slm_loglik=lag.logll, slm_aic=lag.aic,
                slm_rho=float(np.asarray(lag.betas).ravel()[-1]), sem_prespecified_trigger_met=bool(rm.p_sim < ALPHA),
                max_vif=float(vif.max()), cond_number=float(np.linalg.cond(Xc.values)))
    for nm, m in [("sem", err), ("slm", lag)]:
        res = np.asarray(m.e_filtered if nm == "sem" else m.u).ravel()
        np.random.seed(SEED)
        r = esda.Moran(res, w, permutations=PERM)
        diag[f"{nm}_resid_moran_I"], diag[f"{nm}_resid_moran_p"] = r.I, r.p_sim
    return pd.DataFrame(rows), diag


def jackknife(g):
    """POST-HOC: leave-one-unit-out ranges of every coefficient in all three models (Queen rebuilt each time)."""
    rec = []
    for i in range(len(g)):
        gi = g.drop(index=i).reset_index(drop=True)
        wi = Queen.from_dataframe(gi, use_index=False, silence_warnings=True)
        if wi.islands:
            gi = gi.drop(index=wi.islands).reset_index(drop=True)
            wi = Queen.from_dataframe(gi, use_index=False, silence_warnings=True)
        wi.transform = "r"
        y, X = gi.arhti_share.values, gi[X_VARS]
        o = sm.OLS(y, sm.add_constant(X)).fit().params
        e = np.asarray(spreg.ML_Error(y[:, None], X.values, wi).betas).ravel()
        lg = np.asarray(spreg.ML_Lag(y[:, None], X.values, wi).betas).ravel()
        r = dict(dropped=g.unit[i])
        for j, v in enumerate(X_VARS):
            r[f"OLS|{v}"], r[f"SEM|{v}"], r[f"SLM|{v}"] = o[v], e[j + 1], lg[j + 1]
        r["SEM|lambda"], r["SLM|rho"] = e[-1], lg[-1]
        rec.append(r)
    jk = pd.DataFrame(rec)
    rng = []
    for c in jk.columns[1:]:
        m, v = c.split("|")
        rng.append(dict(model=m, term=v, min=jk[c].min(), max=jk[c].max(),
                        sign_changes=bool((jk[c] > 0).any() and (jk[c] < 0).any()), refits=len(jk)))
    return jk, pd.DataFrame(rng)


def descriptives(g):
    s = g.arhti_share
    return dict(n=len(g), arhti_mean=s.mean(), arhti_median=s.median(), arhti_min=s.min(), arhti_max=s.max(),
                arhti_zero=int((s == 0).sum()), commercial_median=g.commercial_share.median(),
                arhti_pooled=g.n_arhti.sum() / g.rp_mouzas.sum(), rp_mouzas=int(g.rp_mouzas.sum()))


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    assigned = gpd.read_file(GPKG, layer="tehsil").rp_mouzas.sum()
    q1 = "tehsil" if assigned / PUNJAB_RP >= GATE else "district"
    levels = [q1] + [l for l in ["tehsil", "district"] if l != q1]

    G, LS, LC, BV, DS, WI, MD, RG, store = [], [], [], [], [], [], [], [], {}
    for level in levels:
        role = "Q1 unit (gate)" if level == q1 else "MAUP comparison"
        for scen in ["A", "B"]:
            g, excl = load(level, scen)
            W_, info = weights(g)
            for wn, w in W_.items():
                if info[wn]["islands"]:
                    sys.exit(f"{level}/{scen}/{wn}: islands {info[wn]['islands']} (prespecified: drop and list); stopping for review")
                WI.append(dict(level=level, scenario=scen, weights=wn, **{k: (", ".join(v) if isinstance(v, list) else v)
                                                                            for k, v in info[wn].items()}))
                for var in ["arhti_share", "commercial_share"]:
                    G.append(dict(level=level, role=role, scenario=scen, variable=var, weights=wn, n=len(g), **gmoran(g[var].values, w)))
                np.random.seed(SEED)
                b = esda.Moran_BV(g.arhti_share.values, g.commercial_share.values, w, permutations=PERM)
                BV.append(dict(level=level, role=role, scenario=scen, weights=wn, n=len(g), I_bv=b.I, z_perm=b.z_sim, p_perm=b.p_sim))
                l = lisa(g, g.arhti_share.values, w)
                LS.append(l.assign(level=level, scenario=scen, weights=wn, analysis="LISA arhti_share"))
                c = counts(l)
                for cat in CATS:
                    LC.append(dict(level=level, role=role, scenario=scen, analysis="LISA arhti_share", weights=wn, n=len(g),
                                   cluster=cat, p05=int(c.loc[cat, "cluster_p05"]), p01=int(c.loc[cat, "cluster_p01"]),
                                   fdr05=int(c.loc[cat, "cluster_fdr05"]), bh_cutoff=l.fdr_cutoff.iloc[0],
                                   bh_fallback_bonferroni=bool(l.bh_fallback_bonferroni.iloc[0])))
                lb = lisa(g, g.arhti_share.values, w, bv=g.commercial_share.values)
                LS.append(lb.assign(level=level, scenario=scen, weights=wn, analysis="Bivariate LISA arhti x lag(commercial)"))
                cb = counts(lb)
                for cat in CATS:
                    LC.append(dict(level=level, role=role, scenario=scen, analysis="Bivariate LISA arhti x lag(commercial)",
                                   weights=wn, n=len(g), cluster=cat, p05=int(cb.loc[cat, "cluster_p05"]),
                                   p01=int(cb.loc[cat, "cluster_p01"]), fdr05=int(cb.loc[cat, "cluster_fdr05"]),
                                   bh_cutoff=lb.fdr_cutoff.iloc[0], bh_fallback_bonferroni=bool(lb.bh_fallback_bonferroni.iloc[0])))
            DS.append(dict(level=level, role=role, scenario=scen, excluded_zero_rp="; ".join(excl.unit), **descriptives(g)))
            store[(level, scen)] = g
            if scen == "A":
                coef, diag = models(g, W_["Queen"])
                MD.append(coef.assign(level=level, role=role, n=len(g)))
                RG.append(dict(level=level, role=role, weights="Queen", **diag))

    JR = []
    for level in levels:
        jk, rng = jackknife(store[(level, "A")])
        jk.assign(level=level).to_csv(OUT / f"jackknife_posthoc_{level}.csv", index=False)
        JR.append(rng.assign(level=level))

    gm, lsa, lc, bv = pd.DataFrame(G), pd.concat(LS), pd.DataFrame(LC), pd.DataFrame(BV)
    ds, wi, md, rg, jr = pd.DataFrame(DS), pd.DataFrame(WI), pd.concat(MD), pd.DataFrame(RG), pd.concat(JR)
    for df, nm in [(gm, "moran_global"), (lsa, "lisa_arhti"), (lc, "lisa_counts"), (bv, "moran_bivariate"),
                   (ds, "q1_descriptives"), (wi, "weights_summary"), (md, "models_arhti"), (rg, "regression_diagnostics"),
                   (jr, "jackknife_ranges")]:
        df.assign(permutations=PERM, seed=SEED, vintage=VINTAGE).to_csv(OUT / f"{nm}.csv", index=False)
    for old in ["ols_arhti.csv", "ols_diagnostics.csv", "sem_arhti.csv", "jackknife_posthoc.csv", "lisa_bivariate_arhti_commercial.csv",
                "analysis_data_district.csv"]:
        (OUT / old).unlink(missing_ok=True)   # superseded by the tables above
    for level in levels:
        store[(level, "A")].drop(columns="geometry").to_csv(OUT / f"analysis_data_{level}.csv", index=False)

    cooc = mouza_cooccurrence()
    cooc.assign(vintage=VINTAGE).to_csv(OUT / "mouza_cooccurrence.csv", index=False)
    sens = cholistan_sensitivity(levels, store, lsa)
    sens.assign(vintage=VINTAGE).to_csv(OUT / "cholistan_sensitivity.csv", index=False)
    write_summary(q1, assigned, gm, lc, bv, ds, wi, md, rg, jr, sens, lsa)
    crs_verification()
    print(f"Q1 unit: {q1}; n = {', '.join(f'{r.level}/{r.scenario}: {r.n}' for _, r in ds.iterrows())}; "
          f"Cholistan-sensitivity changed items: {len(sens)}")
    return 0


OLD_CRS = "ESRI:102028"   # analysis CRS before D025; used here only to document the change
CRS_PAIRS = [("Attock", "Bahawalpur"), ("Kasur", "Multan"), ("Rawalpindi", "Rahim Yar Khan"), ("Dera Ghazi Khan", "Sialkot"),
             ("Mianwali", "Okara")]
BOUNDARY_VINTAGE = "OCHA COD-AB Pakistan boundaries (valid_on 2022-09-09); Q1 units (scenario A)"


def crs_verification():
    """D025/D026 checks: analysis CRS vs ESRI:102028 (areas, centroid distances, grid north) and kNN-5 neighbour changes
    (geodesic kNN vs the earlier planar ESRI:102028 kNN). Writes crs_verification.csv and knn5_neighbour_changes_{level}.csv."""
    from libpysal.weights import KNN
    from pyproj import Transformer

    rows = []
    for level in ["district", "tehsil"]:
        g = gpd.read_file(GPKG, layer=LAYERS[(level, "A")])
        name, pc = ("adm3_name", "adm3_pcode") if level == "tehsil" else ("adm2_name", "adm2_pcode")
        g = g[g.arhti_share.notna()].reset_index(drop=True)
        new, old = g.to_crs(common.CRS), g.to_crs(OLD_CRS)
        rows += [(f"{level}: max |area new/old - 1|", float(np.abs(new.area / old.area - 1).max()), None, None),
                 (f"{level}: max |area new / OCHA area_sqkm - 1|", float(np.abs(new.area / 1e6 / g.area_sqkm - 1).max()), None, None)]
        w_new = common.geodesic_knn(new, k=K)
        c = old.geometry.centroid
        w_old = KNN(np.column_stack([c.x.values, c.y.values]), k=K)
        ch = []
        for i in range(len(g)):
            a, b = set(w_new.neighbors[i]), set(w_old.neighbors[i])
            if a != b:
                ch.append(dict(level=level, unit=g[name][i], pcode=g[pc][i],
                               dropped="; ".join(sorted(g[name][j] for j in b - a)),
                               added="; ".join(sorted(g[name][j] for j in a - b))))
        pd.DataFrame(ch).assign(vintage=BOUNDARY_VINTAGE).to_csv(OUT / f"knn5_neighbour_changes_{level}.csv", index=False)
        rows.append((f"{level}: units whose kNN-5 set changed (n = {len(g)})", len(ch), None, None))
        if level == "district":
            ll = common.centroid_lonlat(g)
            cn, co = new.geometry.centroid, old.geometry.centroid
            idx = {n: i for i, n in enumerate(g[name])}
            for a, b in CRS_PAIRS:
                i, j = idx[a], idx[b]
                geo = common.GEOD.inv(ll[i, 0], ll[i, 1], ll[j, 0], ll[j, 1])[2] / 1e3
                dn, do = cn[i].distance(cn[j]) / 1e3, co[i].distance(co[j]) / 1e3
                rows.append((f"distance {a}–{b} (km): geodesic / new CRS / old CRS", f"{geo:.1f} / {dn:.1f} / {do:.1f}",
                             round(dn / geo - 1, 4), round(do / geo - 1, 4)))
            # grid north vs true north at the Punjab centroid: direction of a short step due north, in projected units
            punjab = gpd.read_file(GPKG, layer=LAYERS[(level, "A")]).to_crs(common.CRS).union_all()   # all 36 districts
            p = gpd.GeoSeries([punjab.centroid], crs=common.CRS).to_crs(4326).iloc[0]
            t = Transformer.from_crs(4326, common.CRS, always_xy=True)
            (x0, x1), (y0, y1) = t.transform([p.x, p.x], [p.y, p.y + 0.01])
            rows.append(("new CRS: angle between grid north and true north at Punjab centroid (deg)",
                         round(float(np.degrees(np.arctan2(x1 - x0, y1 - y0))), 3), None, None))
    (pd.DataFrame(rows, columns=["check", "value", "rel_error_new", "rel_error_old"]).assign(vintage=BOUNDARY_VINTAGE)
       .to_csv(OUT / "crs_verification.csv", index=False))


COOC_X = {"commercial": "n_commercial", "ztbl": "n_ztbl", "onlinebank_in_mouza": "n_onlinebank_in_mouza",
          "coop": "n_coop", "mfb": "n_mfb", "any formal (commercial, ZTBL, cooperative or MFB)": "n_anyformal"}   # last three: D042
COOC_BREAKS = [0.80, 0.95, 1.053, 1.25]
COOC_LABELS = ["< 0.80", "0.80–0.95", "0.95–1.053 (≈ independence)", "1.053–1.25", "> 1.25"]


def mouza_cooccurrence():
    """EXPLORATORY (D035). Mouza-level records -> tehsil strata. Outputs only tehsil aggregates and pooled statistics."""
    from statsmodels.stats.contingency_tables import StratifiedTable
    spec = importlib.util.spec_from_file_location("m04", ROOT / "scripts" / "04_extract_mouza.py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    df = mod.load_excel()
    p = df[df.prv_desc == "PUNJAB"].copy()
    ind = mod.mouza_indicators(p, [])
    ind["source_code"] = "PB-" + p.dist_code.astype(str).str.zfill(3) + "-" + p.teh_code.astype(str).str.zfill(3)
    ind = ind[ind.rp_mouzas == 1]
    xw = pd.read_csv(ROOT / "data" / "interim" / "tehsil_crosswalk.csv")
    xw = xw[xw.validated == True]  # noqa: E712
    ind["pcode"] = ind.source_code.map(dict(zip(xw.source_code, xw.ocha_pcode)))
    ind["is_cholistan"] = ind.source_code.str.startswith("PB-999")
    names = dict(zip(gpd.read_file(GPKG, layer="tehsil").adm3_pcode, gpd.read_file(GPKG, layer="tehsil").adm3_name))
    rows = []
    for scen in ["A", "B"]:
        d = ind[ind.pcode.notna() & ~(ind.is_cholistan & (scen == "B"))]
        expected_n = PUNJAB_RP if scen == "A" else PUNJAB_RP - int(ind.is_cholistan.sum())
        assert len(d) == expected_n, f"scenario {scen}: {len(d)} mouzas != {expected_n}"
        a = d.n_arhti.astype(bool)
        d = d.assign(n_anyformal=(d.n_commercial.astype(bool) | d.n_ztbl.astype(bool) | d.n_coop.astype(bool) | d.n_mfb.astype(bool)).astype(int))
        for xn, col in COOC_X.items():
            x = d[col].astype(bool)
            tabs, dropped = [], 0
            for pc, g in d.groupby("pcode"):
                ga, gx = a[g.index], x[g.index]
                t = np.array([[(ga & gx).sum(), (ga & ~gx).sum()], [(~ga & gx).sum(), (~ga & ~gx).sum()]], dtype=float)
                if (t.sum(0) == 0).any() or (t.sum(1) == 0).any():
                    dropped += 1; continue
                tabs.append(t)
            st = StratifiedTable(tabs)
            pooled = np.sum(tabs, axis=0)                      # summed 2x2 over informative strata (descriptive only)
            lo, hi = st.oddsratio_pooled_confint(0.05)
            bd = st.test_equal_odds(adjust=True)
            cmh = st.test_null_odds(correction=True)
            rows.append(dict(record="pooled (Mantel-Haenszel)", scenario=scen, pair=f"arhti x {xn}", n_mouzas=int(sum(t.sum() for t in tabs)),
                             n_strata=len(tabs), strata_dropped_zero_margin=dropped, mh_or=st.oddsratio_pooled, ci95_low=lo, ci95_high=hi,
                             breslow_day_tarone_stat=bd.statistic, breslow_day_tarone_p=bd.pvalue, cmh_stat=cmh.statistic, cmh_p=cmh.pvalue,
                             n_both_sources=int(pooled[0, 0]), n_arhti_only=int(pooled[0, 1]), n_other_only=int(pooled[1, 0]),
                             n_neither=int(pooled[1, 1]), mouzas_in_dropped_strata=int(len(d) - pooled.sum())))
        # per tehsil, arhti x commercial
        for pc, g in d.groupby("pcode"):
            n = len(g); na, nc = int(g.n_arhti.sum()), int(g.n_commercial.sum()); nb = int((g.n_arhti.astype(bool) & g.n_commercial.astype(bool)).sum())
            est = (n >= 20) and na > 0 and nc > 0
            obs, exp_ = nb / n, (na / n) * (nc / n)
            ratio = obs / exp_ if est else np.nan
            rows.append(dict(record="tehsil (arhti x commercial)", scenario=scen, pcode=pc, tehsil=names.get(pc), n_mouzas=n, n_arhti=na,
                             n_commercial=nc, n_both=nb, share_arhti=na / n, share_commercial=nc / n, observed_both=obs,
                             expected_both_independence=exp_, obs_exp_ratio=ratio, estimable=est,
                             ratio_class=(COOC_LABELS[int(np.digitize(ratio, COOC_BREAKS))] if est else "not estimable")))
    return pd.DataFrame(rows).assign(label="EXPLORATORY; availability reports, not borrowing; association, not substitution or complementarity")


def cholistan_sensitivity(levels, store, lsa):
    rows = []
    for level in levels:
        gA, gB = store[(level, "A")], store[(level, "B")]
        sch, _, _ = common.choose_scheme(gA.arhti_share)
        cA, cB = dict(zip(gA.pcode, sch.find_bin(gA.arhti_share.values))), dict(zip(gB.pcode, sch.find_bin(gB.arhti_share.values)))
        ta, tc = gA.arhti_share.quantile([1 / 3, 2 / 3]).values, gA.commercial_share.quantile([1 / 3, 2 / 3]).values
        biv = lambda g: dict(zip(g.pcode, [f"A{a + 1}-C{c + 1}" for a, c in zip(np.digitize(g.arhti_share, ta, right=True),
                                                                                  np.digitize(g.commercial_share, tc, right=True))]))
        bA, bB = biv(gA), biv(gB)
        vA, vB, nm = dict(zip(gA.pcode, gA.arhti_share)), dict(zip(gB.pcode, gB.arhti_share)), dict(zip(gA.pcode, gA.unit))
        for p in sorted(set(cA) | set(cB)):
            base = dict(level=level, unit=nm.get(p), pcode=p, arhti_A=vA.get(p), arhti_B=vB.get(p))
            if vA.get(p) != vB.get(p):
                rows.append(dict(base, item="arhti_share value", option_A=round(vA.get(p), 3), option_B=round(vB.get(p), 3)))
            if cA.get(p) != cB.get(p):
                rows.append(dict(base, item="arhti_share map class (option-A breaks)", option_A=int(cA[p]) + 1, option_B=int(cB[p]) + 1))
            if bA.get(p) != bB.get(p):
                rows.append(dict(base, item="bivariate class (option-A tertiles)", option_A=bA.get(p), option_B=bB.get(p)))
        for an in ["LISA arhti_share", "Bivariate LISA arhti x lag(commercial)"]:
            for wn in WNAMES:
                sel = lambda s: lsa[(lsa.level == level) & (lsa.scenario == s) & (lsa.weights == wn) & (lsa.analysis == an)].set_index("pcode")
                la, lb = sel("A"), sel("B")
                for col in ["cluster_p05", "cluster_p01", "cluster_fdr05"]:
                    for p in la.index:
                        if la.loc[p, col] != lb.loc[p, col]:
                            rows.append(dict(level=level, unit=la.loc[p, "unit"], pcode=p, item=f"{an} | {wn} | {col}",
                                             option_A=la.loc[p, col], option_B=lb.loc[p, col], arhti_A=vA.get(p), arhti_B=vB.get(p)))
    return pd.DataFrame(rows, columns=["level", "unit", "pcode", "item", "option_A", "option_B", "arhti_A", "arhti_B"])


def write_summary(q1, assigned, gm, lc, bv, ds, wi, md, rg, jr, sens, lsa):
    f = lambda df: df.to_markdown(index=False, floatfmt=".3f")
    L = [f"# Spatial statistics summary: EXPLORATORY ({dt.date.today()})", "",
         f"Prespecified in D018. Administrative assignment {assigned:,.0f}/{PUNJAB_RP:,} ({assigned / PUNJAB_RP:.1%}) passes the 95% "
         f"gate, so **Q1 unit = {q1}**. The other level is a labelled MAUP comparison. Scenario A = Cholistan merged into its parent "
         f"tehsils (primary); B = Cholistan excluded (sensitivity, D015). Weights: Queen contiguity, row-standardised (primary); kNN-5 "
         f"from geodesic centroid distances, row-standardised (sensitivity, D026). {PERM} permutations, seed {SEED}. "
         f"CRS: {common.CRS_LABEL}. Data: {VINTAGE}.", "",
         "## Samples (Q1 excludes units with zero rural populated mouzas, D028)", "", f(ds), "", "## Weights", "", f(wi), "",
         "## Global Moran's I", "", f(gm.drop(columns=["z_norm", "p_norm"])), "",
         "## Bivariate global Moran's I (arhti_share at i vs spatial lag of commercial_share)", "", f(bv), "",
         "## LISA counts (p < 0.05, p < 0.01, FDR 0.05; `bh_cutoff` = Benjamini–Hochberg p-value cutoff for that run; "
         "`bh_fallback_bonferroni` = True if no p-value passed BH: cutoff shown as blank and no unit is FDR-significant)", "", f(lc), ""]
    for an in ["LISA arhti_share", "Bivariate LISA arhti x lag(commercial)"]:
        s = lsa[(lsa.level == q1) & (lsa.scenario == "A") & (lsa.weights == "Queen") & (lsa.analysis == an) & (lsa.p_sim < ALPHA)]
        L += [f"{an}: significant {q1}s (Queen, scenario A, p < 0.05; † = FDR survivor):", "",
              ", ".join(f"{r.unit} ({r.quadrant}{'†' if r.cluster_fdr05 != 'not significant' else ''})"
                        for _, r in s.sort_values(["quadrant", "p_sim"]).iterrows()) or "none", ""]
    L += ["## Regression (EXPLORATORY: OLS; spatial error = prespecified check; spatial lag = POST-HOC; none chosen on significance)", "",
          f(rg.set_index(["level", "role", "weights"]).T.reset_index().rename(columns={"index": "diagnostic"})), "",
          f(md[["level", "n", "model", "term", "coef", "se", "stat", "p", "vif"]]), "",
          "## Leave-one-out jackknife ranges (POST-HOC)", "", f(jr[["level", "model", "term", "min", "max", "sign_changes", "refits"]]), "",
          "## Mouza-level co-occurrence (EXPLORATORY, D035; pooled statistics only)", "",
          f(pd.read_csv(OUT / "mouza_cooccurrence.csv").query("record != 'tehsil (arhti x commercial)'").dropna(axis=1, how="all").drop(columns=["vintage", "label"], errors="ignore")), "",
          f"## Cholistan sensitivity (B vs A): {len(sens)} changed items (`cholistan_sensitivity.csv`)", "",
          f(sens) if len(sens) else "none", ""]
    (OUT / "spatial_stats_summary.md").write_text("\n".join(L) + "\n")


if __name__ == "__main__":
    sys.exit(main())
