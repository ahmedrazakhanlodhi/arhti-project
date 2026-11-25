# Decisions log

Every transformation that drops, merges or renames geographic units is logged here with its reason. Source and
processing decisions are logged too. Status: **DONE** (applied in a script), **OPEN** (needs Ahmed's decision; nothing applied yet).

## D001 (2026-10-31, DONE): CL1 Annex fetched from SBP archive mirror
`https://www.sbp.org.pk/acd/2022/CL1-Annex.pdf` redirects to a Cloudflare-blocked circulars search page (HTTP 403).
`scripts/01_download.py` falls back to `https://archive.sbp.org.pk/acd/2022/CL1-Annex.pdf`, which is the same SBP path on
SBP's archive domain. The file is *Indicative Credit Limits and Eligible Items for Agriculture Financing 2022-23
(Revised: August 2022)*, the document cited in the note under the SBP FY24 district tables. **Ahmed to confirm.**

## D002 (2026-10-31, DONE): Archives extracted to data/interim
`scripts/02_extract_archives.py` extracts the Mouza Census RAR5 with macOS bsdtar and the OCHA shapefile zip with Python.
Both go to `data/interim/`, and `data/raw/` is untouched. No units dropped or renamed.

## Open questions (no transformation applied yet)

### O1 [resolved, D005]: Which mouzas count as "rural populated" (Q1 denominator) [resolved: see D005]
The published Punjab totals in Mouza Census report Table 8.1 (23,130 mouzas; ZTBL 16,989; Cooperative 5,753; Commercial
8,832; MFB 3,526; NGO 1,054; RSP 1,985; Govt 1,195; Commission agent/Arthi 7,290; Others 5,184) are reproduced
**exactly** from the Excel by keeping status `P1Q09` ∈ {1 Rural, 3 Partly urban} plus status 4 Forest with ≥1
settlement (`P1Q10` > 0). This drops 1,371 urban, 1,844 unpopulated and 117 unpopulated forest mouzas. The definition
matches the report's own ("rural + partly urban + forest populated", p. 1). **Proposed; needs Ahmed's OK.**

### O2 [resolved, D024]: Tehsil crosswalk, Mouza Census 2020 ↔ OCHA boundaries
Mouza Census Punjab has 150 tehsil names (142 with rural mouzas). OCHA ADM3 (valid 2022-09-09) has 139 Punjab tehsils,
and Census 2023 Table 1 has about 145. Names differ in spelling (e.g., `MAINWALI`, `SHEIKHUPRA`, `TALA GANG`,
`YAZMAN` vs `YAZMAN `), and the sources include non-standard units (`DE-EXCLUDED AREA D.G KHAN`, `DE-EXCLUDED AREA
RAJANPUR`, `CHOLISTAN`, and two different `YAZMAN` tehsils under Bahawalpur and Cholistan). Per the standing rules, a
crosswalk table must be built with exact or code matches only, and every non-exact match goes to Ahmed for review.

### O3 [resolved, D022/D024]: District crosswalk, SBP ↔ Ag Census ↔ OCHA
SBP's *Punjab* table has 37 rows and **includes Islamabad**. OCHA and Census 2023 have 36 Punjab districts. The Ag Census
xls has a separate `CHOLISTAN AREA` under Bahawalpur division. SBP spellings differ (`Jehlum`, `Mandibahauddin`,
`Rahimyar Khan`, `D.G.Khan`), and OCHA uses `Leiah` for Layyah. The handling of Islamabad and Cholistan is Ahmed's decision.

### O4: Data-quality flags (not corrected)
- SBP branch list, `Banks` sheet, row 16602 (UBL): coded Punjab / Lahore, but the locality text reads "…Bajaur Road Tehsil
  Munda District Lower Dir" (KP).
- SBP DWS PDF, "ALL PAKISTAN" non-farm row: the first two figures appear transposed relative to the xlsx (266,909.7 printed
  before 1,047,849). The xlsx looks correct. Column header "18=3+7+13" in both files is presumably a typo for 3+8+13.

---

## D003 (2026-10-31, DONE): Islamabad (ICT) excluded from the Punjab analysis
The Mouza Census Punjab report also prints ICT (PDF p. 28: "ICT has been included in the Punjab report"). ICT is not
part of Punjab. In the Excel it is a separate province (`ISLAMABAD CAPITAL TERRITORY`, 195 mouzas, 1 tehsil), and the
report's PUNJAB total row (26,462 mouzas; 23,130 rural populated) already excludes it. `scripts/04_extract_mouza.py`
keeps `prv_desc == PUNJAB` only. ICT rows in the PDF are tagged `ict` and left out of validation.

## D004 (2026-10-31, superseded by D015-final: Cholistan now merged as option A, B as sensitivity): Cholistan kept as a separate "district", not merged
For Mouza Census 2020 only, PBS treats Cholistan as a district of Punjab (PDF p. 29, Caution note j; also PDF p. 26). In the Excel it is
`dist_code 999`, Bahawalpur division, with three tehsils whose names repeat tehsils of other districts: **FORT ABBAS**
(code 71; the other Fort Abbas is in Bahawalnagar), **YAZMAN** (code 79; the other is in Bahawalpur) and **LIAQUATPUR**
(code 81; the other is in Rahim Yar Khan). They are kept as 3 separate rows with `is_cholistan = True` and
`tehsil_uid` PB-999-071 / -079 / -081. They are **not merged** into the parent tehsils yet. That decision (and the
mapping to OCHA polygons) is Ahmed's.

## D005 (2026-10-31, DONE): Rural populated mouza definition applied (was O1)
`rp_mouzas` = status Rural (1) + Partly urban (3) + Forest (4) with ≥1 settlement. This reproduces every published
rural-populated count in Tables 1.1, 6.3, 6.7, 8.1 and 8.2, at every level. Dropped from the denominator: urban (1,371),
unpopulated (1,844) and unpopulated forest (117) mouzas. They stay counted in the `mouzas_*` status columns.

## D006 (2026-10-31, DONE): Whitespace-only name normalisation; units keyed by PBS codes
Names are upper-cased, stripped and space-collapsed. This merges `YAZMAN ` → `YAZMAN` and `LIAQUATPUR ` → `LIAQUATPUR`
(Cholistan tehsils that appeared with and without a trailing space under the **same** tehsil code), plus a trailing-space
variant of `BAHAWALPUR DIVISION` (same division code 8). No unit was renamed otherwise. The unit key is
`tehsil_uid = PB-<dist_code>-<teh_code>`. The script stops if any code maps to more than one normalised name.
Result: 150 raw (district, tehsil-name) strings → **148 tehsils**.

## D007 (2026-10-31, superseded, now DONE; see D007-final below): Which "others" to use
The detailed Table 8.1 (p. 479) prints Punjab "Others" = 5,184 (Excel `P8Q019`). The summary Table 8.1 (p. 54) prints
9,418 = NGO 1,054 + RSP 1,985 + Govt 1,195 + Others 5,184, which is a sum of non-exclusive mentions, not of mouzas. `n_others`
holds the detailed-table column (5,184). `n_ngo`, `n_rsp` and `n_govt` are kept separately, and no summed "others" is built.
**Ahmed to decide.**

## D008 (2026-10-31, DONE): Distance 0 to metalled road not banded
23 rural-populated mouzas (20 metalled-road, 3 bricked-road) record distance 0 km. The published Table 6.3 bands start
at 1 km and are filled only for mud-road mouzas, so these 23 are in no band. This matches the published counts exactly.

## D009 (2026-10-31, DONE): Script numbered 04, not 02
The brief asked for `02_extract_mouza.py`, but `02_extract_archives.py` (which produces this script's input) and
`03_inspect_raw.py` already exist. To keep run order it is `scripts/04_extract_mouza.py`.

## D010 (2026-10-31, DONE): Boundary join script numbered 05
The brief asked for `03_boundaries_join.py`. `03_inspect_raw.py` exists and this step needs `04_extract_mouza.py`'s
output, so it is `scripts/05_boundaries_join.py`.

## D011 (2026-10-31, DONE): OCHA boundary preparation
Used `pak_admin3` / `pak_admin2` (plain, not the `_em` variants), filtered to `adm1_name == Punjab`: 139 tehsils and
36 districts. All geometries are valid, so none were repaired. Reprojected to ESRI:102028; projected areas equal OCHA's `area_sqkm`
(ratio 1.0000). Saved as `data/interim/punjab_boundaries.gpkg` (`adm3`, `adm2`). No units dropped or renamed.

## D012 (2026-10-31, DONE): Crosswalk rules
Exact → normalized (generic rules only, listed in `match_audit.md`) → rapidfuzz WRatio proposals (≥ 60, within the
same district, among OCHA units not already matched). **Validated** = exact, normalized or Ahmed-accepted manual, and
the district is validated. Normalized matches are non-exact, so they are counted as validated for the gate but listed
for Ahmed's review (rule 4). Fuzzy proposals are never applied automatically. Ahmed accepts them by setting `decision = accept`
in `docs/crosswalk_manual.csv`. The script reads that file on every run and never overwrites it.

## D013 (2026-10-31, DONE): Join method
Only validated matches are joined. Counts of all census tehsils assigned to one OCHA polygon are **summed**, then shares
are recomputed (never averaged). This also covers accepted many-to-one cases (Bahawalpur, Gujranwala Saddar + City) and,
if chosen, Cholistan option A. OCHA polygons without a validated match keep null values (`match_status`).

## D014 (2026-10-31, superseded by D024/D030: administrative assignment now 100%, gate GO, Q1 at tehsil): Gate = NO-GO; district fallback built
Validated tehsil matches cover 20,612 / 23,130 rural populated mouzas (89.1% < 95%). The `district_fallback` layer sums
tehsil counts to census districts and recomputes shares. It covers 22,156 mouzas (95.8%). Layyah (district proposal
→ Leiah, 651 mouzas) and Cholistan (323) are not validated. If Ahmed accepts the tehsil proposals in
`docs/crosswalk_manual.csv`, tehsil coverage would be 97.0% (fuzzy proposals only) or 99.9% (plus Cholistan option A
and the two former tribal areas). Lawa (17 mouzas) would remain unmatched.

## D015 (2026-10-31, superseded, now DONE; see D015-final below): Cholistan: option A (merge into parent tehsils by PBS code) recommended; not applied
See `match_audit.md`. **Awaiting Ahmed's decision.**

## D016 (2026-10-31, CLOSED; see D016-final / D025 below): ESRI:102028 is centred at 125°E
The standing-rule CRS (Asia South Albers Equal Area Conic) has central meridian 125°E and standard parallels 7°N and 32°S.
It is designed for Southeast Asia and Australia. Areas are correct, since it is equal-area. Over Punjab (~72°E) the map is
rotated about 10.8° from true north, and shapes are sheared. The check map's north arrow is drawn to true north. Alternatives
for Ahmed to consider: a custom Albers equal-area centred on Punjab (e.g., lon_0 = 72, lat_1 = 28, lat_2 = 33), which keeps
equal area with little distortion. Changing it would change standing rule 7, so it is **Ahmed's decision**.

---

## D017 (2026-10-31, DONE): Raster context: sources, CRS, resolution, resampling (`scripts/06_raster_context.py`)
- **Script number 06**: the brief's `04_raster_context.py` is taken.
- **WorldCover source:** the Zenodo record (doi:10.5281/zenodo.7254221) offers only 60° macrotile zips. Punjab needs
  N30E060 + S30E060 (17.5 + 9.9 GB). The identical v200 product is served by ESA's official public AWS bucket as 3°×3°
  tiles. Only the 7 tiles intersecting Punjab (N27E069, N27E072, N30E069, N30E072, N30E075, N33E069, N33E072; ~0.9 GB)
  are downloaded. Zenodo DOI cited as the dataset reference.
- **Travel time source:** MAP public GeoServer WCS, coverage `Accessibility__201501_Global_Travel_Time_to_Cities`,
  clipped server-side to 69–76°E, 27–35°N. No login or Earth Engine needed. Values are int32 minutes, nodata −9999. The WCS
  reports a placeholder unit (W·m⁻²·sr⁻¹); the paper defines the values as minutes.
- **CRS:** rasters stay in their native EPSG:4326 grids (no raster reprojection, so no resampling of categorical or
  integer data). Polygons (ESRI:102028) are reprojected to EPSG:4326 for zonal statistics only.
- **Resolution / resampling:** cropland mask = class 40 on the 10 m (1/12000°) grid. Valid = class ≠ 0. Block-averaged
  10×10 → 1/1200° (~93 m × 80 m at 30°N) cropland fraction, before any zonal statistics (this is average resampling). For travel-time weights, a
  further exact 10×10 block average → 1/120°, which nests exactly in the travel-time grid. No 10 m travel-time surface is created.
- **Zonal rule:** a cell belongs to a polygon if its centre lies inside (rasterize, all_touched = False). Cells are equal-angle,
  not equal-area; within one district the cos(latitude) area difference is about 1%, and it is ignored.
- **Cropland-weighted travel time:** for each polygon, Σ(tᵢ·cᵢ)/Σcᵢ over 1 km cells, where cᵢ is the cell's 2021
  cropland fraction. A weighted median is also reported. This summarises modelled travel time where cropland is,
  not where farmers live.

## D018 (2026-10-31, PRESPECIFIED before running `scripts/07_spatial_stats.py`): Spatial statistics plan
- **Unit:** decided by the gate (D014). The script recomputes it: tehsil if validated coverage ≥ 95%, else district.
  Currently **district** (no review decisions recorded in `docs/crosswalk_manual.csv`).
- **Units dropped from the analysis:** polygons with undefined `arhti_share`. At district level that is Leiah (match
  unvalidated, D014) and Lahore (0 rural populated mouzas). Weights are built on the remaining polygons.
- **Primary weights:** Queen contiguity (libpysal `Queen.from_dataframe`, on ESRI:102028 polygons), row-standardised.
- **Sensitivity weights:** k-nearest neighbours, k = 5, on polygon centroids in ESRI:102028, row-standardised.
- **Inference:** 999 conditional permutations, seed **20261031** for every run. Significance threshold p < 0.05 (pseudo
  p-value). Also report p < 0.01 as a stricter check, and the count under an FDR (α = 0.05) bound for LISA.
- **Islands / disconnected components:** reported. Any island would be dropped from that weights object and listed.
- **Global Moran's I:** `arhti_share`, `commercial_share`. Report I, E[I], z (permutation-based and normality-based), pseudo p.
- **LISA:** `arhti_share`. Labels High-High, Low-Low, High-Low, Low-High, not significant, under both thresholds.
- **Bivariate LISA:** x = `arhti_share` at i, y = spatial lag of `commercial_share` (esda `Moran_Local_BV`), with a global bivariate Moran's I.
- **Descriptive OLS (exploratory):** `arhti_share ~ commercial_share + ztbl_share + onlinebank_over25km_share +
  tt_city_cropw_hours + cropland_share + road_metalled_share`. Here `onlinebank_over25km_share` = (26–50 km + 51+ km
  bands)/rp_mouzas. The 51+ band alone is zero in 11 of 34 districts (207 mouzas Punjab-wide), so it is too sparse.
  `tt_city_cropw_hours` = cropland-weighted mean travel time / 60. HC3 robust SEs (small n), VIFs, Moran's I on
  residuals (999 permutations, Queen), plus spreg's Moran/LM residual diagnostics.
- **Spatial error model:** fitted (spreg ML_Error, Queen) if residual Moran's I has p < 0.05, and compared with OLS
  (coefficients, λ, log-likelihood, AIC).
- **kNN rerun:** global Moran's I and LISA for `arhti_share` under kNN-5, compared unit by unit with Queen.
- **Vintages differ** (Mouza Census Jan–Mar 2020; WorldCover 2021; MAP 2015) and every output states them. The results are
  associations only.

## D019 (2026-10-31, superseded by D019-final below): Additions and departures from D018 after the run
- **Added (not prespecified):** a leave-one-district-out jackknife of OLS and SEM coefficients (`outputs/tables/jackknife_posthoc.csv`).
  It is labelled post-hoc in every output.
- **Not acted on:** the LM diagnostics favour a spatial *lag* specification (robust LM lag p = 0.007 vs robust LM error
  p = 0.073). D018 prespecified only an error model, so no lag model was fitted. **Ahmed to decide** whether to add one, as
  an explicitly post-hoc check.
- Dropped from the district analysis: Lahore (0 rural populated mouzas) and Leiah (unvalidated match). n = 34.

## D020 (2026-10-31, FEASIBILITY ONLY, nothing built): Mouza Census 2008 comparison
- **Obtainable from PBS (checked 2026-10-31):** `Mouza_spss_2008.rar` (Punjab.sav: full variable set, but variables are
  unlabelled `FLD###`); `Mouza-Census-2008-Excel.rar` (Punjab file holds only fields 197–209 and has exactly 16,384 rows, the old
  Excel row limit, so it is likely truncated); the 2008 questionnaire and manual (scanned images, no text layer); the country report
  tables (`Country-Report-on-Mouza-Census-2008-Table-1-to-29-Questionnaire-PDF.pdf`, province level only). The 2008
  Punjab provincial report link returns 404, so no published district/tehsil tables were found.
- **Comparable item:** 2008 Table 8 reports "mouzas reporting credit facility by type of institution **and by gender**"
  (separate male and female availability), with 9 source columns including "Arthi/Commission agent". The PDF text layer
  scrambles the header order, and a footnote suggests some categories are combined (ZTBL / RSP / Government). Punjab rural
  populated mouzas: 23,941 (2008) vs 23,130 (2020).
- **Boundaries:** Chiniot district was created from Jhang after 2008 [CHECK year], so a district comparison would need
  Jhang + Chiniot merged in 2020. Other district changes 2008–2020 [CHECK]. Tehsil-level comparison is not advisable.
- **Assessment:** feasible at **district** level only, after (1) mapping `FLD###` variables to questions from the scanned
  questionnaire by hand, (2) validating the reconstructed Punjab totals against the 2008 country report, (3) deciding how the
  gender-split 2008 question maps to the single 2020 item, and (4) aggregating Jhang + Chiniot. Validation below province
  level would not be possible without the provincial report.

---

## D021 (2026-10-31, PRESPECIFIED before running `scripts/08_credit_allocation.py`): Credit-allocation definitions
- **Script number 08**: the brief's `06_credit_allocation.py` is taken.
- **SBP source:** `DistrictWise-Detail-Jul-Jun-2024.xlsx`, Punjab FARM-sector block only (non-farm ignored). The district rows
  are banks' lending by booking district, including an Islamabad row. The "MFIs" row (Punjab-wide only, subsistence columns
  only) and the "All Punjab" row (= district Total + MFIs) are used **only** for province-level validation and the headline.
  They are never used in district measures.
- **Thresholds:** read from CL1-Annex Table 2.7 by the script (stop if not found).
- **Small farms** = Ag Census size classes Under 1.0 … 7.5–<12.5 acres (sum of 5 classes), the closest match to SBP
  "up to 12.5 acres". **Large-farm operated area** = classes 50–<100 and 100+ acres, the closest match to SBP "above 50".
- **Measures:** `small_farm_reach` = SBP subsistence-holding disbursed borrowers / small farms × 1,000.
  `tenant_share` = tenant farms / all farms; `owner_cum_tenant_share` separately. `large_farm_area_share` = farm area of
  ≥50-acre farms / all farm area ("concentration of operated area"). `avg_loan_size_<cat>` = disbursed amount × 10⁶ /
  disbursed borrowers (Rs), used **only** as a data-quality flag.
- **Data-quality flags (SBP rows, before any matching):** (F1) avg loan size in any category > 5× or < 0.2× the median of
  Punjab district rows for that category. (F2) above-economic disbursement > 75% of the district's farm-sector
  disbursement (i.e., > 3× subsistence + economic combined). Categories with < 20 borrowers are not loan-size-flagged
  (ratio unstable) but are listed.
- **Islamabad** is dropped from all Punjab analysis (not part of Punjab; not in the Ag Census or OCHA Punjab).
- **Crosswalks** (SBP ↔ OCHA ADM2; Ag Census ↔ OCHA ADM2; branch list ↔ OCHA ADM2): same rules as D012 (exact /
  normalized = validated; fuzzy = proposal). Proposals go to `docs/crosswalk_manual_district.csv` for Ahmed and are
  **excluded until accepted**.
- **Cholistan Area** (Ag Census, separate unit under Bahawalpur division; no SBP or OCHA counterpart): excluded from
  district denominators pending Ahmed's Cholistan decision (D015). The size of the exclusion is reported.
- **Mouza Census variables:** `arhti_share` and `commercial_share` from the district fallback layer (tehsil counts summed to
  districts, shares recomputed; D014).
- **Spatial statistics:** Global Moran's I for `small_farm_reach` with the D018 weights. Primary Queen, row-standardised;
  sensitivity kNN-5; 999 permutations; seed 20261031; p < 0.05 (p < 0.01 stricter).
- **"Two kinds of exclusion":** `commercial_share` ≥ sample median AND `small_farm_reach` ≤ sample 33.3rd percentile, among
  districts with both values. Wording: "consistent with barriers beyond physical distance".
- **Concentration curve:** districts sorted by `small_farm_reach` ascending. x = cumulative share of small farms, y =
  cumulative share of subsistence borrowers. A concentration coefficient (1 − 2 × area under the curve) is reported as a
  descriptive summary of concentration only.
- **Sensitivity:** everything rerun excluding F1/F2-flagged districts.
- **Correlations in scatter plots:** Spearman ρ with n, descriptive only.

## D022 (2026-10-31, partly superseded by D024: D.G.Khan, Jehlum, Layyah accepted; Q2 n = 36): Credit-allocation crosswalks and exclusions (`scripts/08_credit_allocation.py`)
- **Ag Census → OCHA ADM2:** 35 normalized (suffix " DISTRICT" dropped), validated. `LAYYAH DISTRICT` → Leiah is fuzzy-proposed (60).
- **SBP → OCHA ADM2:** 31 exact plus 2 normalized (`Mandibahauddin`, `Rahimyar Khan`), validated. Proposed, awaiting review:
  `D.G.Khan` → Dera Ghazi Khan (72), `Jehlum` → Jhelum (83), `Layyah` → Leiah (60).
- **Branch list → OCHA ADM2:** `Rajan Pur` normalized. `D.G.Khan` and `Layyah` proposed.
- **Effect:** Dera Ghazi Khan, Jhelum and Leiah have no `small_farm_reach` until Ahmed accepts the rows in
  `docs/crosswalk_manual_district.csv`. Analysis n = 33 (32 where arhti_share is needed; Lahore has no rural mouzas).
- **Dropped:** Islamabad (SBP row; not Punjab). **Excluded from denominators:** Cholistan Area (19,536 farms, 0.4%) pending D015.
- **MFIs** (74,494 borrowers, Rs 5,127.5 mn; Punjab-wide only) are used only in the province headline.
- **Flagged (D021 rules, applied as written):** Rawalpindi (F1 + F2), Lahore (F1 + F2), Faisalabad (F1), Chakwal (F1, low side),
  plus Islamabad (dropped) and Jehlum (F1, subsistence 38.7× median; unmatched anyway). Suspects named in the brief but **not flagged**
  under the prespecified thresholds: Rahim Yar Khan (above-economic 71% of amount), Multan (55%). Thresholds were not changed.

## D023 (2026-10-31, DONE): Figures and QGIS package
- **Script numbers 09/10**: the brief's `07_figures.py` is taken. `10_export_qgis.py` writes `outputs/arhti_project.gpkg`.
- **Classification rule (all choropleths):** 5-class Fisher-Jenks unless a class holds < 3 units, otherwise 5-class quantiles.
  Both GADFs are reported (`outputs/tables/classification_comparison.csv`, Fig S1). Result: natural breaks for tehsil arhti_share
  (GADF 0.821 vs 0.785) and rp_mouzas (0.757 vs 0.700); **quantiles** for district small_farm_reach (Fisher-Jenks put 2 districts
  in its top class). The bivariate map uses tertiles by design.
- **Units by figure:** descriptive tehsil maps (Figs 2–3) show validated tehsils only, with unvalidated polygons hatched.
  Inferential maps (Fig 4) use districts, per the gate (D014).
- **Colour:** dataviz reference palette. Sequential ramps validated as ordinal (light end ≥ 2:1 contrast); 3 categorical slots
  validated all-pairs. Bivariate: J. Stevens 3×3 scheme. LISA: red/blue poles with a neutral grey.
- **North arrows** point to true north (D016). Figure 6 (now appendix Figure S6) is a chart, so it has no north arrow or scale bar.
- **Script 08 changed:** it now saves `outputs/tables/sbp_province_headline.csv` and stores `flagged` as nullable 0/1. A text-typed
  field had made flagged districts count as 0 on a draft map. Results are unchanged.


---

# Decisions of 2026-10-31 (second round), decided by Ahmed

## D024 (2026-10-31, DONE, decided by Ahmed): Crosswalk decisions recorded
- Files: `docs/crosswalk_manual.csv` (tehsils) and `docs/crosswalk_manual_district.csv` (districts, every source). Every row keeps
  source name, source code, source district, OCHA name, OCHA p-code, match_type, decision, decided_by ("Ahmed"), date and
  historical_name. Original census names and codes are never overwritten.
- match_type values: **spelling** (9: Kot Chhutta→Kot Chatta, Sammundri→Summundri, Kot Radha Kishon→Kot Radha Kishen,
  Nowshera (Khushab)→Naushera, Mainwali→Mianwali, Liaquatpur (Rahim Yar Khan)→Liaqatpur, Sheikhupra→Sheikhupura, Layyah→Leiah,
  18-Hazari→Athara Hazari); **normalized** (11 rule-based); **rename** (2: De-excluded Area D.G. Khan→D.G Khan (Tribal Area)
  PK60701, also known as Koh-e-Suleman; De-excluded Area Rajanpur→Rajanpur (Tribal Area) PK62903); **parent_aggregation** (8:
  Bahawalpur Saddar + City→Bahawalpur; Gujranwala Saddar + City→Gujranwala; Lawa (17 mouzas)→Tala Gang PK60504, whose OCHA polygon
  (~2,975 km²) is consistent with the pre-split combined Talagang; Cholistan option A: PB-999-071→Fort Abbas, PB-999-079→Yazman,
  PB-999-081→Liaqatpur). Lahore's Model Town, Raiwind, Shalimar are left unmatched (0 rural populated mouzas).
- Districts: D.G.Khan→Dera Ghazi Khan, Jehlum→Jhelum, Layyah→Leiah accepted as spelling for the Mouza Census, SBP, Ag Census
  and branch list.
- Rules enforced in `05`/`08`: numerators and denominators are summed before shares are recomputed (never averaged); no source unit
  is assigned twice (checked); no harmonized district or tehsil identifier is duplicated (checked); harmonized totals reconcile to
  23,130 rural populated mouzas (option A; 22,807 under option B). **Administrative assignment: 23,130 / 23,130 (100%).**

## D015-final (2026-10-31, DONE, decided by Ahmed): Cholistan
Option A is primary: the Cholistan tehsils are summed into Fort Abbas, Yazman and Liaqatpur. Option B (exclude Cholistan) is a
required sensitivity scenario, run from the same processed file (`is_cholistan` flag; layers `*_optB`). Every tehsil
classification, LISA label and summary statistic that changes under B is listed in `outputs/tables/cholistan_sensitivity.csv`.
A change that affects a main conclusion must be reported in the main text. Maps carry the note that Fort Abbas, Yazman and
Liaqatpur combine desert (Cholistan) and irrigated mouzas.

## D007-final (2026-10-31, DONE, decided by Ahmed): "others"
Use the detailed-table Others (5,184 for Punjab). Keep n_ngo, n_rsp and n_govt separate. Never build or report a summed
"others" as a count of distinct mouzas.

## D019-final (2026-10-31, DONE, decided by Ahmed): Models
The spatial error model remains the prespecified check. A spatial lag model is added as a POST-HOC exploratory comparison.
For both, report weights, coefficients, uncertainty, residual diagnostics and n, and never choose on significance. Both belong
in the paper's appendix; the main text leads with clustering and descriptive results. (Implemented in `07`: OLS + SEM + SLM,
LM diagnostics, residual Moran's I for all three, POST-HOC jackknife ranges.)

## D027 (2026-10-31, DONE, decided by Ahmed): Coverage language
"Administrative assignment" (the share of rural populated mouzas assigned to a polygon) is distinct from geographic
precision. Aggregated units (parent_aggregation) conceal internal differences. This wording is used in methods and captions.

## D028 (2026-10-31, DONE, decided by Ahmed): Q1 sample
Units with zero rural populated mouzas (Lahore Cantt and Lahore City tehsils; Lahore district) have undefined shares and are
excluded from Q1 statistics but kept in Q2. n is reported for every analysis (Q1 tehsil n = 137; district comparison n = 35;
Q2 n = 36).

## D016-final / D025 (2026-10-31, DONE, decided by Ahmed): Analysis CRS changed
Standing rule 7 now uses a custom Albers equal-area projection centred on Punjab:
`+proj=aea +lat_1=28 +lat_2=33 +lat_0=30 +lon_0=72 +datum=WGS84 +units=m +no_defs` (`scripts/common.py: CRS`). Reason:
ESRI:102028 is centred at 125°E. It rotated Punjab about 10.8° and distorted distances (e.g., Attock–Bahawalpur centroid distance
419 km in ESRI:102028 vs 519 km geodesic). Every use of ESRI:102028 in `scripts/` has been replaced. Verification
(`outputs/tables/crs_verification.csv`):
- 5 centroid pairs agree with geodesic distances within 0.06% (old CRS: −19% to +17%).
- Unit areas are unchanged vs the previous run (max relative difference 6×10⁻⁶ districts, 1.3×10⁻⁵ tehsils; both CRSs are equal-area).
- Grid north is within 0.06° of true north at the Punjab centroid, so north arrows point straight up.
- These checks and the kNN-5 neighbour-change tables are rebuilt by `scripts/07_spatial_stats.py` (`crs_verification()`), comparing against ESRI:102028 directly. The rebuilt grid-north angle is −0.06° at the centroid of all 36 districts (−0.061° in the first, one-off check, which used a slightly different reference point); every other value is unchanged. Added 2026-11-23.

## D026 (2026-10-31, DONE, decided by Ahmed): kNN weights from geodesic distances
kNN-5 weights are built from GEODESIC distances between unit centroids (centroids computed in the analysis CRS; distances on the
WGS84 ellipsoid via `pyproj.Geod`; ties broken by stable index order; `common.geodesic_knn`), so they do not depend on the
projection. Compared with the previous planar ESRI:102028 kNN on the same units, the neighbour set changed for 22 of 35
districts and 93 of 137 tehsils (`outputs/tables/knn5_neighbour_changes_{district,tehsil}.csv`).

## D029 (2026-10-31, DONE, decided by Ahmed): Presence, availability and allocation kept separate
- **PRESENCE** (physical facilities): onlinebank_in_mouza_share, onlinebank_over25km_share (Mouza Census 2020); branches per 10,000
  farms = branches_scheduled (SBP list, 30 Jun 2024) / Ag Census farms × 10,000 [superseded by D034: RURAL branches].
- **AVAILABILITY** (reported credit sources): commercial_share, ztbl_share, coop_share, mfb_share, arhti_share (Mouza Census 2020).
- **ALLOCATION** (who formal credit reaches): small_farm_reach = reported subsistence-holding borrower records per 1,000 farms
  under 12.5 acres (SBP FY2023-24, by booking district; borrower records may not be unique individuals).
- The Figure 5 classification is renamed "High reported commercial-bank credit availability, low small-farm reach". A parallel
  PRESENCE classification ("High branch presence, low small-farm reach": branches per 10,000 farms in the top half) is added. The
  phrase "bank presence" is never used for commercial_share.

## D030 (2026-10-31, DONE, decided by Ahmed): Q1 unit, MAUP comparison, LISA reporting, extra tables
- The gate passes (100% administrative assignment), so Q1 spatial statistics run at **tehsil** level with the D018 weights,
  permutations and seed. District results are kept as a labelled MAUP comparison. Q2 stays at district level.
- LISA maps and tables state counts at p < 0.05, p < 0.01 and FDR 0.05. Maps outline FDR survivors with a heavy border.
- POST-HOC exploratory association table (`outputs/tables/exploratory_associations.csv`): Spearman correlations of arhti_share with a
  fixed list. Raw and Benjamini–Hochberg p-values within each level × scenario family. Branches per 10,000 farms are available at
  district level only (farms are not published by tehsil).
- Q2 tenure table (`outputs/tables/q2_tenure_associations.csv`): Spearman correlations of small_farm_reach with tenant_share,
  owner_cum_tenant_share and large_farm_area_share, all districts and excluding flagged districts. BH-adjusted within each family.

## D031 (2026-10-31, DONE): Implementation notes
- Script numbering kept in run order. `07` was rewritten (Q1 at the gated unit, scenarios A/B, three models). `11_qgis_project.py`
  (QGIS's own Python) builds `outputs/arhti_project.qgz` and `outputs/qgis_styles/*.qml`. Shared definitions live in `scripts/common.py`.
- Superseded outputs removed: `ols_arhti.csv`, `ols_diagnostics.csv`, `sem_arhti.csv`, `jackknife_posthoc.csv`,
  `lisa_bivariate_arhti_commercial.csv`, `fig4_lisa_arhti_district.*` (now Figure S2), `check_map_arhti.png`,
  `concentration_curve_small_farms.png`. The pre-change outputs are kept in `data/interim/previous_run_snapshot_2026-10-31/`.
- Field aliases in `outputs/arhti_project.gpkg` were verified to display in QGIS 4.2.3 (headless PyQGIS).


## D032 (2026-10-31, DONE, decided by Ahmed): Scope of standing rule 12
Rule 12 covers the group's OWN fieldwork sites and interview locations. Town-level locations of PUBLISHED studies (IGC 2013 arhti
interviews; PMN/MEDA 2019 focus groups) may be shown as CONTEXT only, never as data for statistics or choropleths. The project rules
(`docs/project_rules.md`) were amended accordingly.

## D033 (2026-10-31, DONE): Literature context layer: geocoding method and coordinates
- Input: `docs/literature_evidence.csv` (values supplied by Ahmed only; nothing looked up or inferred). Chichawatni and Depalpur
  have no crop in the brief and are left blank.
- Method: OpenStreetMap Nominatim search API, query "<town>, Punjab, Pakistan", `countrycodes=pk`, 1.2 s between requests, project
  User-Agent, retrieved 2026-10-31. Raw responses are cached in `data/raw/geocoding/nominatim_literature_locations.json` (reruns reuse
  the cache). Rule: highest-importance result of class `place` with type city/town/village; otherwise the highest-importance result.
  The expected district is NOT used to choose, so the district check is an independent check.
- Every point has `location_precision` = "town centre, approximate". Tehsil and district come from a spatial join with the OCHA ADM3
  layer in the analysis CRS.

| Location | Lon | Lat | Source | OCHA tehsil | OCHA district | District check |
|---|---|---|---|---|---|---|
| Nankana Sahib | 73.70910 | 31.45487 | OSM Nominatim node/2667308200 (place/town), retrieved 2026-10-31 | Nankana Sahib | Nankana Sahib | match |
| Jalalpur Bhattian | 73.37776 | 32.06344 | OSM Nominatim node/2447971011 (place/town), retrieved 2026-10-31 | Pindi Bhattian | Hafizabad | match |
| Khanpur | 70.65601 | 28.64774 | OSM Nominatim node/281405781 (place/city), retrieved 2026-10-31 | Khanpur | Rahim Yar Khan | match |
| Khanewal | 71.92789 | 30.30225 | OSM Nominatim node/251165455 (place/city), retrieved 2026-10-31 | Khanewal | Khanewal | match |
| Sahiwal | 73.11106 | 30.67151 | OSM Nominatim node/251318496 (place/city), retrieved 2026-10-31 | Sahiwal | Sahiwal | match |
| Okara | 73.44933 | 30.80913 | OSM Nominatim node/251318194 (place/city), retrieved 2026-10-31 | Okara | Okara | match |
| Chichawatni | 72.69140 | 30.53169 | OSM Nominatim node/251321140 (place/city), retrieved 2026-10-31 | Chichawatni | Sahiwal | match |
| Depalpur | 73.65137 | 30.66918 | OSM Nominatim node/281437566 (place/city), retrieved 2026-10-31 | Depalpur | Okara | match |
| Bahawalpur | 71.66387 | 29.39464 | OSM Nominatim relation/16117506 (boundary/administrative), retrieved 2026-10-31 | Bahawalpur | Bahawalpur | match |
| Sialkot | 74.54156 | 32.49449 | OSM Nominatim node/2408222266 (place/city), retrieved 2026-10-31 | Sialkot | Sialkot | match |

- Lower-confidence placements: **Bahawalpur** (no `place` result; the rule fell back to the administrative relation "Tehsil
  Bahawalpur City", whose representative point is used); **Khanpur** (8 place candidates named Khanpur; the highest-importance one is
  in Rahim Yar Khan, matching the table); **Sahiwal** (Sahiwal city in Sahiwal district chosen by the rule; a town named Sahiwal
  also exists in Sargodha district; the brief did not name the district).
- Scripts renumbered to keep run order: `11_literature_context.py` (new), `12_qgis_project.py` (was 11).
- Outputs: layer `literature_evidence` in `outputs/arhti_project.gpkg` and `data/processed/literature_evidence.gpkg`; Figure S3;
  `outputs/tables/literature_locations_context.csv` (descriptive; no statistics on these points).

## D034 (2026-10-31, DONE, decided by Ahmed): PRESENCE uses rural branches
`rural_branches_per_10k_farms` = `branches_rural` / Ag Census `farms` × 10,000, where `branches_rural` counts branches coded "R"
(rural) in the SBP list of scheduled bank branches as on 30 June 2024. It replaces all-branch density in the presence-based "two
kinds of exclusion" classification (Figure 5C) and in every presence variable. Reason: all-branch counts are dominated by urban
branches and measure urbanization rather than farm access. For example, Lahore has 190.4 branches per 10,000 farms in total but 3.9
rural (verified from the data: 1,798 vs 37 branches; 94,410 farms). `all_branches_per_10k_farms` is kept only as a labelled
SENSITIVITY column. The cut-points are unchanged in form: top half of rural_branches_per_10k_farms AND bottom third of small_farm_reach.

## D035 (2026-10-31, PRESPECIFIED before running; EXPLORATORY): Mouza-level co-occurrence of reported credit sources
- **Records:** mouza-level Mouza Census 2020 records, rural populated mouzas only (D005). Scenario A: Cholistan mouzas belong to
  their parent OCHA tehsils. Scenario B: Cholistan mouzas excluded.
- **Strata:** harmonized OCHA tehsil (the Q1 unit), via the crosswalk (D024).
- **Indicators per mouza (0/1):** arhti (code 8), commercial bank (code 3), ZTBL (code 1), online commercial bank in mouza (8.2 = yes).
- **(a) Pooled association:** Mantel–Haenszel pooled odds ratio of arhti vs X (X = commercial, ZTBL, online bank in mouza),
  stratified by tehsil, with 95% CI (statsmodels `StratifiedTable`). The Breslow–Day test of homogeneity uses the Tarone adjustment;
  the CMH test of OR = 1 is also reported. Strata with a zero row or column margin carry no information on the OR and are dropped
  from (a); the number dropped is reported. n (mouzas, strata) is reported for each test.
- **(b) Per tehsil (arhti × commercial):** observed share reporting BOTH; expected share under independence = share(arhti) ×
  share(commercial); ratio = observed / expected. **Not estimable** if the tehsil has fewer than 20 rural populated mouzas, or zero
  mouzas reporting arhti, or zero reporting commercial bank. The counts of tehsils with ratio > 1, < 1 and = 1 are reported.
- **(c) Map (Figure S4):** fixed diverging classes, symmetric on the log scale around 1: < 0.80, 0.80–0.95, 0.95–1.053, 1.053–1.25,
  > 1.25 (blue below 1, neutral grey around 1, red above 1). Not-estimable tehsils are hatched. Caption: "Within-tehsil
  co-occurrence of reported credit sources across mouzas; availability reports, not borrowing; association, not substitution or
  complementarity in behaviour."
- **(d) Privacy:** no mouza names or codes appear in any figure, table or the app. Outputs contain only tehsil aggregates and pooled
  statistics.
- Implemented inside `07_spatial_stats.py` (table) and `09_figures.py` (Figure S4), so the script numbering is unchanged.

## D036 (2026-10-31, DONE, decided by Ahmed): Benjamini–Hochberg cutoff stated with every FDR count
Every LISA caption and table that reports FDR counts states the Benjamini–Hochberg p-value cutoff used (esda `fdr`, α = 0.05;
computed separately for each level × scenario × weights run). esda returns the critical value k·α/n for the largest k with
p(k) < k·α/n. When NO p-value passes, esda returns α/n (a Bonferroni bound) instead. In that case true BH rejects nothing, so the
script labels no unit FDR-significant and reports the cutoff as "none" (`bh_fallback_bonferroni` = True). Checked on 2026-10-31:
the fallback occurred only in bivariate LISA runs (tehsil Queen; district Queen and kNN-5) and had flagged no unit, so no
earlier count changes.

## D037 (2026-10-31, DONE): Outputs added for the companion app; web copies (`scripts/18_export_web.py`)
No geographic unit was dropped, merged or renamed. To keep every number in the app traceable to `outputs/`:
- `08` now writes the concentration curve for BOTH samples (`concentration_curve.csv`, column `sample`) and
  `concentration_coefficients.csv` (previously the excluding-flagged curve and both coefficients existed only inside Figure 6).
- `09` appends app class breaks (D023 rule, scenario-A values) for every app map variable to `classification_comparison.csv`
  (figure = "App tehsil" / "App district" / "App district Q2"), adds `bins_exact` (full-precision breaks), and writes
  `outputs/tables/figure_numbers.csv` (the same numbers as `docs/figure_numbers.md`).
- `10` adds `q1_districts_mouza_census_2020_MAUP` and `q1_districts_cholistan_excluded_optB_MAUP` (district Q1 MAUP layers,
  with district LISA labels) to `outputs/arhti_project.gpkg`.
- `18_export_web.py` writes EPSG:4326 GeoJSON copies with `shapely.coverage_simplify` (shared edges stay shared; tolerance 0.0005° for
  tehsils/districts), each < 3 MB, feature counts asserted. Disbursement-amount and loan-size columns are dropped from every web
  table except `sbp_province_headline.csv` (rule 11). Web copies are for display only; statistics stay in the analysis CRS.
- Scenario-B maps use the scenario-A class breaks (as in `cholistan_sensitivity.csv`). The bivariate map is shown for scenario A
  only (Figure 3); the B layer's `bivariate_class` uses tertiles recomputed on B, whose cut-points are not in `outputs/`.

## D038 (2026-10-31, DONE, decided by Ahmed): Simplified and finalised presentation (no numbers changed)
- One main question for the paper and app: "Where is arhti credit available in rural Punjab, and how does its geography
  compare with formal banking?" Q1 is the main analysis; Q2 is presented as a second lens on a separate dataset and period.
- Figure 5 is now a single panel (small_farm_reach, flagged districts marked, province headline box with the booking-location
  caveat). The three-panel version is appendix Figure S5; the concentration curve is appendix Figure S6 (was Figure 6).
- Figure credit on every figure: "Ahmed Raza Khan Lodhi and Hasnain Akram, PPHA 38520, University of Chicago".
- `scripts/17_key_numbers.py` writes `outputs/tables/key_numbers.csv` and `docs/key_numbers.md`: every number used in the paper,
  app and slides, with source file, row filter and column. `scripts/18_export_web.py` exports only what the five-page app needs.
- Project rules for readers: `docs/project_rules.md`.

## D039 (2026-11-01, DONE, decided by Ahmed): Rule change for Part 3; new sources (ACCESS, ALLOCATION, REPORTING GEOGRAPHY, COST)
- **Rule change (rule 11):** district disbursement AMOUNTS may be mapped ONLY in the reporting-geography outputs
  (`scripts/13_reporting_geography.py`: Figure R1, Figure R2, `reporting_geography.csv`, the credit columns of
  `district_scorecard.csv`). Every such output is labelled "district as reported by SBP (attribution under verification)" until
  Ahmed confirms whether SBP's district is the lending branch's or the financed farm's. All other rules stand; existing outputs
  are unchanged.
- **Attribution evidence (Step 0):** the wording defining "district" in ACD Circular 2 of 2007 and AC&MFD Circular Letter 2 of
  2015 could not be read (sbp.org.pk returned HTTP 403 to every automated request). The local SBP files (DistrictWise-Detail
  workbook headers "Name of Districts"; DWS PDF; CL1 Annex) contain no definition. The earlier "booking district" wording
  (rule 11, `docs/validation_sbp.md`) was a project assumption, not an SBP quotation.
- **Holding classes:** SBP "up to 12.5 / above 12.5-50 / above 50 acres" matched to census classes "under 12.5 / 12.5-under 50 /
  50 and above"; farms of exactly 12.5 or 50 acres fall in different classes (not identifiable in the published classes).
- **Crop structure:** district areas of wheat, rice, cotton, maize and sugarcane from the Agricultural Census 2024 Punjab report,
  Tables 6.9-6.13 (column "area under crop", acres; checked against rendered page images) and Table 6.1 (total cropped area).
  Districts + Cholistan Area sum exactly to the Punjab row for every column. The Crop Reporting Service Punjab has district files
  for rice, cotton and maize (2022-25) but none was found for wheat or sugarcane, and the federal 2023-24 district edition was not
  published (latest found: 2022-23); the Agricultural Census was therefore used for all five crops (one source, one reference
  period: Rabi 2023-24 + Kharif 2024). Accessed 2026-11-01.
- **Lending rates:** SBP Monthly Statistical Bulletin Table 3.33 "Average Rate of Return on Advances of Specialized Agricultural
  Finance Institutions and Agriculture Lending of Commercial Banks" (simple average of June quarter end; percent per annum),
  September 2026 edition (PDF p. 90), checked against the June 2024 edition (PDF p. 89) for all 60 overlapping non-provisional
  values (all equal). Both editions are downloaded by `scripts/01_download.py` (accessed 2026-11-01).
- **Kissan Card:** registration opened 1 June 2024 (CM Special Monitoring Unit page); cards operational 15 October 2024 (Ahmed).
  Eligibility 1 to 12.5 acres; loan limit Rs 30,000 per acre capped at Rs 150,000 per season, i.e. sized on 5 acres (Punjab
  Portal, CM Kissan Card Scheme). Both dates are after the FY2023-24 SBP data period except the last month of registration.
- **Not on the rate axis:** PMN/MEDA 2019 ~180% focus-group markup (`docs/price_ladder_notes.md`).

## D040 (2026-11-01, DONE): District geography is the 36-district basis
SBP FY2023-24 district rows, the Agricultural Census 2024 district tables and the OCHA COD-AB boundaries (valid_on 2022-09-09)
all use the same 36 Punjab districts, so every district statistic is on that basis. Punjab has reportedly created further
districts since 2022 (for example Murree, Talagang, Wazirabad, Kot Addu and Taunsa; not verified here), so the 36 units do not
match the current administrative map. No unit was split or reallocated; maps and tables should state "36 districts (pre-split
boundaries as used by SBP FY2023-24 and the Agricultural Census 2024)". The Cholistan Area of the Agricultural Census is not a
district and is excluded from district ratios (as in D021); the SBP Islamabad row is reported separately.

