import streamlit as st

from lib import data, maps, ui

ui.page("Access", "Where credit sources are reported as available · Mouza Census 2020")
ui.narrative("Access")
k = data.kn
t = data.props("tehsils")
ok = t.rp_mouzas.fillna(0) > 0
hatched = {p: "No rural populated mouzas (not in the analysis)" for p in t.loc[~ok, "adm3_pcode"]}

st.subheader("Arhti credit availability by tehsil")
view = st.segmented_control("Map", ["Arhti share", "Clusters (LISA)"], default="Arhti share", key="acc_view") or "Arhti share"
tt = {r.adm3_pcode: {"Tehsil": f"{r.adm3_name} ({r.adm2_name})", "Arhti credit reported": ui.pct(r.arhti_share),
                     "Commercial-bank credit reported": ui.pct(r.commercial_share),
                     "Cluster (p < 0.05)": r.lisa_queen_p05 if isinstance(r.lisa_queen_p05, str) else "—"} for r in t.itertuples()}
tips = ["Tehsil", "Arhti credit reported", "Commercial-bank credit reported", "Cluster (p < 0.05)", "Note"]
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
        ui.class_legend(c, t.arhti_share[ok], ui.OCHRE5, "Share of rural populated mouzas reporting arhti credit",
                        [("#fff", f"No rural populated mouzas (n = {int((~ok).sum())})", "hatch")])
    else:
        vc = t.loc[ok, "lisa_queen_p05"].value_counts()
        ui.legend([(ui.LISA_C[x], f"{x} (n = {int(vc.get(x, 0))})", "") for x in ["High-High", "Low-Low", "Low-High", "High-Low", "not significant"]]
                  + [("#fff", f"Survives FDR 0.05: outlined (n = {len(fdr)})", "outline"),
                     ("#fff", f"No rural populated mouzas (n = {int((~ok).sum())})", "hatch")],
                  "Local clusters of arhti credit (p < 0.05)", f"Benjamini–Hochberg cutoff {k('bh_cutoff_queen')}.")
    st.write("")
    if clicked and clicked.get("adm3_pcode") in set(t.adm3_pcode):
        r = t[t.adm3_pcode == clicked["adm3_pcode"]].iloc[0]
        rows = ([("District", r.adm2_name), ("Arhti credit reported", ui.pct(r.arhti_share)),
                 ("Commercial-bank credit reported", ui.pct(r.commercial_share)), ("Cluster (p < 0.05)", r.lisa_queen_p05),
                 ("Cluster after FDR 0.05", r.lisa_queen_fdr05)] if r.rp_mouzas and r.rp_mouzas > 0
                else [("District", r.adm2_name), ("Note", "No rural populated mouzas")])
        ui.card(r.adm3_name, rows)
    else:
        st.caption("Click a tehsil for details.")
st.caption(f"Arhti credit is reported in {k('arhti_pooled')} of {k('rp_mouzas')} rural populated mouzas. Global Moran's I = "
           f"{k('moran_arhti_queen')} (p = {k('moran_arhti_queen_p')}); Queen contiguity, row-standardised, {k('permutations')} "
           f"permutations, seed {k('seed')}.")

st.subheader("Arhti and commercial-bank credit together")
okb = t.bivariate_class.notna()
fills = {p: ui.BIV[int(cl[1]) - 1][int(cl[4]) - 1] for p, cl in zip(t.adm3_pcode[okb], t.bivariate_class[okb])}
lab = {1: "low", 2: "middle", 3: "high"}
tt2 = {r.adm3_pcode: {"Tehsil": f"{r.adm3_name} ({r.adm2_name})",
                      "Group": (f"arhti {lab[int(r.bivariate_class[1])]}, banks {lab[int(r.bivariate_class[4])]}" if isinstance(r.bivariate_class, str) else "—")}
       for r in t.itertuples()}
a, b = st.columns([3, 1.2], gap="large")
with a:
    m2 = maps.base()
    maps.layer(m2, "tehsils", "adm3_pcode", fills, {p: "No rural populated mouzas" for p in t.loc[~okb, "adm3_pcode"]},
               ["Tehsil", "Group", "Note"], tt2)
    maps.show(m2, key="acc_biv")
    ui.vintage(t.vintage.iloc[0])
with b:
    cnt = t.bivariate_class.value_counts()
    cells = "".join(f'<div style="background:{ui.BIV[ra - 1][rc - 1]};color:{"#ffffff" if ra + rc >= 5 else ui.INK}">'
                    f'{int(cnt.get(f"A{ra}-C{rc}", 0))}</div>' for ra in (3, 2, 1) for rc in (1, 2, 3))
    st.markdown(f'<div style="display:flex;gap:.6rem;align-items:center"><div style="writing-mode:vertical-rl;transform:rotate(180deg);'
                f'font-size:.82rem;color:{ui.MUTED}">Arhti credit: low → high</div><div><div class="biv">{cells}</div>'
                f'<div style="font-size:.82rem;color:{ui.MUTED};margin-top:.3rem">Commercial-bank credit: low → high</div></div></div>',
                unsafe_allow_html=True)
    cut = {i: data.fig_number(i) for i in ["arhti_share tertile 1/3", "arhti_share tertile 2/3", "commercial_share tertile 1/3",
                                           "commercial_share tertile 2/3"]}
    ui.legend([], "", f"Tehsils per group (thirds of each share). Cut-points: arhti {ui.pct(cut['arhti_share tertile 1/3'])}, "
              f"{ui.pct(cut['arhti_share tertile 2/3'])}; commercial-bank {ui.pct(cut['commercial_share tertile 1/3'])}, "
              f"{ui.pct(cut['commercial_share tertile 2/3'])}.")
    st.write("")
    ui.callout(k("mh_or"), "odds ratio within tehsils",
               f"A village reporting commercial-bank credit is slightly more likely also to report arhti credit (95% CI {k('mh_lo')}–"
               f"{k('mh_hi')}; {k('mh_n_mouzas')} mouzas). The association differs across tehsils (Breslow–Day p {k('bd_p')}): "
               f"{k('tehsils_ratio_above1')} tehsils above and {k('tehsils_ratio_below1')} below independence.")
st.info("Reports of two credit sources in the same village describe what is available there. They do not show what farmers do, or "
        "whether one source substitutes for or complements the other.")

with st.expander("Methods and sensitivity"):
    st.markdown(
        f"- Bivariate Moran's I (arhti share × neighbours' commercial-bank share) = {k('bv_queen')} (p = {k('bv_queen_p')}).\n"
        f"- EXPLORATORY: arhti share vs cropland share, Spearman ρ = {k('rho_cropland')} (BH p {k('rho_cropland_pbh')}); vs share of villages "
        f"with an online commercial-bank branch (PRESENCE), ρ = {k('rho_onlinebank')} (BH p {k('rho_onlinebank_pbh')}).\n"
        f"- LISA counts: High-High {k('lisa_hh_p05')} / {k('lisa_hh_p01')} / {k('lisa_hh_fdr05')}, Low-Low {k('lisa_ll_p05')} / "
        f"{k('lisa_ll_p01')} / {k('lisa_ll_fdr05')} at p < 0.05 / p < 0.01 / FDR 0.05.\n"
        f"- Geodesic kNN-5 weights: Moran's I {k('moran_arhti_knn')}. District level: {k('moran_arhti_district')}.\n"
        f"- Cholistan desert mouzas excluded (scenario B): Moran's I {k('moran_arhti_B')}; odds ratio {k('mh_or_B')} "
        f"({k('mh_lo_B')}–{k('mh_hi_B')}).")
