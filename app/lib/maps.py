"""Folium map helpers. Units without a value are drawn hatched, never dropped."""

from __future__ import annotations

import copy

import folium
import streamlit as st
from folium.plugins import StripePattern
from streamlit_folium import st_folium

from lib import data, ui


@st.cache_data(show_spinner=False)
def bounds(name: str) -> list[list[float]]:
    xs, ys = [], []

    def walk(c):
        if isinstance(c[0], (int, float)):
            xs.append(c[0]); ys.append(c[1])
        else:
            for x in c:
                walk(x)
    for f in data.geo(name)["features"]:
        walk(f["geometry"]["coordinates"])
    return [[min(ys), min(xs)], [max(ys), max(xs)]]


def base() -> folium.Map:
    """No third-party tiles: neighbouring provinces from the OCHA layer form a muted background."""
    m = folium.Map(tiles=None, zoom_control=True, scrollWheelZoom=False, control_scale=True, zoom_snap=0.25, zoom_delta=0.5)
    m.get_root().header.add_child(folium.Element(f"<style>.leaflet-container{{background:{ui.SAND};}}</style>"))
    folium.GeoJson(data.geo("provinces"), interactive=False,
                   style_function=lambda f: {"fillColor": "#fbf8f2", "fillOpacity": 1, "color": "#d8ceba", "weight": 0.8}).add_to(m)
    return m


def layer(m, name, key, fills: dict, hatched: dict, tooltip: list[str], tt: dict, outline: set | None = None, opacity=0.92):
    """fills: key -> colour; hatched: key -> reason (no value / not in analysis); tt: key -> {alias: text}."""
    gj = copy.deepcopy(data.geo(name))
    stripes = StripePattern(angle=-45, weight=2, space=4, color="#b8ad99", opacity=0.9)
    stripes.add_to(m)
    outline = outline or set()
    for f in gj["features"]:
        p = f["properties"]; k = p.get(key)
        p["_fill"], p["_hatch"], p["_out"] = fills.get(k), k in hatched, k in outline
        for i, a in enumerate(tooltip):
            p[f"_t{i}"] = tt.get(k, {}).get(a, hatched.get(k, "—") if a == "Note" else "—")

    def style(f):
        p = f["properties"]
        if p["_hatch"]:
            return {"fillPattern": stripes, "fillOpacity": 1, "color": "#a69c88", "weight": 0.7}
        s = {"fillColor": p["_fill"] or "#efe9dd", "fillOpacity": opacity, "color": "#ffffff", "weight": 0.5}
        if p["_out"]:
            s.update(color=ui.INK, weight=2.4)
        return s
    folium.GeoJson(gj, style_function=style, highlight_function=lambda f: {"weight": 3, "color": ui.INK},
                   tooltip=folium.GeoJsonTooltip(fields=[f"_t{i}" for i in range(len(tooltip))], aliases=tooltip, sticky=True,
                                                 style="font-size:13px;")).add_to(m)
    folium.GeoJson(data.geo("punjab_outline"), interactive=False,
                   style_function=lambda f: {"fill": False, "color": "#7a7062", "weight": 1.1}).add_to(m)


def show(m, key: str) -> dict | None:
    """Render; return the clicked feature's properties (or None)."""
    (s, w), (n, e) = bounds("punjab_outline")
    out = st_folium(m, key=key, height=ui.map_height(), use_container_width=True, center=[(s + n) / 2, (w + e) / 2], zoom=6.5,
                    returned_objects=["last_active_drawing"])
    f = (out or {}).get("last_active_drawing")
    return (f or {}).get("properties") if f else None
