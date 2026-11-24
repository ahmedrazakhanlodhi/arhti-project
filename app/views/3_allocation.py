import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from lib import data, maps, ui

ui.page("Allocation", "Who formal credit reaches · SBP FY2023-24 and Agricultural Census 2024")
ui.narrative("Allocation")
k = data.kn

# ---------------------------------------------------------------- holding classes (province level)
st.subheader("Holding classes: farms and area vs borrower records and disbursement (Punjab)")
h = data.table("holding_class_shares")
fig = go.Figure()
for col, lab, colr in [("share_farms", "Share of farms", ui.INDIGO5[1]), ("share_operated_area", "Share of operated farm area", ui.INDIGO5[3]),
                       ("share_borrower_records", "Share of borrower records", ui.OCHRE5[1]), ("share_disbursement", "Share of disbursement", ui.OCHRE5[3])]:
    fig.add_trace(go.Bar(x=[c.replace("_", "-") for c in h.holding_class], y=100 * h[col], name=lab, marker_color=colr,
                         text=[f"{100 * v:.1f}" for v in h[col]], textposition="outside",
                         customdata=np.stack([h.sbp_definition, h.pbs_classes_used], axis=1),
                         hovertemplate=f"{lab}: %{{y:.1f}}%<br>SBP: %{{customdata[0]}}<br>census: %{{customdata[1]}}<extra></extra>"))
fig.update_layout(barmode="group", height=420, margin=dict(l=10, r=10, t=10, b=40), plot_bgcolor=ui.SAND, paper_bgcolor=ui.SAND,
                  yaxis=dict(title="Percent of Punjab total", gridcolor="#e3d9c6", range=[0, 105]), legend=dict(orientation="h", y=1.08),
                  font=dict(family="Inter, sans-serif", color=ui.INK))
st.plotly_chart(fig, config={"displayModeBar": False}, key="hc_bars")
ui.vintage(h.vintage.iloc[0])
st.caption("Province level. Census classes (under 12.5 / 12.5 to under 50 / 50 and above) differ from SBP's (up to 12.5 / above 12.5 to "
           "50 / above 50) at the two boundary points. Operated (farm) area, not owned land. Larger holdings need larger loans.")

# ---------------------------------------------------------------- small-farm reach
st.subheader("Small-farm reach by district")
d = data.props("districts")
fl = d.flagged.astype(int) == 1
c = data.classes("small_farm_reach", "Fig 5")
kk = data.class_index(d.small_farm_reach, c["bins"])
tt = {r.adm2_pcode: {"District": r.adm2_name, "Small-farm reach": ui.num(r.small_farm_reach),
                     "SBP data-quality screen": "flagged" if r.flagged == 1 else "not flagged"} for r in d.itertuples()}
a, b = st.columns([3, 1.2], gap="large")
with a:
    m = maps.base()
    maps.layer(m, "districts", "adm2_pcode", {d.loc[i, "adm2_pcode"]: ui.INDIGO5[j] for i, j in kk.items() if j >= 0}, {},
               ["District", "Small-farm reach", "SBP data-quality screen"], tt, outline=set(d.loc[fl, "adm2_pcode"]))
    maps.show(m, key="alloc_reach")
    ui.vintage(d.vintage.iloc[0])
with b:
    ui.class_legend(c, d.small_farm_reach, ui.INDIGO5, "Subsistence-holding borrower records per 1,000 farms under 12.5 acres",
                    [("#fff", f"Flagged in SBP data-quality screen: outlined (n = {int(fl.sum())})", "outline")], fmt=ui.num)
    st.caption(f"Median {k('reach_median')}; Moran's I {k('moran_reach')}. Borrower records may not be unique people.")

