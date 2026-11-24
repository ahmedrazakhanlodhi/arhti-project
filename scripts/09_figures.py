"""09_figures.py: publication figures 1-6 (+ S1 classification comparison, S2 district LISA), PNG 300 dpi + PDF.

    .venv/bin/python -I scripts/09_figures.py      (after 08_credit_allocation.py)

CRS: common.CRS (Albers equal-area centred on Punjab, D025); grid north = true north within 0.1 deg, so north arrows point
straight up. Every map has a north arrow, a 100 km scale bar, a source/vintage footer and explicit symbols for missing or
excluded units. Concepts are kept apart (D029): PRESENCE, AVAILABILITY, ALLOCATION. Every number drawn on a figure is
written, with source and vintage, to docs/figure_numbers.md.

Classification rule (common.choose_scheme, D023): 5-class Fisher-Jenks unless a class holds < 3 units, else quantiles.
"""

from __future__ import annotations

import datetime as dt
import importlib.util
import sys
import warnings
from pathlib import Path

import geopandas as gpd
import mapclassify
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.patches import Patch, Rectangle

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[1]
_cs = importlib.util.spec_from_file_location("common", ROOT / "scripts" / "common.py")
common = importlib.util.module_from_spec(_cs); _cs.loader.exec_module(common)

P, T, F = ROOT / "data" / "processed", ROOT / "outputs" / "tables", ROOT / "outputs" / "figures"
CRS = common.CRS
AUTHOR = "Ahmed Raza Khan Lodhi and Hasnain Akram, PPHA 38520, University of Chicago"
V_MC = "Mouza Census 2020 (PBS), fieldwork Jan–Mar 2020"
V_SBP = "SBP, FY2023-24 (Jul 2023–Jun 2024), recorded by loan-booking district"
V_AGC = "Agricultural Census 2024 (PBS), sample-based, fieldwork 2024–25"
V_BR = "SBP list of scheduled bank branches as on 30 June 2024"
V_B = "Boundaries: OCHA COD-AB Pakistan, valid_on 2022-09-09"
DESERT_NOTE = ("Fort Abbas, Yazman and Liaqatpur combine desert (Cholistan) and irrigated mouzas (Cholistan merged into parent "
               "tehsils, option A; option B in cholistan_sensitivity.csv).")
PERMS = "999 permutations, seed 20261031"

BLUE5 = ["#86b6ef", "#5598e7", "#2a78d6", "#1c5cab", "#0d366b"]
ORANGE5 = ["#f29a72", "#eb6834", "#c9531f", "#9a3d14", "#6b280b"]
CAT = {"blue": "#2a78d6", "orange": "#eb6834", "aqua": "#1baf7a"}
NEUTRAL, MISSING, EDGE, INK, MUTED, GRID = "#f0efec", "#e2e1dc", "#ffffff", "#1f1f1f", "#5c5b57", "#e6e6e3"
LISA_C = {"High-High": "#e34948", "High-Low": "#f2a7a6", "Low-Low": "#2a78d6", "Low-High": "#9ec5f4", "not significant": NEUTRAL}
BIV = [["#e8e8e8", "#ace4e4", "#5ac8c8"], ["#dfb0d6", "#a5add3", "#5698b9"], ["#be64ac", "#8c62aa", "#3b4994"]]
NUMS, CLS_ROWS = [], []
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8, "axes.titlesize": 9, "pdf.fonttype": 42})


def num(fig, item, value, source):
    NUMS.append(dict(figure=fig, item=item, value=value, source=source))


# ------------------------------------------------------------------------------------------ furniture
def frame(ax, g, pad=(0.18, 0.04, 0.08, 0.03)):
    x0, y0, x1, y1 = g.total_bounds
    w, h = x1 - x0, y1 - y0
    ax.set_xlim(x0 - pad[0] * w, x1 + pad[1] * w); ax.set_ylim(y0 - pad[2] * h, y1 + pad[3] * h)
    ax.set_axis_off(); ax.set_aspect("equal")


def furniture(ax, g, scale_km=100):
    x0, y0, x1, y1 = g.total_bounds
    w, h = x1 - x0, y1 - y0
    sx, sy = x0 - 0.16 * w, y0 - 0.05 * h
    seg = scale_km * 1000 / 2
    for i, col in enumerate([INK, "white"]):
        ax.add_patch(Rectangle((sx + i * seg, sy), seg, 0.008 * h, facecolor=col, edgecolor=INK, lw=0.6, zorder=6))
    for i, lab in enumerate(["0", f"{scale_km // 2}", f"{scale_km} km"]):
        ax.text(sx + i * seg, sy + 0.016 * h, lab, ha="center", va="bottom", fontsize=6.5, color=INK, zorder=6)
    ax0, ay0 = x0 - 0.12 * w, y0 + 0.05 * h
    ax.annotate("", xy=(ax0, ay0 + 0.07 * h), xytext=(ax0, ay0),
                arrowprops=dict(arrowstyle="-|>,head_width=0.35,head_length=0.7", color=INK, lw=1.3), zorder=6)
    ax.text(ax0, ay0 + 0.09 * h, "N", ha="center", va="center", fontsize=9, fontweight="bold", color=INK)


def footer(fig, lines, y=0.0):
    txt = "\n".join(lines + [f"CRS: {common.CRS_LABEL}; north arrow = true north.",
                             f"{AUTHOR}. Generated {dt.date.today()} by scripts/09_figures.py."])
    fig.text(0.01, y, txt, fontsize=6.2, color=MUTED, va="bottom", ha="left")


def save(fig, name):
    for ext, kw in [("png", dict(dpi=300)), ("pdf", {})]:
        fig.savefig(F / f"{name}.{ext}", bbox_inches="tight", facecolor="white", **kw)
    plt.close(fig)


def note(label):
    return Line2D([], [], ls="", marker="", label=label)


