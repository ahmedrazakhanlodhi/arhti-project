"""15_course_methods.py: additional spatial methods (all EXPLORATORY / post-hoc, D041), tables, layers and appendix figures.

    .venv/bin/python -I scripts/15_course_methods.py      (after 14_cost_context.py)

Q1 unit: tehsils, Cholistan option A, n = 137 (units with zero rural populated mouzas excluded, D028).
Q2 unit: 36 districts (counts only; SBP districts as reported, attribution under verification, D039).
Spatial statistics: 999 permutations, seed 20261031; weights row-standardised unless stated; FDR = Benjamini-Hochberg 0.05.

1. Weights sensitivity for global Moran's I: Queen, Rook, kNN-5 (geodesic), distance band (geodesic, smallest threshold
   leaving no unit without a neighbour), inverse distance within that band. Also Geary's C (Queen).
2. Moran scatterplot (Queen): standardised arhti_share vs its spatial lag; the slope is Moran's I.         -> Figure S7
3. Getis-Ord Gi* hot and cold spots (Queen with self, binary), p < 0.05 and FDR 0.05; compared with LISA.  -> Figure S8
4. Trend surface: OLS of arhti_share on centroid x, y (first and second order); residual map and Moran's I. -> Figure S9
5. Evenness: index of dissimilarity D (Duncan & Duncan 1955) for tehsils (mouzas reporting a source vs all rural
   populated mouzas) and districts (SBP subsistence borrower records vs farms under 12.5 acres; branches vs farms).
6. k-means district typology on standardised attributes, without and with location (x, y). k by silhouette.   -> Figure S10
7. Projection distortion (Tissot indicatrix): ESRI:102028 vs the analysis CRS.                              -> Figure S11
8. Classification histograms: equal interval, quantiles, natural breaks (k = 5) with GADF.                 -> Figure S12
9. Dasymetric dot layer: 1 dot = 1,000 farms under 12.5 acres, placed only on cropland (WorldCover 2021);
   district point layer of SBP subsistence borrower records (counts) for proportional symbols. Mapped in QGIS (Figure 6).

Writes outputs/tables/course_*.csv, layers course_* in outputs/arhti_project.gpkg, figures figS7-figS12.
"""

from __future__ import annotations

import importlib.util
import warnings
from pathlib import Path

import esda
import geopandas as gpd
import mapclassify
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import rasterio  # noqa: E402
import rasterio.mask  # noqa: E402
import statsmodels.api as sm  # noqa: E402
from libpysal.weights import W, Queen, Rook  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402
from pyproj import Geod, Proj, Transformer  # noqa: E402
from shapely.geometry import Point, Polygon  # noqa: E402
from sklearn.cluster import KMeans  # noqa: E402
from sklearn.metrics import silhouette_score  # noqa: E402

warnings.filterwarnings("ignore")
np.seterr(all="ignore")
ROOT = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


common = load("common", ROOT / "scripts" / "common.py")
figs = load("figs", ROOT / "scripts" / "09_figures.py")

PROC = ROOT / "data" / "processed" / "punjab_credit_context.gpkg"
GPKG = ROOT / "outputs" / "arhti_project.gpkg"
CROP = ROOT / "data" / "interim" / "worldcover_cropland_frac_1200.tif"
T, F = ROOT / "outputs" / "tables", ROOT / "outputs" / "figures"
SEED, PERM, ALPHA, K = 20261031, 999, 0.05, 5
DOT_FARMS = 1000
ATTR = "district as reported by SBP (attribution under verification)"
V_MC = "Mouza Census 2020 (PBS, Jan-Mar 2020; enumerator-reported availability); OCHA COD-AB boundaries (valid_on 2022-09-09)"
V_Q2 = (f"SBP, FY2023-24 (Jul 2023-Jun 2024), {ATTR}; Agricultural Census 2024 (PBS), sample-based, fieldwork 2024-25; "
        "SBP branch list 30 Jun 2024; not contemporaneous")
V_ALL = "Mouza Census 2020; SBP FY2023-24; Agricultural Census 2024; SBP branch list 30 Jun 2024; not contemporaneous"
TYPO_VARS = {"arhti_share": "arhti credit availability (share of mouzas)",
             "commercial_share": "commercial-bank credit availability (share of mouzas)",
             "small_farm_reach": "small-farm reach (records per 1,000 farms < 12.5 ac)",
             "rural_branches_per_10k_farms": "rural bank branches per 10,000 farms",
             "tenant_share": "tenant farms (share of farms)",
             "cropland_share": "cropland (share of area)"}


# ------------------------------------------------------------------------------------------ helpers
def tehsils():
    g = gpd.read_file(PROC, layer="tehsil").to_crs(common.CRS)
    g = g[g.arhti_share.notna()].reset_index(drop=True)
    return g.rename(columns={"adm3_name": "unit", "adm3_pcode": "pcode"})


def districts():
    return gpd.read_file(GPKG, layer="q2_districts_credit_allocation").to_crs(common.CRS)


def bh_cutoff(p, alpha=ALPHA):
    """Benjamini-Hochberg: largest p(i) <= i/n * alpha; None if no p-value passes (nothing rejected)."""
    p = np.sort(np.asarray(p)); n = len(p)
    ok = p <= np.arange(1, n + 1) / n * alpha
    return float(p[ok].max()) if ok.any() else None


def weights_set(g):
    d = common.geodesic_distance_matrix(common.centroid_lonlat(g))
    np.fill_diagonal(d, np.inf)
    band = float(d.min(axis=1).max())                    # every unit has >= 1 neighbour within this distance
    nb, wt_band, wt_inv = {}, {}, {}
    for i in range(len(g)):
        j = np.where(d[i] <= band)[0]
        nb[i] = list(j); wt_band[i] = [1.0] * len(j); wt_inv[i] = list(1.0 / (d[i, j] / 1000.0))
    ws = {"Queen": Queen.from_dataframe(g, use_index=False, silence_warnings=True),
          "Rook": Rook.from_dataframe(g, use_index=False, silence_warnings=True),
          "kNN-5 (geodesic)": common.geodesic_knn(g, k=K),
          f"Distance band (geodesic, {band / 1000:.1f} km)": W(nb, wt_band, silence_warnings=True),
          f"Inverse distance within {band / 1000:.1f} km": W(nb, wt_inv, silence_warnings=True)}
    for w in ws.values():
        w.transform = "r"
    return ws, band


def moran(y, w):
    np.random.seed(SEED)
    m = esda.Moran(y, w, permutations=PERM)
    return m


def save_layer(gdf, layer):
    gdf.to_crs(common.CRS).to_file(GPKG, layer=layer, driver="GPKG")


def map_footer(fig, lines):
    figs.footer(fig, lines)
    fig.texts[-1].set_text(fig.texts[-1].get_text().replace("scripts/09_figures.py", "scripts/15_course_methods.py"))


