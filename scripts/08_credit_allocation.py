"""08_credit_allocation.py: district-level reach of formal agricultural credit by holding size (descriptive).

    .venv/bin/python -I scripts/08_credit_allocation.py     (after 05_boundaries_join.py and 06_raster_context.py)

Definitions and screening rules were prespecified in docs/decisions.md D021 before this script was first run.

Sources
- SBP, district-wise agri credit FY2023-24 (Jul 2023-Jun 2024): DistrictWise-Detail-Jul-Jun-2024.xlsx, Punjab FARM block.
  Validated against DWS-Jul-Jun-2024.pdf row by row, and against the published All-Punjab figures.
- SBP Indicative Credit Limits 2022-23 (CL1-Annex.pdf), Table 2.7: Punjab holding thresholds (parsed, not typed in).
- Agricultural Census 2024 (PBS; sample-based; fieldwork Sep 2024 + Jan-Feb 2025; ag year 2023-24):
  Table_3_District.xls (farms, farm area, cultivated area by size), Table_1_District.xls (farms by tenure by size).
  Validated against the Punjab report Tables 1.1 and 1.3.
- Mouza Census 2020 district aggregates (arhti_share, commercial_share) from data/processed/punjab_credit_context.gpkg.
- SBP list of scheduled bank branches as on 30 June 2024 (context only).
"""

from __future__ import annotations

import datetime as dt
import importlib.util
import re
import sys
import warnings
from pathlib import Path

import esda
import geopandas as gpd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pypdfium2 as pdfium
from libpysal.weights import Queen
from scipy.stats import spearmanr
from statsmodels.stats.multitest import multipletests

warnings.filterwarnings("ignore", category=UserWarning)

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
SBP_XLSX = RAW / "sbp" / "DistrictWise-Detail-Jul-Jun-2024.xlsx"
SBP_PDF = RAW / "sbp" / "DWS-Jul-Jun-2024.pdf"
CL1_PDF = RAW / "sbp" / "CL1-Annex.pdf"
BRANCH_XLSX = RAW / "sbp" / "Bank-Branches-Jun-2024.xlsx"
AGC_T1 = RAW / "ag_census_2024" / "Table_1_District.xls"
AGC_T3 = RAW / "ag_census_2024" / "Table_3_District.xls"
AGC_PDF = RAW / "ag_census_2024" / "IAC-Punjab-Report-25-05-2026-1.pdf"
CONTEXT = ROOT / "data" / "processed" / "punjab_credit_context.gpkg"
MANUAL = ROOT / "docs" / "crosswalk_manual_district.csv"
OUT_T, OUT_F = ROOT / "outputs" / "tables", ROOT / "outputs" / "figures"
OUT_GPKG = ROOT / "data" / "processed" / "district_credit_allocation.gpkg"
VAL_MD = ROOT / "docs" / "validation_sbp.md"
SUM_MD = OUT_T / "credit_allocation_summary.md"

EXPECTED = {"all_borrowers": 732856, "all_amount": 887737.4, "abv_borrowers": 8024, "abv_amount": 438386.5}
SEED, PERM, ALPHA, K = 20261031, 999, 0.05, 5
V_SBP = "SBP, FY2023-24 (Jul 2023-Jun 2024), loans by booking district"
V_AGC = "Agricultural Census 2024 (PBS), sample-based, fieldwork 2024-25"
V_MC = "Mouza Census 2020 (PBS), Jan-Mar 2020"
V_BR = "SBP list of scheduled bank branches as on 30 June 2024"
CATS = {"sub": "subsistence", "eco": "economic", "abv": "above_economic", "tot": "total"}
FIELDS = ["borrowers", "amount_mn", "recovery_mn", "outst_borrowers", "outst_mn"]
SMALL = ["UNDER 1.0", "1.0 TO UNDER 2.5", "2.5 TO UNDER 5.0", "5.0 TO UNDER 7.5", "7.5 TO UNDER 12.5"]
LARGE = ["50.0 TO UNDER 100.0", "100.0 AND ABOVE"]
ALLCLS = SMALL + ["12.5 TO UNDER 25.0", "25.0 TO UNDER 50.0"] + LARGE

# name-matching rules shared with 05_boundaries_join.py (exact / normalized / fuzzy-proposed)
_cs = importlib.util.spec_from_file_location("common", ROOT / "scripts" / "common.py")
common = importlib.util.module_from_spec(_cs); _cs.loader.exec_module(common)
_spec = importlib.util.spec_from_file_location("bj", ROOT / "scripts" / "05_boundaries_join.py")
bj = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bj)


def up(s):
    return re.sub(r"\s+", " ", str(s)).strip().upper()


def pdf_text(path):
    d = pdfium.PdfDocument(str(path))
    return {i + 1: d[i].get_textpage().get_text_range() for i in range(len(d))}


NUM = re.compile(r"^-?[\d,]*\.?\d+$|^-$")


def split_row(line):
    toks = line.split()
    k = len(toks)
    while k and NUM.match(toks[k - 1]):
        k -= 1
    vals = [0.0 if t == "-" else float(t.replace(",", "")) for t in toks[k:]]
    return " ".join(toks[:k]), vals