def legend(ax, handles, title, loc="upper left", anchor=(0.0, 0.0), ncol=1):
    return ax.legend(handles=handles, title=title, loc=loc, bbox_to_anchor=anchor, fontsize=6.8, title_fontsize=7.2,
                     frameon=False, ncol=ncol, alignment="left", handlelength=1.6, handleheight=1.1)


def hatch_patch(label):
    return Patch(facecolor=MISSING, edgecolor="#8a8984", hatch="////", lw=0.4, label=label)


def plot_missing(ax, g):
    if len(g):
        g.plot(ax=ax, facecolor=MISSING, edgecolor="#8a8984", hatch="////", linewidth=0.3, zorder=2)


def desert_outline(ax, teh):
    d = teh[teh.contains_cholistan == True]  # noqa: E712
    d.plot(ax=ax, facecolor="none", edgecolor=INK, linewidth=0.9, linestyle="--", zorder=4)
    return Line2D([], [], color=INK, lw=0.9, ls="--", label=f"Includes Cholistan desert mouzas (n = {len(d)})")


def classify(values, name, fig):
    pick, q, j = common.choose_scheme(values)
    why = ("natural breaks (every Fisher-Jenks class holds >= 3 units; higher GADF)" if pick is j
           else f"quantiles (a Fisher-Jenks class holds only {int(min(j.counts))} unit(s))")
    for nm, c in [("quantiles", q), ("Fisher-Jenks", j)]:
        CLS_ROWS.append(dict(figure=fig, variable=name, scheme=nm, n=len(pd.Series(values).dropna()), gadf=round(c.get_gadf(), 3),
                             bins=";".join(f"{b:.3f}" for b in c.bins),
                             bins_exact=";".join(repr(float(b)) for b in c.bins), counts=";".join(map(str, c.counts)), chosen=(c is pick),
                             reason=why if c is pick else ""))
    return pick, why, pick is j


def class_labels(c, fmt, vmin):
    lo = [vmin] + list(c.bins[:-1])
    return [f"{fmt.format(a)} – {fmt.format(b)}  (n = {n})" for a, b, n in zip(lo, c.bins, c.counts)]


def choropleth(ax, g, col, c, ramp):
    ok = g[g[col].notna()].copy()
    ok["_k"] = c.find_bin(ok[col].values)
    for k, colr in enumerate(ramp):
        ok[ok._k == k].plot(ax=ax, color=colr, edgecolor=EDGE, linewidth=0.3, zorder=1)


# ------------------------------------------------------------------------------------------ data
def load():
    teh = gpd.read_file(P / "punjab_credit_context.gpkg", layer="tehsil").to_crs(CRS)
    dist = gpd.read_file(P / "district_credit_allocation.gpkg", layer="district").to_crs(CRS)
    xw = pd.read_csv(ROOT / "data" / "interim" / "tehsil_crosswalk.csv")
    adm1 = gpd.read_file(ROOT / "data" / "interim" / "boundaries_shp" / "pak_admin1.shp").to_crs(CRS)
    return dict(teh=teh, dist=dist, xw=xw, adm1=adm1, ict=adm1[adm1.adm1_name == "Islamabad"],
                lisa=pd.read_csv(T / "lisa_arhti.csv"), gm=pd.read_csv(T / "moran_global.csv"), lc=pd.read_csv(T / "lisa_counts.csv"),
                excl=pd.read_csv(T / "two_kinds_of_exclusion.csv"), head=pd.read_csv(T / "sbp_province_headline.csv"))