# ------------------------------------------------------------------------------------------ 1-3 autocorrelation
def autocorrelation(g):
    y = g.arhti_share.values
    ws, band = weights_set(g)
    rows = []
    for nm, w in ws.items():
        m = moran(y, w)
        card = list(w.cardinalities.values())
        rows.append(dict(statistic="Moran's I", weights=nm, value=m.I, expected=m.EI, z_perm=m.z_sim, p_perm=m.p_sim,
                         mean_neighbours=float(np.mean(card)), min_neighbours=min(card), islands=len(w.islands)))
    np.random.seed(SEED)
    gc = esda.Geary(y, ws["Queen"], permutations=PERM)
    rows.append(dict(statistic="Geary's C", weights="Queen", value=gc.C, expected=gc.EC, z_perm=gc.z_sim, p_perm=gc.p_sim,
                     mean_neighbours=float(np.mean(list(ws["Queen"].cardinalities.values()))), min_neighbours=None, islands=0))
    sens = pd.DataFrame(rows).assign(variable="arhti_share", level="tehsil", scenario="A", n=len(g), permutations=PERM,
                                     seed=SEED, transform="row-standardised", vintage=V_MC)
    sens.to_csv(T / "course_weights_sensitivity.csv", index=False)

    # Moran scatterplot (Figure S7)
    wq = ws["Queen"]
    z = (y - y.mean()) / y.std()
    lag = np.array([sum(wq.weights[i][k] * z[j] for k, j in enumerate(wq.neighbors[i])) for i in range(len(z))])
    I = sens.loc[sens.weights == "Queen", "value"].iloc[0]
    fig, ax = plt.subplots(figsize=(6.2, 5.6))
    quad = np.where((z >= 0) & (lag >= 0), "High-High", np.where((z < 0) & (lag < 0), "Low-Low",
                    np.where((z >= 0) & (lag < 0), "High-Low", "Low-High")))
    for q in ["High-High", "Low-Low", "High-Low", "Low-High"]:
        k = quad == q
        ax.scatter(z[k], lag[k], s=16, color=figs.LISA_C[q], edgecolor=figs.INK, linewidth=0.3, label=f"{q} quadrant (n = {k.sum()})", zorder=3)
    xs = np.linspace(z.min(), z.max(), 10)
    ax.plot(xs, I * xs, color=figs.INK, lw=1.2, zorder=4, label=f"Slope = Moran's I = {I:.3f}")
    ax.axhline(0, color=figs.MUTED, lw=0.6); ax.axvline(0, color=figs.MUTED, lw=0.6)
    ax.set_xlabel("arhti_share (standardised z)"); ax.set_ylabel("Spatial lag of z (mean of Queen neighbours)")
    ax.legend(frameon=False, fontsize=7, loc="upper left")
    ax.set_title("Figure S7. Moran scatterplot: reported arhti credit availability, tehsils", loc="left", fontsize=9, fontweight="bold")
    fig.text(0.01, -0.06, "\n".join([
        f"Data: {V_MC}. n = {len(g)} tehsils (Cholistan option A).",
        f"Weights: Queen contiguity, row-standardised; {PERM} permutations, seed {SEED}. Quadrants show where each tehsil sits, not significance.",
        f"Not a map (no north arrow or scale bar). {figs.AUTHOR}. Script: scripts/15_course_methods.py."]), fontsize=6.2, color=figs.MUTED, va="top")
    figs.save(fig, "figS7_moran_scatterplot")

    # Getis-Ord Gi* (Figure S8)
    wb = Queen.from_dataframe(g, use_index=False, silence_warnings=True)
    wb.transform = "b"
    gi = esda.G_Local(y, wb, star=True, permutations=PERM, seed=SEED, n_jobs=1)
    cut = bh_cutoff(gi.p_sim)
    lab = np.where(gi.Zs > 0, "Hot spot", "Cold spot")
    g["gistar_z"] = gi.Zs
    g["gistar_p"] = gi.p_sim
    g["gistar_p05"] = np.where(gi.p_sim < ALPHA, lab, "not significant")
    g["gistar_fdr05"] = np.where((cut is not None) & (gi.p_sim <= (cut or 0)), lab, "not significant")
    lisa = pd.read_csv(T / "lisa_arhti.csv")
    lisa = lisa[(lisa.level == "tehsil") & (lisa.scenario == "A") & (lisa.weights == "Queen")
                & (lisa.analysis == "LISA arhti_share")][["pcode", "cluster_p05"]]
    n0 = len(g)
    g = g.merge(lisa.rename(columns={"cluster_p05": "lisa_queen_p05"}), on="pcode", how="left", validate="one_to_one")
    assert len(g) == n0
    cmp = pd.crosstab(g.gistar_p05, g.lisa_queen_p05).reset_index()
    cmp.assign(note="Gi* (Queen incl. self, binary) at p < 0.05 vs LISA (Queen, row-standardised) at p < 0.05", permutations=PERM,
               seed=SEED, fdr_cutoff=cut, vintage=V_MC).to_csv(T / "course_gistar_vs_lisa.csv", index=False)
    cnt = g.gistar_p05.value_counts().reindex(["Hot spot", "Cold spot", "not significant"], fill_value=0)
    cntf = g.gistar_fdr05.value_counts().reindex(["Hot spot", "Cold spot", "not significant"], fill_value=0)
    pd.DataFrame({"p05": cnt, "fdr05": cntf}).rename_axis("class").reset_index().assign(
        fdr_cutoff=cut, permutations=PERM, seed=SEED, weights="Queen incl. self (Gi*), binary", vintage=V_MC
    ).to_csv(T / "course_gistar_counts.csv", index=False)

    col = {"Hot spot": "#c62f2e", "Cold spot": "#1c5cab", "not significant": figs.NEUTRAL}
    fig, ax = plt.subplots(figsize=(6.6, 8.4))
    fig.subplots_adjust(bottom=0.24)
    for c, cl in col.items():
        sub = g[g.gistar_p05 == c]
        if len(sub):
            sub.plot(ax=ax, color=cl, edgecolor="white", linewidth=0.35)
    g[g.gistar_fdr05 != "not significant"].plot(ax=ax, facecolor="none", edgecolor=figs.INK, linewidth=1.1)
    figs.frame(ax, g); figs.furniture(ax, g)
    figs.legend(ax, [Patch(facecolor=col[c], edgecolor="#bdbcb6", label=f"{c} (p < 0.05; n = {cnt[c]})") for c in col]
                + [Patch(facecolor="none", edgecolor=figs.INK, lw=1.1, label=f"Survives FDR 0.05 (n = {int(cntf[:2].sum())})")],
                "Getis-Ord Gi*: arhti credit availability", anchor=(0.0, 0.0))
    ax.set_title("Figure S8. Hot and cold spots of reported arhti credit availability (Getis-Ord Gi*)", loc="left", fontsize=9, fontweight="bold")
    map_footer(fig, [f"Data: {V_MC}. n = {len(g)} tehsils (Cholistan option A); 2 tehsils with no rural populated mouzas not shown.",
                     f"Gi*: Queen contiguity including each tehsil itself, binary weights; {PERM} permutations, seed {SEED}; "
                     f"FDR = Benjamini-Hochberg (cutoff {cut:.4f})." if cut else "FDR: no unit passes."])
    figs.save(fig, "figS8_gistar_arhti_tehsil")
    return g, sens, band