# ------------------------------------------------------------------------------------------ SBP
def sbp_punjab_farm(val):
    x = pd.read_excel(SBP_XLSX, header=None).dropna(how="all", axis=1)
    x.columns = range(x.shape[1])
    c0 = x[0].astype(str).str.strip()
    start = c0[c0 == "Name of Districts"].index[0] + 4          # first district row (after 3 header rows)
    end = c0[c0 == "All Punjab"].index[0]
    assert "FARM SECTOR" in str(x.iloc[0, 0]) and c0[c0 == "PUNJAB"].index[0] < start, "unexpected layout"
    block = x.iloc[start:end + 1, :21].copy()
    cols = ["district"] + [f"{c}_{f}" for c in CATS for f in FIELDS]
    block.columns = cols
    block["district"] = block["district"].astype(str).str.strip()
    block = block[block.district != "nan"].reset_index(drop=True)
    rows = block[~block.district.isin(["Total", "MFIs", "All Punjab"])].copy()
    special = block.set_index("district").loc[["Total", "MFIs", "All Punjab"]]
    num = [c for c in cols if c != "district"]
    rows[num] = rows[num].astype(float)
    special = special.astype(float)

    # V1 published figures
    ap = special.loc["All Punjab"]
    v1 = [("All Punjab total disbursed borrowers", ap.tot_borrowers, EXPECTED["all_borrowers"]),
          ("All Punjab total disbursed amount (Rs mn)", round(ap.tot_amount_mn, 1), EXPECTED["all_amount"]),
          ("All Punjab above-economic borrowers", ap.abv_borrowers, EXPECTED["abv_borrowers"]),
          ("All Punjab above-economic amount (Rs mn)", round(ap.abv_amount_mn, 1), EXPECTED["abv_amount"])]
    val["v1"] = v1
    # V2 district rows sum to Total; Total + MFIs = All Punjab
    s = rows[num].sum()
    val["v2_rows_vs_total"] = [(c, s[c], special.loc["Total", c]) for c in num if abs(s[c] - special.loc["Total", c]) > 0.01]
    tm = special.loc["Total", num] + special.loc["MFIs", num]
    val["v2_total_mfi_vs_all"] = [(c, tm[c], ap[c]) for c in num if abs(tm[c] - ap[c]) > 0.01]
    # V3 total columns = sum of categories
    bad = []
    for f in FIELDS:
        d = rows[f"sub_{f}"] + rows[f"eco_{f}"] + rows[f"abv_{f}"] - rows[f"tot_{f}"]
        bad += [(r.district, f, float(v)) for r, v in zip(rows.itertuples(), d) if abs(v) > 0.01]
    val["v3_category_sums"] = bad
    # V4 xlsx vs PDF page 1 (Punjab farm sector), every row and column
    pg = pdf_text(SBP_PDF)[1]
    pdf_rows = {}
    for line in pg.splitlines():
        name, v = split_row(line)
        if len(v) == 20 and name:
            pdf_rows[name] = v
    mism, missing = [], []
    for _, r in pd.concat([rows, special.reset_index()]).iterrows():
        if r.district not in pdf_rows:
            missing.append(r.district); continue
        for c, pv in zip(num, pdf_rows[r.district]):
            xv = round(r[c], 0 if "borrowers" in c else 1)
            if abs(xv - pv) > (0 if "borrowers" in c else 0.11):
                mism.append((r.district, c, xv, pv))
    val["v4_pdf_missing"], val["v4_pdf_mismatch"] = missing, mism
    return rows, special


def cl1_thresholds(val):
    pages = pdf_text(CL1_PDF)
    pat = re.compile(r"1\s+Punjab\s+Up to\s+([\d.]+)\s+(\d+)\s+(\d+)\s+([\d.]+)\s+to\s+([\d.]+)\s+(\d+)\s+(\d+)\s+Above\s+([\d.]+)\s+(\d+)\s+(\d+)")
    for n, s in pages.items():
        m = pat.search(re.sub(r"\s+", " ", s))
        if m:
            g = m.groups()
            src = re.search(r"Source:[^\n]*", s)
            val["cl1"] = dict(page=n, line=m.group(0), sub_max=float(g[0]), eco_min=float(g[3]), eco_max=float(g[4]),
                              abv_min=float(g[7]), farms_pct=(g[1], g[5], g[8]), area_pct=(g[2], g[6], g[9]),
                              source=src.group(0).strip() if src else "")
            return val["cl1"]
    sys.exit("CL1-Annex: Punjab holding thresholds not found. STOP: ask Ahmed (D021).")


# ------------------------------------------------------------------------------------------ Ag Census
def agc_block(path, cols):
    x = pd.read_excel(path, header=None)
    names = [up(v) for v in x[0]]
    i0 = names.index("PUNJAB")
    i1 = next(i for i in range(i0 + 1, len(names)) if names[i] in ("SINDH", "BALOCHISTAN") or names[i].startswith("ISLAMABAD"))
    out, unit = [], None
    for i in range(i0, i1):
        n = names[i]
        if n == "NAN":
            continue
        if n in ALLCLS or n == "PRIVATE-FARMS TOTAL":
            out.append(dict(unit=unit, size_class=n, **{k: float(x.iloc[i, c]) for k, c in cols.items()}))
        else:
            unit = n
    return pd.DataFrame(out)


def agc(val):
    t3 = agc_block(AGC_T3, {"farms": 1, "farm_area_ac": 3, "cultivated_ac": 5})
    t1 = agc_block(AGC_T1, {"farms_t1": 3, "owner": 5, "owner_cum_tenant": 7, "tenant": 9})
    a = t3.merge(t1, on=["unit", "size_class"], how="outer", validate="1:1")
    classes = sorted(set(a.size_class) - {"PRIVATE-FARMS TOTAL"}, key=ALLCLS.index)
    val["agc_classes"] = classes
    # A1 classes sum to total; A2 Table1 farms == Table3 farms; A3 tenure parts sum to farms
    tot = a[a.size_class == "PRIVATE-FARMS TOTAL"].set_index("unit")
    cs = a[a.size_class != "PRIVATE-FARMS TOTAL"].groupby("unit")[["farms", "farm_area_ac", "cultivated_ac", "tenant"]].sum()
    val["a1"] = [(u, c, cs.loc[u, c], tot.loc[u, c]) for u in cs.index for c in cs.columns if abs(cs.loc[u, c] - tot.loc[u, c]) > 0.5]
    val["a2"] = a.loc[(a.farms - a.farms_t1).abs() > 0.5, ["unit", "size_class", "farms", "farms_t1"]].values.tolist()
    val["a3"] = a.loc[(a.owner + a.owner_cum_tenant + a.tenant - a.farms_t1).abs() > 0.5, ["unit", "size_class"]].values.tolist()
    # A4 vs published report Tables 1.1 (p. with 'NUMBER AND AREA OF FARMS (ACRES)') and 1.3 (tenure)
    pages = pdf_text(AGC_PDF)
    p11 = next(s for s in pages.values() if "NUMBER AND AREA OF FARMS (ACRES)" in s and "TABLE 1.1" in s)
    p13 = next(s for s in pages.values() if "TENURE CLASSIFICATION OF FARMS AND FARM AREA" in s and "TABLE 1.3" in s)
    pub = {}
    for line in p11.splitlines():
        n, v = split_row(line)
        if len(v) == 7 and n:
            pub.setdefault(up(n), {}).update(farms=v[0], farm_area_ac=v[2], cultivated_ac=v[4])
    for line in p13.splitlines():
        n, v = split_row(line)
        if len(v) == 16 and n:
            pub.setdefault(up(n), {}).update(farms13=v[0], owner=v[2], owner_cum_tenant=v[4], tenant=v[6])
    a4, a4_missing = [], []
    for u, r in tot.iterrows():
        if u not in pub:
            a4_missing.append(u); continue
        for c in ["farms", "farm_area_ac", "cultivated_ac", "owner", "owner_cum_tenant", "tenant"]:
            if c in pub[u] and abs(round(r[c]) - pub[u][c]) > 1:
                a4.append((u, c, round(r[c]), pub[u][c]))
    val["a4"], val["a4_missing"], val["a4_n"] = a4, a4_missing, len(tot) - len(a4_missing)
    # A5 division = sum of its districts (+ Cholistan Area?)
    return a, tot