# ------------------------------------------------------------------------------------------ figures
def fig1(D):
    teh, dist, xw, adm1, ict = D["teh"], D["dist"], D["xw"], D["adm1"], D["ict"]
    fig = plt.figure(figsize=(11, 8.6))
    a, b = fig.add_axes([0.0, 0.34, 0.49, 0.58]), fig.add_axes([0.51, 0.34, 0.49, 0.58])
    mt = teh.match_types.fillna("")
    t = teh.copy()
    t["cls"] = np.select([t.rp_mouzas.fillna(0) == 0, mt.str.contains("parent_aggregation"), mt.str.contains("spelling|rename")],
                         ["No rural populated mouzas", "Parent aggregation (several census units summed)",
                          "Spelling or rename (reviewed by Ahmed)"], "Exact or rule-normalized")
    sty = {"Exact or rule-normalized": CAT["blue"], "Spelling or rename (reviewed by Ahmed)": CAT["orange"],
           "Parent aggregation (several census units summed)": CAT["aqua"], "No rural populated mouzas": NEUTRAL}
    hs = []
    for k, c in sty.items():
        sub = t[t.cls == k]
        sub.plot(ax=a, color=c, edgecolor=EDGE, linewidth=0.3)
        hs.append(Patch(facecolor=c, edgecolor="#bdbcb6", lw=0.4, label=f"{k} (n = {len(sub)})"))
        num("Fig 1", f"Tehsil polygons: {k}", len(sub), f"OCHA ADM3 ({V_B}) × crosswalk (decided by Ahmed)")
    ict.plot(ax=a, facecolor="white", edgecolor=INK, hatch="....", linewidth=0.6)
    hs.append(Patch(facecolor="white", edgecolor=INK, hatch="....", label="Islamabad Capital Territory (excluded)"))
    frame(a, t); furniture(a, t)
    assigned = int(t.rp_mouzas.sum())
    unm = xw[xw.match_type == "unmatched"]
    hs += [note(f"Not assigned to a polygon: {', '.join(unm.source_name.str.title())} ({int(unm.rp_mouzas.sum())} rural populated mouzas)"),
           note("Cholistan (census-only district): 3 tehsils, 323 mouzas, summed into Fort Abbas, Yazman, Liaqatpur (option A)")]
    legend(a, hs, "Mouza Census tehsils → OCHA ADM3 (139 polygons)")
    a.set_title(f"A. Tehsils (Q1): administrative assignment of {assigned:,} of\n23,130 rural populated mouzas ({assigned / 23130:.1%})",
                loc="left")
    num("Fig 1", "Rural populated mouzas administratively assigned", assigned, V_MC)
    ins = a.inset_axes([0.0, 0.66, 0.24, 0.34])
    adm1.plot(ax=ins, color="#d9d8d3", edgecolor="white", linewidth=0.4)
    adm1[adm1.adm1_name == "Punjab"].plot(ax=ins, color=CAT["blue"], edgecolor="white", linewidth=0.4)
    ins.set_axis_off(); ins.set_title("Punjab in Pakistan", fontsize=6.5, color=MUTED)
    d = dist.copy()
    d["cls"] = np.where(d.flagged == 1, "Matched, flagged in SBP data-quality screen", "Matched (SBP + Ag Census + Mouza Census)")
    hd = []
    for k, c in {"Matched (SBP + Ag Census + Mouza Census)": CAT["blue"], "Matched, flagged in SBP data-quality screen": CAT["orange"]}.items():
        sub = d[d.cls == k]
        sub.plot(ax=b, color=c, edgecolor=EDGE, linewidth=0.5)
        hd.append(Patch(facecolor=c, edgecolor="none", label=f"{k} (n = {len(sub)})"))
        num("Fig 1", f"Districts: {k}", len(sub), f"{V_SBP}; {V_AGC}; OCHA ADM2")
    for _, r in d[d.flagged == 1].iterrows():
        p = r.geometry.representative_point()
        b.annotate(r.adm2_name, (p.x, p.y), fontsize=6, ha="center", color=INK, zorder=5)
    ict.plot(ax=b, facecolor="white", edgecolor=INK, hatch="....", linewidth=0.6)
    hd += [Patch(facecolor="white", edgecolor=INK, hatch="....", label="Islamabad (excluded; SBP lists it under Punjab)"),
           note("Ag Census 'Cholistan Area' (19,536 farms, 0.4%) excluded from district denominators"),
           note("Lahore has no rural populated mouzas: excluded from Q1, kept in Q2")]
    frame(b, d); furniture(b, d)
    legend(b, hd, "SBP / Ag Census / Mouza Census districts → OCHA ADM2 (36)")
    b.set_title("B. Districts (Q2): SBP FY2023-24, Agricultural Census 2024\nand Mouza Census 2020 matched to OCHA", loc="left")
    fig.suptitle("Figure 1. Study area and data coverage, Punjab", x=0.01, y=0.995, ha="left", fontsize=11, fontweight="bold")
    footer(fig, [f"Data: {V_MC}; {V_SBP}; {V_AGC}. {V_B}. Vintages differ and are not contemporaneous.",
                 "Administrative assignment = share of rural populated mouzas assigned to a polygon; it is not geographic precision. "
                 "Aggregated polygons conceal internal differences."])
    save(fig, "fig1_study_area_coverage")


def fig2(D):
    t = D["teh"]
    ok = t[t.rp_mouzas > 0]
    c, why, nb = classify(ok.arhti_share, "arhti_share (tehsil)", "Fig 2")
    c2, why2, nb2 = classify(ok.rp_mouzas, "rp_mouzas (tehsil)", "Fig 2 side panel")
    fig = plt.figure(figsize=(11, 8.4))
    a = fig.add_axes([0.0, 0.27, 0.64, 0.59]); b = fig.add_axes([0.67, 0.47, 0.33, 0.38])
    choropleth(a, ok, "arhti_share", c, BLUE5)
    t[t.rp_mouzas.fillna(0) == 0].plot(ax=a, facecolor="white", edgecolor="#8a8984", linewidth=0.4)
    dh = desert_outline(a, t)
    frame(a, t); furniture(a, t)
    h = [Patch(facecolor=col, edgecolor="none", label=l) for col, l in zip(BLUE5, class_labels(c, "{:.2f}", ok.arhti_share.min()))]
    h += [Patch(facecolor="white", edgecolor="#8a8984", label=f"No rural populated mouzas (excluded from Q1; n = {int((t.rp_mouzas.fillna(0) == 0).sum())})"), dh]
    legend(a, h, f"AVAILABILITY: share of rural populated mouzas ({'natural breaks' if nb else 'quantiles'}, 5 classes; n = {len(ok)})", ncol=2)
    a.set_title("Share of rural mouzas reporting commission-agent credit,\nMouza Census 2020", loc="left", fontsize=10)
    for i, bnd in enumerate(c.bins):
        num("Fig 2", f"arhti_share class {i + 1} upper bound (n = {c.counts[i]})", round(bnd, 3), V_MC)
    choropleth(b, ok, "rp_mouzas", c2, ORANGE5)
    t[t.rp_mouzas.fillna(0) == 0].plot(ax=b, facecolor="white", edgecolor="#8a8984", linewidth=0.4)
    frame(b, t, pad=(0.05, 0.02, 0.05, 0.02))
    legend(b, [Patch(facecolor=col, edgecolor="none", label=l) for col, l in zip(ORANGE5, class_labels(c2, "{:,.0f}", ok.rp_mouzas.min()))],
           f"Rural populated mouzas per tehsil ({'natural breaks' if nb2 else 'quantiles'})")
    b.set_title("Denominator", loc="left", fontsize=8.5)
    for i, bnd in enumerate(c2.bins):
        num("Fig 2 side", f"rp_mouzas class {i + 1} upper bound (n = {c2.counts[i]})", round(bnd, 1), V_MC)
    fig.suptitle("Figure 2. Reported arhti credit availability by tehsil", x=0.01, y=0.995, ha="left", fontsize=11, fontweight="bold")
    footer(fig, [f"Data: {V_MC}. Availability as reported by enumerators, patwaris and local respondents; not household borrowing. {V_B}.",
                 DESERT_NOTE, f"Classification: {why}. Side panel uses its own classes (same rule)."])
    save(fig, "fig2_arhti_share_tehsil")


