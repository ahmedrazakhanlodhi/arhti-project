# Building the final maps in QGIS

**`outputs/arhti_project.qgz`** already contains every final layer, loaded from `outputs/arhti_project.gpkg` and styled to
match `outputs/figures/`. It is built by `scripts/12_qgis_project.py` with QGIS's own Python (QGIS 4.2.3 here). The style of
each layer is also saved as `.qml` in `outputs/qgis_styles/`, so you can re-apply it (Layer Properties → Symbology → Style →
Load Style…). Field aliases display automatically (verified in QGIS 4.2.3). **Print layouts are not built: that is the group's job.**

## Open the project
1. **Project → Open…** → `outputs/arhti_project.qgz`. Project CRS: custom Albers equal-area centred on Punjab
   (`+proj=aea +lat_1=28 +lat_2=33 +lat_0=30 +lon_0=72 +datum=WGS84`, D025). Grid north = true north (within 0.1°).
2. The Layers panel has one group per figure. Only "Figure 2" and "Context" are switched on; tick a group to show it.

| Group | Layers (top → bottom) | Key field / classes |
|---|---|---|
| Figure 1 – coverage | F1A tehsil match type; F1B district coverage; Islamabad (excluded) | `coverage_class` (exact or normalized / spelling or rename / parent aggregation / no rural populated mouzas); districts: matched / flagged |
| Figure 2 – arhti availability | Cholistan desert outline (dashed); no rural populated mouzas; arhti_share; side panel rp_mouzas | natural breaks 0.121 / 0.324 / 0.551 / 0.750 / 1.000 (n = 53 / 38 / 17 / 17 / 12; side panel 74 / 158 / 259 / 405 / 543); read from `classification_comparison.csv` at build time |
| Figure 3 – bivariate | bivariate arhti × commercial | `bivariate_class` A1–A3 × C1–C3 (J. Stevens 3×3 colours) |
| Figure 4 – LISA (tehsil, Q1) | FDR(0.05) survivors (heavy border); LISA Queen p<0.05 | `lisa_queen_p05`; heavy border = `lisa_queen_fdr05` |
| Figure 5 | flagged (triangles); 5A small_farm_reach; 5B availability-based class; 5C presence-based class (RURAL branches per 10,000 farms, D034); Islamabad | quantile breaks 65.7 / 101.7 / 145.4 / 181.4 / 299.0 for 5A; classes labelled |
| Figure S2 – LISA (district, MAUP) | FDR survivors; LISA district | `lisa_queen_p05` (district layer) |
| Figure S3 – published-study locations (CONTEXT only) | S3 points (IGC markets = black circles, PMN/MEDA focus groups = orange squares; labelled by town and study/crop); S3 base map arhti_share | layer `literature_evidence`; never style polygons by any study rate |
| Figure S4 – mouza-level co-occurrence (EXPLORATORY) | S4 observed/expected co-occurrence | `cooc_ratio_class` (fixed classes < 0.80 … > 1.25; hatched = not estimable). Caption verbatim: "Within-tehsil co-occurrence of reported credit sources across mouzas; availability reports, not borrowing; association, not substitution or complementarity in behaviour." |
| Context | Pakistan provinces (inset); Punjab outline | |

Check the class breaks against `outputs/tables/classification_comparison.csv` after any rerun: the project reads them at build time.

## Print Layout (each figure)
1. **Project → New Print Layout** (A4 landscape for the paper, 16:9 for slides). Tick only the group for that figure, then
   **Add Map** → Item Properties → **Lock layers** (and **Lock styles for layers**) so each map item keeps its own layers.
2. **Figure 1 inset:** add a second Map item, tick only "Pakistan provinces (inset)" + "Punjab outline", lock layers; optionally
   add an **Overview** of the main map.
3. **Figure 2 side panel:** a second Map item showing only "F2 side panel: rural populated mouzas".
4. **Legend** → untick *Auto update*. Remove helper layers (outlines, flagged markers) or rename them to match the PNG legends.
   For counts: right-click a legend layer → *Show Feature Count*. **Figure 3** needs a hand-made 3×3 key (nine rectangles with
   the colours in the layer style; axis labels "Arhti credit availability: low → high" and "Commercial-bank credit availability:
   low → high"; cell counts are in `docs/figure_numbers.md`).
5. **Scale bar** → Single Box, kilometres, 2 × 50 km. **North arrow** → points up (grid north = true north in this CRS).
6. **Text items (required on every map):** title; data sources **with vintages** (Mouza Census Jan–Mar 2020; SBP FY2023-24, by
   loan-booking district; Agricultural Census 2024, sample-based, fieldwork 2024–25; SBP branch list 30 Jun 2024; OCHA COD-AB valid_on
   2022-09-09; "not contemporaneous"); authors' names; date. Copy the caption notes from the PNGs:
   - Figs 2–4: "Fort Abbas, Yazman and Liaqatpur combine desert (Cholistan) and irrigated mouzas."
   - Fig 1: "Administrative assignment = share of rural populated mouzas assigned to a polygon; it is not geographic precision."
   - Fig 3: "Co-location of reported sources across units cannot show substitution or complementarity at the borrower level."
   - Fig 4 / S2 (rule 13): Global Moran's I, E[I], z, pseudo p, n; "Queen contiguity, row-standardised; 999 permutations, seed
     20261031; counts at p < 0.05, p < 0.01 and FDR(0.05); FDR survivors have a heavy border; Benjamini–Hochberg p-value cutoff = …"
     (cutoff from `outputs/tables/lisa_counts.csv`, column `bh_cutoff`; tehsil Queen A = 0.0117, district Queen A = 0.0029)
   - Fig 5: "SBP records the district where a loan is booked, which may differ from where the borrower's land is." Never map
     amount shares. Province headline box: 1.1% of farm-sector borrower records, 49.4% of disbursement (SBP FY2023-24).
7. **Layout → Export as Image** (300 dpi PNG) and **Export as PDF** into `outputs/figures/`, names ending `_qgis`.

Presentation and paper: Figures 1–5 (Figure 5 is the single-panel version). Appendix: S1–S6 (S5 = three-panel Figure 5; S6 = concentration curve, a chart; keep the matplotlib version).

**Figure S3 caption (use verbatim):** "Locations of published studies on the cost of arhti credit. Rates come from small, non-representative samples, are reported by crop (IGC) or from focus groups (PMN/MEDA), and are not district or tehsil estimates. Points are approximate town centres." The points are CONTEXT only: do not colour, interpolate or aggregate any rate to polygons.

## Rebuilding the project
`bash run_all.sh` rebuilds it automatically when QGIS is installed in `/Applications`. Manually:
`source scripts/qgis_env.sh && cd /tmp && "$QGIS_PY" -s "<project>/scripts/12_qgis_project.py"`. Rebuilding overwrites
`arhti_project.qgz`: save your layouts in a **copy** (e.g. `arhti_project_layouts.qgz`), or export them as layout templates (.qpt).