# ------------------------------------------------------------------------------------------ crosswalk
def crosswalk(source, names, adm2):
    """exact / normalized automatically; Ahmed's decisions (docs/crosswalk_manual_district.csv) set spelling etc."""
    res = pd.DataFrame(bj.match_units(sorted(set(names)), sorted(adm2.adm2_name)))
    res = res.rename(columns={"left": "source_name", "right": "ocha_name"})
    res["source"] = source
    res = res.merge(adm2[["adm2_name", "adm2_pcode"]], left_on="ocha_name", right_on="adm2_name", how="left") \
             .drop(columns="adm2_name").rename(columns={"adm2_pcode": "ocha_pcode"})
    res["decision"], res["decided_by"], res["date"] = np.where(res.match_type == "exact", "auto (exact)", ""), "", ""
    m = pd.read_csv(MANUAL, dtype=str).fillna("")
    for _, r in m[(m.source == source)].iterrows():
        sel = res.source_name == r.source_name
        if sel.sum() != 1:
            sys.exit(f"district decision does not match exactly one {source} name: {r.source_name}")
        if r.decision == "accept":
            res.loc[sel, ["match_type", "ocha_name", "ocha_pcode"]] = [r.match_type, r.ocha_name, r.ocha_pcode]
        res.loc[sel, ["decision", "decided_by", "date"]] = [r.decision, r.decided_by, r.date]
    res["validated"] = res.match_type.isin(common.VALID_MATCH_TYPES)
    dup = res[res.validated].ocha_pcode.duplicated()
    if dup.any():
        sys.exit(f"{source}: harmonized district identifier assigned twice: {res[res.validated][dup].to_dict('records')}")
    return res


# ------------------------------------------------------------------------------------------ analysis helpers
def flags(rows):
    f = rows.copy()
    for c in ["sub", "eco", "abv"]:
        f[f"avg_loan_{CATS[c]}_rs"] = np.where(f[f"{c}_borrowers"] > 0, f[f"{c}_amount_mn"] * 1e6 / f[f"{c}_borrowers"], np.nan)
    f["abv_amount_share"] = f.abv_amount_mn / f.tot_amount_mn
    pj = f[f.district != "Islamabad"]
    reasons = {d: [] for d in f.district}
    for c in ["sub", "eco", "abv"]:
        col = f"avg_loan_{CATS[c]}_rs"
        med = pj[col].median()
        f[f"{col}_x_median"] = f[col] / med
        for _, r in f.iterrows():
            if r[f"{c}_borrowers"] < 20:
                if r[f"{c}_borrowers"] > 0:
                    reasons[r.district].append(f"note: only {int(r[f'{c}_borrowers'])} {CATS[c]} borrowers (ratio not flagged)")
                continue
            x = r[f"{col}_x_median"]
            if x > 5 or x < 0.2:
                reasons[r.district].append(f"F1 {CATS[c]} avg loan Rs {r[col]:,.0f} = {x:.1f}x Punjab median (Rs {med:,.0f})")
    for _, r in f.iterrows():
        if r.abv_amount_share > 0.75:
            reasons[r.district].append(f"F2 above-economic = {r.abv_amount_share:.0%} of farm-sector disbursement")
    f["flag_reasons"] = f.district.map(lambda d: "; ".join(reasons[d]))
    f["flagged"] = f.district.map(lambda d: any(x.startswith("F") for x in reasons[d]))
    return f


def concentration(d):
    s = d.sort_values("small_farm_reach")
    x = np.r_[0, np.cumsum(s.small_farms) / s.small_farms.sum()]
    y = np.r_[0, np.cumsum(s.sub_borrowers) / s.sub_borrowers.sum()]
    area = np.trapezoid(y, x) if hasattr(np, "trapezoid") else np.trapz(y, x)
    return x, y, 1 - 2 * area, s


def moran(g, var):
    out = []
    g = g.to_crs(common.CRS)
    for nm, w in [("Queen", Queen.from_dataframe(g, use_index=False, silence_warnings=True)),
                  ("kNN-5 (geodesic)", common.geodesic_knn(g, k=K))]:
        isl = [g.adm2_name.iloc[i] for i in w.islands]
        w.transform = "r"
        np.random.seed(SEED)
        m = esda.Moran(g[var].values, w, permutations=PERM)
        out.append(dict(variable=var, weights=nm, n=w.n, islands="; ".join(isl) or "none", components=w.n_components,
                        I=m.I, EI=m.EI, z_perm=m.z_sim, p_perm=m.p_sim, permutations=PERM, seed=SEED))
    return pd.DataFrame(out)


CLASSES = {"availability": ("commercial_share", "High reported commercial-bank credit availability, low small-farm reach"),
           "presence": ("rural_branches_per_10k_farms", "High rural-branch presence, low small-farm reach"),
           "presence_all_branches_SENSITIVITY": ("all_branches_per_10k_farms_sensitivity",
                                                 "SENSITIVITY (all branches): high branch density, low small-farm reach")}


def exclusion(d, kind):
    """kind = availability (commercial_share, Mouza Census) or presence (branches per 10,000 farms): top half AND reach bottom third."""
    col, label = CLASSES[kind]
    b = d.dropna(subset=[col, "small_farm_reach"])
    cm, sr = b[col].median(), b.small_farm_reach.quantile(1 / 3)
    sel = b[(b[col] >= cm) & (b.small_farm_reach <= sr)]
    out = sel[["adm2_name", "commercial_share", "rural_branches_per_10k_farms", "all_branches_per_10k_farms_sensitivity",
               "small_farm_reach", "arhti_share"]].assign(
        classification=label, basis=kind)
    return out, cm, sr, len(b)


def analysis(d, label):
    """Everything in section 4, on district table d (one row per OCHA district with SBP + AgC matched)."""
    r = {"label": label, "n": len(d)}
    for v in ["arhti_share", "commercial_share"]:
        b = d.dropna(subset=[v, "small_farm_reach"])
        rho, p = spearmanr(b.small_farm_reach, b[v])
        r[f"rho_{v}"], r[f"p_{v}"], r[f"n_{v}"] = rho, p, len(b)
    r["moran"] = moran(d.dropna(subset=["small_farm_reach"]).reset_index(drop=True), "small_farm_reach")
    for kind in CLASSES:
        r[f"excl_{kind}"], r[f"excl_{kind}_cut"], r[f"excl_{kind}_sr"], r[f"excl_{kind}_n"] = exclusion(d, kind)
    r["cx"], r["cy"], r["cc"], r["corder"] = concentration(d)
    return r


