import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from lib import data, maps, ui

ui.page("District profiles", "One district at a time, or side by side · descriptive scorecard")
ui.narrative("District profiles")
k = data.kn
sc = data.table("district_scorecard").sort_values("adm2_name")
da = data.table("app_district_access").set_index("adm2_name")
name = st.selectbox("District", sc.adm2_name.tolist(), key="prof_district")
r = sc[sc.adm2_name == name].iloc[0]
acc = da.loc[name] if name in da.index else None
pct, num = ui.pct, ui.num

st.markdown(f"### {name}")
st.markdown(f"**Profile:** {r.profile_type}")
ui.tiles([(num(round(r.farms)), "farms"), (pct(r.smallholder_share), "farms under 12.5 acres"), (pct(r.tenant_share), "tenant farms"),
          (f"{num(round(r.cultivated_ac))} ac", "cultivated area")])

a, b = st.columns([1.6, 1], gap="large")
with a:
    if acc is not None:
        st.markdown("**Reported credit availability: share of rural populated mouzas (Mouza Census 2020)**")
        rows = [("Arhti", acc.arhti_share, "arhti_pooled", ui.OCHRE), ("Commercial banks", acc.commercial_share, "h1_com_share", ui.INDIGO),
                ("ZTBL", acc.ztbl_share, "h1_ztbl_share", ui.INDIGO), ("Cooperative bank", acc.coop_share, "h1_coop_share", ui.INDIGO),
                ("Microfinance banks", acc.mfb_share, "h1_mfb_share", ui.INDIGO), ("Any formal source", acc.anyformal_share, "h1_any_share", ui.INDIGO),
                ("Neither source", acc.neither_share, "all_any_neither_share", "#c9531f"),
                ("Grain market within 10 km", acc.mkt10_share, "mb_w10_mean", "#3a7fc0")]
        fig = go.Figure()
        fig.add_trace(go.Bar(y=[x[0] for x in rows], x=[100 * x[1] for x in rows], orientation="h", marker_color=[x[3] for x in rows],
                             name=name, text=[pct(x[1]) for x in rows], textposition="outside",
                             hovertemplate="%{y}: %{x:.1f}%<extra></extra>"))
        fig.add_trace(go.Scatter(y=[x[0] for x in rows], x=[100 * float(data.kn_row(x[2]).value) for x in rows], mode="markers",
                                 name="Punjab (all rural populated mouzas)", marker=dict(symbol="line-ns-open", size=22, color=ui.INK, line=dict(width=3)),
                                 hovertemplate="Punjab: %{x:.1f}%<extra></extra>"))
        ui.chart(fig, 380, legend_y=1.1, xaxis=dict(title="Percent of rural populated mouzas", range=[0, 112]), yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig, config={"displayModeBar": False}, key=f"prof_acc_{name}")
    else:
        st.info("This district has no rural populated mouzas, so it has no availability figures.")
    ui.card("ACCESS clusters", [("Tehsils in High-High / Low-Low arhti clusters (p < 0.05)", f"{int(r.tehsils_hh_p05)} / {int(r.tehsils_ll_p05)}"),
                                ("… after FDR 0.05", f"{int(r.tehsils_hh_fdr05)} / {int(r.tehsils_ll_fdr05)}"),
                                ("Top two of five crops by area", r.top2_crops)])
    st.write("")
    ui.card("ALLOCATION and PRESENCE", [("Small-farm reach (per 1,000 farms under 12.5 acres)", num(r.small_farm_reach)),
                                        ("… Punjab district median", k("reach_median")),
                                        ("All bank branches per 10,000 farms", num(r.total_branches_per_10k_farms)),
                                        ("Rural branches per 10,000 farms", num(r.rural_branches_per_10k_farms)),
                                        ("SBP data-quality screen", "flagged" if r.flagged == 1 else "not flagged")])
    st.write("")
    ui.card(f"REPORTING GEOGRAPHY ({ui.ATTRIBUTION})",
            [("Credit per cultivated acre (Rs)", num(round(r.credit_per_cultivated_acre_rs)) if pd.notna(r.credit_per_cultivated_acre_rs) else "—"),
             ("LQ, all holdings", f"{r.lq_amount_tot:.2f}"), ("LQ, above-economic", f"{r.lq_amount_abv:.2f}"), ("LQ, subsistence", f"{r.lq_amount_sub:.2f}")])
with b:
    m = maps.base()
    pc = r.adm2_pcode
    maps.layer(m, "districts", "adm2_pcode", {pc: ui.INDIGO}, {}, ["District"],
               {p: {"District": n} for p, n in zip(data.props("districts").adm2_pcode, data.props("districts").adm2_name)}, opacity=0.9)
    maps.show(m, key=f"prof_map_{pc}")
    ui.vintage(r.vintage)
    st.caption(r.profile_rule)
st.info("Caveats: availability is reported by village respondents, not household borrowing; SBP districts are as reported (attribution under "
        "verification); borrower records may not be unique people; the Agricultural Census is sample-based; sources differ in date. "
        + ("This district is flagged in the SBP data-quality screen; its credit figures should be read with care. " if r.flagged == 1 else "")
        + ("This district has no rural populated mouzas, so it has no availability figures and is not classified. " if r.profile_type == "not classified" else ""))

# ---------------------------------------------------------------- compare
st.subheader("Compare districts")
pick = st.multiselect("Choose two or three districts", sc.adm2_name.tolist(), default=[n for n in ["Attock", "Lahore", "Bahawalnagar"]
                                                                                       if n in set(sc.adm2_name)], max_selections=3, key="prof_compare")
if len(pick) >= 2:
    rows = []
    for n in pick:
        s_ = sc[sc.adm2_name == n].iloc[0]
        a_ = da.loc[n] if n in da.index else None
        rows.append({"District": n, "Profile": s_.profile_type, "Farms": num(round(s_.farms)), "Farms under 12.5 acres": pct(s_.smallholder_share),
                     "Tenant farms": pct(s_.tenant_share), "Arhti credit reported": pct(a_.arhti_share) if a_ is not None else "—",
                     "Any formal source reported": pct(a_.anyformal_share) if a_ is not None else "—",
                     "Neither source reported": pct(a_.neither_share) if a_ is not None else "—",
                     "Grain market within 10 km": pct(a_.mkt10_share) if a_ is not None else "—",
                     "Small-farm reach": num(s_.small_farm_reach), "Rural branches per 10,000 farms": num(s_.rural_branches_per_10k_farms),
                     "SBP screen": "flagged" if s_.flagged == 1 else "not flagged"})
    st.dataframe(pd.DataFrame(rows).set_index("District").T, width="stretch")
    st.caption(f"Punjab: small-farm reach district median {k('reach_median')}; arhti credit reported in {k('arhti_pooled')} of rural populated "
               "mouzas. Descriptive comparisons, not rankings.")
else:
    st.caption("Pick at least two districts.")
ui.footer()
