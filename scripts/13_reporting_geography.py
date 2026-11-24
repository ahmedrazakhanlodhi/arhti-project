"""13_reporting_geography.py: ALLOCATION by holding class, REPORTING GEOGRAPHY of SBP district data, crop structure,
and a descriptive district scorecard (D039, D040). Existing outputs are not changed.

    .venv/bin/python -I scripts/13_reporting_geography.py

Outputs
- outputs/tables/holding_class_shares.csv    Punjab shares of farms / operated area / borrower records / disbursement by class
- outputs/tables/crop_structure_district.csv  district crop areas (Agricultural Census 2024, Tables 6.1, 6.9-6.13) and shares
- outputs/tables/reporting_geography.csv      district location quotients (LQ), credit per cultivated acre, branches;
                                              five-city and Islamabad summary rows
- outputs/tables/district_scorecard.csv       one row per district (36) with a descriptive profile type
- outputs/figures/figA1_holding_class_shares, figR1_lq_maps, figR2_city_shares (PNG + PDF)

District disbursement AMOUNTS are mapped only here (rule change D039), labelled with ATTRIBUTION until Ahmed confirms
how SBP assigns loans to districts.
"""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

import geopandas as gpd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import pypdfium2 as pdfium  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
T = ROOT / "outputs" / "tables"
F = ROOT / "outputs" / "figures"
GPKG = ROOT / "outputs" / "arhti_project.gpkg"
AGC_PDF = ROOT / "data" / "raw" / "ag_census_2024" / "IAC-Punjab-Report-25-05-2026-1.pdf"

ATTRIBUTION = "district as reported by SBP (attribution under verification)"
CITIES = ["Lahore", "Rawalpindi", "Multan", "Faisalabad", "Rahim Yar Khan"]
CROPS = {  # crop: (report page, Table, index of the 'area under crop' value among the numbers on each row)
    "wheat": (135, "6.9", 3), "rice": (136, "6.10", 1), "cotton": (137, "6.11", 3), "maize": (138, "6.12", 3),
    "sugarcane": (139, "6.13", 3)}
CROPPED = (102, "6.1", 0)          # total cropped area


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


ca = load("ca", ROOT / "scripts" / "08_credit_allocation.py")      # SBP and Ag Census readers (validated in 08)
figs = load("figs", ROOT / "scripts" / "09_figures.py")            # palettes and map furniture
V_SBP, V_AGC, V_MC, V_BR = ca.V_SBP, ca.V_AGC, ca.V_MC, ca.V_BR
V_SBP_R = f"SBP, FY2023-24 (Jul 2023-Jun 2024), {ATTRIBUTION}"
V_SBP_P = "SBP, FY2023-24 (Jul 2023-Jun 2024), All-Punjab row"   # province level: district attribution does not arise


# ------------------------------------------------------------------------------------------ Part 2: holding classes
CLASS_MAP = {"subsistence": (ca.SMALL, "up to 12.5 acres", "under 12.5 acres (classes under 1.0 ... 7.5 to under 12.5)",
                             "SBP includes holdings of exactly 12.5 acres; the census places 12.5 in 12.5 to under 25"),
             "economic": (["12.5 TO UNDER 25.0", "25.0 TO UNDER 50.0"], "above 12.5 to 50 acres", "12.5 to under 50 acres",
                          "SBP includes exactly 50 and excludes exactly 12.5; the census does the reverse"),
             "above_economic": (ca.LARGE, "above 50 acres", "50 acres and above",
                                "farms of exactly 50 acres are 'economic' for SBP and 'large' in the census")}


