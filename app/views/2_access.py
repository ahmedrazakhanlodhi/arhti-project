import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from lib import data, maps, ui

ui.page("Access", "Where credit sources are reported as available · Mouza Census 2020")
ui.narrative("Access")
k = data.kn
t = data.props("tehsils")
acc = data.table("app_tehsil_access")
t = t.merge(acc.drop(columns=["adm3_name", "adm2_name", "rp_mouzas", "arhti_share", "commercial_share", "ztbl_share", "coop_share",
                              "mfb_share", "vintage"]), on="adm3_pcode", how="left")
ok = t.rp_mouzas.fillna(0) > 0
hatched = {p: "No rural populated mouzas (not in the analysis)" for p in t.loc[~ok, "adm3_pcode"]}
hatch_item = [("#fff", f"No rural populated mouzas (n = {int((~ok).sum())})", "hatch")]

# ---------------------------------------------------------------- 1. arhti availability and clusters
st.subheader("Arhti credit availability by tehsil")
view = st.segmented_control("Map", ["Arhti share", "Clusters (LISA)"], default="Arhti share", key="acc_view") or "Arhti share"
tt = {r.adm3_pcode: {"Tehsil": f"{r.adm3_name} ({r.adm2_name})", "Arhti credit reported": ui.pct(r.arhti_share),
                     "Any formal credit reported": ui.pct(r.anyformal_share),
                     "Cluster (p < 0.05)": r.lisa_queen_p05 if isinstance(r.lisa_queen_p05, str) else "—"} for r in t.itertuples()}
tips = ["Tehsil", "Arhti credit reported", "Any formal credit reported", "Cluster (p < 0.05)", "Note"]
a, b = st.columns([3, 1.2], gap="large")
with a:
    m = maps.base()
    if view == "Arhti share":
        c = data.classes("arhti_share", "Fig 2")
        kk = data.class_index(t.arhti_share[ok], c["bins"])
        maps.layer(m, "tehsils", "adm3_pcode", {t.loc[i, "adm3_pcode"]: ui.OCHRE5[j] for i, j in kk.items() if j >= 0}, hatched, tips, tt)
    else:
        fdr = set(t.loc[ok & (t.lisa_queen_fdr05 != "not significant"), "adm3_pcode"])
        maps.layer(m, "tehsils", "adm3_pcode", {r.adm3_pcode: ui.LISA_C[r.lisa_queen_p05] for r in t[ok].itertuples()}, hatched, tips, tt,
                   outline=fdr)
    clicked = maps.show(m, key=f"acc_{view}")
    ui.vintage(t.vintage.iloc[0])
with b:
    if view == "Arhti share":
        ui.class_legend(c, t.arhti_share[ok], ui.OCHRE5, "Share of rural populated mouzas reporting arhti credit", hatch_item)
    else:
        vc = t.loc[ok, "lisa_queen_p05"].value_counts()
        ui.legend([(ui.LISA_C[x], f"{x} (n = {int(vc.get(x, 0))})", "") for x in ["High-High", "Low-Low", "Low-High", "High-Low", "not significant"]]
                  + [("#fff", f"Survives FDR 0.05: outlined (n = {len(fdr)})", "outline")] + hatch_item,
                  "Local clusters of arhti credit (p < 0.05)", f"Benjamini–Hochberg cutoff {k('bh_cutoff_queen')}.")
    st.write("")
    if clicked and clicked.get("adm3_pcode") in set(t.adm3_pcode):
        r = t[t.adm3_pcode == clicked["adm3_pcode"]].iloc[0]
        rows = ([("District", r.adm2_name), ("Arhti credit reported", ui.pct(r.arhti_share)),
                 ("Commercial-bank credit", ui.pct(r.commercial_share)), ("ZTBL credit", ui.pct(r.ztbl_share)),
                 ("Any formal source", ui.pct(r.anyformal_share)), ("Neither source", ui.pct(r.neither_share)),
                 ("Grain market within 10 km", ui.pct(r.mkt10_share)), ("Cluster (p < 0.05)", r.lisa_queen_p05)]
                if r.rp_mouzas and r.rp_mouzas > 0 else [("District", r.adm2_name), ("Note", "No rural populated mouzas")])
        ui.card(r.adm3_name, rows)
    else:
        st.caption("Click a tehsil for its profile.")
