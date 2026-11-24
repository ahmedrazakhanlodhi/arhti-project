"""16_qgis_layouts.py: QGIS Print Layouts for the paper's maps (Figures 2-6), exported as PNG (300 dpi) and PDF.

Runs with QGIS's own Python (PyQGIS), after 12_qgis_project.py and 15_course_methods.py. run_all.sh sets the environment when
QGIS is installed; manually:  source scripts/qgis_env.sh && cd /tmp && "$QGIS_PY" -s "<project>/scripts/16_qgis_layouts.py"

Opens outputs/arhti_project.qgz (written by 12), adds the Figure 6 layers (dasymetric dots of small farms; proportional circles
of SBP subsistence-holding borrower records, Flannery-compensated) and the exploratory Gi* / typology layers (15), builds one
Print Layout per figure and saves the project with its layouts. Every layout has: title, subtitle, main map with neatline,
Pakistan inset with the main-map extent (figure-ground), legend with feature counts, scale bar (km), true-north arrow,
data sources with vintage, CRS, and authors. Outputs: outputs/figures/fig{2..6}_*_qgis.{png,pdf}.
In the QGIS GUI the same layouts are under Project > Layout Manager; docs/qgis_steps.md lists the menu path for each element.
"""

import csv
import os
import re
import sys
from pathlib import Path

from qgis.core import (Qgis, QgsApplication, QgsCategorizedSymbolRenderer, QgsFillSymbol,
                       QgsLayerTreeLayer, QgsLayoutExporter, QgsLayoutItemLabel, QgsLayoutItemLegend, QgsLayoutItemMap,
                       QgsLayoutItemMapOverview, QgsLayoutItemPicture, QgsLayoutItemScaleBar, QgsLayoutItemShape, QgsLayoutPoint,
                       QgsLayoutSize, QgsLegendStyle, QgsMarkerSymbol, QgsPrintLayout, QgsProject, QgsProperty, QgsRectangle,
                       QgsRendererCategory, QgsSingleSymbolRenderer, QgsSizeScaleTransformer, QgsSymbolLayer, QgsTextFormat,
                       QgsVectorLayer, QgsCoordinateTransform, QgsRenderContext, QgsGraduatedSymbolRenderer, QgsRendererRange)
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QColor, QFont

ROOT = Path(__file__).resolve().parents[1]
GPKG = ROOT / "outputs" / "arhti_project.gpkg"
QGZ = ROOT / "outputs" / "arhti_project.qgz"
FIG = ROOT / "outputs" / "figures"
STY = ROOT / "outputs" / "qgis_styles"
MM = Qgis.LayoutUnit.Millimeters
INK, MUTED, NEUTRAL = "#1f1f1f", "#5c5b57", "#f0efec"
BIV = [["#e8e8e8", "#ace4e4", "#5ac8c8"], ["#dfb0d6", "#a5add3", "#5698b9"], ["#be64ac", "#8c62aa", "#3b4994"]]
AUTHOR = "Ahmed Raza Khan Lodhi and Hasnain Akram, PPHA 38520, University of Chicago"
CRS_LABEL = "Albers equal-area centred on Punjab (lat_1 28, lat_2 33, lat_0 30, lon_0 72; WGS84)"
V_MC = "Mouza Census 2020 (PBS), fieldwork Jan–Mar 2020; availability as reported by village respondents, not household borrowing"
V_SBP = "SBP, FY2023-24 (Jul 2023–Jun 2024), district as reported by SBP (attribution under verification)"
V_AGC = "Agricultural Census 2024 (PBS), sample-based, fieldwork 2024–25"
V_WC = "ESA WorldCover 2021 v200 (cropland)"
V_B = "Boundaries: OCHA COD-AB Pakistan, valid_on 2022-09-09"
PAGE_W, PAGE_H = 170.0, 206.0          # mm; fits a US Letter / A4 text block at full width
MAP = (5.0, 26.0, 112.0, 150.0)        # x, y, w, h of the main map (mm)
RIGHT_X = 120.0


def svg_north():
    base = Path(os.environ.get("PYTHONHOME", "")) / "qgis" / "svg" / "arrows" / "NorthArrow_02.svg"
    if base.exists():
        return str(base)
    for p in QgsApplication.svgPaths():
        c = Path(p) / "arrows" / "NorthArrow_02.svg"
        if c.exists():
            return str(c)
    sys.exit("north arrow SVG not found")