def holding_classes(a, special, rows36):
    """Shares by class. Primary (*_36): the 36 districts on both sides (SBP district rows without Islamabad and without the
    MFI row, which has no district; census Punjab minus the Cholistan Area). Comparison: SBP All Punjab row vs census Punjab (D042)."""
    p = a[a.unit == "PUNJAB"]
    ch = a[a.unit == "CHOLISTAN AREA"]
    tot = p[p.size_class == "PRIVATE-FARMS TOTAL"].iloc[0]
    tot36 = tot[["farms", "farm_area_ac", "cultivated_ac"]] - ch[ch.size_class == "PRIVATE-FARMS TOTAL"].iloc[0][["farms", "farm_area_ac", "cultivated_ac"]]
    ap, dr = special.loc["All Punjab"], special.loc["Total"]
    d36 = rows36[[c for c in rows36.columns if c.endswith(("_borrowers", "_amount_mn"))]].sum()
    rows = []
    for k, (cls, sbp_def, pbs_def, mismatch) in CLASS_MAP.items():
        s = p[p.size_class.isin(cls)][["farms", "farm_area_ac", "cultivated_ac"]].sum()
        s36 = s - ch[ch.size_class.isin(cls)][["farms", "farm_area_ac", "cultivated_ac"]].sum()
        pre = {"subsistence": "sub", "economic": "eco", "above_economic": "abv"}[k]
        rows.append(dict(
            holding_class=k, sbp_definition=sbp_def, pbs_classes_used=pbs_def, boundary_mismatch=mismatch,
            share_farms=s.farms / tot.farms, share_operated_area=s.farm_area_ac / tot.farm_area_ac,
            share_cultivated_area=s.cultivated_ac / tot.cultivated_ac,
            share_borrower_records=ap[f"{pre}_borrowers"] / ap.tot_borrowers, share_disbursement=ap[f"{pre}_amount_mn"] / ap.tot_amount_mn,
            share_borrower_records_banks_only=dr[f"{pre}_borrowers"] / dr.tot_borrowers,
            share_disbursement_banks_only=dr[f"{pre}_amount_mn"] / dr.tot_amount_mn,
            farms=s.farms, operated_area_ac=s.farm_area_ac, borrower_records=ap[f"{pre}_borrowers"], disbursement_mn=ap[f"{pre}_amount_mn"],
            share_farms_36=s36.farms / tot36.farms, share_operated_area_36=s36.farm_area_ac / tot36.farm_area_ac,
            share_borrower_records_36=d36[f"{pre}_borrowers"] / d36.tot_borrowers, share_disbursement_36=d36[f"{pre}_amount_mn"] / d36.tot_amount_mn,
            borrower_records_36=d36[f"{pre}_borrowers"], disbursement_mn_36=d36[f"{pre}_amount_mn"], farms_36=s36.farms,
            disbursement_per_record_mn_36=d36[f"{pre}_amount_mn"] / d36[f"{pre}_borrowers"],
            total_borrower_records_36=d36.tot_borrowers, total_disbursement_mn_36=d36.tot_amount_mn,
            total_borrower_records_all_punjab=ap.tot_borrowers, total_disbursement_mn_all_punjab=ap.tot_amount_mn,
            mfi_borrower_records=special.loc["MFIs"].tot_borrowers))
    d = pd.DataFrame(rows)
    for c in ["share_farms", "share_operated_area", "share_borrower_records", "share_disbursement", "share_farms_36",
              "share_operated_area_36", "share_borrower_records_36", "share_disbursement_36"]:
        assert abs(d[c].sum() - 1) < 1e-6, c
    d["ratio_records_to_farms_36"] = d.share_borrower_records_36 / d.share_farms_36
    d["ratio_disbursement_to_farms_36"] = d.share_disbursement_36 / d.share_farms_36
    d["sbp_scope"] = ("*_36 (primary) = 36 district rows, banks only (no Islamabad, no MFIs); unsuffixed = All Punjab row (banks + MFIs); "
                     "*_banks_only = district rows incl. Islamabad, no MFIs")
    d["pbs_scope"] = "*_36 = PUNJAB minus Cholistan Area (36 districts); unsuffixed = PUNJAB total incl. Cholistan Area"
    d["note"] = "Province level only; operated (farm) area, not owned area; borrower records may not be unique people"
    d["vintage"] = f"{V_SBP_P}; {V_AGC}"
    return d