# ------------------------------------------------------------------------------------------ figures
BLUE, INK, MUTED, GRID = "#2a78d6", "#1f1f1f", "#6b6b6b", "#e6e6e3"


def scatter(d, flagged, path):
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.6), sharey=True)
    for ax, v, lab in [(axes[0], "arhti_share", "AVAILABILITY: arhti_share (share of rural mouzas reporting arhti credit, Mouza Census 2020)"),
                       (axes[1], "commercial_share", "AVAILABILITY: commercial_share (reported commercial-bank credit, Mouza Census 2020)")]:
        b = d.dropna(subset=[v, "small_farm_reach"])
        fl = b.adm2_name.isin(flagged)
        ax.scatter(b[v][~fl], b.small_farm_reach[~fl], s=36, color=BLUE, edgecolor="white", linewidth=1, zorder=3)
        ax.scatter(b[v][fl], b.small_farm_reach[fl], s=40, facecolor="white", edgecolor=BLUE, linewidth=1.5, zorder=3)
        for _, r in b[fl].iterrows():
            ax.annotate(r.adm2_name, (r[v], r.small_farm_reach), xytext=(4, 3), textcoords="offset points", fontsize=7, color=MUTED)
        rho, p = spearmanr(b.small_farm_reach, b[v])
        ax.set_title(f"vs {v}: Spearman ρ = {rho:.2f} (n = {len(b)})", fontsize=9, color=INK, loc="left")
        ax.set_xlabel(lab, fontsize=8, color=MUTED)
        ax.grid(color=GRID, linewidth=0.6); ax.set_axisbelow(True)
        for s in ["top", "right"]:
            ax.spines[s].set_visible(False)
        ax.tick_params(labelsize=7, colors=MUTED)
    axes[0].set_ylabel("ALLOCATION: small_farm_reach\n(subsistence-holding borrower records per 1,000 farms < 12.5 acres)", fontsize=8, color=MUTED)
    fig.suptitle("Punjab districts: small-farm reach (allocation) vs reported credit availability",
                 fontsize=10, x=0.01, ha="left")
    fig.text(0.01, -0.06, f"Open circles = districts flagged in the SBP data-quality screen. Vintages differ and are not "
             f"contemporaneous: {V_SBP}; {V_AGC}; {V_MC}.\nBorrower counts may double-count farmers borrowing from several "
             f"banks (records may not be unique individuals). Descriptive association only.", fontsize=7, color=MUTED)
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def conc_fig(res_all, res_sens, path):
    fig, ax = plt.subplots(figsize=(5.6, 5.4))
    ax.plot([0, 1], [0, 1], color=MUTED, lw=1, ls="--", label="Equal share (45° line)")
    ax.plot(res_all["cx"], res_all["cy"], color=BLUE, lw=2, label=f"All matched districts (n = {res_all['n']}), CC = {res_all['cc']:.2f}")
    ax.plot(res_sens["cx"], res_sens["cy"], color="#eb6834", lw=2,
            label=f"Excluding flagged (n = {res_sens['n']}), CC = {res_sens['cc']:.2f}")
    ax.set_xlabel("Cumulative share of small farms (< 12.5 acres)\n(districts ordered by small_farm_reach, lowest first)", fontsize=8)
    ax.set_ylabel("Cumulative share of subsistence-holding borrowers", fontsize=8)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_aspect("equal")
    ax.grid(color=GRID, linewidth=0.6); ax.set_axisbelow(True)
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    ax.legend(fontsize=7, frameon=False, loc="upper left")
    ax.set_title("Concentration of subsistence-holding borrowers relative to small farms", fontsize=9, loc="left")
    fig.text(0.01, -0.05, f"CC = concentration coefficient (1 − 2 × area under curve); a descriptive summary of concentration.\n"
             f"{V_SBP}; {V_AGC}. Not contemporaneous.", fontsize=6.5, color=MUTED)
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)


