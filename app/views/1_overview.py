import html

import streamlit as st

from lib import data, ui

ui.page("Where the Bank Ends and the Arhti Begins", "Indus Data Folio · agricultural credit in Punjab")
q, c = data.narrative("Central question"), data.narrative("Main conclusion")
if q:
    st.markdown(f'<div class="lede"><b>{html.escape(q)}</b></div>', unsafe_allow_html=True)
st.write("")
if c:
    st.markdown(f'<div class="lede">{html.escape(c)}</div>', unsafe_allow_html=True)
else:
    ui.narrative("Main conclusion")
st.write("")
st.write("")

k = data.kn
cards = [
    (k("mh_or"), "ACCESS · odds ratio, arhti and bank credit in the same village",
     f"95% CI {k('mh_lo')}–{k('mh_hi')}; varies across tehsils (Breslow–Day p {k('bd_p')}).", "mh_or"),
    (f"{k('reach_min')}–{k('reach_max')}", "ALLOCATION · borrower records per 1,000 farms under 12.5 acres",
     f"Small-farm reach across {k('n_districts_q2')} districts.", "reach_min"),
    (f"{k('lahore_total_branches_10k')} vs {k('lahore_rural_branches_10k')}", "REPORTING GEOGRAPHY · Lahore: all vs rural branches per 10,000 farms",
     "All scheduled-bank branches vs branches coded rural; SBP branch list, 30 Jun 2024.", "lahore_total_branches_10k"),
    (f"{k('rate_comm_prod_2023')}%", "COST · commercial-bank agricultural rate, FY2023-24",
     f"Published arhti estimates (IGC 2013, by crop): {k('lit_igc_rates')}. Not matched contracts.", "rate_comm_prod_2023"),
]
cols = st.columns(4, gap="medium")
for col, (v, t, s, kid) in zip(cols, cards):
    with col:
        ui.callout(v, t, s)
        ui.vintage(data.kn_row(kid).vintage)

st.write("")
with st.expander("Introduction and conclusion", expanded=False):
    ui.narrative("Introduction")
    ui.narrative("Conclusion")