def coverage_reconciliation(rows, special):
    """SBP farm-sector totals by holding class: 36 districts + Islamabad + MFIs (no district) = All Punjab (D043)."""
    cols = ["sub_borrowers", "eco_borrowers", "abv_borrowers", "tot_borrowers", "sub_amount_mn", "eco_amount_mn", "abv_amount_mn", "tot_amount_mn"]
    isl = rows[rows.district == "Islamabad"][cols].sum()
    d36 = rows[rows.district != "Islamabad"][cols].sum()
    mfi = special.loc["MFIs"].reindex(cols).fillna(0)
    ap = special.loc["All Punjab"].reindex(cols)
    out = pd.DataFrame([d36, isl, mfi, d36 + isl + mfi, ap], index=["36 districts (banks)", "Islamabad row (banks)", "MFIs (Punjab-wide, no district)",
                                                                     "Sum of the three", "SBP All Punjab row"])
    gap = (out.loc["Sum of the three"] - out.loc["SBP All Punjab row"]).abs().max()
    assert gap < 1, f"reconciliation gap {gap}"
    out = out.rename_axis("scope").reset_index()
    for c in [c for c in cols if c.endswith("_mn")]:
        out[c.replace("_mn", "_bn")] = out[c] / 1000
    out["vintage"] = f"{V_SBP_R}; farm sector"
    return out


def agc_area_check(a):
    """Agricultural Census Table 3, Punjab: implied average farm area by size class vs the class limits (D042)."""
    p = a[(a.unit == "PUNJAB") & (a.size_class != "PRIVATE-FARMS TOTAL")].copy()
    lims = {"UNDER 1.0": (0, 1), "1.0 TO UNDER 2.5": (1, 2.5), "2.5 TO UNDER 5.0": (2.5, 5), "5.0 TO UNDER 7.5": (5, 7.5),
            "7.5 TO UNDER 12.5": (7.5, 12.5), "12.5 TO UNDER 25.0": (12.5, 25), "25.0 TO UNDER 50.0": (25, 50),
            "50.0 TO UNDER 100.0": (50, 100), "100.0 AND ABOVE": (100, None)}
    p["class_lower_ac"] = p.size_class.map(lambda c: lims[c][0])
    p["class_upper_ac"] = p.size_class.map(lambda c: lims[c][1])
    p["implied_avg_farm_area_ac"] = p.farm_area_ac / p.farms
    p["implied_avg_cultivated_ac"] = p.cultivated_ac / p.farms
    p["within_class_limits"] = (p.implied_avg_farm_area_ac >= p.class_lower_ac) & (p.class_upper_ac.isna() | (p.implied_avg_farm_area_ac < p.class_upper_ac.fillna(1e9)))
    p["vintage"] = V_AGC
    p = p.sort_values("class_lower_ac")
    return p[["size_class", "class_lower_ac", "class_upper_ac", "farms", "farm_area_ac", "cultivated_ac", "implied_avg_farm_area_ac",
              "implied_avg_cultivated_ac", "within_class_limits", "vintage"]]