def fig3(D):
    t = D["teh"]
    ok = t[t.rp_mouzas > 0].copy()
    qa, qc = ok.arhti_share.quantile([1 / 3, 2 / 3]).values, ok.commercial_share.quantile([1 / 3, 2 / 3]).values
    ok["ra"], ok["rc"] = np.digitize(ok.arhti_share, qa, right=True), np.digitize(ok.commercial_share, qc, right=True)
    fig = plt.figure(figsize=(8.5, 8.8))
    a = fig.add_axes([0.0, 0.22, 1.0, 0.64])
    for (ra, rc), g in ok.groupby(["ra", "rc"]):
        g.plot(ax=a, color=BIV[ra][rc], edgecolor=EDGE, linewidth=0.3)
    t[t.rp_mouzas.fillna(0) == 0].plot(ax=a, facecolor="white", edgecolor="#8a8984", linewidth=0.4)
    dh = desert_outline(a, t)
    frame(a, t); furniture(a, t)
    lg = a.inset_axes([0.78, 0.04, 0.17, 0.17])
    cnt = ok.groupby(["ra", "rc"]).size()
    for ra in range(3):
        for rc in range(3):
            lg.add_patch(Rectangle((rc, ra), 1, 1, facecolor=BIV[ra][rc], edgecolor="white"))
            n = int(cnt.get((ra, rc), 0))
            lg.text(rc + 0.5, ra + 0.5, str(n), ha="center", va="center", fontsize=6, color=INK if ra + rc < 3 else "white")
            num("Fig 3", f"Tehsils in cell arhti tertile {ra + 1} × commercial tertile {rc + 1}", n, V_MC)
    lg.set_xlim(0, 3); lg.set_ylim(0, 3); lg.set_xticks([]); lg.set_yticks([])
    lg.set_xlabel("Commercial-bank credit\navailability: low → high", fontsize=6.2)
    lg.set_ylabel("Arhti credit availability:\nlow → high", fontsize=6.2)
    for s in lg.spines.values():
        s.set_visible(False)
    legend(a, [note(f"Tertile cut-points: arhti_share {qa[0]:.2f}, {qa[1]:.2f}; commercial_share {qc[0]:.2f}, {qc[1]:.2f}"),
               note(f"n = {len(ok)} tehsils; numbers in the key are tehsils per cell"),
               Patch(facecolor="white", edgecolor="#8a8984", label=f"No rural populated mouzas (n = {int((t.rp_mouzas.fillna(0) == 0).sum())})"), dh],
           "Key")
    for nm, v in [("arhti_share tertile 1/3", qa[0]), ("arhti_share tertile 2/3", qa[1]),
                  ("commercial_share tertile 1/3", qc[0]), ("commercial_share tertile 2/3", qc[1])]:
        num("Fig 3", nm, round(v, 3), V_MC)
    a.set_title("Substitutes or neighbours?\nReported arhti vs commercial-bank credit AVAILABILITY, by tehsil", loc="left", fontsize=9.5)
    fig.suptitle("Figure 3. Bivariate map (3 × 3 tertiles)", x=0.01, y=0.995, ha="left", fontsize=11, fontweight="bold")
    footer(fig, ["Co-location of reported sources across units cannot show substitution or complementarity at the borrower level.",
                 f"Data: {V_MC}; shares of rural populated mouzas reporting each source (multiple responses; not additive). {V_B}.",
                 DESERT_NOTE])
    save(fig, "fig3_bivariate_arhti_commercial")


def lisa_map(D, level, name, title, fig_label):
    lay = D["teh"] if level == "tehsil" else D["dist"]
    pc = "adm3_pcode" if level == "tehsil" else "adm2_pcode"
    nm = "adm3_name" if level == "tehsil" else "adm2_name"
    L = D["lisa"]
    q = L[(L.level == level) & (L.scenario == "A") & (L.weights == "Queen") & (L.analysis == "LISA arhti_share")]
    d = lay.merge(q[["pcode", "cluster_p05", "cluster_p01", "cluster_fdr05", "p_sim"]], left_on=pc, right_on="pcode", how="left")
    g = D["gm"]; g = g[(g.level == level) & (g.scenario == "A") & (g.weights == "Queen") & (g.variable == "arhti_share")].iloc[0]
    lc = D["lc"]; lc = lc[(lc.level == level) & (lc.scenario == "A") & (lc.weights == "Queen") & (lc.analysis == "LISA arhti_share")].set_index("cluster")
    cut = lc.bh_cutoff.iloc[0]
    cut_txt = f"Benjamini–Hochberg p-value cutoff = {cut:.4f}" if pd.notna(cut) else "Benjamini–Hochberg: no p-value passes (cutoff: none)"
    num(fig_label, "Benjamini–Hochberg p-value cutoff (FDR 0.05)", round(float(cut), 5) if pd.notna(cut) else "none", f"{V_MC}; Queen; {PERMS}")
    fig = plt.figure(figsize=(8.5, 9.0))
    a = fig.add_axes([0.0, 0.26, 1.0, 0.6])
    hs = []
    for k in ["High-High", "Low-Low", "High-Low", "Low-High", "not significant"]:
        sub = d[d.cluster_p05 == k]
        if len(sub):
            sub.plot(ax=a, color=LISA_C[k], edgecolor=EDGE, linewidth=0.3 if level == "tehsil" else 0.5)
        r = lc.loc[k]
        hs.append(Patch(facecolor=LISA_C[k], edgecolor="#bdbcb6", lw=0.4,
                        label=f"{k}: p<0.05 n = {r.p05}; p<0.01 n = {r.p01}; FDR n = {r.fdr05}"))
        for col, lab in [("p05", "p < 0.05"), ("p01", "p < 0.01"), ("fdr05", "FDR 0.05")]:
            num(fig_label, f"LISA {k} {level}s ({lab})", int(r[col]), f"{V_MC}; Queen; {PERMS}")
    fdr = d[d.cluster_fdr05.notna() & (d.cluster_fdr05 != "not significant")]
    fdr.plot(ax=a, facecolor="none", edgecolor=INK, linewidth=1.8, zorder=5)
    hs.append(Patch(facecolor="none", edgecolor=INK, lw=1.8, label=f"Heavy border: FDR(0.05) survivor (n = {len(fdr)}; {cut_txt})"))
    nod = d[d.cluster_p05.isna()]
    if len(nod):
        nod.plot(ax=a, facecolor="white", edgecolor="#8a8984", linewidth=0.4)
        hs.append(Patch(facecolor="white", edgecolor="#8a8984", label=f"Not analysed (no rural populated mouzas): {', '.join(nod[nm])}"))
    if level == "tehsil":
        hs.append(desert_outline(a, D["teh"]))
    else:
        for _, r in d[d.p_sim < 0.05].iterrows():
            p = r.geometry.representative_point()
            a.annotate(r[nm], (p.x, p.y), fontsize=6, ha="center", color="white" if r.cluster_p05 in ("High-High", "Low-Low") else INK)
    frame(a, d); furniture(a, d)
    legend(a, hs, "Local Moran's I cluster for arhti_share (colour: pseudo p < 0.05)")
    a.set_title(f"Global Moran's I = {g.I:.3f} (E[I] = {g.EI:.3f}, z = {g.z_perm:.2f}, pseudo p = {g.p_perm:.3f}); n = {int(g.n)} {level}s\n"
                f"Queen contiguity, row-standardised; {PERMS}", loc="left", fontsize=9)
    for k, v in [("Global Moran's I", round(g.I, 3)), ("E[I]", round(g.EI, 3)), ("z (permutation)", round(g.z_perm, 2)),
                 ("pseudo p", round(g.p_perm, 3)), (f"n {level}s", int(g.n))]:
        num(fig_label, k, v, f"{V_MC}; Queen; {PERMS}")
    fig.suptitle(title, x=0.01, y=0.995, ha="left", fontsize=11, fontweight="bold")
    footer(fig, [f"Weights: Queen contiguity, row-standardised; {PERMS}. Colours show pseudo p < 0.05; counts are given at p < 0.05, "
                 f"p < 0.01 and FDR(0.05) to acknowledge multiple testing; FDR survivors have a heavy border; {cut_txt}.",
                 f"Data: {V_MC}" + (", tehsil counts summed to districts (shares recomputed)" if level == "district" else "") + f". {V_B}."]
           + ([DESERT_NOTE] if level == "tehsil" else ["District level shown as a MAUP comparison; the Q1 unit is the tehsil (gate passed)."]))
    save(fig, name)


