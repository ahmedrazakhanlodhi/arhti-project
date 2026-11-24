# Project rules: Where the Bank Ends and the Arhti Begins

**Geographic Access, Landholding Structure, and the Allocation of Agricultural Credit in Punjab, Pakistan.**
Final group project for PPHA 38520 (GIS Applications in the Social Sciences, UChicago Harris). Built in QGIS.
Presentation: Nov 30, 2026. Paper: Dec 9, 2026. This is a **descriptive** project, not a causal one.

## Research questions
**Main question (paper and app):** Where is arhti credit available in rural Punjab, and how does its geography
compare with formal banking? Q1 is the main analysis; Q2 is a second lens on a separate dataset and period.

- **Q1 (tehsil level, geographic exclusion):** Across Punjab's rural tehsils, is reported arhti credit availability
  associated with weaker formal banking access, or does it concentrate where banks and markets already exist?
  Data: Mouza Census 2020.
- **Q2 (district level, economic exclusion):** Does formal agricultural credit reach smallholders and tenant-heavy
  areas in proportion to their share of farms? Data: SBP FY2023-24 and Agricultural Census 2024.

## Layout
- `data/raw/`: downloaded source files. **Read-only. Never modify, overwrite, or delete.**
- `data/interim/`: cleaned or extracted intermediates.
- `data/processed/`: analysis-ready files (GeoPackage for anything geographic).
- `scripts/`: numbered in run order (`01_download.py`, `02_...`). Run with `.venv/bin/python -I scripts/NN_x.py`.
- `outputs/figures/`, `outputs/tables/`: exported maps and tables.
- `docs/`: `decisions.md`, `data_inventory.md`, `manual_downloads.md`, `pakistan_primer.md`.

## Standing rules
1. **Never invent, estimate, or fill in data values.** If something is missing or ambiguous, stop and ask Ahmed.
2. **Reproducibility:** every script must be re-runnable from raw data. Number scripts in run order (01_, 02_, ...).
   Never modify files in `data/raw`.
3. **Log geographic changes:** every transformation that drops, merges, or renames geographic units must be logged
   in `docs/decisions.md` with the reason.
4. **No fuzzy-only matching:** never match geographic units by fuzzy name matching alone. Every non-exact match
   needs Ahmed's review before use.
5. **Human verification:** values extracted from PDFs and every non-exact crosswalk match are listed in `docs/human_checklist.md` for checking by hand.
6. **Validate extractions:** check extracted numbers against published totals before using them.
7. **CRS and format:** the projected CRS for analysis is a custom Albers equal-area projection centred on Punjab:
   `+proj=aea +lat_1=28 +lat_2=33 +lat_0=30 +lon_0=72 +datum=WGS84 +units=m +no_defs` (defined once in `scripts/common.py`).
   kNN weights use geodesic distances. Store geographic data as GeoPackage (`.gpkg`). (Changed 2026-10-31 by Ahmed, D025;
   ESRI:102028 was centred at 125°E and rotated/distorted Punjab.)
8. **Descriptive language only:** "associated with", "concentrated", "clusters spatially". Never "causes",
   "drives", or "explains".
9. **Banned term:** never use "credit desert". Use "low observed credit reach" or "low reported availability".
10. **Data vintage on every output:** every map and table states its vintage (e.g., "Mouza Census, Jan-Mar 2020";
    "SBP, FY2023-24"; "Agricultural Census 2024, sample-based"). Never present different vintages as contemporaneous.
11. **SBP booking-location caveat:** SBP lending data record the place of loan **booking**, which may differ from
    where the land is. Never map district shares of disbursement **amounts**. Use borrower-count measures for maps.
    Exception (D039, 2026-11-01): district amounts may be mapped ONLY in the reporting-geography outputs, labelled
    "district as reported by SBP (attribution under verification)" until the attribution is confirmed.
12. **No fieldwork locations (own fieldwork):** do not map, list, or reference the group's OWN fieldwork sites or interview
    locations anywhere in the project. Town-level locations of PUBLISHED studies may be shown as CONTEXT only, never as data
    for statistics or choropleths. (Scope clarified 2026-10-31 by Ahmed, D032.)
13. **Spatial statistics:** state the spatial weights (type, contiguity/k, row-standardisation) and permutation
    settings (number, seed) before any Moran's I / LISA run, and report them in captions.