st.caption(f"Arhti credit is reported in {k('arhti_pooled')} of {k('rp_mouzas')} rural populated mouzas. Global Moran's I = "
           f"{k('moran_arhti_queen')} (p = {k('moran_arhti_queen_p')}); Queen contiguity, row-standardised, {k('permutations')} "
           f"permutations, seed {k('seed')}.")

# ---------------------------------------------------------------- 2. arhti and each formal source
st.subheader("Arhti and formal credit together")
SRC = {"commercial": "Commercial banks", "ztbl": "ZTBL", "coop": "Cooperative bank", "mfb": "Microfinance banks",
       "anyformal": "Any formal source"}
SRC_H1 = {"commercial": "commercial", "ztbl": "ztbl", "coop": "coop", "mfb": "mfb", "anyformal": "any formal"}
src = st.segmented_control("Formal source", list(SRC), default="commercial", format_func=SRC.get, key="acc_src") or "commercial"
h1 = data.table("course_h1_by_source").set_index("source").loc[SRC_H1[src]]
col = f"biv_{src}"
okb = ok & t[col].notna()
fills = {p: ui.BIV[int(cl[1]) - 1][int(cl[4]) - 1] for p, cl in zip(t.adm3_pcode[okb], t[col][okb])}
lab = {1: "low", 2: "middle", 3: "high"}
tt2 = {r.adm3_pcode: {"Tehsil": f"{r.adm3_name} ({r.adm2_name})", "Arhti credit": ui.pct(r.arhti_share),
                      f"{SRC[src]}": ui.pct(getattr(r, f"{src}_share")),
                      "Group": (f"arhti {lab[int(getattr(r, col)[1])]}, {SRC[src].lower()} {lab[int(getattr(r, col)[4])]}"
                                if isinstance(getattr(r, col), str) and r.rp_mouzas > 0 else "—")} for r in t.itertuples()}
a, b = st.columns([3, 1.2], gap="large")
with a:
    m2 = maps.base()
    maps.layer(m2, "tehsils", "adm3_pcode", fills, {p: "No rural populated mouzas" for p in t.loc[~okb, "adm3_pcode"]},
               ["Tehsil", "Arhti credit", SRC[src], "Group", "Note"], tt2)
    maps.show(m2, key=f"acc_biv_{src}")
    ui.vintage(t.vintage.iloc[0])
with b:
    cnt = t.loc[okb, col].value_counts()
    cells = "".join(f'<div style="background:{ui.BIV[ra - 1][rc - 1]};color:{"#ffffff" if ra + rc >= 5 else ui.INK}">'
                    f'{int(cnt.get(f"A{ra}-C{rc}", 0))}</div>' for ra in (3, 2, 1) for rc in (1, 2, 3))
    st.markdown(f'<div style="display:flex;gap:.6rem;align-items:center"><div style="writing-mode:vertical-rl;transform:rotate(180deg);'
                f'font-size:.82rem;color:{ui.MUTED}">Arhti credit: low → high</div><div><div class="biv">{cells}</div>'
                f'<div style="font-size:.82rem;color:{ui.MUTED};margin-top:.3rem">{SRC[src]}: low → high</div></div></div>',
                unsafe_allow_html=True)
    r0 = t[okb].iloc[0]
    ui.legend([], "", f"Tehsils per group (thirds of each share). Cut-points: arhti {ui.pct(r0.biv_arhti_cut1)}, {ui.pct(r0.biv_arhti_cut2)}; "
              f"{SRC[src].lower()} {ui.pct(r0[f'{col}_cut1'])}, {ui.pct(r0[f'{col}_cut2'])}.")
    st.write("")
    lo, hi = h1.mh_ci95_low, h1.mh_ci95_high
    verdict = ("higher odds" if lo > 1 else ("lower odds" if hi < 1 else "statistically inconclusive"))
    ui.callout(f"{h1.mh_or:.2f}", f"odds ratio within tehsils · {verdict}",
               f"Odds of a village reporting arhti credit where {SRC[src].lower()} credit is also reported, versus not (95% CI {lo:.2f}–{hi:.2f}; "
               f"{int(h1.mh_n_mouzas):,} mouzas in {int(h1.mh_strata)} tehsils; conventional stratified inference).")
    if pd.notna(h1.spearman_rho):
        st.caption(f"Same-tehsil Spearman ρ = {h1.spearman_rho:.3f}; bivariate Moran's I with neighbours = {h1.bivariate_moran_I:.3f}.")
