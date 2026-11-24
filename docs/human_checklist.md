# Human verification checklist (for Ahmed)

Open each source file at the page/sheet/row given and compare the published value with **our extracted value**. In the last
column write ✓ (matches), ✗ (does not match) or a note. The app's Data and methods page reads this column. Do not change the `ID` column.

Files: Mouza report = `data/raw/mouza_census_2020/mouza_census_2020_punjab_report.pdf`; SBP xlsx =
`data/raw/sbp/DistrictWise-Detail-Jul-Jun-2024.xlsx` (sheet "Farm and Non Farm Sectors"); SBP PDF = `data/raw/sbp/DWS-Jul-Jun-2024.pdf`;
Ag Census report = `data/raw/ag_census_2024/IAC-Punjab-Report-25-05-2026-1.pdf`; CL1 = `data/raw/sbp/CL1-Annex.pdf`.
Page numbers are PDF page numbers (the viewer's page counter), not the printed numbers.

| ID | Area | Item | Source file | Page / sheet | Row | Value to compare | Our extracted value | Ahmed: ✓ / ✗ / note |
|---|---|---|---|---|---|---|---|---|
| M1 | Mouza | Table 8.1 tehsil row | Mouza report | PDF p. 501 | SHARAK PUR (Sheikhupura) | rural populated / ZTBL / commercial / commission agent–arthi | 110 / 104 / 61 / 104 | |
| M2 | Mouza | Table 8.1 tehsil row | Mouza report | PDF p. 502 | JHELUM (Jhelum) | rural populated / ZTBL / commercial / commission agent–arthi | 140 / 63 / 15 / 0 (printed "-") | |
| M3 | Mouza | Table 8.1 tehsil row | Mouza report | PDF p. 498 | DE-EXCLUDED AREA D.G KHAN | rural populated / ZTBL / commercial / arthi / others | 330 / 0 / 0 / 1 / 291 | |
| M4 | Mouza | Table 1.1 tehsil row (merged digits in PDF text; checked visually against rendered page images; human check pending) | Mouza report | PDF p. 79 | JAND (Attock) | total / rural / urban / partly urban / forest pop. / forest unpop. / unpopulated / rural populated | 80 / 64 / 1 / 1 / 0 / 0 / 14 / 65 | |
| M5 | Mouza | Table 1.1 tehsil row (as M4) | Mouza report | PDF p. 79 | PINDI GHEB (Attock) | same columns as M4 | 80 / 70 / 2 / 3 / 0 / 2 / 3 / 73 | |
| S1 | SBP | All-Punjab total disbursed borrowers | SBP xlsx (and SBP PDF p. 1) | Farm and Non Farm Sectors | Excel row 48 "All Punjab", column Q | farm-sector total disbursed borrowers | 732,856 | |
| S2 | SBP | All-Punjab total disbursed amount | SBP xlsx | Farm and Non Farm Sectors | row 48, column R | Rs million | 887,737.4 | |
| S3 | SBP | All-Punjab above-economic borrowers | SBP xlsx | Farm and Non Farm Sectors | row 48, column L | borrowers | 8,024 | |
| S4 | SBP | All-Punjab above-economic amount | SBP xlsx | Farm and Non Farm Sectors | row 48, column M | Rs million | 438,386.5 | |
| S5 | SBP | District row | SBP xlsx | Farm and Non Farm Sectors | row 9 "Attock", columns B / C | subsistence borrowers / amount (Rs mn) | 4,901 / 10,212.7 | |
| S6 | SBP | District row (flagged: subsistence avg loan 38.7× median) | SBP xlsx | Farm and Non Farm Sectors | row 21 "Jehlum", columns B / C | subsistence borrowers / amount (Rs mn) | 1,410 / 24,942.0 | |
| S7 | SBP | District row | SBP xlsx | Farm and Non Farm Sectors | row 37 "Rahimyar Khan", columns B / L | subsistence / above-economic borrowers | 47,717 / 1,139 | |
| A1 | Ag Census | District totals | Ag Census report (Tables 1.1 and 1.3); also `Table_3_District.xls` row 1881, `Table_1_District.xls` row 1019 | PDF pp. 79 and 81 | BHAKKAR DISTRICT | farms / farm area (acres) / tenant farms | 165,761 / 1,858,588 / 9,512 | |
| A2 | Ag Census | District totals | as A1; `Table_3_District.xls` row 1794, `Table_1_District.xls` row 972 | PDF pp. 79 and 81 | OKARA DISTRICT | farms / farm area (acres) / tenant farms | 136,365 / 886,180 / 21,971 | |
| A3 | Ag Census | Column identification | `Table_1_District.xls` | Sheet1 | any district block | columns D/F/H/J = total / owner / owner-cum-tenant / tenant farms (number) | as stated in `data_inventory.md` | |
| C1 | CL1 | Table 2.7 Punjab thresholds | CL1 | PDF p. 11 | "1 Punjab" | subsistence / economic / above-economic (acres) | up to 12.5 / 12.5 to 50 / above 50 | |
| C2 | CL1 | Basis of the holding categories | CL1 (and SBP guidance) | PDF p. 11 and text around Table 2.7 | — | owned area or operated area? (not stated in Table 2.7) | not found in the document | |
| X1 | Crosswalk | parent_aggregation | `docs/crosswalk_manual.csv`; OCHA polygon in QGIS | — | LAWA (PB-052-174, Chakwal, 17 mouzas) → Tala Gang PK60504 | is Lawa inside the OCHA Tala Gang polygon (~2,975 km²)? | assigned | |
| X2 | Crosswalk | parent_aggregation (Cholistan option A) | `docs/crosswalk_manual.csv` | — | Cholistan YAZMAN (PB-999-079, 144 mouzas) → Yazman PK60305 | same PBS tehsil code (79) as Bahawalpur's Yazman | assigned | |
| X3 | Crosswalk | spelling | `docs/crosswalk_manual.csv` | — | 18-HAZARI (PB-035-108, Jhang) → Athara Hazari PK61204 | same unit | assigned | |
| X4 | Crosswalk | rename | `docs/crosswalk_manual.csv` | — | DE-EXCLUDED AREA D.G KHAN (PB-029-084) → D.G Khan (Tribal Area) PK60701 | same unit (historical name; also Koh-e-Suleman) | assigned | |
| X5 | Crosswalk | parent_aggregation | `docs/crosswalk_manual.csv` | — | BAHAWALPUR SADDAR (114) + BAHAWALPUR CITY (0) → Bahawalpur PK60302 | OCHA Bahawalpur covers both | assigned | |
| R1 | Raster | One ~100 m cropland-fraction cell | `data/interim/worldcover_cropland_frac_1200.tif` vs WorldCover tile `data/raw/worldcover/ESA_WorldCover_10m_2021_v200_N27E072_Map.tif` | QGIS | cell with upper-left corner 73.1408 E, 29.5425 N | share of class-40 pixels in the 10×10 block (Identify tool) | 0.87 | |
| L1 | Literature | Geocoded point (fallback rule) | `outputs/arhti_project.gpkg` layer `literature_evidence` | QGIS | Bahawalpur (PMN/MEDA FGD) | is 71.66387 E, 29.39464 N at Bahawalpur town centre? (Nominatim gave an administrative relation, not a place) | placed in OCHA Bahawalpur tehsil | |
| L2 | Literature | Geocoded point (ambiguous name) | as L1 | QGIS | Khanpur (IGC) | is the study's Khanpur the city in Rahim Yar Khan (70.65601 E, 28.64774 N)? | district check: match | |
| L3 | Literature | Geocoded point (ambiguous name) | as L1 | QGIS | Sahiwal (IGC, maize) | Sahiwal city in Sahiwal district (73.11106 E, 30.67151 N), not Sahiwal in Sargodha? | district check: match | |
| L4 | Literature | Values transcribed into `docs/literature_evidence.csv` | IGC 2013 PDF p. 39 (Table 11); PMN/MEDA 2019 PDF pp. 19, 23 | — | all 10 rows | rates, sample, basis; then fill `verified_by_ahmed` | as supplied by Ahmed | |
| P1 | Rates | SBP Table 3.33, FY2012-13 | SBP Monthly Statistical Bulletin, Sep 2026 (`data/raw/sbp_bulletin/MSB_September_2026.pdf`) | PDF p. 90 | 2012-13 | ZTBL prod / dev; PPCB prod / dev; commercial prod / dev (% p.a.) | 12.00 / 13.80; 19.00 / 18.00; 16.00 / 16.00 | |
| P2 | Rates | SBP Table 3.33, FY2023-24 | as P1 | PDF p. 90 | 2023-24 | as P1 | 29.42 / 29.42; 20.67 / 22.71; 22.96 / 22.94 | |
| P3 | Rates | IGC 2013 farmer-reported bank rates | IGC 2013 PDF (`docs/literature_evidence.csv` URL) | page to be found | — | bank interest rates reported by interviewed farmers | 9–18% (supplied by Ahmed; page not yet recorded) | |
| Q1 | LQ | Lahore, above-economic amount LQ | SBP xlsx (row "Lahore", column M) and Ag Census `Table_3_District.xls` (Lahore cultivated area) | Farm and Non Farm Sectors | Lahore | share of Punjab abv amount ÷ share of cultivated area | 14.06 (`outputs/tables/reporting_geography.csv`) | |
| Q2 | LQ | Jhelum, subsistence amount LQ (flagged district) | SBP xlsx (row "Jehlum", column C) and Ag Census | Farm and Non Farm Sectors | Jhelum | share of Punjab sub amount ÷ share of cultivated area | 6.47 | |
| K1 | Crops | Table 6.9 wheat area | Ag Census report | PDF p. 135 | BAHAWALNAGAR DISTRICT | area under wheat, total (acres) | 1,056,209 | |
| K2 | Crops | Table 6.13 sugarcane area | Ag Census report | PDF p. 139 | RAHIM YAR KHAN DISTRICT | area under sugarcane (acres) | 378,161 | |
| D1 | Attribution | Definition of "district" in SBP agricultural credit returns | ACD Circular 2 of 2007 + annexures; AC&MFD Circular Letter 2 of 2015 + templates (open in a browser; automated access blocked) | — | — | lending-branch district or financed-farm district? | not found (D039) | |

