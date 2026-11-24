import pandas as pd
import streamlit as st

from lib import data, maps, ui

ui.page("District profiles", "One district at a time · descriptive scorecard")
ui.narrative("District profiles")
sc = data.table("district_scorecard").sort_values("adm2_name")
name = st.selectbox("District", sc.adm2_name.tolist(), key="prof_district")
r = sc[sc.adm2_name == name].iloc[0]

a, b = st.columns([1.6, 1], gap="large")
with a:
    st.markdown(f"### {name}")
    st.markdown(f"**Profile:** {r.profile_type}")
    pct, num = ui.pct, ui.num
    ui.card("Farms and crops", [("Farms", num(round(r.farms))), ("Cultivated area (acres)", num(round(r.cultivated_ac))),
                                ("Farms under 12.5 acres", pct(r.smallholder_share)), ("Tenant farms", pct(r.tenant_share)),
                                ("Top two of five crops by area", r.top2_crops)])
    st.write("")
    ui.card("ACCESS (Mouza Census 2020)", [("Arhti credit reported", pct(r.arhti_share)), ("Commercial-bank credit reported", pct(r.commercial_share)),
                                           ("ZTBL credit reported", pct(r.ztbl_share)),
                                           ("Tehsils in High-High / Low-Low arhti clusters (p < 0.05)", f"{int(r.tehsils_hh_p05)} / {int(r.tehsils_ll_p05)}"),
                                           ("… after FDR 0.05", f"{int(r.tehsils_hh_fdr05)} / {int(r.tehsils_ll_fdr05)}")])
    st.write("")
    ui.card("ALLOCATION and PRESENCE", [("Small-farm reach (per 1,000 farms under 12.5 acres)", num(r.small_farm_reach)),
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
