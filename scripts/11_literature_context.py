"""11_literature_context.py: published evidence on the cost of arhti credit as CONTEXT (never data for statistics/choropleths).

    .venv/bin/python -I scripts/11_literature_context.py      (after 10_export_qgis.py)

Input: docs/literature_evidence.csv (values supplied by Ahmed; not looked up or inferred).
Geocoding (D033): OpenStreetMap Nominatim search API, one query per town ("<town>, Punjab, Pakistan", countrycodes=pk),
<= 1 request/second, project User-Agent. Raw responses are cached in data/raw/geocoding/ and reused, so reruns do not query again.
Selection rule (does NOT use the expected district, so the district check is a real check): among results with class
'place' and type city/town/village, take the highest Nominatim importance; otherwise the highest-importance result.
Outputs: data/processed/literature_evidence.gpkg; layer `literature_evidence` appended to outputs/arhti_project.gpkg;
outputs/tables/literature_locations_context.csv (descriptive: tehsil, district, Q1 LISA labels; no statistics);
outputs/figures/figS3_literature_locations.{png,pdf}.
"""

from __future__ import annotations

import datetime as dt
import importlib.util
import json
import sqlite3
import sys
import time
import warnings
from pathlib import Path

import geopandas as gpd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import pyogrio
import requests
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[1]


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / file)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod


common = _load("common", "common.py")
figs = _load("figs", "09_figures.py")
exp = _load("exp", "10_export_qgis.py")

CSV = ROOT / "docs" / "literature_evidence.csv"
CACHE = ROOT / "data" / "raw" / "geocoding" / "nominatim_literature_locations.json"
OUT_GPKG = ROOT / "data" / "processed" / "literature_evidence.gpkg"
PROJ_GPKG = ROOT / "outputs" / "arhti_project.gpkg"
TABLE = ROOT / "outputs" / "tables" / "literature_locations_context.csv"
URL = "https://nominatim.openstreetmap.org/search"
UA = {"User-Agent": "arhti-project-ppha38520/1.0 (UChicago Harris coursework; low-volume, cached)"}
CAPTION = ("Locations of published studies on the cost of arhti credit. Rates come from small, non-representative samples, are "
           "reported by crop (IGC) or from focus groups (PMN/MEDA), and are not district or tehsil estimates. Points are approximate "
           "town centres.")
ALIASES = {"study": "Study (CONTEXT only)", "year": "Publication year", "location": "Study location (town)",
           "district": "District as given in the literature table (OCHA name)", "location_type": "Grain market / focus group",
           "crops": "Crops at this location (as given)", "metric": "Metric reported by the study", "value": "Value(s) as published",
           "basis": "Basis of the metric", "sample": "Study sample", "page": "Page(s)", "url": "Source URL",
           "verified_by_ahmed": "Verified by Ahmed", "note": "Note", "location_precision": "Location precision",
           "geocode_source": "Geocoding source", "osm_display_name": "OSM display name", "ocha_tehsil": "OCHA tehsil (spatial join)",
           "ocha_district": "OCHA district (spatial join)", "district_check": "District matches literature table"}


def geocode(towns):
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    new = [t for t in towns if t not in cache]
    for t in new:
        r = requests.get(URL, params=dict(q=f"{t}, Punjab, Pakistan", countrycodes="pk", format="jsonv2", addressdetails=1, limit=10),
                         headers=UA, timeout=30)
        r.raise_for_status()
        cache[t] = dict(query=f"{t}, Punjab, Pakistan", retrieved=dt.date.today().isoformat(), results=r.json())
        time.sleep(1.2)
    if new:
        CACHE.parent.mkdir(parents=True, exist_ok=True)
        CACHE.write_text(json.dumps(cache, indent=1, ensure_ascii=False))
    out = {}
    for t in towns:
        res = cache[t]["results"]
        places = [x for x in res if x.get("category", x.get("class")) == "place" and x.get("type") in ("city", "town", "village")]
        pool = places or res
        if not pool:
            out[t] = None
            continue
        best = max(pool, key=lambda x: float(x.get("importance") or 0))
        out[t] = dict(lat=float(best["lat"]), lon=float(best["lon"]), osm=f"{best.get('osm_type')}/{best.get('osm_id')}",
                      type=f"{best.get('category', best.get('class'))}/{best.get('type')}", name=best.get("display_name"),
                      n_results=len(res), n_place=len(places), retrieved=cache[t]["retrieved"])
    return out