# ------------------------------------------------------------------------------------------ main
def main() -> int:
    OUT_T.mkdir(parents=True, exist_ok=True); OUT_F.mkdir(parents=True, exist_ok=True)
    val = {}
    rows, special = sbp_punjab_farm(val)
    thr = cl1_thresholds(val)
    a, agc_tot = agc(val)
    ctx = gpd.read_file(CONTEXT, layer="district")
    adm2 = ctx[["adm2_name", "adm2_pcode", "geometry"]].copy()

    # SBP screen (all SBP rows incl. Islamabad, before matching)
    f = flags(rows)
    f["vintage"] = V_SBP
    f.to_csv(OUT_T / "sbp_punjab_farm_fy24_screen.csv", index=False)

    # Ag Census district measures (Cholistan Area excluded, D021)
    dist_units = [u for u in agc_tot.index if u.endswith(" DISTRICT")]
    small = a[a.size_class.isin(SMALL)].groupby("unit").farms.sum()
    large_area = a[a.size_class.isin(LARGE)].groupby("unit").farm_area_ac.sum()
    m = agc_tot.loc[dist_units, ["farms", "farm_area_ac", "cultivated_ac", "owner", "owner_cum_tenant", "tenant"]].copy()
    m["small_farms"] = small.reindex(m.index)
    m["large_farm_area_ac"] = large_area.reindex(m.index)
    m["tenant_share"] = m.tenant / m.farms
    m["owner_cum_tenant_share"] = m.owner_cum_tenant / m.farms
    m["owner_share"] = m.owner / m.farms
    m["large_farm_area_share"] = m.large_farm_area_ac / m.farm_area_ac
    m["small_farm_share_of_farms"] = m.small_farms / m.farms
    m = m.reset_index().rename(columns={"unit": "agc_district"})
    chol = agc_tot.loc["CHOLISTAN AREA"] if "CHOLISTAN AREA" in agc_tot.index else None

    # Crosswalks
    br = pd.read_excel(BRANCH_XLSX, sheet_name="Banks", header=1, dtype=str)
    br.columns = [c.strip() for c in br.columns]
    br = br[br.Province.str.strip() == "Punjab"].copy()
    br["district"] = br.District.str.strip()
    xw = pd.concat([crosswalk("SBP", [d for d in rows.district if d != "Islamabad"], adm2),
                    crosswalk("AgCensus", m.agc_district, adm2),
                    crosswalk("BranchList", br.district, adm2)], ignore_index=True)
    xw.to_csv(ROOT / "data" / "interim" / "district_crosswalk_sbp_agc_branches.csv", index=False)
    ok = xw[xw.validated]
    sbp_map = dict(zip(ok[ok.source == "SBP"].source_name, ok[ok.source == "SBP"].ocha_pcode))
    agc_map = dict(zip(ok[ok.source == "AgCensus"].source_name, ok[ok.source == "AgCensus"].ocha_pcode))
    br_map = dict(zip(ok[ok.source == "BranchList"].source_name, ok[ok.source == "BranchList"].ocha_pcode))

    s = f[f.district != "Islamabad"].assign(adm2_pcode=lambda x: x.district.map(sbp_map)).dropna(subset=["adm2_pcode"])
    m["adm2_pcode"] = m.agc_district.map(agc_map)
    br["adm2_pcode"] = br.district.map(br_map)
    bc = br.dropna(subset=["adm2_pcode"]).groupby("adm2_pcode").agg(
        branches_scheduled=("Bank", "size"),
        branches_rural=("Area(Rural/Urban)", lambda x: int((x.str.strip() == "R").sum())),
        branches_ztbl=("Bank", lambda x: int(x.str.contains("ZTBL").sum())))

    d = adm2.merge(ctx[["adm2_pcode", "arhti_share", "commercial_share", "rp_mouzas"]], on="adm2_pcode", how="left")
    d = d.merge(s[["adm2_pcode", "district", "sub_borrowers", "sub_amount_mn", "eco_borrowers", "abv_borrowers",
                   "tot_borrowers", "avg_loan_subsistence_rs", "avg_loan_economic_rs", "avg_loan_above_economic_rs",
                   "abv_amount_share", "flagged", "flag_reasons"]].rename(columns={"district": "sbp_district"}),
                on="adm2_pcode", how="left")
    d = d.merge(m.dropna(subset=["adm2_pcode"]), on="adm2_pcode", how="left").merge(bc, on="adm2_pcode", how="left")
    d["small_farm_reach"] = d.sub_borrowers / d.small_farms * 1000
    # PRESENCE (D034): rural branches ("R" in the SBP list) per 10,000 farms; all-branch density only as a SENSITIVITY column
    d["rural_branches_per_10k_farms"] = d.branches_rural / d.farms * 10000
    d["all_branches_per_10k_farms_sensitivity"] = d.branches_scheduled / d.farms * 10000
    assert not d.adm2_pcode.duplicated().any(), "duplicated harmonized district identifier"
    # nullable 0/1 integer so the GeoPackage stores a number, not text; null = SBP row not matched (unknown)
    d["flagged"] = d.flagged.map({True: 1, False: 0}).astype("Int64")
    d["vintage"] = f"{V_SBP}; {V_AGC}; {V_MC}; branches: {V_BR}. Not contemporaneous."
    an = d.dropna(subset=["small_farm_reach"]).reset_index(drop=True)
    flagged_names = list(an[an.flagged == 1].adm2_name)
    sens = an[an.flagged != 1].reset_index(drop=True)

    R = analysis(an, "all matched districts")
    S = analysis(sens, "excluding flagged districts")

    OUT_GPKG.unlink(missing_ok=True)
    d.to_file(OUT_GPKG, layer="district", driver="GPKG")
    d.drop(columns="geometry").to_csv(OUT_T / "district_credit_allocation.csv", index=False)
    pd.concat([R["moran"].assign(sample=R["label"]), S["moran"].assign(sample=S["label"])]).assign(
        vintage=f"{V_SBP}; {V_AGC}").to_csv(OUT_T / "moran_small_farm_reach.csv", index=False)
    pd.concat([X[f"excl_{k}"].assign(sample=X["label"], cut_top_half=X[f"excl_{k}_cut"], cut_reach_p33=X[f"excl_{k}_sr"],
                                      n_classified=X[f"excl_{k}_n"]) for X in (R, S) for k in CLASSES]).assign(
        vintage=f"{V_SBP}; {V_AGC}; {V_MC}; branches: {V_BR}").to_csv(OUT_T / "two_kinds_of_exclusion.csv", index=False)
    tenure = q2_tenure(an, sens)
    tenure.to_csv(OUT_T / "q2_tenure_associations.csv", index=False)
    assoc = exploratory_associations(d)
    assoc.to_csv(OUT_T / "exploratory_associations.csv", index=False)
    q2_cholistan(d, R)
    pd.concat([X["corder"][["adm2_name", "small_farm_reach", "small_farms", "sub_borrowers"]].assign(
        sample=X["label"], cum_small_farms=X["cx"][1:], cum_sub_borrowers=X["cy"][1:]) for X in (R, S)]).assign(
        vintage=f"{V_SBP}; {V_AGC}").to_csv(OUT_T / "concentration_curve.csv", index=False)
    pd.DataFrame([dict(sample=X["label"], n=X["n"], concentration_coefficient=X["cc"]) for X in (R, S)]).assign(
        definition="1 - 2 x area under the curve; districts ordered by small_farm_reach; describes concentration, not fairness",
        vintage=f"{V_SBP}; {V_AGC}").to_csv(OUT_T / "concentration_coefficients.csv", index=False)
    scatter(an, flagged_names, OUT_F / "small_farm_reach_vs_mouza_credit.png")
    (OUT_F / "concentration_curve_small_farms.png").unlink(missing_ok=True)   # superseded by Figure S6 (09_figures.py)

    ap, tt = special.loc["All Punjab"], special.loc["Total"]
    pd.DataFrame([
        dict(scope="All Punjab (banks + MFIs)", abv_borrowers=ap.abv_borrowers, tot_borrowers=ap.tot_borrowers,
             abv_amount_mn=ap.abv_amount_mn, tot_amount_mn=ap.tot_amount_mn),
        dict(scope="District rows only (banks; incl. Islamabad)", abv_borrowers=tt.abv_borrowers, tot_borrowers=tt.tot_borrowers,
             abv_amount_mn=tt.abv_amount_mn, tot_amount_mn=tt.tot_amount_mn)]).assign(
        abv_borrower_share=lambda x: x.abv_borrowers / x.tot_borrowers, abv_amount_share=lambda x: x.abv_amount_mn / x.tot_amount_mn,
        vintage=V_SBP).to_csv(OUT_T / "sbp_province_headline.csv", index=False)
    write_validation(val, f, special, thr, chol, agc_tot, xw)
    write_summary(R, S, d, an, f, special, thr, chol, agc_tot, xw, flagged_names, bc, br, tenure, assoc)
    print(SUM_MD.read_text()[:3000])
    return 0


# ------------------------------------------------------------------------------------------ associations
def spearman_family(df, y, xs, family):
    rows = []
    for x in xs:
        b = df[[y, x]].dropna()
        rho, p = spearmanr(b[y], b[x]) if len(b) > 3 else (np.nan, np.nan)
        rows.append(dict(family=family, y=y, x=x, n=len(b), rho=rho, p_raw=p))
    out = pd.DataFrame(rows)
    ok = out.p_raw.notna()
    out.loc[ok, "p_bh"] = multipletests(out.loc[ok, "p_raw"], method="fdr_bh")[1]
    return out