COOC_COLORS = ["#2a78d6", "#9ec5f4", NEUTRAL, "#f2a7a6", "#e34948"]
COOC_LABELS = ["< 0.80", "0.80–0.95", "0.95–1.053 (≈ independence)", "1.053–1.25", "> 1.25"]


def figS4(D):
    c = pd.read_csv(T / "mouza_cooccurrence.csv")
    tt = c[(c.record == "tehsil (arhti x commercial)") & (c.scenario == "A")]
    pooled = c[(c.record.str.startswith("pooled")) & (c.scenario == "A") & (c.pair == "arhti x commercial")].iloc[0]
    t = D["teh"].merge(tt[["pcode", "obs_exp_ratio", "ratio_class", "estimable", "n_mouzas"]], left_on="adm3_pcode", right_on="pcode", how="left")
    t["ratio_class"] = t.ratio_class.fillna("not estimable")
    fig = plt.figure(figsize=(8.8, 9.2))
    a = fig.add_axes([0.0, 0.25, 1.0, 0.62])
    hs = []
    for lab, col in zip(COOC_LABELS, COOC_COLORS):
        sub = t[t.ratio_class == lab]
        if len(sub):
            sub.plot(ax=a, color=col, edgecolor=EDGE, linewidth=0.3)
        hs.append(Patch(facecolor=col, edgecolor="#bdbcb6", lw=0.4, label=f"{lab} (n = {len(sub)})"))
        num("Fig S4", f"Tehsils with observed/expected {lab}", len(sub), f"{V_MC}; scenario A")
    ne = t[t.ratio_class == "not estimable"]
    plot_missing(a, ne)
    hs.append(hatch_patch(f"Not estimable: < 20 rural populated mouzas, or no mouza reporting arhti or commercial (n = {len(ne)})"))
    hs.append(desert_outline(a, D["teh"]))
    est = tt[tt.estimable == True]  # noqa: E712
    n_hi, n_lo = int((est.obs_exp_ratio > 1).sum()), int((est.obs_exp_ratio < 1).sum())
    hs.append(note(f"Estimable tehsils: ratio > 1: {n_hi}; < 1: {n_lo}"))
    hs.append(note(f"Pooled Mantel–Haenszel OR (within-tehsil) = {pooled.mh_or:.2f} (95% CI {pooled.ci95_low:.2f}–{pooled.ci95_high:.2f}); "
                   f"Breslow–Day (Tarone) homogeneity p {'< 0.001' if pooled.breslow_day_tarone_p < 0.001 else '= ' + format(pooled.breslow_day_tarone_p, '.3f')}"))
    for k, v in [("Estimable tehsils with ratio > 1", n_hi), ("Estimable tehsils with ratio < 1", n_lo),
                 ("Pooled MH OR arhti x commercial", round(pooled.mh_or, 3)), ("MH OR 95% CI", f"{pooled.ci95_low:.3f}–{pooled.ci95_high:.3f}"),
                 ("Breslow–Day (Tarone) p", "< 0.001" if pooled.breslow_day_tarone_p < 0.001 else round(pooled.breslow_day_tarone_p, 4))]:
        num("Fig S4", k, v, f"{V_MC}; scenario A; mouza-level records, tehsil strata")
    frame(a, t); furniture(a, t)
    legend(a, hs, "Observed / expected share of mouzas reporting BOTH arhti and commercial-bank credit (fixed classes)")
    a.set_title("EXPLORATORY: within-tehsil co-occurrence of reported arhti and commercial-bank credit (AVAILABILITY)", loc="left", fontsize=9)
    fig.suptitle("Figure S4. Mouza-level co-occurrence of reported credit sources, by tehsil", x=0.01, y=0.995, ha="left", fontsize=11, fontweight="bold")
    footer(fig, ["Within-tehsil co-occurrence of reported credit sources across mouzas; availability reports, not borrowing; association, "
                 "not substitution or complementarity in behaviour.",
                 "Expected = share(arhti) × share(commercial) under independence. Only tehsil aggregates are shown (no mouza names or codes). "
                 f"Data: {V_MC}; rural populated mouzas; Cholistan merged into parent tehsils (option A). {V_B}.", DESERT_NOTE])
    save(fig, "figS4_mouza_cooccurrence")


