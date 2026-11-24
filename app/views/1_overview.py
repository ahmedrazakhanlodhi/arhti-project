import html

import streamlit as st

from lib import data, ui

ui.page("Where the Bank Ends and the Arhti Begins", "Indus Data Folio · agricultural credit in Punjab",
        subtitle="Mapping the overlapping geographies of agricultural finance", authors=True)
k = data.kn
st.markdown('<div class="scope">' + "".join(f"<span>{html.escape(x)}</span>" for x in [
    f"{k('rp_mouzas')} rural populated mouzas", f"{k('n_tehsils')} tehsils", f"{k('n_districts_q2')} districts",
    "Mouza Census 2020", "SBP FY2023-24", "Agricultural Census 2024"]) + "</div>", unsafe_allow_html=True)

q, c = data.narrative("Central question"), data.narrative("Main conclusion")
if c:
    st.markdown(f'<div class="lede">{html.escape(c)}</div>', unsafe_allow_html=True)
else:
    ui.narrative("Main conclusion")
st.write("")

CARDS = [  # value, title, sentence, arhti accent, key numbers whose vintage applies
    (k("all_any_overlap"), "Overlapping credit networks",
     f"of arhti-reporting villages also report a formal source (province-wide, {k('h1_any_share')} of villages report one).", True,
     ["all_any_overlap"]),
    (f"+{k('mb_w10_sem_pp')} pp", "The geography of grain markets",
     f"more arhti availability per one-SD rise in villages within 10 km of a grain market (spatial error model; adjusted p "
     f"{k('mb_w10_sem_holm')}).", True, ["mb_w10_sem_pp"]),
    (f"{k('hc36_subsistence_farms')} vs {k('hc36_subsistence_disbursement')}", "The smallholder disparity",
     "Subsistence holdings' share of farms versus their share of recorded disbursement (36 districts).", False,
     ["hc36_subsistence_farms"]),
    (f"{k('five_credit_share_abv')} vs {k('five_area_share')}", "The urban concentration",
     "Five city districts' share of above-economic disbursement versus their share of cultivated area (district as reported by SBP).", False,
     ["five_credit_share_abv"]),
    (k("all_any_neither_share"), "Limited reported availability",
     f"of rural populated mouzas ({k('all_any_neither')}) report neither arhti credit nor any examined formal source.", True,
     ["all_any_neither_share"]),
    (f"{k('hc36_abv_ratio_sub')}×", "The financing disparity",
     "Disbursement per above-economic borrower record relative to a subsistence record (not average loan size).", False,
     ["hc36_abv_ratio_sub"]),
]
for row in (CARDS[:3], CARDS[3:]):
    cols = st.columns(3, gap="medium")
    for col, (v, t, s, arhti, _) in zip(cols, row):
        with col:
            ui.finding(v, t, s, arhti)
st.caption("Descriptive, area-level findings. Ochre cards concern arhti (informal) credit; indigo cards concern formal lending.")
with st.expander("Where these numbers come from"):
    for v, t, s, _, ids in CARDS:
        st.markdown(f"**{t}** ({v})")
        ui.vintage(data.kn_row(ids[0]).vintage)

st.subheader("Explore")
LINKS = [("views/2_access.py", "Access", "Where arhti and formal credit are reported, clusters, markets, and villages with neither.", ":material/map:"),
         ("views/3_allocation.py", "Allocation", "How formal lending is distributed across holding classes and districts.", ":material/agriculture:"),
         ("views/4_reporting.py", "Reporting geography", "Where lending is recorded relative to farmland, with robustness checks.",
          ":material/account_balance:"),
         ("views/5_cost.py", "Cost", "Formal lending rates beside published arhti cost estimates.", ":material/payments:"),
         ("views/6_profiles.py", "District profiles", "Any district at a glance, or two or three side by side.", ":material/location_city:"),
         ("views/7_methods.py", "Data and methods", "Sources, concepts, verification status, reproducibility.", ":material/menu_book:")]
for row in (LINKS[:3], LINKS[3:]):
    cols = st.columns(3, gap="medium")
    for col, (path, label, desc, icon) in zip(cols, row):
        with col:
            st.page_link(path, label=label, icon=icon)
            st.caption(desc)

with st.expander("Introduction and conclusion", expanded=False):
    if q:
        st.markdown(f"**{q}**")
    ui.narrative("Introduction")
    ui.narrative("Conclusion")
ui.footer()