def main() -> int:
    lit = pd.read_csv(CSV, dtype=str).fillna("")
    geo = geocode(list(dict.fromkeys(lit.location)))
    missing = [t for t, g in geo.items() if g is None]
    if missing:
        sys.exit(f"Could not geocode: {missing}. Stop and ask Ahmed (rule 1).")
    lit["lon"] = lit.location.map(lambda t: geo[t]["lon"]); lit["lat"] = lit.location.map(lambda t: geo[t]["lat"])
    lit["location_precision"] = "town centre, approximate"
    lit["geocode_source"] = lit.location.map(lambda t: f"OSM Nominatim {geo[t]['osm']} ({geo[t]['type']}), retrieved {geo[t]['retrieved']}")
    lit["osm_display_name"] = lit.location.map(lambda t: geo[t]["name"])
    pts = gpd.GeoDataFrame(lit, geometry=gpd.points_from_xy(lit.lon, lit.lat), crs=4326).to_crs(common.CRS)

    teh = gpd.read_file(ROOT / "data" / "processed" / "punjab_credit_context.gpkg", layer="tehsil").to_crs(common.CRS)
    j = gpd.sjoin(pts, teh[["adm3_pcode", "adm3_name", "adm2_name", "geometry"]], how="left", predicate="within")
    pts["ocha_tehsil"], pts["ocha_district"], pts["adm3_pcode"] = j.adm3_name.values, j.adm2_name.values, j.adm3_pcode.values
    pts["district_check"] = (pts.ocha_district == pts.district).map({True: "match", False: "MISMATCH"})

    # descriptive cluster context (current Q1 unit = tehsil, scenario A)
    L = pd.read_csv(ROOT / "outputs" / "tables" / "lisa_arhti.csv")
    L = L[(L.level == "tehsil") & (L.scenario == "A") & (L.analysis == "LISA arhti_share")]
    ctx = pts[["study", "year", "location", "location_type", "crops", "district", "ocha_tehsil", "adm3_pcode", "ocha_district",
               "district_check", "lon", "lat", "location_precision"]].copy()
    for wn, tag in [("Queen", "queen"), ("kNN-5 (geodesic)", "knn5")]:
        q = L[L.weights == wn].set_index("pcode")
        ctx[f"lisa_{tag}_bh_cutoff"] = q.fdr_cutoff.iloc[0]
        for col in ["cluster_p05", "cluster_p01", "cluster_fdr05"]:
            ctx[f"lisa_{tag}_{col.replace('cluster_', '')}"] = ctx.adm3_pcode.map(q[col])
    arhti = dict(zip(teh.adm3_pcode, teh.arhti_share))
    ctx["tehsil_arhti_share_MouzaCensus2020"] = ctx.adm3_pcode.map(arhti)
    ctx = ctx.assign(note="CONTEXT only: descriptive placement of published-study towns; no statistics on these points. "
                          "Study values are not tehsil or district estimates.",
                     vintage="Studies: IGC 2013 (interviews 2012), PMN/MEDA 2019 (2018); LISA: Mouza Census 2020, Queen and geodesic "
                             "kNN-5, 999 permutations, seed 20261031")
    ctx.to_csv(TABLE, index=False)

    out = pts.drop(columns=["lon", "lat"])
    OUT_GPKG.unlink(missing_ok=True)
    out.to_file(OUT_GPKG, layer="literature_evidence", driver="GPKG")
    if PROJ_GPKG.exists():
        con = sqlite3.connect(PROJ_GPKG)
        con.execute("DELETE FROM gpkg_data_columns WHERE table_name = 'literature_evidence'"); con.commit(); con.close()
        pyogrio.write_dataframe(out, PROJ_GPKG, layer="literature_evidence", driver="GPKG", layer_options={"OVERWRITE": "YES"})
        exp.OUT = PROJ_GPKG
        exp.write_aliases({"literature_evidence": {k: v for k, v in ALIASES.items() if k in out.columns}})

    figure(pts, teh)
    print(ctx[["study", "location", "district", "ocha_tehsil", "ocha_district", "district_check", "lon", "lat",
               "lisa_queen_p05", "lisa_queen_fdr05", "lisa_knn5_p05"]].to_string(index=False))
    for t, g in geo.items():
        print(f"{t}: {g['osm']} {g['type']} | {g['n_place']} place results of {g['n_results']} | {g['name']}")
    return 0