## D041 (2026-11-24, DONE): Course-method extensions, QGIS print layouts, script renumbering
Added after the course slides and final-project rubric were reviewed. Every new analysis is **EXPLORATORY / post-hoc**
(not part of the prespecified D018 / D021 analyses) and is labelled so in tables, figures and text. No geographic unit was
dropped, merged or renamed.
- **`scripts/15_course_methods.py`** (new): weights sensitivity for global Moran's I (Queen; Rook; geodesic kNN-5; geodesic
  distance band = smallest threshold that leaves no tehsil without a neighbour; inverse distance within that band; all
  row-standardised) and Geary's C; Moran scatterplot (Figure S7); Getis-Ord Gi* (Queen including self, binary; p < 0.05 and
  Benjamini-Hochberg FDR 0.05; Figure S8); first- and second-order trend surfaces on tehsil centroids with a residual map and the
  residuals' Moran's I (Figure S9); index of dissimilarity (Duncan & Duncan 1955) for tehsils (mouzas reporting each source vs all
  rural populated mouzas) and districts (SBP subsistence borrower records vs farms under 12.5 acres; branches vs farms; counts
  only, rule 11); k-means typology of 35 districts on six standardised attributes, with and without location, k in 2..6 chosen
  by silhouette with a minimum type size of 3 (Figure S10); Tissot indicatrix for ESRI:102028 vs the analysis CRS (Figure S11);
  classification histograms with GADF (Figure S12); dasymetric dot layer (1 dot = 1,000 farms under 12.5 acres, sampled within
  each district's cropland cells with cropland fraction >= 0.25, seed 20261031) and a district point layer of SBP subsistence
  borrower records for proportional symbols. All spatial statistics: 999 permutations, seed 20261031.
- **`scripts/16_qgis_layouts.py`** (new, QGIS Python): Print Layouts for Figures 2-6 saved inside `outputs/arhti_project.qgz` and
  exported to `outputs/figures/*_qgis.{png,pdf}`. These QGIS versions are the paper's map figures; the matplotlib versions
  (09) stay for the app and the appendix. Figure 6 is new: dasymetric dots of small farms with Flannery-compensated proportional
  circles of borrower records (counts, district as reported by SBP).
- **Renumbering:** `15_key_numbers.py` → `17_key_numbers.py`; `16_export_web.py` → `18_export_web.py`, so scripts stay in run order.
- **Why no Euclidean buffer of cities or markets:** the OCHA capitals file has only provincial capitals and no mandi coordinates
  are available; geocoding them would add unverified locations. The Mouza Census distance bands to the nearest bank branch and
  grain market (in mouza, 1-10, 11-25, 26-50, 51+ km) are used as the multiple-ring buffer measure, and MAP travel time (a
  cost-distance surface) as the network/time measure.

## D042 (2026-11-24, DONE): Revisions after an external review
All new analyses are EXPLORATORY. No geographic unit was dropped, merged or renamed.
- **SBP coverage, primary basis = 36 districts.** Holding-class shares are now computed on the 36 district rows (banks only;
  Islamabad and the MFI row, which has no district, excluded) against census Punjab minus the Cholistan Area, so the province
  comparison uses the same units as the district analysis. The SBP All Punjab row (banks + MFIs, incl. Islamabad) is kept as a
  comparison (`holding_class_shares.csv`, columns `*_36` vs unsuffixed). Figure A1 shows the 36-district basis.
- **Agricultural Census class areas.** In the published Punjab Table 3, farm area ÷ farms exceeds the class's upper limit in
  three classes below 12.5 acres (2.5–<5: 5.38 ac; 5–<7.5: 9.08 ac; 7.5–<12.5: 15.02 ac); the other classes are within bounds.
  Cause unknown (classification basis, estimation, or a table error); not resolved here. Area shares by class are reported as
  indicative and H2 rests mainly on farm counts. Added to the limitations and to the human checklist (N5).
- **H1 against every formal source.** `07_spatial_stats.py` now pools within-tehsil Mantel-Haenszel odds ratios for arhti ×
  cooperative bank, × MFB and × any formal source (commercial, ZTBL, cooperative or MFB), and records each pooled 2×2 table.
  `15_course_methods.py` adds `course_h1_by_source.csv` (same-tehsil Spearman, bivariate Moran's I, odds ratio by source).
- **Market-access model** (`course_market_model.csv`): arhti_share on cropland share, share of mouzas > 50 km from a grain
  market, commercial and ZTBL availability, share > 25 km from an online bank, and cropland-weighted travel time (standardised);
  OLS (HC3), binomial GLM on mouza counts with quasi-binomial standard errors (dispersion computed by hand as Pearson χ²/df;
  statsmodels' `scale="X2"` returns a wrong value for two-column binomial data), and a spatial error model (Queen).
- **Wording.** H1 is "not supported as a uniform relationship" rather than "rejected"; H3 compares subsistence lending with
  cultivated area (its stated benchmark); the thesis is restated to what the analysis shows (arhti credit follows farmland and
  coexists with formal credit; recorded formal lending concentrates by holding size and in a few city districts).
- **Build fix.** `19_build_documents.py` dropped bullet continuation lines indented by two spaces, truncating the research
  questions, H1, H2 and the appendix list in the .docx; fixed.

## D043 (2026-11-24, DONE): Revisions after a second external review
All new analyses are EXPLORATORY. No geographic unit was dropped, merged or renamed.
- **Wording.** H1 results for ZTBL and "any formal source" are "statistically inconclusive" (point estimates slightly below 1,
  CIs include 1), not "no association"; the cropland association is reported as not robust to the spatial error model; the
  borderline results of the planned spatial error model (commercial availability +, distance to online banks −) are discussed;
  Table B5 is labelled "planned" (OLS and spatial error prespecified in D018/D019; spatial lag post hoc).
- **H1 completeness.** `07_spatial_stats.py` records the full 2×2 over all 23,130 mouzas (arhti × commercial; arhti × any formal)
  and per-tehsil shares (any formal; neither). `course_h1_by_source.csv` now fills the any-formal row (Spearman, bivariate Moran)
  and adds Benjamini-Hochberg adjustments across the five sources. New Figure S13 maps the share of mouzas reporting neither arhti
  nor any formal source (limited reported availability, not exclusion).
- **Market-distance bands** (`course_market_bands.csv`, Table B9): shares within 10 km, within 25 km and over 50 km of a grain market
  (Mouza Census bands), each in place of the market term of the exploratory model. Added after the first models; all bands reported.
- **H2/H3 sensitivity** (`course_h2_h3_sensitivity.csv`, Table B8): headlines without the flagged districts; a rule-based city group
  (five largest urban populations, Population Census 2023: Lahore, Faisalabad, Rawalpindi, Gujranwala, Multan); leave one city out;
  benchmarks using district farm counts within each holding class (`course_lq_class_farms.csv`). The paper's five city districts
  were chosen without a stated rule and are treated as an exploratory group.
- **Tables.** SBP coverage reconciliation (B6: 36 districts + Islamabad + MFIs = All Punjab), census class-area check (B7),
  representation ratios (class share ÷ farm share) in `holding_class_shares.csv`.
- **Wording of the screen.** "Average loan" replaced by "disbursement per borrower record" (08 flag reasons, methods).
- **Figures.** Figure 5's note now reads the 36-district figures from `holding_class_shares.csv`; Figure 3's key shows the tehsil count
  in each cell.
- **Not added:** a land-record (PLRA) eligibility condition for the Kissan Card; it could not be confirmed from an official page
  (checklist N6).

## D044 (2026-11-24, DONE): Revisions after a third external review
No geographic unit was dropped, merged or renamed; new results are EXPLORATORY.
- **Kissan Card eligibility** confirmed on the official Special Monitoring Unit page (smu.punjab.gov.pk/kissan-card, accessed
  2026-11-24): "Famers who own land and whose land record is available in PLRA will be entitled for loan"; holdings up to 12.5 acres;
  Rs 30,000 per acre up to Rs 150,000 per season. Added to the paper with the source. (Bank of Punjab and punjab.gov.pk pages did
  not load.)
- **Table B9 diagnostics:** n, coefficient SE and 95% CI, λ, AIC and residual Moran's I for each spatial error model;
  Benjamini-Hochberg and Holm adjustments across the three distance bands.
- **Aggregation:** the province-wide (unstratified) odds ratio for arhti × any formal source (1.26) is reported beside the
  within-tehsil Mantel-Haenszel estimate (0.95); overlap shares (79.9% of arhti-reporting mouzas also report a formal source).
- **City group wording:** "the five districts with the largest urban populations" (absolute urban population, Population Census
  2023, Table 1), not "most urban"; Table B10 lists them; the flagged-exclusion row of Table B8 keeps only Multan and Rahim Yar Khan.
- **Figures:** new QGIS Figure 7 (A: share of mouzas within 10 km of a grain market; B: share reporting neither arhti nor any formal
  source; classes include their lower bound, as in S13, which is now superseded in the paper); Figure R2 adds the subsistence
  disbursement series.
- **Document:** appendix tables on landscape pages with repeated header rows, integer formatting, renamed columns.

## D045 (2026-11-24, DONE): App synchronized with the paper; layout refresh
- **Content:** the app now shows the final paper's results: 36-district holding-class shares (with a toggle to the SBP All Punjab
  row), disbursement per borrower record and representation ratios, the census class-area note, H1 against every formal source
  (selector drives the bivariate map; classes use the Figure 3 rule and reproduce it exactly for commercial banks), grain-market
  proximity (map and Table B9 results), mouzas reporting neither source (map and counts), H3 robustness and benchmark selector
  (cultivated area / farms in the class / all farms), the Kissan Card land-record condition, and the repository link.
- **New data in app/data** (written by 15 and 18): `app_tehsil_access.csv` and `app_district_access.csv` (pooled shares, never
  averaged), the H1, market-band, sensitivity, reconciliation, census-check and class-LQ tables, and downsized figure images for the
  presentation story.
- **Amounts rule:** the overview and presentation story show the five-city share of above-economic disbursement as one labelled figure
  (district as reported by SBP), as the paper does; district amounts are still mapped only on the reporting-geography page.
- **Design:** finding-first overview (six equal-height cards), collapsible data-vintage notes, authors once plus a page footer, shared
  chart style, district tiles and comparison, and a guided seven-screen story in presentation mode. Internal notes and file paths
  removed from the Cost page; the PMN/MEDA focus-group markup is no longer shown there.

## D046 (2026-11-24, DONE): Verdict wording and conclusion
- **Wording.** Verdicts now state what the evidence shows instead of "not supported": H1, "the evidence favours coexistence
  (H1-alt) over gap-filling"; H2, "formal lending is disproportionate"; H3, "recorded lending is concentrated". The hypotheses,
  tests and numbers are unchanged; the hypotheses are not restated after the fact.
- **Conclusion.** The paper, slides, speaker notes, README and app now end on one stated conclusion: the arhti does not begin
  where the bank ends; the two systems overlap, and the sharpest contrasts in formal credit are by holding size and by where loans
  are recorded. Policy implications are hedged ("may be insufficient").
- No geographic unit was dropped, merged or renamed; no number changed.

## D047 (2026-11-24, DONE): Plainer, more direct prose in the paper
- **Style.** Abstract, introduction, discussion and conclusion rewritten in a plainer, more direct voice: the introduction opens with
  the puzzle already in the paper (farmers with bank accounts who still borrow from arhtis at a far higher implicit cost, Haq et al.
  2013), states the simple substitution story and the answer early, and the discussion and conclusion use short declarative
  sentences. Literature, methods, results and limitations are unchanged apart from removing one repeated sentence.
- **Unchanged:** hypotheses, tests, numbers, hedges and descriptive language. Body plus references still end on page 12 (limit:
  12 pages excluding figures).

## D048 (2026-11-24, DONE): Final paper voice, with the authors' opening account
- **Text.** Adopted the authors' final revision: the introduction opens with one author's professional observations from bank
  supervision (deferred fertilizer pricing, family ties to arhti families, documentation delays, religious views on deferred
  prices) before the province-wide evidence. Limitations state that the account is not a systematic sample or a Shariah ruling.
- **Edits on adoption.** Banned terms removed ("credit deserts"; "explain" wording); H1 verdict kept as "the evidence favours
  coexistence over gap-filling", with its reason; thesis paragraph restored; prose tightened so text and references still end on
  page 12 (limit: 12 pages excluding figures). Methods section unchanged.
- **New number.** 75.9% of mouzas not reporting arhti credit report a formal source (script 07, `share_nonarhti_mouzas_with_other`;
  key number `all_any_overlap_nonarhti`), shown beside the 79.9% overlap in the paper, slide 6 and the app. Rs 4,000 in the
  opening account is an author's illustrative observation, not data, and is allowlisted as such in the tests.
- No geographic unit was dropped, merged or renamed.

## D049 (2026-11-24, DONE): Review round on the final draft (religion, figure placement, Table B9, verification)
- **Conclusion.** Religion returns in the closing paragraph beside trust, collateral and flexible repayment ("a contract they
  regarded as permissible trade rather than interest"). The IGC questionnaire lists "religious reasons" among barriers to banks
  (PDF p. 66), so the point is grounded beyond the opening account.
- **Figures.** Figures 2, 7 and 5 now sit in the text beside the findings they show (`[Figure: file.png]` markers in
  `docs/paper_draft.md`, read by `scripts/19_build_documents.py`); the other figures stay in the Figures section, which says so.
  The rubric limit is 12 pages exclusive of figures: without the three inline figures, text and references end at mid-page 12;
  with them, at the same point on page 14 (the figures take exactly two pages).
- **Tables.** Table B9 (19 columns) is split into B9a (descriptives, OLS, quasi-binomial) and B9b (spatial error model). Table B2
  now points to Figure 7B; Figure S13, which is not in the paper, is no longer cited in the paper, the app story or the outline.
- **Verification.** Raw files: all 85 logged SHA-256 checksums match `docs/download_log.csv`. IGC 2013 figures machine-checked
  against the PDF (Table 11 on PDF p. 40; farmer-reported bank rates of 9 to 18 percent on p. 44; bank accounts pp. 6 and 44;
  325 markets pp. 5 and 24); `docs/human_checklist.md` updated. SBP district attribution remains unresolved: every sbp.org.pk page
  returned HTTP 403 to automated access (again), and neither the SBP workbook nor its PDF defines the district basis.
- **Replication.** `bash run_all.sh` from raw data (19 scripts, exit 0): raw files unchanged; all CSV tables and matplotlib PNGs
  byte-identical; all six QGIS layout PNGs pixel-identical; every layer of the five committed GeoPackages identical in attributes and
  geometry. Remaining byte differences are run dates, timings, file metadata and random IDs/colours in unused fallback symbols of
  the .qml styles. Tests 16/16.
- No geographic unit was dropped, merged or renamed; no number changed.