# ---------------------------------------------------------------- crops
st.subheader("Crop structure")
crop = data.table("crop_structure_district")
sc = data.table("district_scorecard")[["adm2_pcode", "agc_district"]]
crop = crop.merge(sc, on="agc_district", how="left")
CROPS = ["wheat", "rice", "cotton", "maize", "sugarcane"]
sel = st.segmented_control("Crop", CROPS, default="wheat", key="alloc_crop", format_func=str.capitalize) or "wheat"
BANDS = [0.05, 0.15, 0.3, 0.45]                      # display bands for share of cropped area
LABS = ["< 5%", "5% – 15%", "15% – 30%", "30% – 45%", "45% and above"]
v = crop.set_index("adm2_pcode")[f"{sel}_share_of_cropped"]
kc = pd.Series(np.digitize(v.values, BANDS), index=v.index)
a, b = st.columns([3, 1.2], gap="large")
with a:
    m2 = maps.base()
    maps.layer(m2, "districts", "adm2_pcode", {p: ui.INDIGO5[j] for p, j in kc.items()}, {}, ["District", "Share of cropped area", "Top two crops"],
               {r.adm2_pcode: {"District": r.agc_district.replace(" DISTRICT", "").title(), "Share of cropped area": ui.pct(r[f"{sel}_share_of_cropped"]),
                               "Top two crops": r.top2_crops} for _, r in crop.iterrows()})
    maps.show(m2, key=f"alloc_crop_{sel}")
    ui.vintage(crop.vintage.iloc[0])
with b:
    ui.legend([(ui.INDIGO5[i], f"{l} (n = {int((kc == i).sum())})", "") for i, l in enumerate(LABS)], f"{sel.capitalize()}: share of cropped area",
              "Fixed display bands. Agricultural Census 2024, Tables 6.1 and 6.9–6.13; reference period Rabi 2023-24 + Kharif 2024.")
    st.caption(f"Wheat is the largest of the five crops in {k('top_crop_wheat')} districts and rice in {k('top_crop_rice')}.")

# ---------------------------------------------------------------- concentration curve
st.subheader("Concentration of borrower records over small farms")
CU, CO = data.table("concentration_curve"), data.table("concentration_coefficients")
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode="lines", name="Equal reach", line=dict(color="#8a8984", dash="dash", width=1.5), hoverinfo="skip"))
for s, colr in [("all matched districts", ui.INDIGO), ("excluding flagged districts", ui.OCHRE)]:
    dd = CU[CU["sample"] == s]
    cc = CO[CO["sample"] == s].iloc[0]
    fig2.add_trace(go.Scatter(x=[0] + dd.cum_small_farms.tolist(), y=[0] + dd.cum_sub_borrowers.tolist(), mode="lines+markers",
                              name=f"{s} (coefficient {cc.concentration_coefficient:.3f})", line=dict(color=colr, width=2),
                              marker=dict(size=6, color=colr), text=[""] + dd.adm2_name.tolist(),
                              hovertemplate="%{text}<br>small farms %{x:.1%}<br>borrower records %{y:.1%}<extra></extra>"))
fig2.update_layout(height=460, margin=dict(l=10, r=10, t=10, b=40), plot_bgcolor=ui.SAND, paper_bgcolor=ui.SAND,
                   legend=dict(orientation="h", y=-0.18), font=dict(family="Inter, sans-serif", color=ui.INK),
                   xaxis=dict(title="Cumulative share of farms under 12.5 acres (districts by reach, lowest first)", tickformat=".0%",
                              gridcolor="#e3d9c6", range=[0, 1.01]),
                   yaxis=dict(title="Cumulative share of subsistence-holding borrower records", tickformat=".0%", gridcolor="#e3d9c6", range=[0, 1.01]))
st.plotly_chart(fig2, config={"displayModeBar": False}, key="alloc_cc")
ui.vintage(CU.vintage.iloc[0])
st.caption(f"Concentration coefficient = {CO.definition.iloc[0]}. Small-farm reach is higher where tenant farms are a larger share of farms "
           f"(Spearman ρ = {k('rho_tenant')}, BH p {k('rho_tenant_pbh')}).")
