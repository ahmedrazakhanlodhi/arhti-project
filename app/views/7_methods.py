import html

import streamlit as st

from lib import data, ui

ui.page("Data and methods", "Sources, concepts, verification and reproducibility")

st.subheader("Sources and vintages")
src = data.sources()
st.dataframe(src[["Dataset", "Source", "Reference period", "Geographic level", "URL"]], hide_index=True, width="stretch",
             column_config={"URL": st.column_config.LinkColumn("Link")})
st.caption("From docs/data_inventory.md, plus SBP Monthly Statistical Bulletin Table 3.33 (September 2026 edition) for lending rates. "
           "The sources differ in date and geographic unit and are never treated as contemporaneous.")

st.subheader("Three ideas kept apart")
st.caption("They measure different things and are never used interchangeably.")
cols = st.columns(3, gap="medium")
for col, (name, src_) in zip(cols, [("Presence", "SBP branch list; Mouza Census distances"), ("Availability", "Mouza Census 2020"),
                                     ("Allocation", "SBP lending records, FY2023-24")]):
    with col:
        st.markdown(f'<div class="finding{" arhti" if name == "Availability" else ""}" style="min-height:230px"><div class="t">{name}</div>'
                    f'<div class="s">{html.escape(data.content("methods.md", name) or "")}</div>'
                    f'<div class="s" style="color:{ui.MUTED};margin-top:auto">Data: {src_}</div></div>', unsafe_allow_html=True)

st.subheader("Main limitations")
ui.narrative("Limitations")

st.subheader("Verification status")
st.markdown(data.content("methods.md", "Verification") or "")
hc = data.checklist()
vc = hc.status.value_counts()
c = st.columns(4)
for col, s in zip(c, ["verified", "does not match", "note", "pending"]):
    col.metric(s.capitalize(), int(vc.get(s, 0)))
st.caption("Manual audit, read live from the project's checklist: values extracted from the printed sources, to be checked by hand. "
           "Pending means the hand check has not been recorded yet, not that the value failed.")
with st.expander("Checklist items"):
    st.dataframe(hc[["ID", "Area", "Item", "Our extracted value", "status"]], hide_index=True, width="stretch")

st.subheader("How the analysis was built")
st.markdown(data.content("methods.md", "How the analysis was built") or "")
st.markdown(data.content("methods.md", "Code") or "")
man = data.manifest()
st.caption(f"App data written {man['generated']} by {man['written_by']}; analysis CRS: {man['analysis_crs']}.")
ui.footer()