def fig_a1(h):
    fig, ax = plt.subplots(figsize=(9.5, 5.6))
    bars = [("share_farms_36", "Share of farms", figs.BLUE5[1]), ("share_operated_area_36", "Share of operated farm area (see note)", figs.BLUE5[3]),
            ("share_borrower_records_36", "Share of borrower records", figs.ORANGE5[1]), ("share_disbursement_36", "Share of disbursement", figs.ORANGE5[3])]
    x = np.arange(len(h)); w = 0.2
    for i, (c, lab, col) in enumerate(bars):
        b = ax.bar(x + (i - 1.5) * w, 100 * h[c], w * 0.92, color=col, label=lab, edgecolor="white", linewidth=1.2)
        for r, v in zip(b, h[c]):
            ax.text(r.get_x() + r.get_width() / 2, 100 * v + 1, f"{100 * v:.1f}", ha="center", va="bottom", fontsize=7, color=figs.INK)
    ax.set_xticks(x, [f"{k.replace('_', '-')}\nSBP: {s}\ncensus: {p.split(' (')[0]}" for k, s, p in
                      zip(h.holding_class, h.sbp_definition, h.pbs_classes_used)], fontsize=7.5)
    ax.set_ylabel("Percent of Punjab total"); ax.set_ylim(0, 105)
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    ax.grid(axis="y", color="#eceae5"); ax.set_axisbelow(True)
    ax.legend(frameon=False, fontsize=7.5, ncol=2, loc="upper center")
    fig.suptitle("Figure A1. Farms, operated area and formal credit by holding class, Punjab's 36 districts", x=0.01, ha="left", fontsize=11, fontweight="bold")
    fig.text(0.01, -0.06, "\n".join([
        "Classes: SBP 'up to 12.5 / above 12.5-50 / above 50 acres' (CL1 Annex) vs census 'under 12.5 / 12.5-under 50 / 50 and above'; the",
        "boundary farms (exactly 12.5 or 50 acres) fall in different classes. Census area = operated (farm) area, not owned land.",
        f"Data: {V_SBP_R}, 36 district rows (banks; Islamabad and the {int(h.mfi_borrower_records.iloc[0]):,} MFI records without a district excluded); "
        f"{V_AGC}, Punjab minus Cholistan Area.",
        f"All Punjab row incl. MFIs and Islamabad: subsistence {100 * h.share_borrower_records.iloc[0]:.1f}% of records, {100 * h.share_disbursement.iloc[0]:.1f}% "
        "of disbursement. Census class areas: in three classes below 12.5 acres the published farm area implies an average above the class "
        "limit (D042), so area shares are indicative. Not contemporaneous; borrower records may not be unique people.",
        f"{figs.AUTHOR}. Script: scripts/13_reporting_geography.py."]),
        fontsize=6.2, color=figs.MUTED, va="top")
    figs.save(fig, "figA1_holding_class_shares")


# ------------------------------------------------------------------------------------------ Part 2.3: crops
NUM = re.compile(r"^([A-Z][A-Z .\-]+?)\s+((?:[\d,.]+|-)(?:\s+(?:[\d,.]+|-))*)\s*$")


def report_table(page: int, idx: int, label: str) -> pd.Series:
    t = pdfium.PdfDocument(AGC_PDF)[page - 1].get_textpage().get_text_range()
    assert f"TABLE {label}" in t.replace("TABLE  ", "TABLE "), (page, label)
    out = {}
    for line in t.splitlines():
        m = NUM.match(line.strip())
        if m and re.search(r"(DISTRICT|DIVISION|CHOLISTAN AREA|^PUNJAB)$", m.group(1).strip()):
            vals = [0.0 if v == "-" else float(v.replace(",", "")) for v in m.group(2).split()]
            assert len(vals) > idx, (label, line)
            out[m.group(1).strip()] = vals[idx]
    return pd.Series(out, name=label)


def crops() -> pd.DataFrame:
    cols = {"cropped_area_ac": report_table(CROPPED[0], CROPPED[2], CROPPED[1])}
    for c, (pg, lab, idx) in CROPS.items():
        cols[f"{c}_area_ac"] = report_table(pg, idx, lab)
    d = pd.DataFrame(cols)
    dist = d[d.index.str.endswith(" DISTRICT")]
    assert len(dist) == 36, len(dist)
    # validation: districts + Cholistan Area sum to Punjab for every column (published rounding allowed)
    chk = (dist.sum() + d.loc["CHOLISTAN AREA"] - d.loc["PUNJAB"]).abs() / d.loc["PUNJAB"]
    assert (chk < 0.001).all(), chk
    out = dist.copy()
    for c in CROPS:
        out[f"{c}_share_of_cropped"] = out[f"{c}_area_ac"] / out.cropped_area_ac
    out["top2_crops"] = [", ".join(sorted(CROPS, key=lambda c: -r[f"{c}_area_ac"])[:2]) for _, r in out.iterrows()]
    out["top_crop"] = out.top2_crops.str.split(", ").str[0]
    out["second_crop"] = out.top2_crops.str.split(", ").str[1]
    out = out.reset_index().rename(columns={"index": "agc_district"})
    out["source"] = ("Agricultural Census 2024, Punjab report, Tables 6.1 (p. 102), 6.9 (p. 135), 6.10 (p. 136), 6.11 (p. 137), "
                     "6.12 (p. 138), 6.13 (p. 139); area in acres; reference period Rabi 2023-24 + Kharif 2024")
    out["vintage"] = V_AGC
    return out, chk.max()


