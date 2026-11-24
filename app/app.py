"""Where the Bank Ends and the Arhti Begins: companion app (PPHA 38520).

    streamlit run app/app.py          (from the project root; add ?present=1 for presentation mode)

The app only displays finished outputs (app/data/, copied from outputs/ by scripts/18_export_web.py).
"""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent))

if "present" not in st.session_state:
    st.session_state.present = st.query_params.get("present") == "1"

st.set_page_config(page_title="Where the Bank Ends and the Arhti Begins", page_icon="🌾", layout="wide",
                   initial_sidebar_state="collapsed" if st.session_state.present else "expanded")

V = Path(__file__).resolve().parent / "views"
pages = [
    st.Page(V / "1_overview.py", title="Overview", icon=":material/home:", default=True),
    st.Page(V / "2_access.py", title="Access", icon=":material/map:", url_path="access"),
    st.Page(V / "3_allocation.py", title="Allocation", icon=":material/agriculture:", url_path="allocation"),
    st.Page(V / "4_reporting.py", title="Reporting geography", icon=":material/account_balance:", url_path="reporting"),
    st.Page(V / "5_cost.py", title="Cost", icon=":material/payments:", url_path="cost"),
    st.Page(V / "6_profiles.py", title="District profiles", icon=":material/location_city:", url_path="profiles"),
    st.Page(V / "7_methods.py", title="Data and methods", icon=":material/menu_book:", url_path="methods"),
]
with st.sidebar:
    st.toggle("Presentation mode", key="present", help="Larger type, navigation at the top, no menus. URL: ?present=1")
    if st.session_state.present:
        st.query_params["present"] = "1"
    elif "present" in st.query_params:
        del st.query_params["present"]
st.navigation(pages, position="top" if st.session_state.present else "sidebar").run()