def figure(pts, teh):
    ok = teh[teh.rp_mouzas > 0]
    c, _, _ = common.choose_scheme(ok.arhti_share)
    fig = plt.figure(figsize=(9.5, 9.6))
    a = fig.add_axes([0.0, 0.24, 1.0, 0.64])
    figs.choropleth(a, ok, "arhti_share", c, figs.BLUE5)
    teh[teh.rp_mouzas.fillna(0) == 0].plot(ax=a, facecolor="white", edgecolor="#8a8984", linewidth=0.4)
    dh = figs.desert_outline(a, teh)
    for lt, mk, col in [("grain market", "o", "#1f1f1f"), ("focus group", "s", "#eb6834")]:
        s = pts[pts.location_type == lt]
        a.scatter(s.geometry.x, s.geometry.y, marker=mk, s=42, facecolor=col, edgecolor="white", linewidth=1.1, zorder=6)
    # label offsets (points) chosen only to avoid overlaps; leader lines connect each label to its point
    OFF = {"Okara": (14, 26), "Depalpur": (26, -18), "Sahiwal": (-95, 22), "Chichawatni": (-110, -14), "Khanewal": (-105, -10),
           "Nankana Sahib": (12, 6), "Jalalpur Bhattian": (-115, 8), "Sialkot": (8, 6), "Bahawalpur": (10, 6), "Khanpur": (10, -4)}
    for _, r in pts.iterrows():
        lab = (f"IGC 2013: {r.crops or 'crop not stated'}" if r.location_type == "grain market" else "PMN/MEDA 2019: focus group")
        a.annotate(f"{r.location}\n{lab}", (r.geometry.x, r.geometry.y), xytext=OFF.get(r.location, (6, 4)), textcoords="offset points",
                   fontsize=6.2, color="#1f1f1f", zorder=7, arrowprops=dict(arrowstyle="-", color="#5c5b57", lw=0.5),
                   bbox=dict(boxstyle="round,pad=0.15", facecolor="white", edgecolor="none", alpha=0.85))
    figs.frame(a, teh); figs.furniture(a, teh)
    h = [Patch(facecolor=col, edgecolor="none", label=l) for col, l in zip(figs.BLUE5, figs.class_labels(c, "{:.2f}", ok.arhti_share.min()))]
    h += [Line2D([], [], marker="o", ls="", markerfacecolor="#1f1f1f", markeredgecolor="white", label="IGC 2013 market location (8)"),
          Line2D([], [], marker="s", ls="", markerfacecolor="#eb6834", markeredgecolor="white", label="PMN/MEDA 2019 focus-group location (2)"),
          Patch(facecolor="white", edgecolor="#8a8984", label="No rural populated mouzas"), dh]
    figs.legend(a, h, "AVAILABILITY: share of rural mouzas reporting arhti credit (Mouza Census 2020; tehsil; natural breaks)", ncol=2)
    a.set_title("CONTEXT: published studies on the cost of arhti credit, over reported arhti availability", loc="left", fontsize=9.5)
    fig.suptitle("Figure S3. Locations of published studies on the cost of arhti credit", x=0.01, y=0.995, ha="left", fontsize=11,
                 fontweight="bold")
    lines = [CAPTION, "Study rates are NOT shown, coloured, interpolated or aggregated to any polygon. Studies: Haq, Aslam et al. 2013 "
             "(IGC/NIBAF/PMN; interviews 2012); PMN/MEDA 2019 (FGDs 2018). Geocoding: OSM Nominatim town centres (D033).",
             f"Map: {figs.V_MC}. {figs.V_B}. Vintages differ (2012, 2018, 2020) and are not contemporaneous. {figs.DESERT_NOTE}",
             f"CRS: {common.CRS_LABEL}; north arrow = true north. {figs.AUTHOR}. Generated {dt.date.today()} by scripts/11_literature_context.py."]
    fig.text(0.01, 0.0, "\n".join(lines), fontsize=6.2, color=figs.MUTED, va="bottom", ha="left")
    figs.save(fig, "figS3_literature_locations")


if __name__ == "__main__":
    sys.exit(main())