# ------------------------------------------------------------------------------------------ Part 3: reporting geography
def reporting(rows, a, dca, q2):
    agc_cls = {k: a[a.size_class.isin(v[0])].groupby("unit")[["farms", "farm_area_ac"]].sum() for k, v in CLASS_MAP.items()}
    s = rows.set_index("district")
    d = dca[["adm2_name", "adm2_pcode", "sbp_district", "agc_district", "farms", "cultivated_ac", "flagged"]].dropna(subset=["sbp_district"]).copy()
    assert len(d) == 36
    for pre in ["sub", "eco", "abv", "tot"]:
        d[f"{pre}_amount_mn"] = d.sbp_district.map(s[f"{pre}_amount_mn"])
        d[f"{pre}_borrowers"] = d.sbp_district.map(s[f"{pre}_borrowers"])
    for k, pre in [("subsistence", "sub"), ("economic", "eco"), ("above_economic", "abv")]:
        d[f"{pre}_farms"] = d.agc_district.map(agc_cls[k].farms)
    area_share = d.cultivated_ac / d.cultivated_ac.sum()
    d["area_share"] = area_share
    d["farm_share"] = d.farms / d.farms.sum()
    for pre in ["sub", "eco", "abv", "tot"]:
        d[f"credit_share_{pre}"] = d[f"{pre}_amount_mn"] / d[f"{pre}_amount_mn"].sum()
        d[f"lq_amount_{pre}"] = d[f"credit_share_{pre}"] / area_share
        fshare = d.farm_share if pre == "tot" else d[f"{pre}_farms"] / d[f"{pre}_farms"].sum()
        d[f"lq_borrowers_{pre}"] = (d[f"{pre}_borrowers"] / d[f"{pre}_borrowers"].sum()) / fshare
    d["credit_per_cultivated_acre_rs"] = d.tot_amount_mn * 1e6 / d.cultivated_ac
    br = q2.set_index("adm2_pcode")
    d["branches_total"] = d.adm2_pcode.map(br.branches_scheduled)
    d["branches_rural"] = d.adm2_pcode.map(br.branches_rural)
    d["total_branches_per_10k_farms"] = d.branches_total / d.farms * 1e4
    d["rural_branches_per_10k_farms"] = d.branches_rural / d.farms * 1e4
    d["record_type"] = "district"
    # summaries
    def summ(mask, name):
        g = d[mask]
        r = dict(record_type="summary", adm2_name=name)
        for pre in ["sub", "eco", "abv", "tot"]:
            r[f"credit_share_{pre}"] = g[f"credit_share_{pre}"].sum()
        r.update(area_share=g.area_share.sum(), farm_share=g.farm_share.sum(),
                 rural_branch_share=g.branches_rural.sum() / d.branches_rural.sum(),
                 total_branch_share=g.branches_total.sum() / d.branches_total.sum(),
                 credit_per_cultivated_acre_rs=g.tot_amount_mn.sum() * 1e6 / g.cultivated_ac.sum())
        return r
    summary = [summ(d.adm2_name.isin(CITIES), "Five cities combined (" + ", ".join(CITIES) + ")")]
    summary += [summ(d.adm2_name == c, c) for c in CITIES]
    summary.append(summ(~d.adm2_name.isin(CITIES), "Other 31 districts combined"))
    isb = s.loc["Islamabad"]
    tot_incl = s[[c for c in s.columns if c.endswith("_amount_mn")]].sum()
    summary.append(dict(record_type="Islamabad (booked; not in area ratios)", adm2_name="Islamabad",
                        **{f"credit_share_{p}": isb[f"{p}_amount_mn"] / tot_incl[f"{p}_amount_mn"] for p in ["sub", "eco", "abv", "tot"]},
                        **{f"{p}_amount_mn": isb[f"{p}_amount_mn"] for p in ["sub", "eco", "abv", "tot"]},
                        note="share of SBP district rows INCLUDING Islamabad; Islamabad has no Punjab farmland in the Ag Census denominator"))
    out = pd.concat([d, pd.DataFrame(summary)], ignore_index=True)
    out["district_attribution"] = ATTRIBUTION
    out["scope"] = ("36 Punjab districts (SBP district rows matched to Ag Census); Islamabad reported separately; MFIs (Punjab-only row) "
                    "excluded from district ratios")
    out["lq_definition"] = ("lq_amount_h = district share of Punjab class-h disbursement / district share of cultivated area; "
                            "lq_borrowers_h = district share of class-h borrower records / district share of class-h farms")
    out["vintage"] = f"{V_SBP_R}; {V_AGC} (cultivated area, farms by class); {V_BR}"
    return out