st.info("Reports of two credit sources in the same village describe what is available there. They do not show what farmers do, or "
        "whether one source substitutes for or complements the other.")

# ---------------------------------------------------------------- 3. grain markets
st.subheader("Proximity to grain markets")
ui.narrative("Market access")
MB = data.table("course_market_bands").set_index("band")
w10 = MB.loc["mkt_grain_within10_share"]
BANDS = [0.2, 0.4, 0.6, 0.8]
BLUES = ["#e7f0f7", "#b6d2ea", "#7aaedb", "#3a7fc0", "#0d366b"]
BLABS = ["< 20%", "20–40%", "40–60%", "60–80%", "≥ 80%"]
km = pd.Series(np.digitize(t.mkt10_share[ok], BANDS), index=t.index[ok])       # classes include their lower bound (Figure 7)
a, b = st.columns([3, 1.2], gap="large")
with a:
    m3 = maps.base()
    maps.layer(m3, "tehsils", "adm3_pcode", {t.loc[i, "adm3_pcode"]: BLUES[j] for i, j in km.items()}, hatched,
               ["Tehsil", "Grain market within 10 km", "Arhti credit reported", "Note"],
               {r.adm3_pcode: {"Tehsil": f"{r.adm3_name} ({r.adm2_name})", "Grain market within 10 km": ui.pct(r.mkt10_share),
                               "Arhti credit reported": ui.pct(r.arhti_share)} for r in t.itertuples()})
    maps.show(m3, key="acc_mkt")
    ui.vintage(t.vintage.iloc[0])
with b:
    ui.legend([(c_, f"{l} (n = {int((km == i).sum())})", "") for i, (c_, l) in enumerate(zip(BLUES, BLABS))] + hatch_item,
              "Share of mouzas with a grain market within 10 km (incl. in the mouza)", "Fixed classes, as in Figure 7A.")
    st.write("")
    ui.callout(f"+{100 * w10.sem_coef_per_sd:.1f} pp", "arhti availability per one-SD rise",
               f"Spatial error model, 95% CI {w10.sem_ci95_low:.3f} to {w10.sem_ci95_high:.3f}; p = {w10.sem_p:.3f}, "
               f"{w10.sem_p_holm:.3f} after Holm adjustment across three distance bands. Exploratory.")
bt = MB.reset_index()[["label", "mean_share", "spearman_rho", "ols_p", "glm_p", "sem_coef_per_sd", "sem_p", "sem_p_holm"]]
bt.columns = ["Market measure", "Share of mouzas", "Spearman ρ", "OLS p", "Quasi-binomial p", "Spatial error coef. (per SD)",
              "Spatial error p", "Holm p (3 bands)"]
with st.expander("All three distance bands (Table B9)"):
    st.dataframe(bt.round(3), hide_index=True, width="stretch")
    st.caption("Each band replaces the market term in the same model (controls: cropland, commercial and ZTBL availability, distance "
               "to an online bank branch, travel time). Added after the first models were run; all bands reported.")