# ------------------------------------------------------------------------------------------ 4 trend surface
def trend_surface(g):
    c = g.geometry.centroid
    x, yk = (c.x.values - c.x.mean()) / 1000, (c.y.values - c.y.mean()) / 1000      # km from the mean centroid
    y = g.arhti_share.values
    X1 = sm.add_constant(np.column_stack([x, yk]))
    X2 = sm.add_constant(np.column_stack([x, yk, x ** 2, x * yk, yk ** 2]))
    wq = Queen.from_dataframe(g, use_index=False, silence_warnings=True); wq.transform = "r"
    rows, fits = [], {}
    for order, X in [(1, X1), (2, X2)]:
        m = sm.OLS(y, X).fit()
        mi = moran(m.resid, wq)
        fits[order] = m
        rows.append(dict(order=order, terms="x, y" if order == 1 else "x, y, x², xy, y²", n=len(y), r2=m.rsquared,
                         adj_r2=m.rsquared_adj, aic=m.aic, resid_moran_I=mi.I, resid_moran_p=mi.p_sim))
    pd.DataFrame(rows).assign(variable="arhti_share", coordinates="tehsil centroids, analysis CRS, km from mean centroid",
                              weights_for_residual_moran="Queen, row-standardised", permutations=PERM, seed=SEED,
                              status="EXPLORATORY (global trend surface; Week 7)", vintage=V_MC
                              ).to_csv(T / "course_trend_surface.csv", index=False)
    g["trend2_fitted"] = fits[2].fittedvalues
    g["trend2_resid"] = fits[2].resid

    fig, axes = plt.subplots(1, 2, figsize=(12.5, 7.2))
    fig.subplots_adjust(wspace=0.02, bottom=0.2)
    fb = mapclassify.EqualInterval(np.clip(g.trend2_fitted, 0, 1), k=5)
    for i, cl in enumerate(figs.BLUE5):
        g[fb.yb == i].plot(ax=axes[0], color=cl, edgecolor="white", linewidth=0.3)
    lim = float(np.nanmax(np.abs(g.trend2_resid)))
    rb = [-0.3, -0.1, 0.1, 0.3]
    rk = np.digitize(g.trend2_resid, rb)
    rc = ["#1c5cab", "#9ec5f4", figs.NEUTRAL, "#f2a7a6", "#c62f2e"]
    rl = ["< -0.30 (over-predicted)", "-0.30 to -0.10", "-0.10 to 0.10", "0.10 to 0.30", "> 0.30 (under-predicted)"]
    for i, cl in enumerate(rc):
        g[rk == i].plot(ax=axes[1], color=cl, edgecolor="white", linewidth=0.3)
    for ax in axes:
        figs.frame(ax, g); figs.furniture(ax, g)
    lo = [f"{fb.bins[i - 1] if i else max(0, g.trend2_fitted.min()):.2f} – {b:.2f}" for i, b in enumerate(fb.bins)]
    figs.legend(axes[0], [Patch(facecolor=c, edgecolor="#bdbcb6", label=f"{l}  (n = {n})") for c, l, n in zip(figs.BLUE5, lo, fb.counts)],
                "Fitted share (second-order trend surface; equal interval)", ncol=2)
    figs.legend(axes[1], [Patch(facecolor=c, edgecolor="#bdbcb6", label=f"{l}  (n = {int((rk == i).sum())})") for i, (c, l) in enumerate(zip(rc, rl))],
                "Residual = observed − fitted share", ncol=2)
    r2 = rows[1]
    axes[0].set_title(f"A. Second-order trend surface (R² = {r2['r2']:.2f})", loc="left", fontsize=9.5)
    axes[1].set_title(f"B. Residuals (Moran's I of residuals = {r2['resid_moran_I']:.2f}, p = {r2['resid_moran_p']:.3f})", loc="left", fontsize=9.5)
    fig.suptitle("Figure S9. Global trend surface of reported arhti credit availability and its residuals (exploratory)",
                 x=0.01, y=0.99, ha="left", fontsize=10.5, fontweight="bold")
    map_footer(fig, [f"Data: {V_MC}. n = {len(g)} tehsils. OLS of arhti_share on centroid x, y, x², xy, y² (km from the mean centroid); "
                     f"first order R² = {rows[0]['r2']:.2f}. Max |residual| = {lim:.2f}.",
                     "Residuals still cluster: a smooth province-wide gradient does not account for the local pattern. Exploratory, not a model of process."])
    figs.save(fig, "figS9_trend_surface")
    return g, pd.DataFrame(rows)


# ------------------------------------------------------------------------------------------ 5 evenness
def dissimilarity(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    return 0.5 * np.abs(a / a.sum() - b / b.sum()).sum()


def evenness(g, d):
    rows = []
    for col, lab in [("n_arhti", "arhti credit"), ("n_commercial", "commercial-bank credit"), ("n_ztbl", "ZTBL credit")]:
        rows.append(dict(level="tehsil", group=f"mouzas reporting {lab}", reference="all rural populated mouzas",
                         D=dissimilarity(g[col], g.rp_mouzas), n_units=len(g), vintage=V_MC))
    q = d[d.small_farms.notna() & d.sub_borrowers.notna()]
    pairs = [("sub_borrowers", "small_farms", "SBP subsistence-holding borrower records", "farms under 12.5 acres"),
             ("branches_rural", "farms", "rural scheduled-bank branches", "all farms"),
             ("branches_scheduled", "farms", "all scheduled-bank branches", "all farms")]
    for a, b, la, lb in pairs:
        rows.append(dict(level="district", group=la, reference=lb, D=dissimilarity(q[a], q[b]), n_units=len(q), vintage=V_Q2))
    out = pd.DataFrame(rows)
    out["reading"] = ("share of the group that would have to be in other units for its distribution to match the reference "
                      "(0 = identical distributions, 1 = completely separate)")
    out.to_csv(T / "course_dissimilarity.csv", index=False)
    return out


# ------------------------------------------------------------------------------------------ 6 k-means typology
def typology(d):
    x = d.dropna(subset=list(TYPO_VARS)).reset_index(drop=True)
    Z = (x[list(TYPO_VARS)] - x[list(TYPO_VARS)].mean()) / x[list(TYPO_VARS)].std(ddof=0)
    c = x.geometry.centroid
    L = np.column_stack([(c.x - c.x.mean()) / c.x.std(ddof=0), (c.y - c.y.mean()) / c.y.std(ddof=0)])
    specs = {"attributes": Z.values, "attributes + location": np.column_stack([Z.values, L])}
    sil, labels = [], {}
    for nm, M in specs.items():
        best = None
        for k in range(2, 7):
            km = KMeans(n_clusters=k, n_init=50, random_state=SEED).fit(M)
            s = silhouette_score(M, km.labels_)
            sil.append(dict(spec=nm, k=k, silhouette=s, min_cluster_size=int(np.bincount(km.labels_).min())))
            if (best is None or s > best[0]) and np.bincount(km.labels_).min() >= 3:
                best = (s, k, km.labels_)
        # relabel clusters 1..k by descending mean arhti_share so labels are stable and readable
        order = pd.Series(best[2]).groupby(best[2]).apply(lambda s: x.arhti_share.iloc[s.index].mean()).sort_values(ascending=False)
        remap = {old: i + 1 for i, old in enumerate(order.index)}
        labels[nm] = np.array([remap[v] for v in best[2]])
    pd.DataFrame(sil).assign(rule="k in 2..6 with the highest silhouette among solutions whose smallest cluster has >= 3 districts",
                             seed=SEED, n_init=50, variables="; ".join(TYPO_VARS), vintage=V_ALL).to_csv(T / "course_kmeans_silhouette.csv", index=False)
    x["type_attr"] = labels["attributes"]
    x["type_attr_loc"] = labels["attributes + location"]
    prof = []
    for spec, colname in [("attributes", "type_attr"), ("attributes + location", "type_attr_loc")]:
        for t, s in x.groupby(colname):
            r = dict(spec=spec, type=int(t), n_districts=len(s), districts=", ".join(sorted(s.adm2_name)))
            r.update({v: s[v].median() for v in TYPO_VARS})
            prof.append(r)
    pd.DataFrame(prof).assign(statistic="median of districts in the type", seed=SEED, vintage=V_ALL).to_csv(T / "course_kmeans_profiles.csv", index=False)
    out = d.merge(x[["adm2_pcode", "type_attr", "type_attr_loc"]], on="adm2_pcode", how="left")

    pal = ["#2a78d6", "#eb6834", "#1baf7a", "#8c62aa", "#c9a227", "#6b6a66"]
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 7.4))
    fig.subplots_adjust(wspace=0.02, bottom=0.22)
    sdf = pd.DataFrame(sil)
    best_s = {nm: sdf[(sdf.spec == nm) & (sdf.k == len(set(labels[nm])))].silhouette.iloc[0] for nm in specs}
    for ax, colname, title in [(axes[0], "type_attr", f"A. Attributes only (k = {len(set(labels['attributes']))}, "
                                                       f"silhouette {best_s['attributes']:.2f})"),
                               (axes[1], "type_attr_loc", f"B. Attributes + location (x, y) (k = {len(set(labels['attributes + location']))}, "
                                                          f"silhouette {best_s['attributes + location']:.2f})")]:
        ks = sorted(out[colname].dropna().unique())
        for t in ks:
            out[out[colname] == t].plot(ax=ax, color=pal[int(t) - 1], edgecolor="white", linewidth=0.5)
        figs.plot_missing(ax, out[out[colname].isna()])
        figs.frame(ax, out); figs.furniture(ax, out)
        pr = pd.DataFrame(prof); pr = pr[pr.spec == ("attributes" if colname == "type_attr" else "attributes + location")]
        hs = [Patch(facecolor=pal[int(r.type) - 1], edgecolor="#bdbcb6",
                    label=f"Type {int(r.type)} (n = {r.n_districts}): arhti {r.arhti_share:.0%}, commercial {r.commercial_share:.0%}, "
                          f"reach {r.small_farm_reach:.0f}") for r in pr.itertuples()]
        hs.append(figs.hatch_patch("Not classified (no rural populated mouzas)"))
        figs.legend(ax, hs, "Type: medians of districts in the type")
        ax.set_title(title, loc="left", fontsize=9.5)
    fig.suptitle("Figure S10. Exploratory k-means typology of districts (descriptive groups, not rankings)",
                 x=0.01, y=0.99, ha="left", fontsize=10.5, fontweight="bold")
    map_footer(fig, [f"Variables (z-scores): {'; '.join(TYPO_VARS.values())}. k chosen by silhouette (k = 2 to 6; smallest type >= 3 districts); "
                     f"n_init = 50, seed {SEED}.",
                     f"Data: {V_Q2}; Mouza Census 2020 (Jan-Mar 2020); ESA WorldCover 2021. Types group similar districts; "
                     "they are not contiguous regions and carry no label of need. Silhouettes near 0.25 indicate weak separation between types."])
    figs.save(fig, "figS10_kmeans_typology")
    return out