def tfmt(size, bold=False, color=INK):
    f = QgsTextFormat()
    font = QFont("Helvetica"); font.setBold(bold)
    f.setFont(font); f.setSize(size); f.setSizeUnit(Qgis.RenderUnit.Points); f.setColor(QColor(color))
    return f


def with_counts(layer):
    """Append (n = k) to every legend class of the layer's renderer (QGIS cannot count features in a headless run)."""
    r = layer.renderer()
    ctx = QgsRenderContext(); r.startRender(ctx, layer.fields())
    keys = {}
    for f in layer.getFeatures():
        for k in r.legendKeysForFeature(f, ctx):
            keys[k] = keys.get(k, 0) + 1
    r.stopRender(ctx)
    items = r.legendSymbolItems()
    strip = lambda t: re.sub(r" \(n = \d+\)$", "", t or "")
    if hasattr(r, "ranges"):
        for i, it in enumerate(items):
            r.updateRangeLabel(i, f"{strip(r.ranges()[i].label())} (n = {keys.get(it.ruleKey(), 0)})")
    elif hasattr(r, "categories"):
        for i, it in enumerate(items):
            r.updateCategoryLabel(i, f"{strip(r.categories()[i].label())} (n = {keys.get(it.ruleKey(), 0)})")
    return sum(keys.values())


def n_of(layer):
    return sum(1 for _ in layer.getFeatures())


def label(layout, text, x, y, w, h, size=7.0, bold=False, color=INK):
    it = QgsLayoutItemLabel(layout)
    it.setText(text); it.setTextFormat(tfmt(size, bold, color))
    it.attemptMove(QgsLayoutPoint(x, y, MM)); it.attemptResize(QgsLayoutSize(w, h, MM))
    it.setVAlign(Qt.AlignmentFlag.AlignTop)
    layout.addLayoutItem(it)
    return it


def lyr(prj, name):
    found = prj.mapLayersByName(name)
    if not found:
        sys.exit(f"layer not in project: {name}")
    return found[0]


def add_gpkg(prj, group, name, table, subset=None):
    l = QgsVectorLayer(f"{GPKG}|layername={table}", name, "ogr")
    if not l.isValid():
        sys.exit(f"invalid layer {table}")
    if subset:
        l.setSubsetString(subset)
    prj.addMapLayer(l, False)
    node = group.addLayer(l); node.setItemVisibilityChecked(False)
    return l


def punjab_extent(prj, pad=0.03):
    o = lyr(prj, "Punjab outline")
    tr = QgsCoordinateTransform(o.crs(), prj.crs(), prj)
    r = tr.transformBoundingBox(o.extent())
    r.grow(max(r.width(), r.height()) * pad)
    return r


def page(prj, name, title, subtitle):
    lm = prj.layoutManager()
    old = lm.layoutByName(name)
    if old:
        lm.removeLayout(old)
    lay = QgsPrintLayout(prj); lay.initializeDefaults(); lay.setName(name)
    lay.pageCollection().page(0).setPageSize(QgsLayoutSize(PAGE_W, PAGE_H, MM))
    lm.addLayout(lay)
    label(lay, title, 5, 5, PAGE_W - 10, 9, 11.5, True)
    label(lay, subtitle, 5, 14.5, PAGE_W - 10, 10, 8.2, False, MUTED)
    return lay


def main_map(lay, prj, layers, rect=None):
    m = QgsLayoutItemMap(lay)
    m.attemptMove(QgsLayoutPoint(MAP[0], MAP[1], MM)); m.attemptResize(QgsLayoutSize(MAP[2], MAP[3], MM))
    m.setCrs(prj.crs()); m.setLayers(layers); m.setKeepLayerSet(True)
    m.zoomToExtent(rect or punjab_extent(prj))
    m.setFrameEnabled(True); m.setFrameStrokeColor(QColor(INK)); m.setFrameStrokeWidth(QgsLayoutMeasurementMM(0.3))
    m.setBackgroundColor(QColor("#ffffff"))
    lay.addLayoutItem(m)
    return m


def QgsLayoutMeasurementMM(v):
    from qgis.core import QgsLayoutMeasurement
    return QgsLayoutMeasurement(v, MM)


