import streamlit as st

from lib import data, ui

ui.page("Data and methods")

st.subheader("Sources and vintages")
src = data.sources()
st.dataframe(src[["Dataset", "Source", "Reference period", "Geographic level", "URL"]], hide_index=True, width="stretch",
             column_config={"URL": st.column_config.LinkColumn("Link")})
st.caption("From docs/data_inventory.md, plus SBP Monthly Statistical Bulletin Table 3.33 (September 2026 edition) for lending rates. "
           "The sources differ in date and geographic unit and are never treated as contemporaneous.")

st.subheader("Three ideas kept apart")
cols = st.columns(3, gap="medium")
for col, name in zip(cols, ["Presence", "Availability", "Allocation"]):
    with col:
        st.markdown(f"**{name.upper()}**")
        st.markdown(data.content("methods.md", name) or "")

st.subheader("Main limitations")
ui.narrative("Limitations")

st.subheader("Verification status")
hc = data.checklist()
vc = hc.status.value_counts()
c = st.columns(4)
for col, s in zip(c, ["verified", "does not match", "note", "pending"]):
    col.metric(s.capitalize(), int(vc.get(s, 0)))
st.caption("Read live from docs/human_checklist.md: values extracted from the printed sources, to be checked by hand.")
with st.expander("Checklist items"):
    st.dataframe(hc[["ID", "Area", "Item", "Our extracted value", "status"]], hide_index=True, width="stretch")

st.subheader("How the analysis was built")
st.markdown(data.content("methods.md", "How the analysis was built") or "")
st.markdown(data.content("methods.md", "Code") or "")
man = data.manifest()
st.caption(f"App data written {man['generated']} by {man['written_by']}; analysis CRS: {man['analysis_crs']}.")