# ------------------------------------------------------------------------------------------ 7 Tissot indicatrix
def tissot(outline):
    geod = Geod(ellps="WGS84")
    lons, lats = np.arange(69.5, 76.01, 1.5), np.arange(28.0, 34.01, 1.5)
    crss = {"ESRI:102028 (Albers, centred 125°E; previous analysis CRS)": "ESRI:102028",
            "Analysis CRS (Albers, centred 72°E, 30°N; D025)": common.CRS}
    rows = []
    fig, axes = plt.subplots(1, 2, figsize=(12, 6.6))
    for ax, (lab, crs) in zip(axes, crss.items()):
        o = outline.to_crs(crs)
        o.plot(ax=ax, facecolor="#f6f1e7", edgecolor=figs.INK, linewidth=0.6)
        t = Transformer.from_crs(4326, crs, always_xy=True)
        pj = Proj(crs)
        for lo in lons:
            for la in lats:
                az = np.linspace(0, 360, 73)
                ex, ey, _ = geod.fwd(np.full(73, lo), np.full(73, la), az, np.full(73, 40000.0))
                px, py = t.transform(ex, ey)
                ax.add_patch(plt.Polygon(np.column_stack([px, py]), closed=True, facecolor="#eb6834", alpha=0.55, edgecolor="#9a3d14", lw=0.5))
                f = pj.get_factors(lo, la)
                rows.append(dict(crs=lab, lon=lo, lat=la, areal_scale=f.areal_scale, angular_distortion_deg=f.angular_distortion,
                                 meridian_convergence_deg=f.meridian_convergence, parallel_scale=f.parallel_scale, meridional_scale=f.meridional_scale))
        # graticule
        for lo in np.arange(69, 77, 1):
            gx, gy = t.transform(np.full(50, lo), np.linspace(27.5, 34.5, 50)); ax.plot(gx, gy, color=figs.GRID, lw=0.5, zorder=0)
        for la in np.arange(28, 35, 1):
            gx, gy = t.transform(np.linspace(68.5, 76.5, 50), np.full(50, la)); ax.plot(gx, gy, color=figs.GRID, lw=0.5, zorder=0)
        ax.set_aspect("equal"); ax.set_axis_off()
        r = pd.DataFrame([x for x in rows if x["crs"] == lab])
        ax.set_title(f"{lab}\nmeridian convergence {r.meridian_convergence_deg.min():.1f}° to {r.meridian_convergence_deg.max():.1f}°; "
                     f"max angular distortion {r.angular_distortion_deg.max():.2f}°", loc="left", fontsize=8.5)
    pd.DataFrame(rows).assign(circle_radius_km=40, vintage="Projection diagnostic; Punjab outline from OCHA COD-AB (valid_on 2022-09-09)",
                              note="pyproj Proj.get_factors at each grid point; areal_scale = 1 for both (equal-area)"
                              ).to_csv(T / "course_tissot_distortion.csv", index=False)
    fig.suptitle("Figure S11. Tissot indicatrix: 40 km geodesic circles drawn in the previous and the current analysis CRS",
                 x=0.01, y=1.0, ha="left", fontsize=10.5, fontweight="bold")
    fig.text(0.01, -0.02, "\n".join([
        "Both CRSs are equal-area (circles keep their area). Centred far east of Punjab, ESRI:102028 rotates the province and shears the circles; "
        "the Punjab-centred CRS keeps them round (max angular distortion 0.11°) and grid north within 2° of true north across the province.",
        f"Outline: OCHA COD-AB Pakistan, valid_on 2022-09-09. Graticule every 1°. Not a thematic map. {figs.AUTHOR}. Script: scripts/15_course_methods.py."]),
        fontsize=6.4, color=figs.MUTED, va="top")
    figs.save(fig, "figS11_tissot_indicatrix")
    return pd.DataFrame(rows)