def inset(lay, prj, main):
    m = QgsLayoutItemMap(lay)
    m.attemptMove(QgsLayoutPoint(MAP[0] + 2, MAP[1] + 2, MM)); m.attemptResize(QgsLayoutSize(30, 33, MM))
    m.setCrs(prj.crs())
    prov, outl = lyr(prj, "Pakistan provinces (inset)"), lyr(prj, "Punjab outline")
    m.setLayers([outl, prov]); m.setKeepLayerSet(True)
    tr = QgsCoordinateTransform(prov.crs(), prj.crs(), prj)
    r = tr.transformBoundingBox(prov.extent()); r.grow(r.width() * 0.04)
    m.zoomToExtent(r)
    m.setFrameEnabled(True); m.setFrameStrokeColor(QColor(MUTED)); m.setFrameStrokeWidth(QgsLayoutMeasurementMM(0.2))
    ov = QgsLayoutItemMapOverview("Main map extent", m)
    ov.setLinkedMap(main)
    ov.setFrameSymbol(QgsFillSymbol.createSimple({"color": "0,0,0,0", "outline_color": "#c62f2e", "outline_width": "0.4"}))
    m.overviews().addOverview(ov)
    lay.addLayoutItem(m)
    label(lay, "Pakistan (Punjab outlined;\nred box = map extent)", MAP[0] + 2, MAP[1] + 35.5, 40, 7, 5.6, False, MUTED)
    return m


def furniture(lay, main):
    sb = QgsLayoutItemScaleBar(lay)
    sb.setStyle("Single Box"); sb.setLinkedMap(main); sb.applyDefaultSize()
    sb.setUnits(Qgis.DistanceUnit.Kilometers); sb.setUnitLabel("km")
    sb.setSegmentSizeMode(Qgis.ScaleBarSegmentSizeMode.Fixed); sb.setUnitsPerSegment(50); sb.setNumberOfSegments(2)
    sb.setNumberOfSegmentsLeft(0); sb.setHeight(1.6); sb.setTextFormat(tfmt(6.5))
    sb.attemptMove(QgsLayoutPoint(MAP[0] + MAP[2] - 44, MAP[1] + MAP[3] - 11, MM))
    lay.addLayoutItem(sb)
    na = QgsLayoutItemPicture(lay)
    na.setPicturePath(svg_north()); na.setLinkedMap(main); na.setNorthMode(QgsLayoutItemPicture.NorthMode.TrueNorth)
    na.attemptMove(QgsLayoutPoint(MAP[0] + MAP[2] - 13, MAP[1] + MAP[3] - 30, MM)); na.attemptResize(QgsLayoutSize(8, 14, MM))
    lay.addLayoutItem(na)


def legend(lay, main, entries, title, y=MAP[1], h=None, counts=True):
    lg = QgsLayoutItemLegend(lay)
    lg.setTitle(title); lg.setLinkedMap(main)
    lg.setSyncMode(Qgis.LegendSyncMode.Manual)
    root = lg.model().rootGroup(); root.clear()
    for layer, name in entries:
        n = root.addLayer(layer)
        n.setUseLayerName(False); n.setName(name)
        n.setCustomProperty("showFeatureCount", False)
    for comp, size, bold in [(QgsLegendStyle.Style.Title, 8.0, True), (QgsLegendStyle.Style.Group, 7.2, True),
                             (QgsLegendStyle.Style.Subgroup, 7.0, True), (QgsLegendStyle.Style.SymbolLabel, 6.8, False)]:
        st = lg.style(comp); st.setTextFormat(tfmt(size, bold)); lg.setStyle(comp, st)
    lg.setSymbolWidth(5); lg.setSymbolHeight(3.5); lg.setWrapString("|")
    lg.attemptMove(QgsLayoutPoint(RIGHT_X, y, MM))
    lay.addLayoutItem(lg)
    lg.adjustBoxSize()
    return lg


def footer(lay, lines):
    txt = "\n".join(lines + [f"CRS: {CRS_LABEL}; north arrow = true north. {V_B}.",
                             f"{AUTHOR}. Map: QGIS {Qgis.version().split('-')[0]} Print Layout (scripts/16_qgis_layouts.py)."])
    label(lay, txt, 5, MAP[1] + MAP[3] + 4, PAGE_W - 10, PAGE_H - (MAP[1] + MAP[3] + 6), 6.3, False, MUTED)


def export(lay, stem):
    ex = QgsLayoutExporter(lay)
    s = QgsLayoutExporter.ImageExportSettings(); s.dpi = 300
    r1 = ex.exportToImage(str(FIG / f"{stem}_qgis.png"), s)
    p = QgsLayoutExporter.PdfExportSettings(); p.rasterizeWholeImage = False
    r2 = ex.exportToPdf(str(FIG / f"{stem}_qgis.pdf"), p)
    ok = r1 == QgsLayoutExporter.ExportResult.Success and r2 == QgsLayoutExporter.ExportResult.Success
    print(f"{stem}_qgis: {'ok' if ok else f'FAILED {r1} {r2}'}")
    return ok