def q2_tenure(an, sens):
    xs = ["tenant_share", "owner_cum_tenant_share", "large_farm_area_share"]
    t = pd.concat([spearman_family(an, "small_farm_reach", xs, f"all districts (n = {len(an)})"),
                   spearman_family(sens, "small_farm_reach", xs, f"excluding flagged districts (n = {len(sens)})")])
    return t.assign(note="Q2; Spearman; BH-adjusted within each family; descriptive",
                    vintage=f"{V_SBP}; {V_AGC}")


ASSOC_X = ["onlinebank_in_mouza_share", "onlinebank_over25km_share", "rural_branches_per_10k_farms", "commercial_share", "ztbl_share",
           "mkt_grain_in_mouza_share", "mkt_grain_51plus_share", "cropland_share", "tt_city_cropw_hours", "road_metalled_share"]


def exploratory_associations(d):
    """POST-HOC (D030): Spearman of arhti_share with a fixed list, at tehsil (Q1 unit) and district, scenarios A and B."""
    out = []
    br10k = dict(zip(d.adm2_pcode, d.rural_branches_per_10k_farms))
    for level, lay in [("tehsil", {"A": "tehsil", "B": "tehsil_optB"}), ("district", {"A": "district", "B": "district_optB"})]:
        for scen, layer in lay.items():
            g = gpd.read_file(CONTEXT, layer=layer)
            g = g[g.arhti_share.notna()].copy()
            g["tt_city_cropw_hours"] = g.tt_city_cropw_mean_min / 60
            g["rural_branches_per_10k_farms"] = g.adm2_pcode.map(br10k) if level == "district" else np.nan
            xs = ASSOC_X if level == "district" else [x for x in ASSOC_X if x != "rural_branches_per_10k_farms"]
            r = spearman_family(g, "arhti_share", xs, f"{level}, scenario {scen}")
            out.append(r.assign(level=level, scenario=scen))
    a = pd.concat(out)
    return a.assign(label="POST-HOC EXPLORATORY; BH-adjusted within each level x scenario family",
                    note=np.where(a.x == "rural_branches_per_10k_farms", "PRESENCE (rural branches); district only (farms are not available by tehsil)", ""),
                    vintage=f"{V_MC}; WorldCover 2021; MAP 2015; branches: {V_BR}; Ag Census 2024 farms")


def q2_cholistan(d, R):
    """D015: does the availability classification change when Cholistan is excluded (option B commercial_share)?"""
    b = gpd.read_file(CONTEXT, layer="district_optB")[["adm2_pcode", "commercial_share", "arhti_share"]]
    dB = d.drop(columns=["commercial_share", "arhti_share"]).merge(b, on="adm2_pcode", how="left")
    eA, _, _, _ = exclusion(d.dropna(subset=["small_farm_reach"]), "availability")
    eB, _, _, _ = exclusion(dB.dropna(subset=["small_farm_reach"]), "availability")
    rows = [dict(level="district", unit=u, pcode="", item="Q2 availability classification (high commercial_share, low reach)",
                 option_A=u in set(eA.adm2_name), option_B=u in set(eB.adm2_name)) for u in sorted(set(eA.adm2_name) ^ set(eB.adm2_name))]
    f = OUT_T / "cholistan_sensitivity.csv"
    old = pd.read_csv(f) if f.exists() else pd.DataFrame()
    if len(old):
        old = old[~old["item"].astype(str).str.startswith("Q2 ")]
    new = pd.DataFrame(rows, columns=["level", "unit", "pcode", "item", "option_A", "option_B"])
    pd.concat([old, new.assign(vintage=f"{V_MC}; {V_SBP}; {V_AGC}")]).to_csv(f, index=False)
    print(f"Q2 Cholistan sensitivity: availability-classification changes = {len(rows)}; A = {sorted(eA.adm2_name)}, B = {sorted(eB.adm2_name)}")