# ------------------------------------------------------------------------------------------ 8 classification histograms
def histograms(g):
    y = g.arhti_share.values
    schemes = {"Equal interval": mapclassify.EqualInterval(y, k=5), "Quantiles": mapclassify.Quantiles(y, k=5),
               "Natural breaks (Fisher-Jenks)": mapclassify.FisherJenks(y, k=5)}
    fig, axes = plt.subplots(3, 1, figsize=(7.2, 7.6), sharex=True)
    rows = []
    for ax, (nm, c) in zip(axes, schemes.items()):
        ax.hist(y, bins=np.linspace(0, 1, 41), color="#9ec5f4", edgecolor="white")
        for b in c.bins[:-1]:
            ax.axvline(b, color="#c62f2e", lw=1.1)
        ad = c.adcm; tss = np.abs(y - np.median(y)).sum()
        gv = 1 - ad / tss
        rows.append(dict(scheme=nm, k=5, breaks="; ".join(f"{b:.3f}" for b in c.bins), counts="; ".join(map(str, c.counts)), gadf=gv))
        ax.set_title(f"{nm}: classes of {', '.join(map(str, c.counts))} tehsils; GADF = {gv:.3f}", loc="left", fontsize=8.5)
        ax.set_ylabel("Tehsils")
    axes[-1].set_xlabel("arhti_share (share of rural populated mouzas reporting arhti credit)")
    pd.DataFrame(rows).assign(variable="arhti_share", n=len(y), note="GADF = 1 - ADCM / sum|y - median| (higher = better fit)",
                              vintage=V_MC).to_csv(T / "course_classification_histograms.csv", index=False)
    fig.suptitle("Figure S12. Distribution of arhti credit availability and three 5-class schemes (red = class breaks)",
                 x=0.01, y=1.0, ha="left", fontsize=10, fontweight="bold")
    fig.text(0.01, -0.03, f"Data: {V_MC}.\nn = {len(y)} tehsils. Figure 2 uses natural breaks (rule D023). Not a map.\n{figs.AUTHOR}. "
             "Script: scripts/15_course_methods.py.", fontsize=6.2, color=figs.MUTED, va="top")
    fig.tight_layout()
    figs.save(fig, "figS12_classification_histograms")
    return pd.DataFrame(rows)


# ------------------------------------------------------------------------------------------ 9 dasymetric dots
def dasymetric(d):
    rng = np.random.default_rng(SEED)
    dots, rows = [], []
    dd = d.to_crs(4326)
    with rasterio.open(CROP) as r:
        for _, row in dd.iterrows():
            n = int(round(row.small_farms / DOT_FARMS)) if pd.notna(row.small_farms) else 0
            arr, tr = rasterio.mask.mask(r, [row.geometry], crop=True, nodata=np.nan, filled=True)
            a = np.nan_to_num(arr[0], nan=0.0)
            a[a < 0.25] = 0.0                                                         # cropland cells only (>= 25% cropland)
            wsum = a.sum()
            rows.append(dict(adm2_pcode=row.adm2_pcode, adm2_name=row.adm2_name, small_farms=row.small_farms, dots=n,
                             cropland_cells=int((a > 0).sum())))
            if n == 0 or wsum == 0:
                continue
            idx = rng.choice(a.size, size=n, replace=True, p=(a / wsum).ravel())
            ri, ci = np.unravel_index(idx, a.shape)
            xs, ys = rasterio.transform.xy(tr, ri, ci, offset="center")
            jx, jy = rng.uniform(-0.5, 0.5, n) * tr.a, rng.uniform(-0.5, 0.5, n) * tr.e
            for x_, y_ in zip(np.asarray(xs) + jx, np.asarray(ys) + jy):
                dots.append(dict(adm2_pcode=row.adm2_pcode, adm2_name=row.adm2_name, geometry=Point(x_, y_)))
    gd = gpd.GeoDataFrame(dots, crs=4326).assign(farms_per_dot=DOT_FARMS,
                                                 vintage="Agricultural Census 2024 (PBS), sample-based; ESA WorldCover 2021 (cropland >= 25% of ~100 m cell)")
    save_layer(gd, "course_dasymetric_small_farm_dots")
    pts = d.copy()
    pts["geometry"] = d.geometry.representative_point()
    pts = pts[["adm2_pcode", "adm2_name", "sub_borrowers", "small_farms", "small_farm_reach", "flagged", "geometry"]].assign(vintage=V_Q2)
    save_layer(gpd.GeoDataFrame(pts, crs=d.crs), "course_district_borrower_points")
    pd.DataFrame(rows).assign(farms_per_dot=DOT_FARMS, seed=SEED, rule="dots sampled in proportion to cropland fraction, cells >= 0.25",
                              vintage="Agricultural Census 2024; ESA WorldCover 2021").to_csv(T / "course_dasymetric_dots.csv", index=False)
    return gd


# ------------------------------------------------------------------------------------------ 10 H1 by formal source (D042)
H1_SOURCES = {"commercial": ("commercial_share", "arhti x commercial"), "ztbl": ("ztbl_share", "arhti x ztbl"),
              "coop": ("coop_share", "arhti x coop"), "mfb": ("mfb_share", "arhti x mfb"),
              "any formal": ("share_anyformal", "arhti x any formal (commercial, ZTBL, cooperative or MFB)")}


def h1_by_source(g):
    """Same-tehsil Spearman correlation, bivariate Moran's I (arhti_i vs neighbours' source share) and the within-tehsil
    Mantel-Haenszel odds ratio (from 07) for each formal source. EXPLORATORY; availability, not borrowing."""
    from scipy.stats import spearmanr
    wq = Queen.from_dataframe(g, use_index=False, silence_warnings=True); wq.transform = "r"
    allco = pd.read_csv(T / "mouza_cooccurrence.csv")
    co = allco[(allco.record == "pooled (Mantel-Haenszel)") & (allco.scenario == "A")].set_index("pair")
    anyf = allco[(allco.record == "tehsil (arhti x any formal)") & (allco.scenario == "A")][["pcode", "share_anyformal"]]
    g = g.merge(anyf, on="pcode", how="left", validate="one_to_one")
    assert g.share_anyformal.notna().all()
    rows = []
    for src, (col, pair) in H1_SOURCES.items():
        r = dict(source=src, n_tehsils=len(g))
        if col:
            rho, pv = spearmanr(g.arhti_share, g[col])
            np.random.seed(SEED)
            bv = esda.Moran_BV(g.arhti_share.values, g[col].values, wq, permutations=PERM)
            r.update(mouza_share_reporting=float((g[col] * g.rp_mouzas).sum() / g.rp_mouzas.sum()),   # pooled over tehsils
                     spearman_rho=rho, spearman_p=pv, bivariate_moran_I=bv.I, bivariate_moran_p=bv.p_sim)
        m = co.loc[pair]
        r.update(mh_or=m.mh_or, mh_ci95_low=m.ci95_low, mh_ci95_high=m.ci95_high, mh_n_mouzas=int(m.n_mouzas), mh_strata=int(m.n_strata),
                 cmh_p=m.cmh_p,
                 breslow_day_p=m.breslow_day_tarone_p, n_both_sources=m.get("n_both_sources"), n_arhti_only=m.get("n_arhti_only"),
                 n_other_only=m.get("n_other_only"), n_neither=m.get("n_neither"), mouzas_in_dropped_strata=m.get("mouzas_in_dropped_strata"))
        rows.append(r)
    out = pd.DataFrame(rows)
    ok = out.spearman_p.notna()
    from statsmodels.stats.multitest import multipletests
    out.loc[ok, "spearman_p_bh"] = multipletests(out.loc[ok, "spearman_p"], method="fdr_bh")[1]
    out["cmh_p_bh"] = multipletests(out.cmh_p, method="fdr_bh")[1]      # BH across the five within-tehsil comparisons
    out["bivariate_moran_p_bh"] = multipletests(out.bivariate_moran_p, method="fdr_bh")[1]
    out.assign(weights="Queen, row-standardised (bivariate Moran)", permutations=PERM, seed=SEED,
               note="EXPLORATORY (D042). Odds ratios compare odds, not probabilities; strata with an empty row or column are dropped.",
               vintage=V_MC).to_csv(T / "course_h1_by_source.csv", index=False)
    return out


