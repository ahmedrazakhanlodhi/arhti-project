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
BEN = {"area": "Cultivated area (default, as H3)", "class": "Farms in the same holding class", "farms": "All farms"}
ben = st.segmented_control("Benchmark", list(BEN), default="area", format_func=BEN.get, key="rep_ben") or "area"
if ben == "class" and cls == "tot":
    ben = "farms"
lqc = data.table("course_lq_class_farms").set_index("adm2_pcode")
if ben == "area":
    lq = dist[f"lq_amount_{cls}"]
elif ben == "class":
    lq = lqc[f"lq_class_farms_{cls}"].reindex(dist.index)
else:
    lq = dist[f"credit_share_{cls}"] / dist.farm_share
kk = pd.Series(np.digitize(lq.values, ui.LQ_BREAKS), index=lq.index)
d = data.props("districts")
fl = set(d.loc[d.flagged.astype(int) == 1, "adm2_pcode"])
tt = {p: {"District": r.adm2_name, "LQ (this benchmark)": f"{lq[p]:.2f}", "LQ (cultivated area)": f"{r[f'lq_amount_{cls}']:.2f}",
          "Share of class disbursement": ui.pct(r[f"credit_share_{cls}"]), "Share of cultivated area": ui.pct(r.area_share),
          "SBP data-quality screen": "flagged" if p in fl else "not flagged"} for p, r in dist.iterrows()}
a, b = st.columns([3, 1.2], gap="large")
with a:
    m = maps.base()
    maps.layer(m, "districts", "adm2_pcode", {p: ui.LQ_COLS[j] for p, j in kk.items()}, {},
               ["District", "LQ (this benchmark)", "LQ (cultivated area)", "Share of class disbursement", "Share of cultivated area",
                "SBP data-quality screen"],
               tt, outline=fl)
    maps.show(m, key=f"rep_lq_{cls}_{ben}")
    ui.vintage(rg.vintage.iloc[0])
with b:
    ui.legend([(c, f"{l} (n = {int((kk == i).sum())})", "") for i, (c, l) in enumerate(zip(ui.LQ_COLS, ui.LQ_LABS))]
              + [("#fff", f"Flagged in SBP data-quality screen: outlined (n = {len(fl)})", "outline")],
              f"LQ, {CLS[cls].lower()} vs {BEN[ben].split(' (')[0].lower()}", "1 = recorded in proportion to the benchmark. Fixed breaks, "
              "symmetric on a log scale (as Figure R1). 36 districts; Islamabad and MFIs excluded. Class benchmarks use farm counts, since "
              "the census class areas are inconsistent.")

# ---------------------------------------------------------------- city summary
st.subheader("Five large-city districts")
CITIES = ["Lahore", "Rawalpindi", "Multan", "Faisalabad", "Rahim Yar Khan"]
s = rg[rg.record_type == "summary"].copy()
s["label"] = np.where(s.adm2_name.str.startswith("Five"), "Five cities combined", np.where(s.adm2_name.str.startswith("Other"),
                      "Other 31 districts", s.adm2_name))
s = s.set_index("label").loc[["Five cities combined"] + CITIES]
fig = go.Figure()
for col, lab, colr in [("credit_share_tot", "Share of disbursement", ui.INDIGO5[2]), ("credit_share_sub", "Share of subsistence disbursement", ui.INDIGO5[1]),
                       ("credit_share_abv", "Share of above-economic disbursement", ui.INDIGO5[4]),
                       ("area_share", "Share of cultivated area", ui.OCHRE5[2]), ("farm_share", "Share of farms", ui.OCHRE5[1]),
                       ("rural_branch_share", "Share of rural branches", "#8a8984"), ("total_branch_share", "Share of all branches", "#4a4740")]:
    fig.add_trace(go.Bar(x=s.index, y=100 * s[col], name=lab, marker_color=colr, hovertemplate=f"%{{x}}<br>{lab}: %{{y:.1f}}%<extra></extra>"))
ui.chart(fig, 460, legend_y=1.16, barmode="group", yaxis=dict(title="Percent of the 36-district total"))
st.plotly_chart(fig, config={"displayModeBar": False}, key="rep_city")
ui.vintage(rg.vintage.iloc[0])
st.caption(f"Combined, the five districts record {k('five_credit_share_tot')} of disbursement and {k('five_credit_share_abv')} of above-economic "
           f"disbursement, with {k('five_area_share')} of cultivated area and {k('five_farm_share')} of farms. Islamabad (outside the totals): "
           f"{k('isb_credit_share_tot')} of disbursement in SBP district rows including Islamabad.")

st.markdown("**Does the concentration depend on the districts chosen?**")
sv = data.table("course_h2_h3_sensitivity")
lab_sv = {"all 36 districts": "Five city districts (all 36)", "excluding the 5 flagged districts": "Without flagged districts (Multan, RYK left)",
          "all 36 districts; five districts with the largest urban populations (Population Census 2023)": "Five largest urban populations (2023)"}
sv["label"] = sv["sample"].map(lambda x: lab_sv.get(x, x.replace("leave out", "Leave out")))
fig_s = go.Figure()
for col, lab, colr in [("group_abv_ratio_to_cultivated", "Above-economic lending ÷ cultivated-area share", ui.INDIGO5[4]),
                       ("group_sub_ratio_to_cultivated", "Subsistence lending ÷ cultivated-area share", ui.INDIGO5[1])]:
    fig_s.add_trace(go.Bar(y=sv.label, x=sv[col], orientation="h", name=lab, marker_color=colr,
                           hovertemplate="%{y}: %{x:.2f}<extra></extra>"))
fig_s.add_vline(x=1, line_dash="dash", line_color="#8a8984")
ui.chart(fig_s, 420, legend_y=1.12, barmode="group", xaxis=dict(title="Ratio (1 = proportional to cultivated area)"),
         yaxis=dict(autorange="reversed"))
st.plotly_chart(fig_s, config={"displayModeBar": False}, key="rep_sens")
st.caption(f"Leaving out any one city, the rest still record {k('sv_loo_abv_min')} to {k('sv_loo_abv_max')} times their area share of "
           f"above-economic lending. The five districts with the largest urban populations record {k('sv_ur_abv')} of it with "
           f"{k('sv_ur_cult')} of cultivated area. Exploratory; robustness does not settle whether lending is booked or used there.")

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
ui.chart(fig2, 860, legend_y=1.03, xaxis=dict(title="Branches per 10,000 farms (log scale)", type="log"))
st.plotly_chart(fig2, config={"displayModeBar": False}, key="rep_branches")
ui.vintage("SBP list of scheduled bank branches as on 30 June 2024 (rural = branches coded R); Agricultural Census 2024 farms")
st.caption(f"Lahore: {k('lahore_total_branches_10k')} branches per 10,000 farms in total, {k('lahore_rural_branches_10k')} rural. Branch "
           "counts are PRESENCE, not lending.")
with st.expander("Table (sortable)"):
    st.dataframe(dist.reset_index()[["adm2_name", "lq_amount_abv", "lq_amount_eco", "lq_amount_sub", "lq_amount_tot", "lq_borrowers_sub",
                                     "credit_per_cultivated_acre_rs", "total_branches_per_10k_farms", "rural_branches_per_10k_farms"]].round(2),
                 hide_index=True, width="stretch")
    st.caption(f"District = {ui.ATTRIBUTION}.")
ui.footer()
