"""12_qgis_project.py: build outputs/arhti_project.qgz (all final layers, styled) + outputs/qgis_styles/*.qml.

Runs with QGIS's own Python (PyQGIS), not the project .venv. run_all.sh sets the environment automatically when QGIS is
installed; manually:  source scripts/qgis_env.sh && "$QGIS_PY" scripts/12_qgis_project.py
Print layouts are NOT built (the group builds them; docs/qgis_steps.md). Styles mirror outputs/figures/ (09_figures.py).
"""

import csv
import sys
from pathlib import Path

from qgis.core import (QgsApplication, QgsCategorizedSymbolRenderer, QgsCentroidFillSymbolLayer, QgsCoordinateReferenceSystem,
                       QgsFillSymbol, QgsGraduatedSymbolRenderer, QgsLayerTreeGroup, QgsLinePatternFillSymbolLayer,
                       QgsMarkerSymbol, QgsPalLayerSettings, QgsProject, QgsRendererCategory, QgsRendererRange,
                       QgsSimpleFillSymbolLayer, QgsSimpleMarkerSymbolLayer, QgsVectorLayer, QgsVectorLayerSimpleLabeling,
                       QgsTextFormat, QgsSimpleMarkerSymbolLayerBase)
from qgis.PyQt.QtGui import QColor

ROOT = Path(__file__).resolve().parents[1]
GPKG = ROOT / "outputs" / "arhti_project.gpkg"
QGZ = ROOT / "outputs" / "arhti_project.qgz"
STY = ROOT / "outputs" / "qgis_styles"
CRS_PROJ = "+proj=aea +lat_1=28 +lat_2=33 +lat_0=30 +lon_0=72 +datum=WGS84 +units=m +no_defs"
BLUE5 = ["#86b6ef", "#5598e7", "#2a78d6", "#1c5cab", "#0d366b"]
ORANGE5 = ["#f29a72", "#eb6834", "#c9531f", "#9a3d14", "#6b280b"]
NEUTRAL, MISSING, INK = "#f0efec", "#e2e1dc", "#1f1f1f"
BIV = [["#e8e8e8", "#ace4e4", "#5ac8c8"], ["#dfb0d6", "#a5add3", "#5698b9"], ["#be64ac", "#8c62aa", "#3b4994"]]
LISA_C = {"High-High": "#e34948", "Low-Low": "#2a78d6", "High-Low": "#f2a7a6", "Low-High": "#9ec5f4", "not significant": NEUTRAL}


def fill(color, outline="#ffffff", width=0.1):
    return QgsFillSymbol.createSimple({"color": color, "outline_color": outline, "outline_width": str(width), "outline_width_unit": "MM"})


def hatched(base=MISSING):
    s = fill(base, "#8a8984", 0.1)
    lp = QgsLinePatternFillSymbolLayer()
    lp.setLineAngle(45); lp.setDistance(1.2); lp.setColor(QColor("#8a8984")); lp.setLineWidth(0.2)
    s.appendSymbolLayer(lp)
    return s


def outline_only(width=0.6, dashed=False):
    s = QgsFillSymbol.createSimple({"color": "0,0,0,0", "outline_color": INK, "outline_width": str(width),
                                    "outline_width_unit": "MM", "outline_style": "dash" if dashed else "solid"})
    return s


def layer(name, table, subset=None):
    lyr = QgsVectorLayer(f"{GPKG}|layername={table}", name, "ogr")
    if not lyr.isValid():
        sys.exit(f"invalid layer {table}")
    if subset:
        lyr.setSubsetString(subset)
    return lyr


def categorized(lyr, field, mapping):
    cats = [QgsRendererCategory(v, fill(c, "#ffffff", 0.1), v) for v, c in mapping.items()]
    lyr.setRenderer(QgsCategorizedSymbolRenderer(field, cats))


def graduated(lyr, field, breaks, colors, fmt="{:.2f}", lo=0.0):
    rng, prev = [], lo
    for b, c in zip(breaks, colors):
        rng.append(QgsRendererRange(prev, b, fill(c, "#ffffff", 0.1), f"{fmt.format(prev)} – {fmt.format(b)}"))
        prev = b
    lyr.setRenderer(QgsGraduatedSymbolRenderer(field, rng))


def labels(lyr, expr, size=7):
    p = QgsPalLayerSettings()
    p.fieldName, p.isExpression = expr, True
    f = QgsTextFormat(); f.setSize(size); f.setColor(QColor(INK)); p.setFormat(f)
    lyr.setLabeling(QgsVectorLayerSimpleLabeling(p)); lyr.setLabelsEnabled(True)


