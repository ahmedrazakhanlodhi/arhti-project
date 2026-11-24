"""17_key_numbers.py: every number used in the main text, the app and the slides, with its source file and row.

    .venv/bin/python -I scripts/17_key_numbers.py

Reads finished outputs only (no new analysis). Writes outputs/tables/key_numbers.csv (read by the app and tests) and
docs/key_numbers.md (for writing). Each number is located by a file, a row filter and a column, so it can be checked by hand.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pyogrio

ROOT = Path(__file__).resolve().parents[1]
T = ROOT / "outputs" / "tables"
GPKG = ROOT / "outputs" / "arhti_project.gpkg"
ROWS = []


def src(file: str) -> pd.DataFrame:
    if file.startswith("gpkg:"):
        return pyogrio.read_dataframe(GPKG, layer=file[5:], read_geometry=False)
    return pd.read_csv(ROOT / file)


def add(kid, label, file, where, col, fmt, section, agg=None):
    d = src(file)
    for k, v in where.items():
        d = d[d[k].astype(str) == str(v)]
    if agg:
        val = getattr(d[col], agg)()
        n = len(d)
    else:
        assert len(d) == 1, (kid, len(d))
        val, n = d[col].iloc[0], 1
    shown = fmt.format(val) if not isinstance(fmt, type(lambda: 0)) else fmt(val)
    where_txt = "; ".join(f"{k} = {v}" for k, v in where.items()) or "all rows"
    vint = str(d["vintage"].dropna().iloc[0]) if "vintage" in d and d["vintage"].notna().any() else (
        "published study (CONTEXT)" if file.startswith("docs/literature") else "")
    ROWS.append(dict(id=kid, section=section, label=label, value=val, display=shown, source=file.replace("gpkg:", "outputs/arhti_project.gpkg | layer "),
                     row=where_txt + (f" ({agg} over {n} rows)" if agg else ""), column=col, vintage=vint))


def main() -> int:
    MG, LC, BV = "outputs/tables/moran_global.csv", "outputs/tables/lisa_counts.csv", "outputs/tables/moran_bivariate.csv"
    QD, CO, EX = "outputs/tables/q1_descriptives.csv", "outputs/tables/mouza_cooccurrence.csv", "outputs/tables/exploratory_associations.csv"
    HD, Q2, MS = "outputs/tables/sbp_province_headline.csv", "gpkg:q2_districts_credit_allocation", "outputs/tables/moran_small_farm_reach.csv"
    LIT = "docs/literature_evidence.csv"
    pct, f3, f2 = (lambda v: f"{100 * v:.1f}%"), "{:.3f}", "{:.2f}"
    intc = lambda v: f"{int(v):,}"
    tA = dict(level="tehsil", scenario="A")

    # data
    add("n_tehsils", "Tehsils in the Q1 analysis (rural populated mouzas > 0)", QD, tA, "n", intc, "Data")
    add("rp_mouzas", "Rural populated mouzas (denominator of every share)", QD, tA, "rp_mouzas", intc, "Data")
    add("excluded_tehsils", "Tehsils with no rural populated mouzas (not in the Q1 sample)", QD, tA, "excluded_zero_rp", "{}", "Data")
    add("n_districts_q2", "Districts with small-farm reach", Q2, {}, "small_farm_reach", intc, "Data", agg="count")
    # result 1
    add("arhti_pooled", "Share of all rural populated mouzas reporting arhti credit (Punjab, pooled)", QD, tA, "arhti_pooled", pct, "R1 Where")
    add("arhti_median", "Median tehsil arhti_share", QD, tA, "arhti_median", pct, "R1 Where")
    add("arhti_min", "Lowest tehsil arhti_share", QD, tA, "arhti_min", pct, "R1 Where")
    add("arhti_max", "Highest tehsil arhti_share", QD, tA, "arhti_max", pct, "R1 Where")
    add("arhti_zero", "Tehsils where no rural populated mouza reports arhti credit", QD, tA, "arhti_zero", intc, "R1 Where")
    add("commercial_median", "Median tehsil commercial_share (commercial-bank credit reported available)", QD, tA, "commercial_median", pct, "R1 Where")
    # result 2
    q = dict(level="tehsil", scenario="A", variable="arhti_share", weights="Queen")
    add("moran_arhti_queen", "Global Moran's I, arhti_share, tehsils, Queen", MG, q, "I", f3, "R2 Clusters")
    add("moran_arhti_queen_p", "Pseudo p-value (999 permutations)", MG, q, "p_perm", f3, "R2 Clusters")
    add("moran_commercial_queen", "Global Moran's I, commercial_share, tehsils, Queen", MG, dict(q, variable="commercial_share"), "I", f3, "R2 Clusters")
    lq = dict(level="tehsil", scenario="A", analysis="LISA arhti_share", weights="Queen")
    for cl, k in [("High-High", "hh"), ("Low-Low", "ll"), ("Low-High", "lh"), ("High-Low", "hl")]:
        for col, lab in [("p05", "p < 0.05"), ("p01", "p < 0.01"), ("fdr05", "FDR 0.05")]:
            add(f"lisa_{k}_{col}", f"LISA {cl} tehsils, Queen, {lab}", LC, dict(lq, cluster=cl), col, intc, "R2 Clusters")
    add("bh_cutoff_queen", "Benjamini-Hochberg cutoff (pseudo p) for FDR 0.05, LISA arhti, tehsils, Queen", LC, dict(lq, cluster="High-High"),
        "bh_cutoff", "{:.4f}", "R2 Clusters")
    add("permutations", "Permutations", MG, q, "permutations", intc, "R2 Clusters")
    add("seed", "Random seed", MG, q, "seed", "{:.0f}", "R2 Clusters")
    # result 3
    add("bv_queen", "Bivariate Moran's I (arhti_share x lag commercial_share), tehsils, Queen", BV, dict(level="tehsil", scenario="A", weights="Queen"),
        "I_bv", f3, "R3 Gap")
    add("bv_queen_p", "Pseudo p-value, bivariate Moran, Queen", BV, dict(level="tehsil", scenario="A", weights="Queen"), "p_perm", f3, "R3 Gap")
    po = dict(record="pooled (Mantel-Haenszel)", scenario="A", pair="arhti x commercial")
    add("mh_or", "Mantel-Haenszel odds ratio, arhti x commercial-bank credit reported in the same mouza (tehsil strata)", CO, po, "mh_or", f2, "R3 Gap")
    add("mh_lo", "95% CI lower bound", CO, po, "ci95_low", f2, "R3 Gap")
    add("mh_hi", "95% CI upper bound", CO, po, "ci95_high", f2, "R3 Gap")
    add("mh_n_mouzas", "Mouzas in the pooled odds ratio", CO, po, "n_mouzas", intc, "R3 Gap")
    add("mh_strata", "Tehsil strata used", CO, po, "n_strata", intc, "R3 Gap")
    add("bd_stat", "Breslow-Day-Tarone homogeneity statistic", CO, po, "breslow_day_tarone_stat", "{:.1f}", "R3 Gap")
    add("bd_p", "Breslow-Day-Tarone p-value", CO, po, "breslow_day_tarone_p", lambda v: "< 0.001" if v < 0.001 else f"{v:.3f}", "R3 Gap")
    tc = dict(record="tehsil (arhti x commercial)", scenario="A")
    add("tehsils_estimable", "Tehsils with an estimable observed/expected ratio", CO, dict(tc, estimable=True), "pcode", intc, "R3 Gap", agg="count")
    d = src(CO); d = d[(d.record == tc["record"]) & (d.scenario == "A")]
    for kid, lab, val in [("tehsils_ratio_above1", "Tehsils where arhti and commercial-bank credit are co-reported MORE often than independence implies",
                           int((d.obs_exp_ratio > 1).sum())),
                          ("tehsils_ratio_below1", "Tehsils where they are co-reported LESS often than independence implies", int((d.obs_exp_ratio < 1).sum()))]:
        ROWS.append(dict(id=kid, section="R3 Gap", label=lab, value=val, display=f"{val:,}", source=CO,
                         row="record = tehsil (arhti x commercial); scenario = A; obs_exp_ratio " + (">" if "above" in kid else "<") + " 1 (count)",
                         column="obs_exp_ratio", vintage=str(d.vintage.iloc[0])))
    cr = dict(level="tehsil", scenario="A", x="cropland_share")
    add("rho_cropland", "Spearman rho, arhti_share vs cropland share (POST-HOC EXPLORATORY)", EX, cr, "rho", f2, "R3 Gap")
    add("rho_cropland_pbh", "BH-adjusted p-value", EX, cr, "p_bh", lambda v: "< 0.001" if v < 0.001 else f"{v:.3f}", "R3 Gap")
    ob = dict(level="tehsil", scenario="A", x="onlinebank_in_mouza_share")
    add("rho_onlinebank", "Spearman rho, arhti_share vs share of mouzas with an online commercial bank in the mouza (PRESENCE; POST-HOC EXPLORATORY)",
        EX, ob, "rho", f2, "R3 Gap")
    add("rho_onlinebank_pbh", "BH-adjusted p-value", EX, ob, "p_bh", lambda v: "< 0.001" if v < 0.001 else f"{v:.3f}", "R3 Gap")
    # result 4
    add("reach_min", "Lowest district small-farm reach", Q2, {}, "small_farm_reach", "{:.1f}", "R4 Reach", agg="min")
    add("reach_max", "Highest district small-farm reach", Q2, {}, "small_farm_reach", "{:.1f}", "R4 Reach", agg="max")
    add("reach_median", "Median district small-farm reach", Q2, {}, "small_farm_reach", "{:.1f}", "R4 Reach", agg="median")
    add("n_flagged", "Districts flagged in the SBP data-quality screen", Q2, dict(flagged=1), "adm2_name", intc, "R4 Reach", agg="count")
    fl = src(Q2); names = ", ".join(sorted(fl[fl.flagged == 1].adm2_name))
    ROWS.append(dict(id="flagged_names", section="R4 Reach", label="Flagged districts", value=names, display=names,
                     source="outputs/arhti_project.gpkg | layer q2_districts_credit_allocation", row="flagged = 1", column="adm2_name",
                     vintage=str(fl.vintage.iloc[0])))
    add("moran_reach", "Global Moran's I, small_farm_reach, districts, Queen", MS, dict(weights="Queen", sample="all matched districts"), "I", f3, "R4 Reach")
    h = dict(scope="All Punjab (banks + MFIs)")
    add("head_borrower_share", "Above-economic holdings (> 50 acres): share of farm-sector borrower records", HD, h, "abv_borrower_share", pct, "R4 Reach")
    add("head_amount_share", "Above-economic holdings (> 50 acres): share of farm-sector disbursed amount (province only)", HD, h, "abv_amount_share", pct, "R4 Reach")
    add("head_abv_borrowers", "Above-economic borrower records", HD, h, "abv_borrowers", intc, "R4 Reach")
    add("head_tot_borrowers", "All farm-sector borrower records", HD, h, "tot_borrowers", intc, "R4 Reach")
    # robustness
    add("moran_arhti_knn", "Global Moran's I, arhti_share, tehsils, geodesic kNN-5", MG, dict(q, weights="kNN-5 (geodesic)"), "I", f3, "Robustness")
    add("moran_arhti_district", "Global Moran's I, arhti_share, districts (n = 35), Queen", MG, dict(q, level="district"), "I", f3, "Robustness")
    add("moran_arhti_B", "Global Moran's I, arhti_share, tehsils, Queen, Cholistan scenario B", MG, dict(q, scenario="B"), "I", f3, "Robustness")
    add("mh_or_B", "Mantel-Haenszel odds ratio, arhti x commercial, scenario B", CO, dict(po, scenario="B"), "mh_or", f2, "Robustness")
    add("mh_lo_B", "95% CI lower bound, scenario B", CO, dict(po, scenario="B"), "ci95_low", f2, "Robustness")
    add("mh_hi_B", "95% CI upper bound, scenario B", CO, dict(po, scenario="B"), "ci95_high", f2, "Robustness")
    # background (CONTEXT, published studies)
    ig = dict(study='Haq, Aslam et al. (IGC/NIBAF/PMN), "Who is the Arthi?"', location="Nankana Sahib")
    add("lit_igc_rates", "IGC 2013: annualized implicit interest by crop (Table 11; CONTEXT)", LIT, ig, "value", "{}", "Background")
    add("lit_igc_sample", "IGC 2013: sample", LIT, ig, "sample", "{}", "Background")
    pm = dict(study='PMN/MEDA, "Warehouse Receipt Financing"', location="Bahawalpur")
    add("lit_pmn_markup", "PMN/MEDA 2019: reported markup (focus groups; CONTEXT)", LIT, pm, "value", "{}", "Background")
    add("lit_pmn_sample", "PMN/MEDA 2019: sample", LIT, pm, "sample", "{}", "Background")

    # ALLOCATION by holding class (scripts/13_reporting_geography.py; province level)
    HC, RG, SC, RT = ("outputs/tables/holding_class_shares.csv", "outputs/tables/reporting_geography.csv",
                      "outputs/tables/district_scorecard.csv", "outputs/tables/sbp_agri_lending_rates.csv")
    for cls in ["subsistence", "economic", "above_economic"]:
        for col, lab in [("share_farms", "share of farms"), ("share_operated_area", "share of operated farm area"),
                         ("share_borrower_records", "share of SBP borrower records"), ("share_disbursement", "share of SBP disbursement")]:
            add(f"hc_{cls}_{col.replace('share_', '')}", f"{cls.replace('_', '-')} holdings: {lab} (Punjab)", HC, dict(holding_class=cls), col, pct,
                "Allocation by class")
    # REPORTING GEOGRAPHY (district attribution under verification)
    add("lahore_total_branches_10k", "Lahore: all scheduled-bank branches per 10,000 farms", RG, dict(record_type="district", adm2_name="Lahore"),
        "total_branches_per_10k_farms", "{:.1f}", "Reporting geography")
    add("lahore_rural_branches_10k", "Lahore: rural branches per 10,000 farms", RG, dict(record_type="district", adm2_name="Lahore"),
        "rural_branches_per_10k_farms", "{:.1f}", "Reporting geography")
    five = "Five cities combined (Lahore, Rawalpindi, Multan, Faisalabad, Rahim Yar Khan)"
    for col, lab in [("credit_share_tot", "share of disbursement, all holdings"), ("credit_share_abv", "share of above-economic disbursement"),
                     ("credit_share_sub", "share of subsistence disbursement"), ("area_share", "share of cultivated area"),
                     ("farm_share", "share of farms"), ("rural_branch_share", "share of rural branches"), ("total_branch_share", "share of all branches")]:
        add(f"five_{col}", f"Five city districts combined: {lab}", RG, dict(record_type="summary", adm2_name=five), col, pct, "Reporting geography")
    add("isb_credit_share_tot", "Islamabad: share of disbursement in SBP district rows incl. Islamabad", RG,
        dict(record_type="Islamabad (booked; not in area ratios)"), "credit_share_tot", pct, "Reporting geography")
    for pre, lab in [("abv", "above-economic"), ("sub", "subsistence")]:
        for nm in ["Lahore", "Rawalpindi", "Jhelum", "Chakwal"]:
            add(f"lq_{pre}_{nm.lower()}", f"{nm}: amount LQ, {lab} holdings", RG, dict(record_type="district", adm2_name=nm),
                f"lq_amount_{pre}", f2, "Reporting geography")
    # COST (context)
    for period in ["2012-13", "2023-24"]:
        for inst, short in [("Zarai Taraqiati Bank Ltd. (ZTBL)", "ztbl"), ("Punjab Provincial Cooperative Bank (PPCB)", "ppcb"),
                            ("Commercial banks (5 big banks + 14 DPBs)", "comm")]:
            for lt in ["production", "development"]:
                add(f"rate_{short}_{lt[:4]}_{period[:4]}", f"SBP Table 3.33, {inst}, {lt} loans, {period} (% p.a.)", RT,
                    dict(period=period, institution=inst, loan_type=lt), "rate_pct", "{:.2f}", "Cost (context)")
    # SCORECARD profile counts
    for prof in ["high arhti availability + low small-farm reach", "high arhti availability + high small-farm reach",
                 "low arhti availability + low small-farm reach", "low arhti availability + high small-farm reach", "not classified"]:
        add("profile_" + prof.replace(" + ", "_").replace(" ", "_").replace("-", ""), f"Districts with profile '{prof}'", SC,
            dict(profile_type=prof), "adm2_name", intc, "Scorecard", agg="count")

    # ALLOCATION extras: concentration, tenure (one sentence), crops, flagged-district exclusion
    CC, TN, CR = ("outputs/tables/concentration_coefficients.csv", "outputs/tables/q2_tenure_associations.csv",
                  "outputs/tables/crop_structure_district.csv")
    add("cc_all", "Concentration coefficient of borrower records over small farms, all 36 districts", CC, dict(sample="all matched districts"),
        "concentration_coefficient", f3, "Allocation extras")
    add("cc_excl", "Concentration coefficient, excluding the 5 flagged districts", CC, dict(sample="excluding flagged districts"),
        "concentration_coefficient", f3, "Allocation extras")
    add("rho_tenant", "Spearman rho, small_farm_reach vs tenant share of farms (36 districts)", TN,
        dict(family="all districts (n = 36)", x="tenant_share"), "rho", f2, "Allocation extras")
    add("rho_tenant_pbh", "BH-adjusted p, small_farm_reach vs tenant share", TN, dict(family="all districts (n = 36)", x="tenant_share"),
        "p_bh", "{:.3f}", "Allocation extras")
    add("moran_reach_excl", "Moran's I, small_farm_reach, Queen, excluding flagged districts (n = 31)", MS,
        dict(weights="Queen", sample="excluding flagged districts"), "I", f3, "Allocation extras")
    for c in ["wheat", "rice", "cotton", "sugarcane", "maize"]:
        add(f"top_crop_{c}", f"Districts where {c} is the largest of the five tracked crops by area", CR, dict(top_crop=c), "agc_district", intc,
            "Allocation extras", agg="count")
    for c in ["rice", "cotton", "sugarcane", "maize", "wheat"]:
        add(f"second_crop_{c}", f"Districts where {c} is the second-largest of the five tracked crops", CR, dict(second_crop=c), "agc_district",
            intc, "Allocation extras", agg="count")
    PL = "docs/price_ladder.csv"
    add("igc_bank_low", "IGC 2013: lowest bank rate reported by interviewed farmers (% p.a.; supplied by Ahmed, checklist P3)", PL,
        dict(item="Bank rates reported by interviewed farmers"), "rate_low", "{:.0f}", "Cost (context)")
    add("igc_bank_high", "IGC 2013: highest bank rate reported by interviewed farmers (% p.a.)", PL,
        dict(item="Bank rates reported by interviewed farmers"), "rate_high", "{:.0f}", "Cost (context)")
    add("kissan_terms", "Punjab CM Kissan Card: terms and dates", PL, dict(item="Punjab CM Kissan Card (interest-free)"), "note", "{}",
        "Cost (context)")
    # course methods (EXPLORATORY, scripts/15_course_methods.py, D041)
    WS, GC = "outputs/tables/course_weights_sensitivity.csv", "outputs/tables/course_gistar_counts.csv"
    TS, DI = "outputs/tables/course_trend_surface.csv", "outputs/tables/course_dissimilarity.csv"
    KS, KP = "outputs/tables/course_kmeans_silhouette.csv", "outputs/tables/course_kmeans_profiles.csv"
    TI, HI, DO = "outputs/tables/course_tissot_distortion.csv", "outputs/tables/course_classification_histograms.csv", "outputs/tables/course_dasymetric_dots.csv"
    ws = pd.read_csv(ROOT / WS)
    band = ws[ws.weights.str.startswith("Distance band")].weights.iloc[0]
    inv = ws[ws.weights.str.startswith("Inverse distance")].weights.iloc[0]
    add("moran_rook", "Global Moran's I, arhti_share, tehsils, Rook (same neighbour sets as Queen)", WS, dict(statistic="Moran's I", weights="Rook"), "value", f3, "Course methods")
    add("moran_dband", f"Global Moran's I, arhti_share, tehsils, {band}", WS, dict(statistic="Moran's I", weights=band), "value", f3, "Course methods")
    add("dband_km", "Distance band threshold (km, geodesic; smallest with no unit lacking a neighbour)", WS, dict(statistic="Moran's I", weights=band),
        "weights", lambda v: v.split("geodesic, ")[1].rstrip(")"), "Course methods")
    add("moran_invd", f"Global Moran's I, arhti_share, tehsils, {inv}", WS, dict(statistic="Moran's I", weights=inv), "value", f3, "Course methods")
    add("geary_c", "Geary's C, arhti_share, tehsils, Queen (E[C] = 1; < 1 = positive autocorrelation)", WS, dict(statistic="Geary's C"), "value", f3, "Course methods")
    add("geary_c_p", "Geary's C pseudo p-value", WS, dict(statistic="Geary's C"), "p_perm", f3, "Course methods")
    for cl, kk in [("Hot spot", "hot"), ("Cold spot", "cold")]:
        add(f"gistar_{kk}_p05", f"Gi* {cl.lower()}s, p < 0.05", GC, {"class": cl}, "p05", intc, "Course methods")
        add(f"gistar_{kk}_fdr", f"Gi* {cl.lower()}s surviving FDR 0.05", GC, {"class": cl}, "fdr05", intc, "Course methods")
    for o in (1, 2):
        add(f"trend{o}_r2", f"Trend surface order {o}: R²", TS, dict(order=o), "r2", f2, "Course methods")
        add(f"trend{o}_resid_I", f"Trend surface order {o}: Moran's I of residuals (Queen)", TS, dict(order=o), "resid_moran_I", f3, "Course methods")
        add(f"trend{o}_resid_p", f"Trend surface order {o}: residual Moran pseudo p", TS, dict(order=o), "resid_moran_p", f3, "Course methods")
    for g_, kk in [("mouzas reporting arhti credit", "D_arhti"), ("mouzas reporting commercial-bank credit", "D_commercial"),
                   ("mouzas reporting ZTBL credit", "D_ztbl"), ("SBP subsistence-holding borrower records", "D_sub_borrowers"),
                   ("rural scheduled-bank branches", "D_rural_branches"), ("all scheduled-bank branches", "D_all_branches")]:
        add(kk, f"Index of dissimilarity: {g_} vs reference", DI, dict(group=g_), "D", f3, "Course methods")
    for sp, kk in [("attributes", "attr"), ("attributes + location", "loc")]:
        add(f"kmeans_k_{kk}", f"k-means types, {sp}", KP, dict(spec=sp), "type", intc, "Course methods", agg="count")
        add(f"kmeans_sil_{kk}", f"Silhouette of the chosen k-means solution, {sp}", KS, dict(spec=sp), "silhouette", f2, "Course methods", agg="max")
    for crs_lab, kk in [("ESRI:102028 (Albers, centred 125°E; previous analysis CRS)", "old"), ("Analysis CRS (Albers, centred 72°E, 30°N; D025)", "new")]:
        add(f"tissot_angdist_{kk}", f"Maximum angular distortion over the Punjab grid (deg), {crs_lab}", TI, dict(crs=crs_lab), "angular_distortion_deg",
            f2, "Course methods", agg="max")
    for sc, kk in [("Equal interval", "ei"), ("Quantiles", "q"), ("Natural breaks (Fisher-Jenks)", "nb")]:
        add(f"gadf_{kk}", f"GADF, arhti_share, 5 classes, {sc}", HI, dict(scheme=sc), "gadf", f3, "Course methods")
    LD = dict(level="district", scenario="A", analysis="LISA arhti_share", weights="Queen")
    for cl, kk in [("High-High", "hh"), ("Low-Low", "ll")]:
        add(f"lisa_district_{kk}_p05", f"LISA {cl} districts, Queen, p < 0.05 (MAUP comparison)", LC, dict(LD, cluster=cl), "p05", intc, "Course methods")
        add(f"lisa_district_{kk}_fdr", f"LISA {cl} districts, Queen, FDR 0.05 (MAUP comparison)", LC, dict(LD, cluster=cl), "fdr05", intc, "Course methods")
    for mt in ["exact", "normalized", "spelling", "rename", "parent_aggregation", "unmatched"]:
        add(f"xwalk_{mt}", f"Census tehsils matched to OCHA polygons: {mt}", "data/interim/tehsil_crosswalk.csv", dict(match_type=mt),
            "source_code", intc, "Data", agg="count")
    add("xwalk_total", "Census tehsils in the crosswalk", "data/interim/tehsil_crosswalk.csv", {}, "source_code", intc, "Data", agg="count")
    add("kmeans_t1_arhti", "k-means type 1 (attributes): median arhti_share", KP, dict(spec="attributes", type=1), "arhti_share", lambda v: f"{100 * v:.0f}%", "Course methods")
    add("kmeans_t1_reach", "k-means type 1 (attributes): median small-farm reach", KP, dict(spec="attributes", type=1), "small_farm_reach", "{:.0f}", "Course methods")
    add("kmeans_t2_reach", "k-means type 2 (attributes): median small-farm reach", KP, dict(spec="attributes", type=2), "small_farm_reach", "{:.0f}", "Course methods")
    LN = "docs/literature_numbers.csv"
    for lid in ["aleem_cost", "aleem_bank", "igc_markets", "igc_range_low", "igc_range_high", "kf_large_hh", "kf_large_loans",
                "kf_small_hh", "kf_small_loans"]:
        add(f"lit_{lid}", f"Literature: {lid}", LN, dict(id=lid), "display", "{}", "Literature (quoted)")
    add("n_districts_q1", "Districts in the Q1 MAUP comparison (rural populated mouzas > 0)", MG, dict(q, level="district"), "n", intc, "Robustness")
    add("n_tehsil_polygons", "OCHA tehsil polygons in Punjab (Q1 layer, incl. 2 with no rural populated mouzas)",
        "gpkg:q1_tehsils_mouza_census_2020", {}, "adm3_pcode", intc, "Data", agg="count")
    add("dots_total", "Dasymetric dots (1 dot = 1,000 farms under 12.5 acres)", DO, {}, "dots", intc, "Course methods", agg="sum")

    k = pd.DataFrame(ROWS)
    k.to_csv(T / "key_numbers.csv", index=False)
    L = ["# Key numbers", "",
         "Every number used in the main text, the app and the slides. Written by `scripts/17_key_numbers.py` from finished outputs; "
         "nothing here is computed anew. Source = file; Row = filter that selects the row; Column = field.", ""]
    for sec, g in k.groupby("section", sort=False):
        L += [f"## {sec}", "", "| ID | Number | Shown as | Source | Row | Column |", "|---|---|---|---|---|---|"]
        L += [f"| `{r.id}` | {r.label} | **{r.display}** | `{r.source}` | {r.row} | `{r.column}` |" for r in g.itertuples()]
        L.append("")
    (ROOT / "docs" / "key_numbers.md").write_text("\n".join(L))
    print(k[["id", "display"]].to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