# ------------------------------------------------------------------------------------------ 11 market-access model (D042)
MKT_X = {"cropland_share": "cropland (share of area)",
         "mkt_grain_51plus_share": "mouzas > 50 km from a grain market (share)",
         "commercial_share": "commercial-bank credit reported (share)",
         "ztbl_share": "ZTBL credit reported (share)",
         "onlinebank_over25km_share": "mouzas > 25 km from an online bank branch (share)",
         "tt_city_cropw_hours": "travel time to a city, cropland-weighted (hours)"}


def market_model(g):
    """EXPLORATORY: arhti_share on market access, farmland, formal availability and distance, standardised predictors.
    OLS (HC3); binomial GLM on mouza counts (n_arhti of rp_mouzas) with Pearson-scaled SEs (quasi-binomial); spatial error
    model (ML, Queen). Residual Moran's I (Queen) for OLS. Coefficients are per 1 SD of the predictor."""
    import spreg
    g = g.assign(tt_city_cropw_hours=g.tt_city_cropw_mean_min / 60)
    X = g[list(MKT_X)].astype(float)
    Z = (X - X.mean()) / X.std(ddof=0)
    y = g.arhti_share.values
    wq = Queen.from_dataframe(g, use_index=False, silence_warnings=True); wq.transform = "r"
    rows = []
    ols = sm.OLS(y, sm.add_constant(Z)).fit(cov_type="HC3")
    mi = moran(ols.resid, wq)
    for t in Z.columns:
        rows.append(dict(model="OLS (HC3)", term=t, label=MKT_X[t], coef_per_sd=ols.params[t], se=ols.bse[t], p=ols.pvalues[t],
                         n=len(y), fit=f"R² = {ols.rsquared:.3f}; residual Moran's I = {mi.I:.3f} (p = {mi.p_sim:.3f})"))
    from scipy.stats import norm
    glm = sm.GLM(np.column_stack([g.n_arhti, g.rp_mouzas - g.n_arhti]).astype(float), sm.add_constant(Z), family=sm.families.Binomial()).fit()
    phi = glm.pearson_chi2 / glm.df_resid          # quasi-binomial dispersion, computed by hand (statsmodels' scale="X2" is wrong for 2-column endog)
    for t in Z.columns:
        se = glm.bse[t] * np.sqrt(phi)
        rows.append(dict(model="Binomial GLM, quasi-binomial SEs (log-odds)", term=t, label=MKT_X[t], coef_per_sd=glm.params[t], se=se,
                         p=2 * norm.sf(abs(glm.params[t] / se)), n=len(y), fit=f"dispersion = {phi:.1f}; mouzas = {int(g.rp_mouzas.sum()):,}"))
    sem = spreg.ML_Error(y.reshape(-1, 1), Z.values, w=wq, name_x=list(Z.columns), name_y="arhti_share")
    for i, t in enumerate(["CONSTANT"] + list(Z.columns)):
        if t == "CONSTANT":
            continue
        rows.append(dict(model="Spatial error (ML, Queen)", term=t, label=MKT_X[t], coef_per_sd=float(sem.betas[i][0]),
                         se=float(sem.std_err[i]), p=float(sem.z_stat[i][1]), n=len(y),
                         fit=f"lambda = {float(sem.lam):.3f}; log-likelihood = {float(sem.logll):.1f}; AIC = {float(sem.aic):.1f}; "
                             f"OLS AIC = {ols.aic:.1f}"))
    out = pd.DataFrame(rows).assign(y="arhti_share", status="EXPLORATORY (D042); availability, not borrowing; associations, not effects",
                                    permutations=PERM, seed=SEED, vintage=(V_MC + "; ESA WorldCover 2021; MAP travel time 2015"))
    out.to_csv(T / "course_market_model.csv", index=False)
    return out


# ------------------------------------------------------------------------------------------ 12 neither source (D043)
def neither_map(g):
    """Share of each tehsil's rural populated mouzas reporting neither arhti credit nor any formal source (commercial, ZTBL,
    cooperative or MFB). Limited REPORTED availability of these sources, not financial exclusion (other sources exist)."""
    co = pd.read_csv(T / "mouza_cooccurrence.csv")
    t = co[(co.record == "tehsil (arhti x any formal)") & (co.scenario == "A")][["pcode", "share_neither", "share_arhti_only",
                                                                                "share_formal_only", "share_both"]]
    x = g[["pcode", "unit", "rp_mouzas", "geometry"]].merge(t, on="pcode", how="left", validate="one_to_one")
    allm = co[(co.record == "all mouzas (descriptive)") & (co.scenario == "A")]
    breaks = [0.05, 0.10, 0.20, 0.40]
    k = np.digitize(x.share_neither, breaks)
    cols = ["#f6f1e7", "#f2d3b6", "#e9a46c", "#c9531f", "#6b280b"]
    labs = ["< 5%", "5–10%", "10–20%", "20–40%", "≥ 40%"]
    fig, ax = plt.subplots(figsize=(6.6, 8.4)); fig.subplots_adjust(bottom=0.24)
    for i, c in enumerate(cols):
        sub = x[k == i]
        if len(sub):
            sub.plot(ax=ax, color=c, edgecolor="#bdbcb6", linewidth=0.3)
    figs.frame(ax, x); figs.furniture(ax, x)
    figs.legend(ax, [Patch(facecolor=c, edgecolor="#bdbcb6", label=f"{l}  (n = {int((k == i).sum())})") for i, (c, l) in enumerate(zip(cols, labs))],
                "Share of rural populated mouzas reporting neither arhti\nnor any formal source (fixed classes)", anchor=(0.0, 0.0))
    ax.set_title("Limited reported availability: mouzas reporting neither arhti nor formal credit (as Figure 7B)", loc="left",
                 fontsize=9, fontweight="bold")
    r = allm[allm.pair.str.contains("any formal")].iloc[0]
    map_footer(fig, [f"Data: {V_MC}. n = {len(x)} tehsils; {int(r.n_neither):,} of {int(r.n_mouzas):,} rural populated mouzas report neither.",
                     "Formal = commercial bank, ZTBL, cooperative bank or microfinance bank. Other sources (NGOs, rural support programmes, government) "
                     "are not counted, so this is limited reported availability of these sources, not financial exclusion."])
    figs.save(fig, "figS13_neither_source_tehsil")
    x.drop(columns="geometry").assign(vintage=V_MC).to_csv(T / "course_neither_source_tehsil.csv", index=False)
    return x


# ------------------------------------------------------------------------------------------ 13 H2/H3 sensitivity (D043)
URBAN_TOP5_N = 5


def urban_top(n=URBAN_TOP5_N):
    """Districts with the largest urban population, Population Census 2023 (PBS Table 1, Punjab): a lending-independent rule."""
    x = pd.read_excel(ROOT / "data" / "raw" / "pop_census_2023" / "table_1_punjab_districts.xlsx", header=None)
    d = x[x[0].astype(str).str.upper().str.endswith(" DISTRICT")].copy()
    d["district"] = d[0].str.upper().str.replace(" DISTRICT", "", regex=False).str.strip().str.title()
    d["urban_pop"] = d[2].astype(float) * d[8].astype(float) / 100
    return d.sort_values("urban_pop", ascending=False).head(n)[["district", "urban_pop"]]


