"""Shared UI pieces: palette, callouts, legends, cards. No statistics are computed here."""

from __future__ import annotations

import html

import numpy as np
import pandas as pd
import streamlit as st

from lib import data

# ---------------------------------------------------------------- palette
SAND, SAND2, INK, MUTED = "#f6f1e7", "#ece4d3", "#2b2722", "#6f675c"
INDIGO = "#3c3f9c"
INDIGO5 = ["#dcdcf0", "#b0b2de", "#8084c6", "#5157a6", "#2c2f72"]          # sequential, one hue, light -> dark
OCHRE = "#b07a2a"
OCHRE5 = ["#f3e6cc", "#e6c891", "#d1a456", "#ad7d32", "#7a5420"]           # arhti emphasis (restrained ochre)
LQ_BREAKS = [0.25, 0.5, 0.8, 1.25, 2, 4]                                     # same fixed log-symmetric breaks as Figure R1
LQ_COLS = ["#7a5f38", "#b39a72", "#ddd0b6", "#efe9dd", "#b0b2de", "#5157a6", "#262a73"]
LQ_LABS = ["< 0.25", "0.25 – 0.5", "0.5 – 0.8", "0.8 – 1.25 (≈ proportional)", "1.25 – 2", "2 – 4", "> 4"]
ATTRIBUTION = "district as reported by SBP (attribution under verification)"
LISA_C = {"High-High": "#e34948", "High-Low": "#f2a7a6", "Low-Low": "#2a78d6", "Low-High": "#9ec5f4", "not significant": "#efe9dd"}
BIV = [["#e8e8e8", "#ace4e4", "#5ac8c8"], ["#dfb0d6", "#a5add3", "#5698b9"], ["#be64ac", "#8c62aa", "#3b4994"]]   # paper Figure 3
NOTE = "Descriptive results. Sources differ in date and geographic unit."
AUTHORS = "Ahmed Raza Khan Lodhi and Hasnain Akram · PPHA 38520, University of Chicago"
TITLE_FONT = "Literata, Georgia, serif"


def presenting() -> bool:
    return bool(st.session_state.get("present", False))


def map_height() -> int:
    return 620 if presenting() else 540


def pct(v) -> str:
    return "—" if v is None or pd.isna(v) else f"{100 * float(v):.1f}%"


def num(v, digits=1) -> str:
    if v is None or pd.isna(v):
        return "—"
    return f"{int(v):,}" if float(v).is_integer() else f"{float(v):,.{digits}f}"


CSS = f"""
<style>
.block-container {{padding-top: 2.2rem; padding-bottom: 3rem; max-width: 1240px;}}
h1, h2, h3 {{letter-spacing: -0.01em;}}
.lede {{font-size: 1.18rem; line-height: 1.55; color: {INK}; max-width: 54rem;}}
.note {{display:inline-block; font-size:.86rem; color:{MUTED}; border:1px solid #ddd3c0; background:#fbf8f2;
        border-radius: 999px; padding: .2rem .8rem; margin: .2rem 0 1.2rem 0;}}
.callout {{background:#fffdf9; border:1px solid #e3d9c6; border-radius: 14px; padding: 1.1rem 1.2rem; height: 100%;}}
.callout .k {{font-family: Literata, Georgia, serif; font-size: 2.1rem; font-weight: 600; color: {INDIGO}; line-height: 1.1;}}
.callout .t {{font-size: .98rem; color: {INK}; margin-top: .35rem; font-weight: 600;}}
.callout .s {{font-size: .84rem; color: {MUTED}; margin-top: .35rem; line-height: 1.4;}}
.vintage {{font-size: .78rem; color: {MUTED}; margin: .3rem 0 .8rem 0;}}
.lg {{font-size: .88rem; line-height: 1.4;}}
.lg-title {{font-weight: 600; margin-bottom: .4rem;}}
.lg-row {{display:flex; align-items:center; gap:.55rem; margin:.2rem 0;}}
.sw {{display:inline-block; width:18px; height:14px; border:1px solid #c9bfae; border-radius:3px; flex: 0 0 auto;}}
.sw.hatch {{background-image: repeating-linear-gradient(45deg,#c9bfae 0 2px,#ffffff 2px 5px) !important;}}
.sw.outline {{border: 2.5px solid {INK}; background: transparent !important;}}
.lg-note {{font-size:.78rem; color:{MUTED}; margin-top:.5rem;}}
.card {{background:#fffdf9; border:1px solid #e3d9c6; border-radius:12px; padding:.8rem .95rem;}}
.card .h {{font-family: Literata, Georgia, serif; font-weight:600; font-size:1.08rem; margin-bottom:.35rem;}}
.card table {{width:100%; font-size:.88rem; border-collapse:collapse;}}
.card th {{text-align:left; font-weight:500; color:{MUTED}; padding:2px 8px 2px 0; vertical-align:top;}}
.card td {{text-align:right; padding:2px 0; white-space:nowrap;}}
.placeholder {{border:2px dashed #b8a98f; color:#6b5b45; border-radius:10px; padding:.7rem .9rem; margin:.4rem 0 1rem 0;}}
.biv {{display:grid; grid-template-columns: repeat(3, 46px); gap: 3px;}}
.biv div {{height:46px; border-radius:4px; display:flex; align-items:center; justify-content:center; font-size:.85rem;}}
</style>
"""