# ------------------------------------------------------------------------------------------ reports
def write_validation(val, f, special, thr, chol, agc_tot, xw):
    L = [f"# Validation: SBP FY2023-24 and Agricultural Census 2024 extraction ({dt.date.today()})", "",
         f"Written by `scripts/08_credit_allocation.py`. {V_SBP}. {V_AGC}.", "",
         "## SBP: published figures", "", "| Check | Extracted | Published | Result |", "|---|---|---|---|"]
    L += [f"| {n} | {x:,.1f} | {e:,.1f} | {'PASS' if abs(x - e) < 0.05 else '**FAIL**'} |" for n, x, e in val["v1"]]
    tot, mfi = special.loc["Total"], special.loc["MFIs"]
    L += ["", f"The published All-Punjab row = sum of the 37 district rows ('Total': {tot.tot_borrowers:,.0f} borrowers, "
          f"Rs {tot.tot_amount_mn:,.1f} mn) + 'MFIs' ({mfi.tot_borrowers:,.0f} borrowers, Rs {mfi.tot_amount_mn:,.1f} mn, "
          "all in the subsistence columns, Punjab-wide only). **The MFI figures are not distributed to districts and are excluded from all "
          "district measures.** The 37 district rows include **Islamabad**, which is dropped from the analysis.", "",
          "## SBP: internal consistency", "",
          f"- District rows sum to 'Total': {'PASS' if not val['v2_rows_vs_total'] else val['v2_rows_vs_total']}",
          f"- 'Total' + 'MFIs' = 'All Punjab': {'PASS' if not val['v2_total_mfi_vs_all'] else val['v2_total_mfi_vs_all']}",
          f"- Total columns = subsistence + economic + above-economic, every row and field: "
          f"{'PASS' if not val['v3_category_sums'] else val['v3_category_sums']}. (The printed header '18=3+7+13' is a "
          "typo for 3+8+13; the data follow 3+8+13.)",
          f"- xlsx vs DWS PDF p. 1, every row × 20 columns (amounts at 0.1 mn): rows not found in PDF text: "
          f"{val['v4_pdf_missing'] or 'none'}; mismatches: {len(val['v4_pdf_mismatch'])}"]
    L += [f"  - {r}" for r in val["v4_pdf_mismatch"]]
    c = thr
    L += ["", "## SBP holding thresholds (CL1-Annex, *Indicative Credit Limits and Eligible Items for Agriculture "
          f"Financing 2022-23*, Table 2.7, PDF p. {c['page']})", "",
          f"Extracted line: `{c['line']}`", "",
          "| Category (Punjab) | Acres | % of farms | % of area |", "|---|---|---|---|",
          f"| Subsistence holding | up to {c['sub_max']} | {c['farms_pct'][0]} | {c['area_pct'][0]} |",
          f"| Economic holding | {c['eco_min']} to {c['eco_max']} | {c['farms_pct'][1]} | {c['area_pct'][1]} |",
          f"| Above economic holding | above {c['abv_min']} | {c['farms_pct'][2]} | {c['area_pct'][2]} |", "",
          f"{c['source']} The thresholds are from the **2010** census, and the table gives no irrigated/unirrigated split for Punjab. "
          "Whether borrowers are classified by land owned or land operated is not stated in Table 2.7 [CHECK].", "",
          "## Agricultural Census 2024: extraction checks", "",
          f"- Size classes used by PBS: {', '.join(val['agc_classes'])} (acres).",
          f"- Size classes sum to 'PRIVATE-FARMS TOTAL' (farms, farm area, cultivated area, tenant farms), all units: "
          f"{'PASS' if not val['a1'] else val['a1'][:10]}",
          f"- Table_1 farms = Table_3 farms, every unit × class: {'PASS' if not val['a2'] else val['a2'][:10]}",
          f"- Owner + owner-cum-tenant + tenant = farms, every unit × class: {'PASS' if not val['a3'] else val['a3'][:10]}",
          f"- District/division/province totals vs report Table 1.1 (farms, farm area, cultivated area) and Table 1.3 (tenure): "
          f"{val['a4_n']} units compared, {len(val['a4'])} mismatches (±1); units not found in report text: {val['a4_missing'] or 'none'}"]
    L += [f"  - {r}" for r in val["a4"]]
    if chol is not None:
        p = agc_tot.loc["PUNJAB"]
        L += ["", f"**Cholistan Area** (separate Ag Census unit, no SBP/OCHA counterpart): {chol.farms:,.0f} farms "
              f"({chol.farms / p.farms:.1%} of Punjab), {chol.farm_area_ac:,.0f} acres ({chol.farm_area_ac / p.farm_area_ac:.1%}). "
              "Excluded from district denominators pending D015/D021."]
    L += ["", "## Size-class alignment (SBP vs Ag Census): reported, not forced", "",
          "| SBP category | SBP acres | Closest Ag Census classes | Boundary difference |", "|---|---|---|---|",
          f"| Subsistence | up to {c['sub_max']} | Under 1.0 … 7.5–<12.5 | SBP includes exactly 12.5 acres; the census puts 12.5 in 12.5–<25 |",
          f"| Economic | {c['eco_min']}–{c['eco_max']} | 12.5–<25, 25–<50 | SBP includes exactly 50 (and its lower bound overlaps 'up to 12.5'); the census puts 50 in 50–<100 |",
          f"| Above economic | above {c['abv_min']} | 50–<100, 100+ | farms of exactly 50 acres are 'economic' for SBP, 'large' in the census |", "",
          "The cut points coincide (12.5 and 50 acres). The differences are at the two boundary points, and in the concept: the census measures "
          "**operated farm area** of a household's farm in 2023-24; SBP classifies **borrowers** (basis not stated). Farms reported at exactly "
          "12.5 or 50 acres cannot be identified in the published classes, so their size is unknown.", ""]
    L += ["## SBP data-quality screen (D021: F1 loan size >5× or <0.2× Punjab median; F2 above-economic >75% of disbursement)", ""]
    meds = {c2: f[f.district != "Islamabad"][f"avg_loan_{CATS[c2]}_rs"].median() for c2 in ["sub", "eco", "abv"]}
    L += [f"Punjab district medians (excl. Islamabad), Rs per disbursed borrower: subsistence {meds['sub']:,.0f}; "
          f"economic {meds['eco']:,.0f}; above-economic {meds['abv']:,.0f}.", "",
          "| District (SBP name) | Subsistence avg (× median) | Economic avg (×) | Above-econ avg (×) | Above-econ share of amount | Flag reasons |",
          "|---|---|---|---|---|---|"]
    for _, r in f[(f.flag_reasons != "")].sort_values("abv_amount_share", ascending=False).iterrows():
        L.append(f"| {r.district} | {r.avg_loan_subsistence_rs:,.0f} ({r.avg_loan_subsistence_rs_x_median:.1f}) | "
                 f"{r.avg_loan_economic_rs:,.0f} ({r.avg_loan_economic_rs_x_median:.1f}) | "
                 f"{r.avg_loan_above_economic_rs:,.0f} ({r.avg_loan_above_economic_rs_x_median:.1f}) | {r.abv_amount_share:.0%} | {r.flag_reasons} |")
    sus = ["Rawalpindi", "Islamabad", "Lahore", "Rahimyar Khan", "Multan", "Jehlum"]
    L += ["", "### Suspects named in the brief, and near misses (reported; thresholds NOT changed after seeing the data)", "",
          "| District | Flagged | Subsistence × median | Economic × median | Above-econ × median | Above-econ share | Borrowers sub / eco / abv |",
          "|---|---|---|---|---|---|---|"]
    near = f[(f.abv_amount_share.between(0.65, 0.75)) | (f[[f"avg_loan_{CATS[c2]}_rs_x_median" for c2 in ["sub", "eco", "abv"]]]
                                                          .apply(lambda r: ((r > 4) & (r <= 5)).any(), axis=1))]
    for _, r in f[f.district.isin(sus) | f.district.isin(near.district)].iterrows():
        tag = "suspect" if r.district in sus else ("flagged" if r.flagged else "near miss")
        L.append(f"| {r.district} ({tag}) | {r.flagged} | {r.avg_loan_subsistence_rs_x_median:.1f} | {r.avg_loan_economic_rs_x_median:.1f} | "
                 f"{r.avg_loan_above_economic_rs_x_median:.1f} | {r.abv_amount_share:.0%} | {r.sub_borrowers:,.0f} / {r.eco_borrowers:,.0f} / {r.abv_borrowers:,.0f} |")
    L += ["", "Near miss = above-economic share 65–75% or a loan-size ratio of 4–5×. Chakwal's F1 flag is on the LOW side: 1,158 "
          "'economic' borrowers averaging about a subsistence-sized loan. This could be holding-category misclassification, which would also "
          "understate its subsistence borrowers (interpretation; [CHECK]).",
          "", "### Booking location",
          "SBP records each loan where it is **booked**, i.e. the lending branch or office's district, not where the borrower's land is. "
          "Large farm-sector loans, especially above-economic holdings and corporate farming, are often booked at urban or head-office branches. "
          "Lahore, Rawalpindi/Islamabad, Multan and other divisional headquarters therefore record amounts (and some borrowers) whose land "
          "may lie elsewhere. Rural districts' figures understate lending to their land by the same amount. This is why amount shares are never mapped "
          "(rule 11), and why borrower counts, which are less affected but not immune, are used for `small_farm_reach`.", "",
          "## District crosswalks (SBP / Ag Census / branch list → OCHA ADM2)", "",
          "| Source | Source name | OCHA | Match type | Score | Validated |", "|---|---|---|---|---|---|"]
    for _, r in xw[xw.match_type != "exact"].sort_values(["validated", "source"]).iterrows():
        L.append(f"| {r.source} | {r.source_name} | {r.ocha_name if pd.notna(r.ocha_name) else ''} | {r.match_type} | "
                 f"{r.score:.0f} | {r.validated} |")
    L += ["", f"Exact matches not listed. Decisions (decided by Ahmed) are in `{MANUAL.relative_to(ROOT)}`."]
    VAL_MD.write_text("\n".join(L) + "\n")