def fig6_layers(prj, group):
    base = add_gpkg(prj, group, "F6 districts (outline)", "q2_districts_credit_allocation")
    base.setRenderer(QgsSingleSymbolRenderer(QgsFillSymbol.createSimple(
        {"color": "#f6f4ee", "outline_color": "#b9b6ad", "outline_width": "0.15"})))
    dots = add_gpkg(prj, group, "F6 small farms (1 dot = 1,000 farms under 12.5 acres, on cropland)", "course_dasymetric_small_farm_dots")
    dots.setRenderer(QgsSingleSymbolRenderer(QgsMarkerSymbol.createSimple(
        {"name": "circle", "color": "29,92,171,150", "outline_style": "no", "size": "0.45", "size_unit": "MM"})))
    circ = add_gpkg(prj, group, "F6 SBP subsistence-holding borrower records", "course_district_borrower_points")
    vals = [f["sub_borrowers"] for f in circ.getFeatures() if f["sub_borrowers"] is not None]
    vmax = max(vals)
    sym = QgsMarkerSymbol.createSimple({"name": "circle", "color": "235,104,52,110", "outline_color": "#9a3d14",
                                        "outline_width": "0.25", "size_unit": "MM"})
    t = QgsSizeScaleTransformer(QgsSizeScaleTransformer.ScaleType.Flannery, 0, vmax, 0, 16, 0, 0.57)
    prop = QgsProperty.fromField("sub_borrowers"); prop.setTransformer(t)
    sym.setDataDefinedSize(prop)
    r = QgsSingleSymbolRenderer(sym)
    circ.setRenderer(r)
    for l in (base, dots, circ):
        safe = "".join(ch if ch.isalnum() else "_" for ch in l.name()).strip("_")[:80]
        l.saveNamedStyle(str(STY / f"{safe}.qml"))
    return base, dots, circ, vmax


def course_layers(prj, group):
    gi = add_gpkg(prj, group, "S8 Getis-Ord Gi* (p<0.05)", "course_tehsils_gistar_trend")
    cols = {"Hot spot": "#c62f2e", "Cold spot": "#1c5cab", "not significant": NEUTRAL}
    gi.setRenderer(QgsCategorizedSymbolRenderer("gistar_p05", [QgsRendererCategory(
        v, QgsFillSymbol.createSimple({"color": c, "outline_color": "#ffffff", "outline_width": "0.1"}), v) for v, c in cols.items()]))
    ty = add_gpkg(prj, group, "S10 k-means typology (attributes)", "course_districts_typology")
    pal = ["#2a78d6", "#eb6834", "#1baf7a", "#8c62aa", "#c9a227", "#6b6a66"]
    ty.setRenderer(QgsCategorizedSymbolRenderer("type_attr", [QgsRendererCategory(
        i + 1, QgsFillSymbol.createSimple({"color": c, "outline_color": "#ffffff", "outline_width": "0.15"}), f"Type {i + 1}")
        for i, c in enumerate(pal)]))
    for l in (gi, ty):
        safe = "".join(ch if ch.isalnum() else "_" for ch in l.name()).strip("_")[:80]
        l.saveNamedStyle(str(STY / f"{safe}.qml"))


def count(layer_name, prj, expr=None):
    l = lyr(prj, layer_name)
    return sum(1 for _ in l.getFeatures()) if not expr else sum(1 for f in l.getFeatures() if expr(f))


def biv_key(lay, x, y, cell=6.0, counts=None):
    for a in range(3):
        for c in range(3):
            s = QgsLayoutItemShape(lay); s.setShapeType(QgsLayoutItemShape.Shape.Rectangle)
            s.setSymbol(QgsFillSymbol.createSimple({"color": BIV[a][c], "outline_color": "#ffffff", "outline_width": "0.2"}))
            s.attemptMove(QgsLayoutPoint(x + 8 + c * cell, y + (2 - a) * cell, MM)); s.attemptResize(QgsLayoutSize(cell, cell, MM))
            lay.addLayoutItem(s)
            if counts is not None:
                n = counts.get(f"A{a + 1}-C{c + 1}", 0)
                t = label(lay, str(n), x + 8 + c * cell, y + (2 - a) * cell + 1.6, cell, 3.5, 6.0, True, "#ffffff" if a + c >= 3 else INK)
                t.setHAlign(Qt.AlignmentFlag.AlignHCenter)
    label(lay, "Arhti credit →\n(thirds)", x - 1, y + 4, 9, 12, 5.8)
    label(lay, "Commercial-bank credit → (thirds)", x + 7, y + 3 * cell + 1, 40, 4, 5.8)
    label(lay, "Both low = bottom left; both high = top right.\nNumbers = tehsils in each cell.", x + 7, y + 3 * cell + 5, 48, 8, 5.6, False, MUTED)


