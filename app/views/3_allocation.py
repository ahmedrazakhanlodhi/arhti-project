import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from lib import data, maps, ui

ui.page("Allocation", "How formal lending is distributed in recorded data · SBP FY2023-24 and Agricultural Census 2024")
ui.narrative("Allocation")
k = data.kn
h = data.table("holding_class_shares")

# ---------------------------------------------------------------- holding classes, with a coverage toggle
st.subheader("Holding classes: farms vs borrower records and disbursement")
COV = {"36": "36 districts (primary)", "all": "SBP All Punjab row"}
cov = st.segmented_control("Coverage", list(COV), default="36", format_func=COV.get, key="alloc_cov") or "36"
show_area = st.toggle("Show operated farm area (indicative: see the census data-quality note)", value=False, key="alloc_area")
suf = "_36" if cov == "36" else ""
series = [("share_farms", "Share of farms", ui.INDIGO5[1])]
if show_area:
    series.append(("share_operated_area", "Share of operated farm area (indicative)", ui.INDIGO5[3]))
series += [("share_borrower_records", "Share of borrower records", ui.OCHRE5[1]), ("share_disbursement", "Share of disbursement", ui.OCHRE5[3])]
fig = go.Figure()
for col, lab, colr in series:
    v = h[col + suf]
    fig.add_trace(go.Bar(x=[c.replace("_", "-") for c in h.holding_class], y=100 * v, name=lab, marker_color=colr,
                         text=[f"{100 * x:.1f}" for x in v], textposition="outside",
                         customdata=np.stack([h.sbp_definition, h.pbs_classes_used], axis=1),
                         hovertemplate=f"{lab}: %{{y:.1f}}%<br>SBP: %{{customdata[0]}}<br>census: %{{customdata[1]}}<extra></extra>"))
ui.chart(fig, 420, barmode="group", yaxis=dict(title="Percent of total", range=[0, 108]))
st.plotly_chart(fig, config={"displayModeBar": False}, key=f"hc_bars_{cov}_{show_area}")
rc = data.table("sbp_coverage_reconciliation").set_index("scope")
row = rc.loc["36 districts (banks)" if cov == "36" else "SBP All Punjab row"]
st.caption(("36 district rows, banks only; Islamabad and the Punjab-wide MFI records (no district) excluded; census Punjab minus the "
            "Cholistan Area. " if cov == "36" else "SBP All Punjab row: banks in all district rows including Islamabad, plus MFIs; census "
            "Punjab including the Cholistan Area. ")
           + f"Totals: {int(row.tot_borrowers):,} borrower records, Rs {row.tot_amount_bn:,.1f} billion. Larger holdings need larger loans; "
           "proportionality is a benchmark, not an optimum.")
ui.vintage(("SBP, FY2023-24 (Jul 2023-Jun 2024), 36 district rows, district as reported by SBP (attribution under verification); "
            "Agricultural Census 2024 (PBS), sample-based, fieldwork 2024-25, Punjab minus Cholistan Area") if cov == "36" else h.vintage.iloc[0])

a, b = st.columns([1.3, 1], gap="large")
with a:
    st.markdown("**Disbursement per borrower record (36 districts)**")
    fig3 = go.Figure(go.Bar(x=h.disbursement_per_record_mn_36, y=[c.replace("_", "-") for c in h.holding_class], orientation="h",
                            marker_color=[ui.OCHRE5[1], ui.OCHRE5[2], ui.OCHRE5[4]],
                            text=[f"Rs {v:.2f} million" for v in h.disbursement_per_record_mn_36], textposition="outside",
                            hovertemplate="%{y}: Rs %{x:.2f} million per record<extra></extra>"))
    ui.chart(fig3, 230, xaxis=dict(title="Rs million per borrower record (log scale)", type="log", range=[-0.6, 2.75]),
             yaxis=dict(autorange="reversed"))
    fig3.update_layout(showlegend=False)
    st.plotly_chart(fig3, config={"displayModeBar": False}, key="alloc_per_record")
    st.caption(f"About {k('hc36_abv_ratio_sub')} times as much per above-economic record as per subsistence record. Records may count "
               "repeat transactions, so these are not average loan sizes.")
with b:
    st.markdown("**Representation ratio (class share ÷ farm share)**")
    rr = pd.DataFrame({"Holding class": [c.replace("_", "-") for c in h.holding_class],
                       "Borrower records": h.ratio_records_to_farms_36.round(2), "Disbursement": h.ratio_disbursement_to_farms_36.round(2)})
    st.dataframe(rr, hide_index=True, width="stretch")
    st.caption("1 = proportional to the number of farms. Above-economic holdings are over-represented even in the count of records.")
with st.expander("Agricultural Census data-quality note"):
    ac = data.table("agc_class_area_check")
    ac = ac[["size_class", "farms", "farm_area_ac", "implied_avg_farm_area_ac", "within_class_limits"]].copy()
    ac["farms"] = ac.farms.round().astype(int)
    ac["farm_area_ac"] = ac.farm_area_ac.round().astype(int)
    ac.columns = ["Size class (acres)", "Farms", "Farm area (acres)", "Implied average (acres)", "Within class limits"]
    st.dataframe(ac.round(2), hide_index=True, width="stretch")
    st.caption("In three classes below 12.5 acres the published farm area implies an average farm larger than the class limit. This is "
               "unexplained if the size classes and the farm area use the same land concept, so area shares are shown only as indicative "
               "and the analysis rests on farm counts.")

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
    st.caption(f"Median {k('reach_median')}; Moran's I {k('moran_reach')} (p = {k('moran_reach_p')}). Borrower records may not be unique "
               f"people. Dissimilarity between borrower records and small farms across districts: {k('D_sub_borrowers')} "
               f"({k('sv_ex_D')} without flagged districts).")

# ---------------------------------------------------------------- concentration curve
with st.expander("Concentration of borrower records over small farms (technical)"):
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
    ui.chart(fig2, 460, legend_y=-0.2,
             xaxis=dict(title="Cumulative share of farms under 12.5 acres (districts by reach, lowest first)", tickformat=".0%", range=[0, 1.01]),
             yaxis=dict(title="Cumulative share of subsistence-holding borrower records", tickformat=".0%", range=[0, 1.01]))
    st.plotly_chart(fig2, config={"displayModeBar": False}, key="alloc_cc")
    ui.vintage(CU.vintage.iloc[0])
    st.caption(f"Concentration coefficient = {CO.definition.iloc[0]}. It measures inequality in reach across districts, not between farmers. "
               f"Small-farm reach is higher where tenant farms are a larger share of farms (Spearman ρ = {k('rho_tenant')}, BH p "
               f"{k('rho_tenant_pbh')}); this describes districts, not tenants.")

# ---------------------------------------------------------------- crops (context)
with st.expander("Agricultural context: crop structure by district"):
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
ui.footer()