def fig5(D):
    """Main-text Figure 5: single panel (small_farm_reach, flagged districts marked, province headline box)."""
    d, head = D["dist"].copy(), D["head"]
    c, why, nb = classify(d.small_farm_reach, "small_farm_reach (district)", "Fig 5")
    fig = plt.figure(figsize=(8.5, 10.2))
    a = fig.add_axes([0.0, 0.13, 1.0, 0.68])
    choropleth(a, d, "small_farm_reach", c, BLUE5)
    D["ict"].plot(ax=a, facecolor="white", edgecolor=INK, hatch="....", linewidth=0.6)
    fl = d[d.flagged == 1]
    pts = fl.geometry.representative_point()
    a.scatter(pts.x, pts.y, marker="^", s=40, facecolor="white", edgecolor=INK, linewidth=0.9, zorder=5)
    frame(a, d); furniture(a, d)
    h = [Patch(facecolor=col, edgecolor="none", label=l) for col, l in zip(BLUE5, class_labels(c, "{:,.0f}", d.small_farm_reach.min()))]
    h += [Line2D([], [], marker="^", ls="", markerfacecolor="white", markeredgecolor=INK,
                 label=f"Flagged in SBP data-quality screen (n = {len(fl)})"),
          Patch(facecolor="white", edgecolor=INK, hatch="....", label="Islamabad (excluded)")]
    legend(a, h, f"Borrower records per 1,000 farms < 12.5 acres\n({'natural breaks' if nb else 'quantiles'}; n = {int(d.small_farm_reach.notna().sum())})",
           anchor=(0.0, 0.97))
    fig.text(0.01, 0.955, "ALLOCATION: small-farm reach = subsistence-holding borrower records per 1,000 farms under 12.5 acres",
             fontsize=9, ha="left", va="top")
    for i, bnd in enumerate(c.bins):
        num("Fig 5", f"small_farm_reach class {i + 1} upper bound (n = {c.counts[i]})", round(bnd, 1), f"{V_SBP}; {V_AGC}")
    hp = head[head.scope.str.startswith("All Punjab")].iloc[0]
    box = (f"Province level (one statistic, not mapped): above-economic holdings (> 50 acres) account for "
           f"{hp.abv_borrower_share:.1%} of\nfarm-sector borrower records but {hp.abv_amount_share:.1%} of farm-sector disbursement "
           f"(SBP FY2023-24, All-Punjab row incl. MFIs).\nLoans are recorded where they are BOOKED, which may differ from where "
           f"the land is; larger holdings need larger loans.")
    fig.text(0.01, 0.865, box, fontsize=7.4, va="bottom", ha="left",
             bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="#bdbcb6", lw=0.6))
    num("Fig 5", "Above-economic share of farm-sector borrower records", round(hp.abv_borrower_share, 4), V_SBP + " (All Punjab incl. MFIs)")
    num("Fig 5", "Above-economic share of farm-sector disbursement", round(hp.abv_amount_share, 4), V_SBP + " (All Punjab incl. MFIs)")
    fig.suptitle("Figure 5. Who does formal credit reach? Small-farm reach, Punjab districts", x=0.01, y=0.995, ha="left",
                 fontsize=11, fontweight="bold")
    footer(fig, ["SBP records the district where a loan is BOOKED, which may differ from where the borrower's land is; borrower records",
                 "may not be unique individuals. SBP \"up to 12.5 acres\" vs census \"under 12.5 acres\" differ at the boundary.",
                 f"Data: {V_SBP};", f"{V_AGC} (farms < 12.5 acres). Not contemporaneous.",
                 f"Classification: {why}.", f"{V_B}."])
    save(fig, "fig5_small_farm_reach")