def sensitivity():
    """Flagged-district exclusions for H2/H3 headline measures, two city groups (the paper's five; the five districts with the largest urban populations, 2023
    census), leave-one-out for each city, and class-specific benchmarks using the district distribution of farms in the class."""
    rg = pd.read_csv(T / "reporting_geography.csv")
    d = rg[rg.record_type == "district"].copy()
    rows = []

    def measures(x, label, group=None):
        r = dict(sample=label, n_districts=len(x))
        r["D_sub_borrowers_vs_small_farms"] = dissimilarity(x.sub_borrowers, x.sub_farms)
        for c in ["sub", "abv"]:
            r[f"{c}_share_of_disbursement"] = x[f"{c}_amount_mn"].sum() / x.tot_amount_mn.sum()
            r[f"{c}_share_of_records"] = x[f"{c}_borrowers"].sum() / x.tot_borrowers.sum()
        if group is not None:
            gm = x.adm2_name.isin(group)
            r["group"] = ", ".join(group)
            r["group_districts_in_sample"] = int(gm.sum())
            r["group_cultivated_share"] = x[gm].cultivated_ac.sum() / x.cultivated_ac.sum()
            r["group_farm_share"] = x[gm].farms.sum() / x.farms.sum()
            for c in ["tot", "sub", "abv"]:
                r[f"group_{c}_disbursement_share"] = x[gm][f"{c}_amount_mn"].sum() / x[f"{c}_amount_mn"].sum()
                r[f"group_{c}_ratio_to_cultivated"] = r[f"group_{c}_disbursement_share"] / r["group_cultivated_share"]
            for c in ["sub", "abv"]:
                r[f"group_{c}_class_farm_share"] = x[gm][f"{c}_farms"].sum() / x[f"{c}_farms"].sum()
                r[f"group_{c}_ratio_to_class_farms"] = r[f"group_{c}_disbursement_share"] / r[f"group_{c}_class_farm_share"]
        return r

    paper5 = ["Lahore", "Rawalpindi", "Multan", "Faisalabad", "Rahim Yar Khan"]
    ut = urban_top(8)
    ut.assign(rank=range(1, len(ut) + 1), source="PBS, Population Census 2023, Table 1 (Punjab districts): population 2023 x urban proportion",
              url="https://www.pbs.gov.pk/wp-content/uploads/2020/07/table_1_punjab_districts.xlsx").to_csv(T / "course_urban_population_top.csv", index=False)
    urban5 = list(ut.head(URBAN_TOP5_N).district)
    missing = [n for n in urban5 if n not in set(d.adm2_name)]
    assert not missing, f"census district names not in the district table: {missing}"
    flagged = list(d[d.flagged == 1].adm2_name)
    rows.append(measures(d, "all 36 districts", paper5))
    rows.append(measures(d[d.flagged != 1], "excluding the 5 flagged districts", [c for c in paper5 if c not in flagged]))
    rows.append(measures(d, "all 36 districts; five districts with the largest urban populations (Population Census 2023)", urban5))
    for c in paper5:
        rows.append(dict(measures(d[d.adm2_name != c], f"leave out {c}", [x for x in paper5 if x != c]), kind="leave-one-out"))
    out = pd.DataFrame(rows).assign(flagged_districts=", ".join(flagged), note="EXPLORATORY (D043); counts and SBP district rows as reported "
                                    "(attribution under verification); class farm counts from the Agricultural Census 2024", vintage=V_Q2)
    out.to_csv(T / "course_h2_h3_sensitivity.csv", index=False)
    # class-specific benchmark for every district: class disbursement share / class farm share
    for c in ["sub", "eco", "abv"]:
        d[f"lq_class_farms_{c}"] = (d[f"{c}_amount_mn"] / d[f"{c}_amount_mn"].sum()) / (d[f"{c}_farms"] / d[f"{c}_farms"].sum())
    d[["adm2_name", "adm2_pcode", "flagged", "lq_amount_sub", "lq_amount_abv", "lq_class_farms_sub", "lq_class_farms_eco", "lq_class_farms_abv"]
      ].assign(definition="lq_class_farms_c = district share of class-c disbursement / district share of class-c farms (farm counts, not area)",
               vintage=V_Q2).to_csv(T / "course_lq_class_farms.csv", index=False)
    return out


# ------------------------------------------------------------------------------------------ 14 grain-market distance bands (D043)
def market_bands(g):
    """Spearman correlations of arhti_share with the share of mouzas within 10 km, within 25 km and more than 50 km of a grain market
    (Mouza Census distance bands), BH-adjusted; and the market term's estimate when each band replaces the > 50 km share in the
    exploratory model (OLS HC3, quasi-binomial, spatial error)."""
    import spreg
    from scipy.stats import norm, spearmanr
    from statsmodels.stats.multitest import multipletests
    g = g.assign(tt_city_cropw_hours=g.tt_city_cropw_mean_min / 60,
                 mkt_grain_within10_share=(g.n_mkt_grain_in_mouza + g.n_mkt_grain_1_10) / g.rp_mouzas,
                 mkt_grain_within25_share=(g.n_mkt_grain_in_mouza + g.n_mkt_grain_1_10 + g.n_mkt_grain_11_25) / g.rp_mouzas)
    bands = {"mkt_grain_within10_share": "grain market within 10 km (share of mouzas)",
             "mkt_grain_within25_share": "grain market within 25 km (share of mouzas)",
             "mkt_grain_51plus_share": "grain market more than 50 km away (share of mouzas)"}
    wq = Queen.from_dataframe(g, use_index=False, silence_warnings=True); wq.transform = "r"
    base = [c for c in MKT_X if c != "mkt_grain_51plus_share"]
    rows = []
    for b, lab in bands.items():
        rho, pv = spearmanr(g.arhti_share, g[b])
        X = g[base + [b]].astype(float); Z = (X - X.mean()) / X.std(ddof=0)
        ols = sm.OLS(g.arhti_share.values, sm.add_constant(Z)).fit(cov_type="HC3")
        glm = sm.GLM(np.column_stack([g.n_arhti, g.rp_mouzas - g.n_arhti]).astype(float), sm.add_constant(Z), family=sm.families.Binomial()).fit()
        phi = glm.pearson_chi2 / glm.df_resid
        se = glm.bse[b] * np.sqrt(phi)
        sem = spreg.ML_Error(g.arhti_share.values.reshape(-1, 1), Z.values, w=wq, name_x=list(Z.columns))
        j = 1 + list(Z.columns).index(b)
        bse = float(sem.std_err[j])
        mres = moran(np.asarray(sem.e_filtered).ravel(), wq)            # spatially filtered residuals
        rows.append(dict(band=b, label=lab, n_tehsils=len(g), mean_share=float((g[b] * g.rp_mouzas).sum() / g.rp_mouzas.sum()),
                         spearman_rho=rho, spearman_p=pv,
                         ols_coef_per_sd=ols.params[b], ols_p=ols.pvalues[b], glm_coef_per_sd=glm.params[b],
                         glm_p=2 * norm.sf(abs(glm.params[b] / se)), sem_coef_per_sd=float(sem.betas[j][0]), sem_se=bse,
                         sem_ci95_low=float(sem.betas[j][0]) - 1.96 * bse, sem_ci95_high=float(sem.betas[j][0]) + 1.96 * bse,
                         sem_p=float(sem.z_stat[j][1]), sem_lambda=float(sem.lam), sem_aic=float(sem.aic), ols_aic=sm.OLS(
                             g.arhti_share.values, sm.add_constant(Z)).fit().aic, sem_resid_moran_I=mres.I, sem_resid_moran_p=mres.p_sim))
    out = pd.DataFrame(rows)
    out["spearman_p_bh"] = multipletests(out.spearman_p, method="fdr_bh")[1]
    out["sem_p_bh"] = multipletests(out.sem_p, method="fdr_bh")[1]          # family = the three band definitions
    out["sem_p_holm"] = multipletests(out.sem_p, method="holm")[1]
    out.assign(controls="; ".join(base), status="EXPLORATORY (D043)", vintage=V_MC).to_csv(T / "course_market_bands.csv", index=False)
    return out


