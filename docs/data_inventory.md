# Data inventory

All files were accessed on **2026-10-31** by `scripts/01_download.py`. File sizes and SHA-256 checksums are in
`docs/download_log.csv`. Raw files live in `data/raw/<folder>/` and are read-only. Extracted copies are in `data/interim/`
(made by `scripts/02_extract_archives.py`). Structure details are in `docs/raw_inspection.md` (made by `scripts/03_inspect_raw.py`).

Status key: **downloaded**, **needs manual download**, or **not yet inspected**. All 12 files below are downloaded and
structurally inspected. None has been cleaned or used in analysis yet.

| # | Dataset | Source | URL | Accessed | Format | Geographic level | Reference period | Status |
|---|---|---|---|---|---|---|---|---|
| 1 | Mouza Census 2020, Punjab report | PBS (Agricultural Census Wing) | https://www.pbs.gov.pk/wp-content/uploads/2020/07/mouza_census_2020_punjab_report.pdf | 2026-10-31 | PDF, 638 pp | Province / division / district / tehsil tables (counts of mouzas reporting each facility) | Fieldwork Jan–Mar 2020 (Punjab covered in Jan 2020, report p. 4) | downloaded; inspected |
| 2 | Mouza Census 2020, Excel (RAR) → `Mouza Census-2020.xlsx` | PBS | https://www.pbs.gov.pk/wp-content/uploads/2020/07/mc2020.excel-1.rar | 2026-10-31 | RAR5 → XLSX (1 sheet, 51,888 records × 224 cols) | **Mouza (record-level)**, all Pakistan; Punjab = 26,462 mouzas, 37 district units, 150 tehsil names | Jan–Mar 2020 | downloaded; extracted; inspected; Punjab credit counts validated against report Table 8.1 |
| 3 | SBP district-wise agri credit detail, FY24 | State Bank of Pakistan (ACD) | https://archive.sbp.org.pk/acd/DistrictWise-Detail-Jul-Jun-2024.xlsx | 2026-10-31 | XLSX (1 sheet) | District (by province) | FY2023-24 (Jul 2023–Jun 2024), cumulative | downloaded; inspected |
| 4 | SBP district-wise agri credit summary, FY24 | SBP (ACD) | https://archive.sbp.org.pk/acd/DWS-Jul-Jun-2024.pdf | 2026-10-31 | PDF, 10 pp | District | FY2023-24 | downloaded; inspected (same tables as #3) |
| 5 | SBP *Indicative Credit Limits and Eligible Items for Agriculture Financing 2022-23* (Revised Aug 2022), the "CL1 Annex" | SBP | Requested: https://www.sbp.org.pk/acd/2022/CL1-Annex.pdf (blocked by Cloudflare). **Obtained from** https://archive.sbp.org.pk/acd/2022/CL1-Annex.pdf | 2026-10-31 | PDF, 25 pp (page 1 is an image) | Province (definitions) | 2022-23; holding-size thresholds cite Agricultural Census **2010** | downloaded (fallback mirror); inspected |
| 6 | SBP list of bank branches, 30 Jun 2024 | SBP | https://www.sbp.org.pk/assets/document/publications/Bank-Branches-Jun-2024.xlsx | 2026-10-31 | XLSX, 2 sheets (`Banks` 16,867 rows; `MFBsD & DFIs` 1,488 rows) | Branch (text: province, division, district, tehsil, city, locality). **No coordinates.** | As of 30 Jun 2024 | downloaded; inspected |
| 7 | Agricultural Census 2024, Punjab report | PBS | https://www.pbs.gov.pk/wp-content/uploads/2020/07/IAC-Punjab-Report-25-05-2026-1.pdf | 2026-10-31 | PDF, 288 pp | Province / division / district | Agricultural year Rabi 2023-24 + Kharif 2024. Fieldwork Sep 2024 (northern areas) and Jan–10 Feb 2025 (rest). **Sample-based** (district-level design, 15% MoE at 95%) | downloaded; inspected |
| 8 | Agricultural Census 2024, `Table_1_District.xls` | PBS | https://www.pbs.gov.pk/wp-content/uploads/2020/07/Table_1_District.xls | 2026-10-31 | XLS, 1 sheet, **no column headers** | District × farm-size class (KP, Punjab, Sindh, Balochistan, ICT …) | As #7 | downloaded; inspected; contents identified by matching report Table 1.3 (see below) |
| 9 | Agricultural Census 2024, `Table_3_District.xls` | PBS | https://www.pbs.gov.pk/wp-content/uploads/2020/07/Table_3_District.xls | 2026-10-31 | XLS, 1 sheet, **no column headers** | District × farm-size class | As #7 | downloaded; inspected; contents identified by matching report Table 1.1 (see below) |
| 10 | Population Census 2023, Table 1, Punjab districts | PBS | https://www.pbs.gov.pk/wp-content/uploads/2020/07/table_1_punjab_districts.xlsx (linked from https://www.pbs.gov.pk/result-excel/, "Table-1 … Punjab → District Wise") | 2026-10-31 | XLSX, 1 sheet | District and tehsil, each split total / rural / urban (36 district rows, ~145 tehsil rows) | Census 2023 (also gives 2017 population and the 2017–23 growth rate) | downloaded; inspected |
| 11 | OCHA COD-AB Pakistan, `pak_admin_boundaries.shp.zip` | OCHA / HDX | Resolved at run time from https://data.humdata.org/dataset/cod-ab-pak (resource `pak_admin_boundaries.shp.zip`) | 2026-10-31 | Shapefile zip (admin0–3, lines, points; plain and `_em` variants), EPSG:4326 | ADM0–ADM3. Punjab: 36 districts (ADM2), **139 tehsils** (ADM3) | `valid_on` 2022-09-09; HDX dataset modified 2026-08-14 | downloaded; extracted; inspected |
| 12 | OCHA COD-AB Pakistan, `pak_admin_boundaries.xlsx` (p-code gazetteer) | OCHA / HDX | as #11 (resource `pak_admin_boundaries.xlsx`) | 2026-10-31 | XLSX, 12 sheets | ADM0–ADM3 names + p-codes | 2022-09-09 | downloaded; inspected |
| 13 | ESA WorldCover 10 m 2021 v200, 7 tiles (N27E069, N27E072, N30E069, N30E072, N30E075, N33E069, N33E072) | ESA / Zanaga et al. 2022, doi:10.5281/zenodo.7254221 | https://esa-worldcover.s3.eu-central-1.amazonaws.com/v200/2021/map/ (official AWS access; Zenodo has only 60° macrotiles) | 2026-10-31 | GeoTIFF (COG), EPSG:4326, 1/12000° | 10 m pixels | 2021 | downloaded; used in 06 (D017) |
| 14 | MAP Accessibility to Cities 2015 (Weiss et al. 2018, doi:10.1038/nature25181), clip 69–76°E, 27–35°N | Malaria Atlas Project | https://data.malariaatlas.org/geoserver/ows (WCS, coverage `Accessibility__201501_Global_Travel_Time_to_Cities`) | 2026-10-31 | GeoTIFF int32 minutes, EPSG:4326, 1/120° | ~1 km pixels | nominal 2015 | downloaded; used in 06 (D017) |

