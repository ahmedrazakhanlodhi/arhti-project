import plotly.graph_objects as go
import streamlit as st

from lib import data, ui

ui.page("Cost", "Context: formal agricultural rates and published arhti estimates")
ui.narrative("Cost")
k = data.kn
pl = data.table("price_ladder")
pl = pl[pl.on_rate_axis.astype(str) == "True"]

COL = {"arhti (commission agent)": ui.OCHRE, "banks (farmer-reported)": "#8a8984"}
for col, panel, title in [(st.container(), "a", "Historical evidence, about 2012-13: arhti estimates vs SBP agricultural rates"),
                          (st.container(), "b", "Recent period, FY2023-24: SBP agricultural rates (Kissan Card shown separately: post-period)")]:
    g = pl[pl.panel == panel].reset_index(drop=True)
    fig = go.Figure()
    for _, r in g.iloc[::-1].iterrows():
        c = COL.get(r.institution, ui.INDIGO if "Kissan" not in r["item"] else "#1baf7a")
        hover = (f"<b>{r['item']}</b><br>{r.rate_low:g}" + (f"–{r.rate_high:g}" if r.rate_high > r.rate_low else "") +
                 f"% per annum<br>{r.date}<br>Basis: {r.basis}<br>Sample: {r['sample']}<br>Source: {r.source}")
        hover = "<br>".join(hover[i:i + 110] for i in range(0, len(hover), 110))
        if r.rate_high > r.rate_low:
            fig.add_trace(go.Scatter(x=[r.rate_low, r.rate_high], y=[r["item"]] * 2, mode="lines", line=dict(color=c, width=8),
                                     hovertemplate=hover + "<extra></extra>", showlegend=False))
        else:
            fig.add_trace(go.Scatter(x=[r.rate_low], y=[r["item"] + (" (from Oct 2024)" if "Kissan" in r["item"] else "")], mode="markers",
                                     marker=dict(size=12, color=c, line=dict(color="white", width=1.5)),
                                     hovertemplate=hover + "<extra></extra>", showlegend=False))
    ui.chart(fig, 130 + 36 * len(g), title=dict(text=title, font=dict(size=15)), xaxis=dict(title="Percent per annum", range=[-2, 90]))
    with col:
        st.plotly_chart(fig, config={"displayModeBar": False}, key=f"cost_{panel}")
        ui.vintage("IGC 2013 (interviews 2012); SBP Monthly Statistical Bulletin Table 3.33 (Sep 2026 edition), FY2012-13" if panel == "a"
                   else "SBP Monthly Statistical Bulletin Table 3.33 (Sep 2026 edition), FY2023-24; Kissan Card from 2024")
st.caption("Purposive small-sample arhti estimates (implicit annualized cost by crop) vs institutional averages (simple average at June "
           "quarter end); not matched contracts. Hover a point for its source, sample and caveats.")
with st.expander("All points with their sources"):
    st.dataframe(pl[["date", "item", "rate_low", "rate_high", "basis", "sample", "source"]], hide_index=True, width="stretch")
st.caption(f"Commercial banks' FY2023-24 averages: {k('rate_comm_prod_2023')}% for production loans and {k('rate_comm_deve_2023')}% for "
           "development loans (SBP Monthly Statistical Bulletin, Table 3.33).")

st.subheader("Kissan Card (post-period context)")
ui.narrative("Kissan Card")
st.caption("Not part of the FY2023-24 lending data. Source: Government of Punjab, Special Monitoring Unit, CM Punjab Kissan Card page.")
ui.footer()