def main():
    QgsApplication.setPrefixPath(str(Path(sys.executable).parent), True)
    app = QgsApplication([], False); app.initQgis()
    prj = QgsProject.instance()
    if not prj.read(str(QGZ)):
        sys.exit(f"cannot read {QGZ}; run 12_qgis_project.py first")
    root = prj.layerTreeRoot()
    for gname in ["Figure 6 – small farms and borrower records (dasymetric)", "Course methods (EXPLORATORY): Gi*, typology"]:
        old = root.findGroup(gname)
        if old:
            for l in [n.layer() for n in old.findLayers()]:
                prj.removeMapLayer(l)
            root.removeChildNode(old)
    g6 = root.addGroup("Figure 6 – small farms and borrower records (dasymetric)"); g6.setItemVisibilityChecked(False)
    gc = root.addGroup("Course methods (EXPLORATORY): Gi*, typology"); gc.setItemVisibilityChecked(False)
    base6, dots6, circ6, vmax = fig6_layers(prj, g6)
    course_layers(prj, gc)
    outline, ict = lyr(prj, "Punjab outline"), lyr(prj, "Islamabad (excluded)")
    ok = True

    # ---------------------------------------------------------------- Figure 2
    lay = page(prj, "Figure 2 – arhti availability", "Figure 2. Reported arhti credit availability by tehsil",
               "Share of rural populated mouzas where commission-agent (arhti) credit is reported available, Mouza Census 2020 (n = 137 tehsils)")
    a2, zero2, chol2 = lyr(prj, "F2 arhti_share (natural breaks)"), lyr(prj, "F2 no rural populated mouzas"), lyr(prj, "F2 includes Cholistan desert mouzas")
    with_counts(a2)
    m = main_map(lay, prj, [outline, chol2, ict, zero2, a2]); inset(lay, prj, m); furniture(lay, m)
    legend(lay, m, [(a2, "Share of rural populated mouzas|(natural breaks, 5 classes)"), (zero2, f"No rural populated mouzas|(excluded; n = {n_of(zero2)})"),
                    (chol2, f"Includes Cholistan desert|mouzas (n = {n_of(chol2)})"), (ict, "Islamabad (not in Punjab data)")], "AVAILABILITY")
    den = lyr(prj, "F2 side panel: rural populated mouzas")
    m2 = QgsLayoutItemMap(lay); m2.attemptMove(QgsLayoutPoint(RIGHT_X, 104, MM)); m2.attemptResize(QgsLayoutSize(45, 50, MM))
    m2.setCrs(prj.crs()); m2.setLayers([outline, den]); m2.setKeepLayerSet(True); m2.zoomToExtent(punjab_extent(prj))
    m2.setFrameEnabled(True); m2.setFrameStrokeColor(QColor(MUTED)); m2.setFrameStrokeWidth(QgsLayoutMeasurementMM(0.2)); lay.addLayoutItem(m2)
    label(lay, "Denominator: rural populated mouzas per tehsil (natural breaks; light = 2–74, dark = 405–543). "
               "Shares in small tehsils rest on few mouzas.", RIGHT_X, 155, 46, 14, 5.8, False, MUTED)
    footer(lay, [f"Data: {V_MC}.", "Fort Abbas, Yazman and Liaqatpur combine desert (Cholistan) and irrigated mouzas (option A; option B in the appendix). "
                 "Classification: natural breaks (rule D023); histogram and alternatives in Figures S1 and S12."])
    ok &= export(lay, "fig2_arhti_share_tehsil")

    # ---------------------------------------------------------------- Figure 3
    lay = page(prj, "Figure 3 – bivariate", "Figure 3. Arhti and commercial-bank credit availability together (bivariate map)",
               "Tehsils classed by thirds of arhti_share and of commercial_share, Mouza Census 2020 (n = 137 tehsils)")
    b3 = lyr(prj, "F3 bivariate arhti x commercial")
    m = main_map(lay, prj, [outline, ict, zero2, b3]); inset(lay, prj, m); furniture(lay, m)
    label(lay, "AVAILABILITY OF TWO SOURCES", RIGHT_X, MAP[1], 45, 5, 8, True)
    bcounts = {}
    for f in b3.getFeatures():
        if f["bivariate_class"]:
            bcounts[f["bivariate_class"]] = bcounts.get(f["bivariate_class"], 0) + 1
    biv_key(lay, RIGHT_X, MAP[1] + 8, counts=bcounts)
    vals = lambda fld: sorted(f[fld] for f in a2.getFeatures() if f[fld] is not None and f["rp_mouzas"])
    def terc(v):
        n = len(v); return v[int(n / 3)], v[int(2 * n / 3)]
    ta, tc = terc(vals("arhti_share")), terc(vals("commercial_share"))
    label(lay, f"Approximate tercile cuts: arhti {ta[0]:.2f} / {ta[1]:.2f}; commercial-bank {tc[0]:.2f} / {tc[1]:.2f} "
               "(shares of rural populated mouzas).", RIGHT_X, MAP[1] + 41, 46, 8, 5.6, False, MUTED)
    legend(lay, m, [(zero2, f"No rural populated mouzas (n = {n_of(zero2)})"), (ict, "Islamabad (not in Punjab data)")], "", y=MAP[1] + 50)
    label(lay, "Reading: purple-blue tehsils report both sources often; pink tehsils report arhti credit but little commercial-bank credit; "
               "teal tehsils the reverse. Two sources reported in the same tehsil describe availability, not what farmers borrow.",
          RIGHT_X, MAP[1] + 66, 46, 30, 6.0, False, MUTED)
    footer(lay, [f"Data: {V_MC}.", "Classes: terciles of each share across the 137 tehsils (3 × 3 = 9 classes). "
                 "Bivariate global Moran's I (arhti × neighbours' commercial share) = 0.112, p = 0.062 (Queen, 999 permutations, seed 20261031)."])
    ok &= export(lay, "fig3_bivariate_arhti_commercial")

    # ---------------------------------------------------------------- Figure 4
    lay = page(prj, "Figure 4 – LISA", "Figure 4. Spatial clusters of reported arhti credit availability (LISA)",
               "Local Moran's I for arhti_share, tehsils (Q1 unit, n = 137); heavy border = cluster survives false-discovery-rate correction")
    l4, f4 = lyr(prj, "F4 LISA arhti_share (Queen, p<0.05)"), lyr(prj, "F4 FDR(0.05) survivors (heavy border)")
    with_counts(l4)
    m = main_map(lay, prj, [outline, f4, ict, zero2, l4]); inset(lay, prj, m); furniture(lay, m)
    legend(lay, m, [(l4, "LISA cluster type (p < 0.05)"), (f4, f"Survives FDR 0.05|(Benjamini–Hochberg; n = {n_of(f4)})"),
                    (zero2, f"No rural populated mouzas (n = {n_of(zero2)})"), (ict, "Islamabad (not in Punjab data)")], "CLUSTERS")
    footer(lay, [f"Data: {V_MC}.", "Weights: Queen contiguity, row-standardised; 999 permutations, seed 20261031; BH cutoff 0.0117. "
                 "Global Moran's I = 0.536 (p = 0.001). Gi* hot spots (Figure S8) coincide with the High-High clusters."])
    ok &= export(lay, "fig4_lisa_arhti_tehsil")

    # ---------------------------------------------------------------- Figure 5
    lay = page(prj, "Figure 5 – small-farm reach", "Figure 5. Small-farm reach of formal credit by district",
               "SBP subsistence-holding borrower records per 1,000 farms under 12.5 acres (n = 36 districts; counts, not amounts)")
    r5, fl5 = lyr(prj, "F5A small_farm_reach (quantiles)"), lyr(prj, "F5 flagged in SBP screen")
    with_counts(r5)
    m = main_map(lay, prj, [outline, fl5, ict, r5]); inset(lay, prj, m); furniture(lay, m)
    legend(lay, m, [(r5, "Borrower records per 1,000|small farms (quantiles)"), (fl5, f"Flagged in SBP data-quality|screen (n = {n_of(fl5)})"),
                    (ict, "Islamabad (excluded)")], "ALLOCATION")
    with open(ROOT / "outputs" / "tables" / "holding_class_shares.csv") as fh:
        hc = {r["holding_class"]: r for r in csv.DictReader(fh)}["subsistence"]
    label(lay, f"36 districts: subsistence holdings are {100 * float(hc['share_farms_36']):.1f}% of farms and "
               f"{100 * float(hc['share_borrower_records_36']):.1f}% of borrower records but {100 * float(hc['share_disbursement_36']):.1f}% "
               "of the amount disbursed (banks; Islamabad and MFI records without a district excluded). Borrower records may not be unique people.",
          RIGHT_X, 112, 46, 30, 6.0, False, MUTED)
    footer(lay, [f"Data: {V_SBP}; {V_AGC}. Not contemporaneous.", "Flagged districts (Chakwal, Faisalabad, Jhelum, Lahore, Rawalpindi) are marked, not dropped. "
                 "Moran's I of small-farm reach = 0.532 (Queen)."])
    ok &= export(lay, "fig5_small_farm_reach")

    # ---------------------------------------------------------------- Figure 6
    lay = page(prj, "Figure 6 – farms vs borrower records", "Figure 6. Where small farms are, and where small-farm borrower records are reported",
               "Dasymetric dots of farms under 12.5 acres (placed only on cropland) with proportional circles of SBP subsistence-holding borrower records")
    m = main_map(lay, prj, [outline, circ6, dots6, base6]); inset(lay, prj, m); furniture(lay, m)
    legend(lay, m, [(dots6, f"1 dot = 1,000 farms under 12.5 acres|({n_of(dots6):,} dots)")], "FARMS AND BORROWERS")
    t6 = circ6.renderer().symbol().dataDefinedSize().transformer()
    label(lay, "Subsistence-holding borrower records|per district (FY2023-24)".replace("|", "\n"), RIGHT_X, MAP[1] + 20, 46, 8, 7.0, True)
    base_y = MAP[1] + 52
    for v in (50000, 20000, 5000):
        d_mm = t6.size(v)
        e = QgsLayoutItemShape(lay); e.setShapeType(QgsLayoutItemShape.Shape.Ellipse)
        e.setSymbol(QgsFillSymbol.createSimple({"color": "235,104,52,110", "outline_color": "#9a3d14", "outline_width": "0.25"}))
        e.attemptMove(QgsLayoutPoint(RIGHT_X + 2 + (16 - d_mm) / 2, base_y - d_mm, MM)); e.attemptResize(QgsLayoutSize(d_mm, d_mm, MM))
        lay.addLayoutItem(e)
        label(lay, f"{v:,}", RIGHT_X + 21, base_y - d_mm - 1.2, 20, 4, 6.5)
    label(lay, f"Perceptually scaled circles: size follows borrower records with Flannery's compensation (exponent 0.57), because "
               f"readers underestimate circle areas. Largest district: {int(vmax):,} records. Circles sit at a point inside each district; "
               "SBP districts are as reported (where loans are booked may differ from where the land is).", RIGHT_X, base_y + 6, 46, 40, 5.9, False, MUTED)
    footer(lay, [f"Data: {V_AGC} (farms under 12.5 acres); {V_WC}, cells ≥ 25% cropland (~100 m); {V_SBP}. Not contemporaneous.",
                 "Dots are a synthetic redistribution: placed at random within each district's cropland in proportion to cropland fraction (seed 20261031); "
                 "they show density, not farm locations. 36 districts; the census Cholistan Area is excluded."])
    ok &= export(lay, "fig6_dasymetric_farms_borrowers")


    # ---------------------------------------------------------------- Figure 7 (two panels)
    lay = page(prj, "Figure 7 – markets and limited availability", "Figure 7. Proximity to grain markets and limited reported credit availability, by tehsil",
               "A: share of rural populated mouzas with a grain market within 10 km (incl. in the mouza). B: share reporting neither arhti nor any formal source")
    base7 = add_gpkg(prj, g6, "F7 tehsils (course layer)", "course_tehsils_gistar_trend")
    pa = add_gpkg(prj, g6, "F7A grain market within 10 km (share of mouzas)", "course_tehsils_gistar_trend")
    pb = add_gpkg(prj, g6, "F7B neither arhti nor formal credit reported (share of mouzas)", "course_tehsils_gistar_trend")
    base7.setRenderer(QgsSingleSymbolRenderer(QgsFillSymbol.createSimple({"color": "#ffffff", "outline_color": "#8a8984", "outline_width": "0.15"})))

    def fixed(layer, field, breaks, colors, labels):
        """Classes include their lower bound (same convention as Figure S13): QGIS ranges are (lower, upper], so shift each upper bound down."""
        rngs, lo = [], -1e-9
        for b, c, l in zip(breaks, colors, labels):
            up = b - 1e-9
            rngs.append(QgsRendererRange(lo, up, QgsFillSymbol.createSimple({"color": c, "outline_color": "#ffffff", "outline_width": "0.1"}), l))
            lo = up
        layer.setRenderer(QgsGraduatedSymbolRenderer(field, rngs))
        with_counts(layer)
    fixed(pa, "mkt_grain_within10_share", [0.2, 0.4, 0.6, 0.8, 1.0000001], ["#e7f0f7", "#b6d2ea", "#7aaedb", "#3a7fc0", "#0d366b"],
          ["< 20%", "20–40%", "40–60%", "60–80%", "≥ 80%"])
    fixed(pb, "share_neither", [0.05, 0.10, 0.20, 0.40, 1.0000001], ["#f6f1e7", "#f2d3b6", "#e9a46c", "#c9531f", "#6b280b"],
          ["< 5%", "5–10%", "10–20%", "20–40%", "≥ 40%"])
    rect = punjab_extent(prj)
    for i, (lyr_, title_, x0) in enumerate([(pa, "A. Grain market within 10 km", 5.0), (pb, "B. Neither arhti nor formal credit", 87.0)]):
        mm_ = QgsLayoutItemMap(lay); mm_.attemptMove(QgsLayoutPoint(x0, 30, MM)); mm_.attemptResize(QgsLayoutSize(78, 112, MM))
        mm_.setCrs(prj.crs()); mm_.setLayers([outline, lyr_, base7]); mm_.setKeepLayerSet(True); mm_.zoomToExtent(rect)
        mm_.setFrameEnabled(True); mm_.setFrameStrokeColor(QColor(INK)); mm_.setFrameStrokeWidth(QgsLayoutMeasurementMM(0.3)); lay.addLayoutItem(mm_)
        label(lay, title_, x0, 25.5, 78, 4.5, 8.2, True)
        sb = QgsLayoutItemScaleBar(lay); sb.setStyle("Single Box"); sb.setLinkedMap(mm_); sb.applyDefaultSize()
        sb.setUnits(Qgis.DistanceUnit.Kilometers); sb.setUnitLabel("km"); sb.setSegmentSizeMode(Qgis.ScaleBarSegmentSizeMode.Fixed)
        sb.setUnitsPerSegment(50); sb.setNumberOfSegments(2); sb.setNumberOfSegmentsLeft(0); sb.setHeight(1.4); sb.setTextFormat(tfmt(6))
        sb.attemptMove(QgsLayoutPoint(x0 + 40, 132, MM)); lay.addLayoutItem(sb)
        na = QgsLayoutItemPicture(lay); na.setPicturePath(svg_north()); na.setLinkedMap(mm_); na.setNorthMode(QgsLayoutItemPicture.NorthMode.TrueNorth)
        na.attemptMove(QgsLayoutPoint(x0 + 68, 116, MM)); na.attemptResize(QgsLayoutSize(6, 11, MM)); lay.addLayoutItem(na)
        lg = QgsLayoutItemLegend(lay); lg.setTitle(""); lg.setLinkedMap(mm_); lg.setSyncMode(Qgis.LegendSyncMode.Manual)
        root7 = lg.model().rootGroup(); root7.clear()
        n7 = root7.addLayer(lyr_); n7.setUseLayerName(False); n7.setName("Share of rural populated mouzas")
        for comp, size, bold in [(QgsLegendStyle.Style.Subgroup, 7.0, True), (QgsLegendStyle.Style.SymbolLabel, 6.8, False)]:
            st = lg.style(comp); st.setTextFormat(tfmt(size, bold)); lg.setStyle(comp, st)
        lg.setColumnCount(2); lg.setSplitLayer(True); lg.setSymbolWidth(5); lg.setSymbolHeight(3.0)
        lg.attemptMove(QgsLayoutPoint(x0, 144, MM)); lay.addLayoutItem(lg); lg.adjustBoxSize()
    footer(lay, [f"Data: {V_MC}. 137 tehsils; white = no rural populated mouzas. Fixed classes; each class includes its lower bound.",
                 "A: Mouza Census distance bands (in the mouza or 1–10 km). B: formal = commercial bank, ZTBL, cooperative bank or microfinance bank; "
                 "other sources (NGOs, rural support programmes, government) are not counted, so B shows limited reported availability, not exclusion.",
                 "Exploratory: the within-10 km share is associated with arhti availability in OLS, quasi-binomial and spatial error models (Table B9)."])
    ok &= export(lay, "fig7_markets_neither_tehsil")

    prj.writeEntry("Paths", "/Absolute", False)
    w = prj.write(str(QGZ))
    print(f"project with layouts written: {w}; layouts: {[l.name() for l in prj.layoutManager().layouts()]}")
    app.exitQgis()
    return 0 if (ok and w) else 1


if __name__ == "__main__":
    sys.exit(main())
