import plotly.graph_objects as go
import streamlit as st

from lib import data, ui

ui.page("Cost", "Context: formal agricultural rates and published arhti estimates")
ui.narrative("Cost")
k = data.kn
pl = data.table("price_ladder")
pl = pl[pl.on_rate_axis.astype(str) == "True"]

COL = {"arhti (commission agent)": ui.OCHRE, "banks (farmer-reported)": "#8a8984"}
for col, panel, title in [(st.container(), "a", "About 2012-13: arhti estimates vs SBP agricultural rates"),
                          (st.container(), "b", "FY2023-24: SBP agricultural rates, and the Kissan Card")]:
    g = pl[pl.panel == panel].reset_index(drop=True)
    fig = go.Figure()
    for _, r in g.iloc[::-1].iterrows():
        c = COL.get(r.institution, ui.INDIGO if "Kissan" not in r["item"] else "#1baf7a")
        hover = (f"<b>{r['item']}</b><br>{r.rate_low:g}" + (f"–{r.rate_high:g}" if r.rate_high > r.rate_low else "") +
                 f"% per annum<br>{r.date}<br>Basis: {r.basis}<br>Sample: {r['sample']}<br>Source: {r.source}<br>{r.note}")
        hover = "<br>".join(hover[i:i + 110] for i in range(0, len(hover), 110))
        if r.rate_high > r.rate_low:
            fig.add_trace(go.Scatter(x=[r.rate_low, r.rate_high], y=[r["item"]] * 2, mode="lines", line=dict(color=c, width=8),
                                     hovertemplate=hover + "<extra></extra>", showlegend=False))
        else:
            fig.add_trace(go.Scatter(x=[r.rate_low], y=[r["item"] + (" (from Oct 2024)" if "Kissan" in r["item"] else "")], mode="markers",
                                     marker=dict(size=12, color=c, line=dict(color="white", width=1.5)),
                                     hovertemplate=hover + "<extra></extra>", showlegend=False))
    fig.update_layout(height=120 + 34 * len(g), margin=dict(l=10, r=10, t=30, b=40), plot_bgcolor=ui.SAND, paper_bgcolor=ui.SAND,
                      title=dict(text=title, font=dict(size=14)), font=dict(family="Inter, sans-serif", color=ui.INK, size=11),
                      xaxis=dict(title="Percent per annum", range=[-2, 90], gridcolor="#e3d9c6"))
    with col:
        st.plotly_chart(fig, config={"displayModeBar": False}, key=f"cost_{panel}")
        ui.vintage("IGC 2013 (interviews 2012); SBP Monthly Statistical Bulletin Table 3.33 (Sep 2026 edition), FY2012-13" if panel == "a"
                   else "SBP Monthly Statistical Bulletin Table 3.33 (Sep 2026 edition), FY2023-24; Kissan Card from 2024")
st.caption("Purposive small-sample arhti estimates (implicit annualized cost by crop) vs institutional averages (simple average at June "
           "quarter end); not matched contracts. Hover a point for its source, sample and caveats.")
with st.expander("All points with sources (docs/price_ladder.csv)"):
    st.dataframe(pl[["date", "item", "rate_low", "rate_high", "basis", "sample", "source", "note"]], hide_index=True, width="stretch")

st.subheader("Not on the rate axis")
st.markdown(data.text("price_ladder_notes.md").split("\n", 2)[-1])
st.subheader("Kissan Card (post-period context)")
st.markdown(k("kissan_terms"))