def breaks_from_table(figure):
    with open(ROOT / "outputs" / "tables" / "classification_comparison.csv") as fh:
        for r in csv.DictReader(fh):
            if r["figure"] == figure and r["chosen"] == "True":
                return [float(b) for b in r["bins"].split(";")]
    sys.exit(f"no chosen breaks for {figure}")


def main():
    QgsApplication.setPrefixPath(str(Path(sys.executable).parent), True)
    app = QgsApplication([], False); app.initQgis()
    STY.mkdir(parents=True, exist_ok=True)
    prj = QgsProject.instance(); prj.clear()
    prj.setCrs(QgsCoordinateReferenceSystem.fromProj(CRS_PROJ))
    prj.setTitle("Where the Bank Ends and the Arhti Begins (PPHA 38520)")
    root = prj.layerTreeRoot()
    T, D = "q1_tehsils_mouza_census_2020", "q2_districts_credit_allocation"
    built = []

    def add(group, lyr, visible=True):
        prj.addMapLayer(lyr, False)
        node = group.addLayer(lyr)
        node.setItemVisibilityChecked(visible)
        safe = "".join(ch if ch.isalnum() else "_" for ch in lyr.name()).strip("_")
        lyr.saveNamedStyle(str(STY / f"{safe}.qml"))
        built.append(lyr.name())
        return lyr

    def ict(group):
        l = layer("Islamabad (excluded)", "context_islamabad_ict_excluded")
        s = fill("#ffffff", INK, 0.3)
        l.setRenderer(l.renderer().clone()); l.renderer().setSymbol(s)
        add(group, l)

    groups = {}
    for gname in ["Figure 1 – coverage", "Figure 2 – arhti availability (tehsil)", "Figure 3 – bivariate availability",
                  "Figure 4 – LISA (tehsil, Q1)", "Figure 5 – allocation vs availability / presence", "Figure S2 – LISA (district, MAUP)",
                  "Figure S3 – published-study locations (CONTEXT only)", "Figure S4 – mouza-level co-occurrence (EXPLORATORY)", "Context"]:
        groups[gname] = root.addGroup(gname)

    # Figure 1
    g = groups["Figure 1 – coverage"]
    l = layer("F1A tehsil match type", T)
    categorized(l, "coverage_class", {"Exact or rule-normalized": "#2a78d6", "Spelling or rename (reviewed by Ahmed)": "#eb6834",
                                      "Parent aggregation (several census units summed)": "#1baf7a", "No rural populated mouzas": NEUTRAL})
    add(g, l)
    l = layer("F1B district coverage", D)
    categorized(l, "coverage_class", {"Matched": "#2a78d6", "Matched, flagged (SBP screen)": "#eb6834"})
    labels(l, "CASE WHEN \"flagged\" = 1 THEN \"adm2_name\" END")
    add(g, l, False)
    ict(g)
    # Figure 2
    g = groups["Figure 2 – arhti availability (tehsil)"]
    add(g, (lambda x: (x.renderer().setSymbol(outline_only(0.4, True)), x)[1])(
        layer("F2 includes Cholistan desert mouzas", T, '"contains_cholistan" = 1')))
    l = layer("F2 no rural populated mouzas", T, '"rp_mouzas" = 0 OR "rp_mouzas" IS NULL'); l.renderer().setSymbol(fill("#ffffff", "#8a8984", 0.15)); add(g, l)
    l = layer("F2 arhti_share (natural breaks)", T); graduated(l, "arhti_share", breaks_from_table("Fig 2"), BLUE5); add(g, l)
    l = layer("F2 side panel: rural populated mouzas", T, '"rp_mouzas" > 0')
    graduated(l, "rp_mouzas", breaks_from_table("Fig 2 side panel"), ORANGE5, "{:,.0f}", 1); add(g, l, False)
    # Figure 3
    g = groups["Figure 3 – bivariate availability"]
    l = layer("F3 bivariate arhti x commercial", T)
    categorized(l, "bivariate_class", {f"A{a + 1}-C{c + 1}": BIV[a][c] for a in range(3) for c in range(3)})
    add(g, l, False)
    # Figure 4
    g = groups["Figure 4 – LISA (tehsil, Q1)"]
    l = layer("F4 FDR(0.05) survivors (heavy border)", T, "\"lisa_queen_fdr05\" IS NOT NULL AND \"lisa_queen_fdr05\" <> 'not significant'")
    l.renderer().setSymbol(outline_only(0.7)); add(g, l, False)
    l = layer("F4 LISA arhti_share (Queen, p<0.05)", T); categorized(l, "lisa_queen_p05", LISA_C); add(g, l, False)
    # Figure 5
    g = groups["Figure 5 – allocation vs availability / presence"]
    l = layer("F5 flagged in SBP screen", D, '"flagged" = 1')
    s = QgsFillSymbol(); s.deleteSymbolLayer(0)
    cf = QgsCentroidFillSymbolLayer()
    m = QgsMarkerSymbol.createSimple({"name": "triangle", "color": "#ffffff", "outline_color": INK, "size": "2.6"})
    cf.setSubSymbol(m); s.appendSymbolLayer(cf); l.renderer().setSymbol(s); add(g, l, False)
    l = layer("F5A small_farm_reach (quantiles)", D)
    graduated(l, "small_farm_reach", breaks_from_table("Fig 5"), BLUE5, "{:,.0f}", 0); add(g, l, False)
    for nm, fld in [("F5B availability-based class", "class_availability"), ("F5C presence-based class", "class_presence")]:
        l = layer(nm, D)
        vals = sorted({f[fld] for f in l.getFeatures()})
        categorized(l, fld, {v: ("#eb6834" if v.startswith("High") else ("#ffffff" if v == "Not classified" else NEUTRAL)) for v in vals})
        labels(l, f"CASE WHEN \"{fld}\" LIKE 'High%' THEN \"adm2_name\" END")
        add(g, l, False)
    ict(g)
    # Figure S2
    g = groups["Figure S2 – LISA (district, MAUP)"]
    l = layer("S2 FDR(0.05) survivors", D, "\"lisa_queen_fdr05\" IS NOT NULL AND \"lisa_queen_fdr05\" <> 'not significant'")
    l.renderer().setSymbol(outline_only(0.8)); add(g, l, False)
    l = layer("S2 LISA arhti_share district (Queen, p<0.05)", D); categorized(l, "lisa_queen_p05", LISA_C); add(g, l, False)
    # Figure S3: CONTEXT only (published-study towns; never data for statistics or choropleths)
    g = groups["Figure S3 – published-study locations (CONTEXT only)"]
    l = layer("S3 published-study locations (CONTEXT; approximate town centres)", "literature_evidence")
    cats = []
    for v, shape, col in [("grain market", "circle", INK), ("focus group", "square", "#eb6834")]:
        m = QgsMarkerSymbol.createSimple({"name": shape, "color": col, "outline_color": "#ffffff", "size": "2.4"})
        cats.append(QgsRendererCategory(v, m, {"grain market": "IGC 2013 market location", "focus group": "PMN/MEDA 2019 focus-group location"}[v]))
    l.setRenderer(QgsCategorizedSymbolRenderer("location_type", cats))
    labels(l, "\"location\" || '\\n' || CASE WHEN \"location_type\" = 'grain market' THEN 'IGC 2013: ' || "
              "coalesce(nullif(\"crops\", ''), 'crop not stated') ELSE 'PMN/MEDA 2019: focus group' END", 6)
    add(g, l, False)
    l = layer("S3 base map: arhti_share (natural breaks)", T); graduated(l, "arhti_share", breaks_from_table("Fig 2"), BLUE5); add(g, l, False)
    # Figure S4
    g = groups["Figure S4 – mouza-level co-occurrence (EXPLORATORY)"]
    l = layer("S4 observed/expected co-occurrence, arhti x commercial", T)
    s4 = {"< 0.80": "#2a78d6", "0.80–0.95": "#9ec5f4", "0.95–1.053 (≈ independence)": NEUTRAL, "1.053–1.25": "#f2a7a6", "> 1.25": "#e34948"}
    cats = [QgsRendererCategory(v, fill(c, "#ffffff", 0.1), v) for v, c in s4.items()]
    cats.append(QgsRendererCategory("not estimable", hatched(), "not estimable"))
    l.setRenderer(QgsCategorizedSymbolRenderer("cooc_ratio_class", cats)); add(g, l, False)
    # Context
    g = groups["Context"]
    l = layer("Pakistan provinces (inset)", "context_pakistan_provinces"); l.renderer().setSymbol(fill("#d9d8d3", "#ffffff", 0.2)); add(g, l, False)
    l = layer("Punjab outline", "context_punjab_outline"); l.renderer().setSymbol(outline_only(0.4)); add(g, l)
    for gname, node in groups.items():
        node.setItemVisibilityChecked(gname in ("Figure 2 – arhti availability (tehsil)", "Context"))
    prj.writeEntry("Paths", "/Absolute", False)
    ok = prj.write(str(QGZ))
    print(f"project written: {ok} -> {QGZ}; layers: {len(built)}; styles: {len(list(STY.glob('*.qml')))}")
    app.exitQgis()
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