HDX offers no GeoPackage, only a geodatabase, shapefile, GeoJSON and XLSX. The boundaries are stored as GeoPackage in the analysis CRS (Albers equal-area centred on Punjab, D025): `data/interim/punjab_boundaries.gpkg`.

## What the header-less Ag Census files contain (verified, not assumed from names)

- **`Table_1_District.xls` = number of farms by tenure × farm-size class.** Columns (excluding blanks): admin
  unit / size class, Total farms, Owner, Owner-cum-tenant, Tenant. Check: Bhakkar "PRIVATE-FARMS TOTAL" = 165,761 /
  146,580 / 9,669 / 9,512, which equals report **Table 1.3** (Tenure classification of farms, p. 80), number-of-farms
  columns. It does **not** contain the farm-area-by-tenure columns of Table 1.3.
- **`Table_3_District.xls` = number of farms, farm area and cultivated area (acres) × farm-size class.** Columns: farms
  (number, %), farm area (acres, %), cultivated area (acres, %), cultivated as % of farm area, average farm area, average
  cultivated area per farm. Check: Bhakkar total = 165,761 farms / 1,858,588 ac / 1,771,229 ac / 95%, which equals report
  **Table 1.1** (Number and area of farms, acres, p. 78).
- File numbers do **not** match report table numbers (file 1 ↔ report 1.3, file 3 ↔ report 1.1).
- Size classes (acres): Under 1.0; 1.0–<2.5; 2.5–<5.0; 5.0–<7.5; 7.5–<12.5; 12.5–<25; 25–<50; 50–<100; 100+.
- Values are fractional, i.e., weighted sample estimates.