def write_summary(R, S, d, an, f, special, thr, chol, agc_tot, xw, flagged_names, bc, br, tenure, assoc):
    ap = special.loc["All Punjab"]; tot = special.loc["Total"]
    fmt = lambda df: df.to_markdown(index=False, floatfmt=".3f")
    L = [f"# Credit allocation by holding size: district summary (DESCRIPTIVE, {dt.date.today()})", "",
         f"Data: {V_SBP}; {V_AGC}; {V_MC}; branches: {V_BR}. Vintages differ and are not contemporaneous. Unit: OCHA ADM2 district "
         f"(Q2 keeps all districts, including Lahore, which has no rural populated mouzas, D028). CRS: {common.CRS_LABEL}.", "",
         "**Concepts (D029, D034).** PRESENCE = physical facilities (RURAL branches per 10,000 farms; online bank in/near mouza; all-branch density only as a sensitivity). AVAILABILITY = "
         "credit sources reported in the Mouza Census (commercial_share, arhti_share, ...). ALLOCATION = who formal credit reaches: "
         f"small_farm_reach = {common.SFR_DEF}.", "",
         "## Province-level headline (single statistic; not mapped)", "",
         f"Above-economic holdings: {ap.abv_borrowers / ap.tot_borrowers:.1%} of farm-sector disbursed borrower records and "
         f"{ap.abv_amount_mn / ap.tot_amount_mn:.1%} of farm-sector disbursement (All-Punjab row including MFIs; "
         f"{ap.abv_borrowers:,.0f} of {ap.tot_borrowers:,.0f}; Rs {ap.abv_amount_mn:,.1f} of {ap.tot_amount_mn:,.1f} mn). "
         f"Bank district rows only (excl. MFIs, incl. Islamabad): {tot.abv_borrowers / tot.tot_borrowers:.1%} and "
         f"{tot.abv_amount_mn / tot.tot_amount_mn:.1%}. {V_SBP}.", "",
         f"## Coverage", "", f"Districts with small_farm_reach: {len(an)} of 36 (all name matches decided by Ahmed, D022/D024).", "",
         "## Distributions", "",
         an[["small_farm_reach", "rural_branches_per_10k_farms", "all_branches_per_10k_farms_sensitivity", "tenant_share", "owner_cum_tenant_share", "large_farm_area_share",
             "small_farm_share_of_farms"]].describe().T[["count", "min", "25%", "50%", "75%", "max"]].to_markdown(floatfmt=".3f"), "",
         "*large_farm_area_share = concentration of OPERATED area in farms ≥ 50 acres (not landownership).*", ""]
    for X in (R, S):
        L += [f"## Results: {X['label']} (n = {X['n']})", "",
              f"- Spearman ρ, small_farm_reach vs arhti_share = {X['rho_arhti_share']:.2f} (p = {X['p_arhti_share']:.2f}, n = {X['n_arhti_share']}); "
              f"vs commercial_share = {X['rho_commercial_share']:.2f} (p = {X['p_commercial_share']:.2f}, n = {X['n_commercial_share']}).", "",
              "Global Moran's I, small_farm_reach (Queen and geodesic kNN-5, row-standardised; 999 permutations, seed 20261031). Small sample:", "",
              X["moran"][["weights", "n", "islands", "components", "I", "EI", "z_perm", "p_perm"]].to_markdown(index=False, floatfmt=".3f"), ""]
        for kind, (col, label) in CLASSES.items():
            e = X[f"excl_{kind}"]
            L += [f"**{label}** ({col} ≥ median {X[f'excl_{kind}_cut']:.3f} AND small_farm_reach ≤ 33rd percentile "
                  f"{X[f'excl_{kind}_sr']:.1f}; n classified = {X[f'excl_{kind}_n']}): "
                  + (", ".join(e.adm2_name) or "none") + ". Consistent with barriers beyond physical distance; it does not identify them.", ""]
        a_, p_ = set(X["excl_availability"].adm2_name), set(X["excl_presence"].adm2_name)
        old_ = set(X["excl_presence_all_branches_SENSITIVITY"].adm2_name)
        L += [f"Same districts under both classifications: {', '.join(sorted(a_ & p_)) or 'none'}; availability only: "
              f"{', '.join(sorted(a_ - p_)) or 'none'}; presence only: {', '.join(sorted(p_ - a_)) or 'none'}. "
              f"Rural-branch vs all-branch (sensitivity) presence classification: both {', '.join(sorted(p_ & old_)) or 'none'}; "
              f"rural only {', '.join(sorted(p_ - old_)) or 'none'}; all-branch only {', '.join(sorted(old_ - p_)) or 'none'}.", "",
              f"Concentration coefficient (districts ordered by small_farm_reach) = {X['cc']:.3f}. "
              f"Lowest-reach districts: {', '.join(X['corder'].adm2_name.head(5))}. Highest: {', '.join(X['corder'].adm2_name.tail(5)[::-1])}.", ""]
    L += ["## Q2 tenure associations (Spearman; BH-adjusted within each family)", "",
          fmt(tenure[["family", "x", "n", "rho", "p_raw", "p_bh"]]), "",
          "## POST-HOC exploratory associations with arhti_share (BH-adjusted within each level × scenario)", "",
          fmt(assoc[["level", "scenario", "x", "n", "rho", "p_raw", "p_bh", "note"]]), "",
          f"## Flagged districts (excluded in the sensitivity run): {', '.join(flagged_names) or 'none'}", "",
          "See `docs/validation_sbp.md` for reasons.", "",
          f"## PRESENCE: scheduled-bank branches ({V_BR}; rural = coded 'R' in the list)", "",
          f"Punjab rows in the list: {len(br):,} branches (sheet 'Banks', i.e. scheduled banks; microfinance banks and DFIs are on a "
          "separate sheet and not counted). One row coded Lahore has a Lower Dir (KP) address (decisions.md O4); it is counted as listed. "
          "No second source for this date was checked, so no cross-source total comparison is made.", ""]
    SUM_MD.write_text("\n".join(L) + "\n")


if __name__ == "__main__":
    sys.exit(main())