# ------------------------------------------------------------------------------------------ figures R1, R2
LQ_BREAKS = [0.25, 0.5, 0.8, 1.25, 2, 4]
LQ_COLS = ["#0d366b", "#2a78d6", "#9ec5f4", "#f0efec", "#f2a7a6", "#e34948", "#8f1d1c"]
LQ_LABS = ["< 0.25", "0.25 – 0.5", "0.5 – 0.8", "0.8 – 1.25 (≈ proportional)", "1.25 – 2", "2 – 4", "> 4"]


def fig_r1(rg):
    g = gpd.read_file(GPKG, layer="q2_districts_credit_allocation").to_crs(figs.CRS)[["adm2_pcode", "geometry"]]
    d = g.merge(rg[rg.record_type == "district"], on="adm2_pcode", how="left")
    fig, axes = plt.subplots(1, 2, figsize=(13, 8.6))
    fig.subplots_adjust(top=0.9, bottom=0.25, wspace=0.02)
    for ax, pre, title in [(axes[0], "abv", "A. Above-economic holdings (> 50 acres)"), (axes[1], "sub", "B. Subsistence holdings (up to 12.5 acres)")]:
        k = np.digitize(d[f"lq_amount_{pre}"], LQ_BREAKS)
        for i, col in enumerate(LQ_COLS):
            sub = d[(k == i) & d[f"lq_amount_{pre}"].notna()]
            if len(sub):
                sub.plot(ax=ax, color=col, edgecolor="white", linewidth=0.5)
        fl = d[d.flagged == 1]
        pts = fl.geometry.representative_point()
        ax.scatter(pts.x, pts.y, marker="^", s=34, facecolor="white", edgecolor=figs.INK, linewidth=0.9, zorder=5)
        figs.frame(ax, d); figs.furniture(ax, d)
        cnt = [int(((k == i) & d[f"lq_amount_{pre}"].notna()).sum()) for i in range(7)]
        figs.legend(ax, [Patch(facecolor=c, edgecolor="#bdbcb6", label=f"{l}  (n = {n})") for c, l, n in zip(LQ_COLS, LQ_LABS, cnt)]
                    + [figs.Line2D([], [], marker="^", ls="", markerfacecolor="white", markeredgecolor=figs.INK,
                                   label=f"Flagged in SBP data-quality screen (n = {len(fl)})")],
                    "Location quotient (log scale, centred on 1)\nshare of class disbursement ÷ share of cultivated area",
                    ncol=2)   # below the map, so it never covers districts
        ax.set_title(title, loc="left", fontsize=9.5)
    fig.suptitle(f"Figure R1. Where SBP records agricultural lending relative to farmland: location quotients by holding class\n"
                 f"District = {ATTRIBUTION}", x=0.01, y=0.99, ha="left", fontsize=10.5, fontweight="bold")
    fig.text(0.01, 0.0, "\n".join(["LQ = district share of Punjab disbursement in the class ÷ district share of Punjab cultivated area. 1 = proportional; "
                      "> 1 = more lending recorded than farmland. Fixed breaks symmetric on a log scale.",
                      "Disbursement AMOUNTS are mapped here only (D039). Until SBP's district attribution is confirmed, an LQ above 1 may reflect where loans are "
                      "recorded (e.g. city branches) rather than where the land is.",
                      f"Data: {V_SBP_R}; {V_AGC} (cultivated area). 36 districts; Islamabad and MFIs excluded. Not contemporaneous. {figs.V_B}.",
                      f"CRS: {figs.common.CRS_LABEL}; north arrow = true north. {figs.AUTHOR}. Script: scripts/13_reporting_geography.py."]),
             fontsize=6.2, color=figs.MUTED, va="top")
    figs.save(fig, "figR1_lq_maps")