# ---------------------------------------------------------------- 4. neither source
st.subheader("Villages reporting neither arhti nor formal credit")
ui.narrative("Limited availability")
NB = [0.05, 0.10, 0.20, 0.40]
BROWNS = ["#f6f1e7", "#f2d3b6", "#e9a46c", "#c9531f", "#6b280b"]
NLABS = ["< 5%", "5–10%", "10–20%", "20–40%", "≥ 40%"]
kn_ = pd.Series(np.digitize(t.neither_share[ok], NB), index=t.index[ok])
a, b = st.columns([3, 1.2], gap="large")
with a:
    m4 = maps.base()
    maps.layer(m4, "tehsils", "adm3_pcode", {t.loc[i, "adm3_pcode"]: BROWNS[j] for i, j in kn_.items()}, hatched,
               ["Tehsil", "Neither source reported", "Note"],
               {r.adm3_pcode: {"Tehsil": f"{r.adm3_name} ({r.adm2_name})", "Neither source reported": ui.pct(r.neither_share)}
                for r in t.itertuples()})
    maps.show(m4, key="acc_neither")
    ui.vintage(t.vintage.iloc[0])
with b:
    ui.legend([(c_, f"{l} (n = {int((kn_ == i).sum())})", "") for i, (c_, l) in enumerate(zip(BROWNS, NLABS))] + hatch_item,
              "Share of mouzas reporting neither arhti nor any formal source", "Fixed classes, as in Figure 7B.")
parts = [("Both", "all_any_both", ui.INDIGO5[3]), ("Formal only", "all_any_other_only", ui.INDIGO5[1]),
         ("Arhti only", "all_any_arhti_only", ui.OCHRE5[2]), ("Neither", "all_any_neither", "#c9531f")]
fig = go.Figure()
for nm, kid, colr in parts:
    v = float(data.kn_row(kid).value)
    fig.add_trace(go.Bar(x=[v], y=["Rural populated mouzas"], orientation="h", name=f"{nm} ({k(kid)})", marker_color=colr,
                         hovertemplate=f"{nm}: {k(kid)} mouzas<extra></extra>"))
ui.chart(fig, 170, legend_y=1.45, barmode="stack", xaxis=dict(title="Mouzas (Mouza Census 2020)"), yaxis=dict(visible=False))
st.plotly_chart(fig, config={"displayModeBar": False}, key="acc_parts")
st.caption(f"{k('all_any_overlap')} of arhti-reporting mouzas also report a formal source. Formal = commercial bank, ZTBL, cooperative "
           "bank or microfinance bank.")

with st.expander("Methods and sensitivity"):
    st.markdown(
        f"- Bivariate Moran's I (arhti share × neighbours' commercial-bank share) = {k('bv_queen')} (p = {k('bv_queen_p')}).\n"
        f"- EXPLORATORY: arhti share vs cropland share, Spearman ρ = {k('rho_cropland')} (BH p {k('rho_cropland_pbh')}); vs share of villages "
        f"with an online commercial-bank branch (PRESENCE), ρ = {k('rho_onlinebank')} (BH p {k('rho_onlinebank_pbh')}).\n"
        f"- Within-tehsil odds ratios vary across tehsils (Breslow–Day p {k('bd_p')}): {k('tehsils_ratio_above1')} tehsils above and "
        f"{k('tehsils_ratio_below1')} below independence (commercial banks).\n"
        f"- LISA counts: High-High {k('lisa_hh_p05')} / {k('lisa_hh_p01')} / {k('lisa_hh_fdr05')}, Low-Low {k('lisa_ll_p05')} / "
        f"{k('lisa_ll_p01')} / {k('lisa_ll_fdr05')} at p < 0.05 / p < 0.01 / FDR 0.05.\n"
        f"- Geodesic kNN-5 weights: Moran's I {k('moran_arhti_knn')}. District level: {k('moran_arhti_district')}.\n"
        f"- Cholistan desert mouzas excluded (scenario B): Moran's I {k('moran_arhti_B')}; odds ratio {k('mh_or_B')} "
        f"({k('mh_lo_B')}–{k('mh_hi_B')}).")
ui.footer()