PRESENT_CSS = """
<style>
[data-testid="stDecoration"], [data-testid="stMainMenu"], #MainMenu, footer, [data-testid="stAppDeployButton"],
[data-testid="stStatusWidget"] {display:none !important;}
.block-container {max-width: 100%; padding-top: 3.2rem;}
.stMarkdown p, .stMarkdown li, .lede {font-size: 1.2rem !important;}
.callout .k {font-size: 2.6rem;} .lg {font-size: 1.02rem;} .card table {font-size: 1rem;}
</style>
"""


def page(title: str, kicker: str = ""):
    st.markdown(CSS, unsafe_allow_html=True)
    if presenting():
        st.markdown(PRESENT_CSS, unsafe_allow_html=True)
    if kicker:
        st.caption(kicker.upper())
    st.title(title)
    st.markdown(f'<span class="note">{NOTE}</span>', unsafe_allow_html=True)
    st.caption(AUTHORS)


def vintage(text: str):
    """Show a vintage line. Older outputs say "booking district"; until SBP's attribution is confirmed (D039) the app shows the
    neutral wording instead."""
    if text:
        text = (text.replace("loans by booking district", "district as reported by SBP").replace("(booking district)", "(district as reported by SBP)")
                .replace("recorded by loan-booking district", "district as reported by SBP"))
        st.markdown(f'<div class="vintage">Data vintage · {html.escape(text)}</div>', unsafe_allow_html=True)


def narrative(section: str):
    t = data.narrative(section)
    if t is None:
        st.markdown(f'<div class="placeholder"><b>{data.PLACEHOLDER}</b> (app/content/narrative.md → “{html.escape(section)}”)</div>',
                    unsafe_allow_html=True)
    else:
        st.markdown(t)


def callout(value: str, title: str, sub: str = ""):
    st.markdown(f'<div class="callout"><div class="k">{html.escape(value)}</div><div class="t">{html.escape(title)}</div>'
                f'<div class="s">{html.escape(sub)}</div></div>', unsafe_allow_html=True)


def legend(items: list[tuple[str, str, str]], title: str, note: str = ""):
    rows = "".join(f'<div class="lg-row"><span class="sw {cls}" style="background:{fill}"></span>{html.escape(lab)}</div>'
                   for fill, lab, cls in items)
    n = f'<div class="lg-note">{html.escape(note)}</div>' if note else ""
    st.markdown(f'<div class="lg"><div class="lg-title">{html.escape(title)}</div>{rows}{n}</div>', unsafe_allow_html=True)


def class_legend(c: dict, values: pd.Series, ramp: list[str], title: str, extra=None, fmt=pct):
    k = data.class_index(values, c["bins"])
    lo = [float(np.nanmin(pd.to_numeric(values, errors="coerce")))] + c["bins"][:-1]
    items = [(col, f"{fmt(a)} – {fmt(b)}  (n = {int((k == i).sum())})", "") for i, (col, a, b) in enumerate(zip(ramp, lo, c["bins"]))]
    sch = "natural breaks (Fisher-Jenks)" if c["scheme"] == "Fisher-Jenks" else "quantiles"
    legend(items + (extra or []), title, f"Five classes, {sch}, as in the paper.")


def card(title: str, rows: list[tuple[str, str]]):
    body = "".join(f"<tr><th>{html.escape(a)}</th><td>{html.escape(str(b))}</td></tr>" for a, b in rows)
    st.markdown(f'<div class="card"><div class="h">{html.escape(title)}</div><table>{body}</table></div>', unsafe_allow_html=True)
