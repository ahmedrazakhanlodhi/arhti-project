"""Presentation mode: a guided seven-screen story. Numbers come from key numbers; images are the paper's figures (app/data)."""
import html

import streamlit as st

from lib import data, ui

ui.page("Where the Bank Ends and the Arhti Begins", "Indus Data Folio · presentation")
k = data.kn
STEPS = [
    ("Research questions", f"{k('rp_mouzas')} villages", "Where are arhti and formal credit available, and whom does formal lending reach?",
     "Does arhti credit fill the gaps left by formal credit (H1)? Does formal credit reach small farms in proportion (H2)? Is lending "
     "recorded where farmland is (H3)?", "story_1_arhti.png", "Figure 2. Reported arhti credit availability by tehsil, Mouza Census 2020."),
    ("Clusters", f"Moran's I {k('moran_arhti_queen')}", "Informal credit is geographically clustered.",
     f"{k('lisa_hh_p05')} High-High and {k('lisa_ll_p05')} Low-Low tehsils (p < 0.05); the pattern holds across weighting choices.",
     "story_2_clusters.png", "Figure 4. LISA clusters, Queen weights, 999 permutations; heavy border = survives FDR 0.05."),
    ("Market access", f"+{k('mb_w10_sem_pp')} pp", "The arhti follows the market.",
     f"Arhti availability per one-SD rise in villages within 10 km of a grain market (spatial error model; Holm-adjusted p "
     f"{k('mb_w10_sem_holm')}). Cropland's link does not survive spatial modelling.", "story_3_markets.png",
     "Figure 7. A: villages within 10 km of a grain market. B: villages reporting neither source. Exploratory."),
    ("Overlap", k("all_any_overlap"), "Banks and arhtis overlap.",
     f"of arhti-reporting villages also report a formal source. Within tehsils the odds are higher where commercial ({k('h1_com_or')}), "
     f"cooperative ({k('h1_coop_or')}) or microfinance ({k('h1_mfb_or')}) credit is reported.", "story_4_overlap.png",
     "Figure 3. Arhti and commercial-bank availability, terciles."),
    ("Allocation", f"{k('hc36_subsistence_farms')} vs {k('hc36_subsistence_disbursement')}", "Small holdings get a small share of the money.",
     f"Subsistence holdings' share of farms vs recorded disbursement (36 districts). Per borrower record, above-economic holdings receive "
     f"about {k('hc36_abv_ratio_sub')} times as much.", "story_5_holdings.png", "Figure A1. Holding classes, SBP FY2023-24 and Agricultural Census 2024."),
    ("Reporting geography", f"{k('five_credit_share_abv')} vs {k('five_area_share')}", "Recorded lending concentrates in city districts.",
     f"Five city districts' share of above-economic disbursement vs cultivated area ({ui.ATTRIBUTION}). Robust to leaving out any one city.",
     "story_6_cities.png", "Figure R2. Five city districts' shares of lending, farmland, farms and branches."),
    ("Where policy could look", f"{k('all_any_neither')} villages", "Where might financial policy intervene?",
     f"{k('all_any_neither_share')} of villages report neither arhti nor formal credit. Branch expansion alone may be insufficient; "
     "market-linked products and better location reporting are candidate directions.", "story_7_neither.png",
     "Figure S13. Share of villages reporting neither source (limited reported availability, not exclusion)."),
]
n = len(STEPS)
i = int(st.session_state.get("story_step", 0))
i = max(0, min(n - 1, i))
kick, big, head, sub, img, cap = STEPS[i]
c1, c2 = st.columns([1, 1.45], gap="large")
with c1:
    st.markdown(f'<div class="story-k">{i + 1:02d} of {n:02d} · {html.escape(kick)}</div><div class="story-n">{html.escape(big)}</div>'
                f'<div class="story-h">{html.escape(head)}</div><div class="story-s">{html.escape(sub)}</div>'
                f'<div class="story-c">Descriptive, area-level findings. Sources differ in date and unit.</div>', unsafe_allow_html=True)
    st.write("")
    b1, b2, b3 = st.columns([1, 1, 2])
    if b1.button("← Back", disabled=i == 0, key="story_back"):
        st.session_state.story_step = i - 1; st.rerun()
    if b2.button("Next →", disabled=i == n - 1, key="story_next", type="primary"):
        st.session_state.story_step = i + 1; st.rerun()
    st.progress((i + 1) / n)
with c2:
    st.image(str(data.DATA / img), caption=cap, width="stretch")
ui.footer()
