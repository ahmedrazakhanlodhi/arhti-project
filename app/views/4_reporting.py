import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from lib import data, maps, ui

ui.page("Reporting geography", "Where formal agricultural lending is recorded · SBP FY2023-24")
st.warning(f"**District attribution:** every SBP district figure on this page is the {ui.ATTRIBUTION}. Whether SBP's district is the "
           "lending branch's or the financed farm's has not been confirmed, so a high value in a city district may reflect where loans "
           "are recorded rather than where the land is. District disbursement amounts are mapped on this page only.")
ui.narrative("Reporting geography")
k = data.kn
rg = data.table("reporting_geography")
dist = rg[rg.record_type == "district"].set_index("adm2_pcode")

# ---------------------------------------------------------------- LQ map
st.subheader("Location quotient: share of class disbursement ÷ share of cultivated area")
CLS = {"abv": "Above-economic (> 50 acres)", "eco": "Economic (12.5–50 acres)", "sub": "Subsistence (up to 12.5 acres)", "tot": "All holdings"}
cls = st.segmented_control("Holding class", list(CLS), default="abv", format_func=CLS.get, key="rep_cls") or "abv"
lq = dist[f"lq_amount_{cls}"]
kk = pd.Series(np.digitize(lq.values, ui.LQ_BREAKS), index=lq.index)
d = data.props("districts")
fl = set(d.loc[d.flagged.astype(int) == 1, "adm2_pcode"])
tt = {p: {"District": r.adm2_name, "LQ (amount)": f"{r[f'lq_amount_{cls}']:.2f}", "LQ (borrower records)": f"{r[f'lq_borrowers_{cls}']:.2f}",
          "Share of class disbursement": ui.pct(r[f"credit_share_{cls}"]), "Share of cultivated area": ui.pct(r.area_share),
          "SBP data-quality screen": "flagged" if p in fl else "not flagged"} for p, r in dist.iterrows()}
a, b = st.columns([3, 1.2], gap="large")
with a:
    m = maps.base()
    maps.layer(m, "districts", "adm2_pcode", {p: ui.LQ_COLS[j] for p, j in kk.items()}, {},
               ["District", "LQ (amount)", "LQ (borrower records)", "Share of class disbursement", "Share of cultivated area", "SBP data-quality screen"],
               tt, outline=fl)
    maps.show(m, key=f"rep_lq_{cls}")
    ui.vintage(rg.vintage.iloc[0])
with b:
    ui.legend([(c, f"{l} (n = {int((kk == i).sum())})", "") for i, (c, l) in enumerate(zip(ui.LQ_COLS, ui.LQ_LABS))]
              + [("#fff", f"Flagged in SBP data-quality screen: outlined (n = {len(fl)})", "outline")],
              f"LQ, {CLS[cls].lower()}", "1 = recorded in proportion to farmland. Fixed breaks, symmetric on a log scale (as Figure R1). "
              "36 districts; Islamabad and MFIs excluded.")

# ---------------------------------------------------------------- city summary
st.subheader("Five large-city districts")
CITIES = ["Lahore", "Rawalpindi", "Multan", "Faisalabad", "Rahim Yar Khan"]
s = rg[rg.record_type == "summary"].copy()
s["label"] = np.where(s.adm2_name.str.startswith("Five"), "Five cities combined", np.where(s.adm2_name.str.startswith("Other"),
                      "Other 31 districts", s.adm2_name))
s = s.set_index("label").loc[["Five cities combined"] + CITIES]
fig = go.Figure()
for col, lab, colr in [("credit_share_tot", "Share of disbursement", ui.INDIGO5[2]), ("credit_share_abv", "Share of above-economic disbursement", ui.INDIGO5[4]),
                       ("area_share", "Share of cultivated area", ui.OCHRE5[2]), ("farm_share", "Share of farms", ui.OCHRE5[1]),
                       ("rural_branch_share", "Share of rural branches", "#8a8984"), ("total_branch_share", "Share of all branches", "#4a4740")]:
    fig.add_trace(go.Bar(x=s.index, y=100 * s[col], name=lab, marker_color=colr, hovertemplate=f"%{{x}}<br>{lab}: %{{y:.1f}}%<extra></extra>"))
fig.update_layout(barmode="group", height=440, margin=dict(l=10, r=10, t=10, b=40), plot_bgcolor=ui.SAND, paper_bgcolor=ui.SAND,
                  yaxis=dict(title="Percent of the 36-district total", gridcolor="#e3d9c6"), legend=dict(orientation="h", y=1.1),
                  font=dict(family="Inter, sans-serif", color=ui.INK))
st.plotly_chart(fig, config={"displayModeBar": False}, key="rep_city")
ui.vintage(rg.vintage.iloc[0])
st.caption(f"Combined, the five districts record {k('five_credit_share_tot')} of disbursement and {k('five_credit_share_abv')} of above-economic "
           f"disbursement, with {k('five_area_share')} of cultivated area and {k('five_farm_share')} of farms. Islamabad (outside the totals): "
           f"{k('isb_credit_share_tot')} of disbursement in SBP district rows including Islamabad.")

# ---------------------------------------------------------------- branches
st.subheader("Bank branches per 10,000 farms: all vs rural")
br = dist.sort_values("total_branches_per_10k_farms")
fig2 = go.Figure()
for i, r in br.iterrows():
    fig2.add_trace(go.Scatter(x=[r.rural_branches_per_10k_farms, r.total_branches_per_10k_farms], y=[r.adm2_name] * 2, mode="lines",
                              line=dict(color="#d8ceba", width=2), showlegend=False, hoverinfo="skip"))
fig2.add_trace(go.Scatter(x=br.rural_branches_per_10k_farms, y=br.adm2_name, mode="markers", name="Rural branches",
                          marker=dict(size=9, color=ui.OCHRE), hovertemplate="%{y}: %{x:.1f} rural branches per 10,000 farms<extra></extra>"))
fig2.add_trace(go.Scatter(x=br.total_branches_per_10k_farms, y=br.adm2_name, mode="markers", name="All scheduled-bank branches",
                          marker=dict(size=9, color=ui.INDIGO), hovertemplate="%{y}: %{x:.1f} branches per 10,000 farms<extra></extra>"))
fig2.update_layout(height=860, margin=dict(l=10, r=10, t=10, b=40), plot_bgcolor=ui.SAND, paper_bgcolor=ui.SAND,
                   xaxis=dict(title="Branches per 10,000 farms (log scale)", type="log", gridcolor="#e3d9c6"), legend=dict(orientation="h", y=1.03),
                   font=dict(family="Inter, sans-serif", color=ui.INK))
st.plotly_chart(fig2, config={"displayModeBar": False}, key="rep_branches")
ui.vintage("SBP list of scheduled bank branches as on 30 June 2024 (rural = branches coded R); Agricultural Census 2024 farms")
st.caption(f"Lahore: {k('lahore_total_branches_10k')} branches per 10,000 farms in total, {k('lahore_rural_branches_10k')} rural. Branch "
           "counts are PRESENCE, not lending.")
with st.expander("Table (sortable)"):
    st.dataframe(dist.reset_index()[["adm2_name", "lq_amount_abv", "lq_amount_eco", "lq_amount_sub", "lq_amount_tot", "lq_borrowers_sub",
                                     "credit_per_cultivated_acre_rs", "total_branches_per_10k_farms", "rural_branches_per_10k_farms"]].round(2),
                 hide_index=True, width="stretch")
    st.caption(f"District = {ui.ATTRIBUTION}.")