def fig_r2(rg):
    s = rg[(rg.record_type == "summary") & rg.adm2_name.isin(CITIES + [r for r in rg.adm2_name if str(r).startswith("Five cities")])]
    order = [n for n in s.adm2_name if str(n).startswith("Five")] + CITIES
    s = s.set_index("adm2_name").loc[order]
    bars = [("credit_share_tot", "Share of disbursement (all holdings)", figs.ORANGE5[1]),
            ("credit_share_abv", "Share of above-economic disbursement", figs.ORANGE5[3]),
            ("area_share", "Share of cultivated area", figs.BLUE5[3]), ("farm_share", "Share of farms", figs.BLUE5[1]),
            ("rural_branch_share", "Share of rural bank branches", figs.CAT["aqua"]), ("total_branch_share", "Share of all bank branches", "#0e6b4a")]
    fig, ax = plt.subplots(figsize=(11, 5.8))
    x = np.arange(len(s)); w = 0.13
    for i, (c, lab, col) in enumerate(bars):
        ax.bar(x + (i - 2.5) * w, 100 * s[c], w * 0.9, color=col, label=lab, edgecolor="white", linewidth=0.8)
    ax.set_xticks(x, [n if not n.startswith("Five") else "Five cities combined" for n in s.index], fontsize=8)
    ax.set_ylabel("Percent of the 36-district Punjab total")
    for sp in ["top", "right"]:
        ax.spines[sp].set_visible(False)
    ax.grid(axis="y", color="#eceae5"); ax.set_axisbelow(True)
    ax.legend(frameon=False, fontsize=7.5, ncol=3, loc="upper right")
    fig.suptitle(f"Figure R2. Five large-city districts: recorded credit vs farmland, farms and bank branches\nDistrict = {ATTRIBUTION}",
                 x=0.01, ha="left", fontsize=10.5, fontweight="bold")
    isb = rg[rg.adm2_name == "Islamabad"].iloc[0]
    fig.text(0.01, -0.05, "\n".join([
        f"Islamabad (not in the 36-district totals): {100 * isb.credit_share_tot:.1f}% of all disbursement in SBP district rows including Islamabad, "
        f"{100 * isb.credit_share_abv:.1f}% of above-economic disbursement.",
        f"Data: {V_SBP_R}; {V_AGC}; {V_BR} (rural = branches coded R). MFIs excluded. Not contemporaneous.",
        f"{figs.AUTHOR}. Script: scripts/13_reporting_geography.py."]), fontsize=6.2, color=figs.MUTED, va="top")
    figs.save(fig, "figR2_city_shares")


# ------------------------------------------------------------------------------------------ scorecard
PROFILE_RULE = ("Two splits at the median across districts: arhti_share (35 districts with rural populated mouzas) and small_farm_reach "
                "(36 districts). Profile = 'high/low arhti availability + high/low small-farm reach'; Lahore (no rural populated mouzas) is "
                "'not classified'. Descriptive groupings, not rankings.")