def figS5(D):
    """Appendix Figure S5: the three-panel version (allocation, availability-based and presence-based classifications)."""
    d, head, ex = D["dist"].copy(), D["head"], D["excl"]
    c, _, j = common.choose_scheme(d.small_farm_reach)       # same rule and values as Figure 5 (not recorded twice)
    nb, why = c is j, "same classes as Figure 5"
    fig = plt.figure(figsize=(16, 8.4))
    axes = [fig.add_axes([0.0 + i * 0.335, 0.30, 0.32, 0.50]) for i in range(3)]
    a, b, cax = axes
    choropleth(a, d, "small_farm_reach", c, BLUE5)
    D["ict"].plot(ax=a, facecolor="white", edgecolor=INK, hatch="....", linewidth=0.6)
    fl = d[d.flagged == 1]
    pts = fl.geometry.representative_point()
    a.scatter(pts.x, pts.y, marker="^", s=34, facecolor="white", edgecolor=INK, linewidth=0.9, zorder=5)
    frame(a, d); furniture(a, d)
    h = [Patch(facecolor=col, edgecolor="none", label=l) for col, l in zip(BLUE5, class_labels(c, "{:,.0f}", d.small_farm_reach.min()))]
    h += [Line2D([], [], marker="^", ls="", markerfacecolor="white", markeredgecolor=INK, label=f"Flagged in SBP screen (n = {len(fl)})"),
          Patch(facecolor="white", edgecolor=INK, hatch="....", label="Islamabad (excluded)")]
    legend(a, h, f"Borrower records per 1,000 farms < 12.5 acres\n({'natural breaks' if nb else 'quantiles'}; n = {int(d.small_farm_reach.notna().sum())})")
    a.set_title("A. ALLOCATION: small-farm reach\nsubsistence-holding borrower records per 1,000 farms < 12.5 acres", loc="left", fontsize=8.5)
    for ax, basis, title, col in [(b, "availability", "B. AVAILABILITY-based: high reported commercial-bank\ncredit availability, low small-farm reach", "commercial_share"),
                                  (cax, "presence", "C. PRESENCE-based: high rural-branch presence\n(rural branches per 10,000 farms), low small-farm reach", "rural_branches_per_10k_farms")]:
        e = ex[(ex["sample"] == "all matched districts") & (ex.basis == basis)]
        names = set(e.adm2_name)
        has = d.small_farm_reach.notna() & d[col].notna()
        d["cls"] = np.select([d.adm2_name.isin(names), has], ["sel", "other"], "nc")
        lab = e.classification.iloc[0] if len(e) else basis
        sel, oth, nc = d[d.cls == "sel"], d[d.cls == "other"], d[d.cls == "nc"]
        sel.plot(ax=ax, color=CAT["orange"], edgecolor=EDGE, linewidth=0.5)
        oth.plot(ax=ax, color=NEUTRAL, edgecolor="#bdbcb6", linewidth=0.5)
        if len(nc):
            nc.plot(ax=ax, facecolor="white", edgecolor="#8a8984", linewidth=0.5)
        D["ict"].plot(ax=ax, facecolor="white", edgecolor=INK, hatch="....", linewidth=0.6)
        for _, r in sel.iterrows():
            p = r.geometry.representative_point()
            ax.annotate(r.adm2_name, (p.x, p.y), xytext=(0, 6), textcoords="offset points", fontsize=6.8, ha="center", color=INK, fontweight="bold")
        frame(ax, d); furniture(ax, d)
        hh = [Patch(facecolor=CAT["orange"], label=f"{lab} (n = {len(sel)})"), Patch(facecolor=NEUTRAL, edgecolor="#bdbcb6", label=f"Other districts (n = {len(oth)})")]
        if len(nc):
            hh.append(Patch(facecolor="white", edgecolor="#8a8984", label=f"Not classified: {', '.join(nc.adm2_name)} (no {col})"))
        hh.append(note(f"Cut-points: {col} ≥ {e.cut_top_half.iloc[0]:.3f} (median); reach ≤ {e.cut_reach_p33.iloc[0]:.1f} (33rd pct.)"))
        legend(ax, hh, "Top half AND bottom third of small-farm reach")
        ax.set_title(title, loc="left", fontsize=8.5)
        num(f"Fig S5{'B' if basis == 'availability' else 'C'}", f"Districts: {lab}", f"{len(sel)} ({', '.join(sorted(names))})",
            f"{V_SBP}; {V_AGC}; " + (V_MC if basis == "availability" else V_BR))
    hp = head[head.scope.str.startswith("All Punjab")].iloc[0]
    box = (f"Province level (single statistic, not mapped): above-economic holdings (> 50 acres) account for "
           f"{hp.abv_borrower_share:.1%} of farm-sector borrower records but {hp.abv_amount_share:.1%} of farm-sector disbursement "
           f"(SBP FY2023-24, All-Punjab row incl. MFIs)")
    fig.text(0.01, 0.92, box, fontsize=7.5, va="bottom", ha="left",
             bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="#bdbcb6", lw=0.6))
    fig.suptitle("Figure S5. Allocation of formal small-holding credit vs reported availability and physical presence, Punjab districts",
                 x=0.01, y=0.995, ha="left", fontsize=11, fontweight="bold")
    footer(fig, ["SBP records the district where a loan is BOOKED (lending branch or office), which may differ from where the borrower's land is; "
                 "borrower records may not be unique individuals. MFIs (Punjab-wide only) excluded from district measures.",
                 f"Data: {V_SBP}; {V_AGC} (farms < 12.5 acres; Cholistan Area excluded); {V_MC} (commercial_share = AVAILABILITY); "
                 f"{V_BR} (PRESENCE = branches coded rural, per 10,000 farms; all-branch density only as a sensitivity). Not contemporaneous.",
                 f"Panels B and C are consistent with barriers beyond physical distance; they do not identify them. Panel A classification: {why}. {V_B}."])
    save(fig, "figS5_small_farm_reach_classifications")


def fig6(D):
    spec = importlib.util.spec_from_file_location("ca", ROOT / "scripts" / "08_credit_allocation.py")
    ca = importlib.util.module_from_spec(spec); spec.loader.exec_module(ca)
    an = D["dist"][D["dist"].small_farm_reach.notna()]
    x, y, cc, _ = ca.concentration(an)
    xs, ys, ccs, _ = ca.concentration(an[an.flagged != 1])
    nx = int((an.flagged != 1).sum())
    fig, ax = plt.subplots(figsize=(5.8, 5.6))
    ax.plot([0, 1], [0, 1], color=MUTED, lw=1, ls="--", label="45° line: district share of borrower records\n= its share of small farms")
    ax.plot(x, y, color=CAT["blue"], lw=2, label=f"All districts (n = {len(an)}), CC = {cc:.2f}")
    ax.plot(xs, ys, color=CAT["orange"], lw=2, label=f"Excluding flagged districts (n = {nx}), CC = {ccs:.2f}")
    ax.legend(loc="upper left", fontsize=7, frameon=False)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_aspect("equal")
    ax.set_xlabel("Cumulative share of farms < 12.5 acres\n(districts ordered by small_farm_reach, lowest first)")
    ax.set_ylabel("Cumulative share of subsistence-holding borrower records")
    ax.grid(color=GRID, lw=0.6); ax.set_axisbelow(True)
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    ax.set_title("Figure S6. ALLOCATION: concentration of subsistence-holding\nborrower records relative to small farms", loc="left", fontsize=10, fontweight="bold")
    num("Fig S6", "Concentration coefficient, all districts", round(cc, 3), f"{V_SBP}; {V_AGC}")
    num("Fig S6", "Concentration coefficient, excluding flagged", round(ccs, 3), f"{V_SBP}; {V_AGC}")
    num("Fig S6", "n districts (all / excl. flagged)", f"{len(an)} / {nx}", f"{V_SBP}; {V_AGC}")
    fig.text(0.01, -0.10, "CC = 1 − 2 × area under the curve: how unevenly borrower records are concentrated across\n"
             "districts relative to small farms. Ordering by the ratio puts the curve below the 45° line by construction.\n"
             f"Data: {V_SBP};\n{V_AGC}. Not contemporaneous. Records may not be unique individuals.\nNot a map (no north arrow or scale bar). {AUTHOR}.",
             fontsize=6.2, color=MUTED)
    save(fig, "figS6_concentration_curve")
    for old in ["fig6_concentration_curve.png", "fig6_concentration_curve.pdf"]:
        (F / old).unlink(missing_ok=True)