# ------------------------------------------------------------------------------------------ 15 access tables for the app (D045)
def access_tables(g):
    """Tehsil and district shares of rural populated mouzas reporting each source, any formal source, neither, and a grain market
    within 10 / 25 km. District shares are pooled (counts summed over the district's tehsils / rural populated mouzas), never averaged."""
    co = pd.read_csv(T / "mouza_cooccurrence.csv")
    t = co[(co.record == "tehsil (arhti x any formal)") & (co.scenario == "A")][["pcode", "share_anyformal", "share_neither", "share_arhti_only",
                                                                                "share_formal_only", "share_both", "n_mouzas"]]
    x = g[["pcode", "unit", "adm2_name", "rp_mouzas", "n_arhti", "n_commercial", "n_ztbl", "n_coop", "n_mfb", "n_mkt_grain_in_mouza",
           "n_mkt_grain_1_10", "n_mkt_grain_11_25"]].merge(t, on="pcode", how="left", validate="one_to_one")
    assert (x.n_mouzas == x.rp_mouzas).all()
    x["n_anyformal"] = (x.share_anyformal * x.rp_mouzas).round()
    x["n_neither"] = (x.share_neither * x.rp_mouzas).round()
    x["n_mkt10"] = x.n_mkt_grain_in_mouza + x.n_mkt_grain_1_10
    x["n_mkt25"] = x.n_mkt10 + x.n_mkt_grain_11_25
    out_t = x[["pcode", "unit", "adm2_name", "rp_mouzas"]].rename(columns={"pcode": "adm3_pcode", "unit": "adm3_name"})
    for c in ["arhti", "commercial", "ztbl", "coop", "mfb", "anyformal", "neither", "mkt10", "mkt25"]:
        out_t[f"{c}_share"] = x[f"n_{c}"] / x.rp_mouzas
    # bivariate classes (arhti tercile x source tercile), same rule as Figure 3 (10_export_qgis.py): pandas quantiles 1/3, 2/3, right-closed
    qa = out_t.arhti_share.quantile([1 / 3, 2 / 3]).values
    ra = np.digitize(out_t.arhti_share, qa, right=True) + 1
    for c in ["commercial", "ztbl", "coop", "mfb", "anyformal"]:
        qc = out_t[f"{c}_share"].quantile([1 / 3, 2 / 3]).values
        rc = np.digitize(out_t[f"{c}_share"], qc, right=True) + 1
        out_t[f"biv_{c}"] = [f"A{i}-C{j}" for i, j in zip(ra, rc)]
        out_t[f"biv_{c}_cut1"], out_t[f"biv_{c}_cut2"] = qc
    out_t["biv_arhti_cut1"], out_t["biv_arhti_cut2"] = qa
    fig3 = gpd.read_file(GPKG, layer="q1_tehsils_mouza_census_2020")[["adm3_pcode", "bivariate_class"]]
    chk = out_t.merge(fig3, on="adm3_pcode", how="left")
    assert (chk.biv_commercial == chk.bivariate_class).all(), "commercial bivariate classes differ from Figure 3"
    out_t.assign(vintage=V_MC).to_csv(T / "app_tehsil_access.csv", index=False)
    dd = x.groupby("adm2_name")[["rp_mouzas", "n_arhti", "n_commercial", "n_ztbl", "n_coop", "n_mfb", "n_anyformal", "n_neither", "n_mkt10"]].sum()
    out_d = pd.DataFrame({"adm2_name": dd.index, "rp_mouzas": dd.rp_mouzas.values})
    for c in ["arhti", "commercial", "ztbl", "coop", "mfb", "anyformal", "neither", "mkt10"]:
        out_d[f"{c}_share"] = (dd[f"n_{c}"] / dd.rp_mouzas).values
    out_d.assign(vintage=V_MC).to_csv(T / "app_district_access.csv", index=False)
    return out_t, out_d


# ------------------------------------------------------------------------------------------ main
def main() -> int:
    g = tehsils()
    d = districts()
    g, sens, band = autocorrelation(g)
    g, ts = trend_surface(g)
    ev = evenness(g, d)
    typ = typology(d)
    tissot(gpd.read_file(GPKG, layer="context_punjab_outline"))
    hist = histograms(g)
    dots = dasymetric(d)
    h1 = h1_by_source(g)
    mm = market_model(g)
    neither_map(g)
    mb = market_bands(g)
    sv = sensitivity()
    access_tables(g)
    nb = pd.read_csv(T / "course_neither_source_tehsil.csv")[["pcode", "share_neither"]]
    g = g.merge(nb, on="pcode", how="left", validate="one_to_one")
    g["mkt_grain_within10_share"] = (g.n_mkt_grain_in_mouza + g.n_mkt_grain_1_10) / g.rp_mouzas
    keep = ["pcode", "unit", "adm2_name", "rp_mouzas", "arhti_share", "gistar_z", "gistar_p", "gistar_p05", "gistar_fdr05",
            "lisa_queen_p05", "trend2_fitted", "trend2_resid", "share_neither", "mkt_grain_within10_share", "geometry"]
    save_layer(gpd.GeoDataFrame(g[keep].rename(columns={"pcode": "adm3_pcode", "unit": "adm3_name"}), crs=g.crs).assign(vintage=V_MC),
               "course_tehsils_gistar_trend")
    save_layer(typ[["adm2_pcode", "adm2_name", "type_attr", "type_attr_loc", "geometry"]].assign(vintage=V_ALL), "course_districts_typology")
    print(sens[["statistic", "weights", "value", "p_perm"]].to_string(index=False))
    print(ts[["order", "r2", "resid_moran_I", "resid_moran_p"]].to_string(index=False))
    print(ev[["level", "group", "D"]].to_string(index=False))
    print(hist[["scheme", "counts", "gadf"]].to_string(index=False))
    print(h1[["source", "spearman_rho", "bivariate_moran_I", "mh_or", "mh_ci95_low", "mh_ci95_high"]].to_string(index=False))
    print(mm[["model", "term", "coef_per_sd", "p", "fit"]].round(4).to_string(index=False))
    print(mb.drop(columns=["label"]).round(3).to_string(index=False))
    print(sv.drop(columns=["note", "vintage", "flagged_districts", "group"]).round(3).T.to_string())
    print(f"distance band {band / 1000:.1f} km; dots {len(dots)}; typology types attr {typ.type_attr.nunique()}, attr+loc {typ.type_attr_loc.nunique()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