def scorecard(dca, q2, crop, rg):
    d = q2[["adm2_pcode", "adm2_name", "farms", "small_farm_reach", "tenant_share", "flagged", "branches_scheduled", "branches_rural",
            "rural_branches_per_10k_farms", "all_branches_per_10k_farms_sensitivity"]].copy()
    d = d.merge(dca[["adm2_pcode", "agc_district", "cultivated_ac", "small_farms"]], on="adm2_pcode", how="left")
    d["smallholder_share"] = d.small_farms / d.farms
    d = d.merge(crop[["agc_district", "top2_crops"]], on="agc_district", how="left")
    q1 = gpd.read_file(GPKG, layer="q1_districts_mouza_census_2020_MAUP")[["adm2_pcode", "arhti_share", "commercial_share", "ztbl_share", "rp_mouzas"]]
    d = d.merge(q1, on="adm2_pcode", how="left")
    t = gpd.read_file(GPKG, layer="q1_tehsils_mouza_census_2020")
    for col, lab in [("lisa_queen_p05", "p05"), ("lisa_queen_fdr05", "fdr05")]:
        for cl, k in [("High-High", "hh"), ("Low-Low", "ll")]:
            d[f"tehsils_{k}_{lab}"] = d.adm2_name.map(t[t[col] == cl].groupby("adm2_name").size()).fillna(0).astype(int)
    r = rg[rg.record_type == "district"].set_index("adm2_pcode")
    for c in ["credit_per_cultivated_acre_rs", "lq_amount_tot", "lq_amount_sub", "lq_amount_abv", "lq_borrowers_sub", "lq_borrowers_abv"]:
        d[c] = d.adm2_pcode.map(r[c])
    d = d.rename(columns={"all_branches_per_10k_farms_sensitivity": "total_branches_per_10k_farms"})
    ma, mr = d.arhti_share[d.rp_mouzas > 0].median(), d.small_farm_reach.median()
    d["profile_type"] = np.where(d.rp_mouzas.fillna(0) > 0,
                                 np.where(d.arhti_share > ma, "high arhti availability", "low arhti availability") + " + " +
                                 np.where(d.small_farm_reach > mr, "high small-farm reach", "low small-farm reach"), "not classified")
    d["profile_rule"] = PROFILE_RULE + f" Medians: arhti_share {ma:.3f}; small_farm_reach {mr:.1f}."
    d["district_attribution_for_credit_columns"] = ATTRIBUTION
    d["vintage"] = f"{V_MC} (availability, LISA); {V_SBP_R} (credit, reach); {V_AGC} (farms, area, crops, tenure); {V_BR}. Not contemporaneous."
    assert len(d) == 36
    return d


def main() -> int:
    val = {}
    rows, special = ca.sbp_punjab_farm(val)
    assert not val["v2_rows_vs_total"] and not val["v2_total_mfi_vs_all"] and not val["v3_category_sums"], "SBP checks failed"
    a, _ = ca.agc(val)
    dca = pd.read_csv(T / "district_credit_allocation.csv")
    q2 = gpd.read_file(GPKG, layer="q2_districts_credit_allocation")

    h = holding_classes(a, special, rows[rows.district != "Islamabad"])
    h.to_csv(T / "holding_class_shares.csv", index=False)
    coverage_reconciliation(rows, special).to_csv(T / "sbp_coverage_reconciliation.csv", index=False)
    agc_area_check(a).to_csv(T / "agc_class_area_check.csv", index=False)
    fig_a1(h)
    crop, worst = crops()
    crop.to_csv(T / "crop_structure_district.csv", index=False)
    rg = reporting(rows, a, dca, q2)
    rg.to_csv(T / "reporting_geography.csv", index=False)
    fig_r1(rg); fig_r2(rg)
    sc = scorecard(dca, q2, crop, rg)
    sc.to_csv(T / "district_scorecard.csv", index=False)

    print(h[["holding_class", "share_farms", "share_operated_area", "share_borrower_records", "share_disbursement"]].round(4).to_string(index=False))
    print(f"crop tables: districts + Cholistan vs Punjab, max relative gap {worst:.5f}")
    print(sc.profile_type.value_counts().to_string())
    return 0


if __name__ == "__main__":
    sys.exit(main())