def figS1(D):
    t = D["teh"][D["teh"].rp_mouzas > 0]
    rows = [(t, "arhti_share", BLUE5, "{:.2f}", "arhti_share, tehsil (Fig 2)"),
            (t, "rp_mouzas", ORANGE5, "{:,.0f}", "rural populated mouzas, tehsil (Fig 2 side)"),
            (D["dist"][D["dist"].small_farm_reach.notna()], "small_farm_reach", BLUE5, "{:,.0f}", "small_farm_reach, district (Fig 5A)")]
    fig, axes = plt.subplots(3, 2, figsize=(9, 12.5))
    for i, (g, col, ramp, fmt, title) in enumerate(rows):
        for k2, (nm, c) in enumerate([("Quantiles", mapclassify.Quantiles(g[col], k=5)), ("Natural breaks (Fisher-Jenks)", mapclassify.FisherJenks(g[col], k=5))]):
            ax = axes[i, k2]
            choropleth(ax, g, col, c, ramp)
            frame(ax, D["teh"], pad=(0.02, 0.02, 0.02, 0.02))
            ax.legend(handles=[Patch(facecolor=cc, label=l) for cc, l in zip(ramp, class_labels(c, fmt, g[col].min()))], fontsize=5.8,
                      frameon=False, loc="lower right")
            ax.set_title(f"{title}\n{nm}: GADF = {c.get_gadf():.3f}", fontsize=7.5, loc="left")
    fig.suptitle("Figure S1. Quantile vs natural-breaks classification for each choropleth", x=0.01, ha="left", fontsize=11, fontweight="bold")
    fig.text(0.01, 0.0, f"GADF = goodness of absolute deviation fit. Data: {V_MC}; {V_SBP}; {V_AGC}. Small comparison panels: no north arrow/"
             f"scale bar (see Figs 2 and 5). {AUTHOR}.", fontsize=6.2, color=MUTED)
    save(fig, "figS1_classification_comparison")


def main() -> int:
    F.mkdir(parents=True, exist_ok=True)
    D = load()
    fig1(D); fig2(D); fig3(D)
    lisa_map(D, "tehsil", "fig4_lisa_arhti_tehsil", "Figure 4. Spatial clusters of reported arhti credit availability (tehsil, Q1 unit)", "Fig 4")
    lisa_map(D, "district", "figS2_lisa_arhti_district", "Figure S2. MAUP comparison: LISA clusters of arhti_share at district level", "Fig S2")
    (F / "fig4_lisa_arhti_district.png").unlink(missing_ok=True); (F / "fig4_lisa_arhti_district.pdf").unlink(missing_ok=True)
    (F / "check_map_arhti.png").unlink(missing_ok=True)
    fig5(D); figS5(D); fig6(D); figS1(D); figS4(D)
    for old in ["fig5_small_farm_reach_exclusion.png", "fig5_small_farm_reach_exclusion.pdf"]:
        (F / old).unlink(missing_ok=True)
    APP_VARS = {"tehsil": ["arhti_share", "commercial_share", "ztbl_share", "coop_share", "mfb_share", "onlinebank_in_mouza_share",
                           "onlinebank_over25km_share", "mkt_grain_in_mouza_share", "mkt_grain_51plus_share", "cropland_share",
                           "tt_city_cropw_mean_min", "rp_mouzas"]}
    APP_VARS["district"] = APP_VARS["tehsil"]
    dq1 = gpd.read_file(P / "punjab_credit_context.gpkg", layer="district")
    for lvl, g in [("tehsil", D["teh"][D["teh"].rp_mouzas > 0]), ("district", dq1[dq1.rp_mouzas > 0])]:
        for v in APP_VARS[lvl]:
            classify(g[v], f"{v} ({lvl})", f"App {lvl}")
    dd = D["dist"]
    for v in ["small_farm_reach", "tenant_share", "large_farm_area_share", "rural_branches_per_10k_farms"]:
        classify(dd[v], f"{v} (district)", "App district Q2")
    pd.DataFrame(CLS_ROWS).to_csv(T / "classification_comparison.csv", index=False)
    nd = pd.DataFrame(NUMS)
    nd.to_csv(T / "figure_numbers.csv", index=False)   # same numbers as docs/figure_numbers.md, machine-readable (app)
    L = [f"# Every number shown in Figures 1–5, S1, S2, S4–S6 (S3: scripts/11) ({dt.date.today()})", "", "Written by `scripts/09_figures.py`.", "",
         nd.to_markdown(index=False), "", "## Classification comparison", "", pd.DataFrame(CLS_ROWS).to_markdown(index=False)]
    (ROOT / "docs" / "figure_numbers.md").write_text("\n".join(L) + "\n")
    print(pd.DataFrame(CLS_ROWS)[["figure", "variable", "scheme", "gadf", "counts", "chosen"]].to_string(index=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
