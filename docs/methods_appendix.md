# Methods appendix

*Where the Bank Ends and the Arhti Begins: Geographic Access, Landholding Structure, and the Allocation of Agricultural
Credit in Punjab, Pakistan.* PPHA 38520 final project. This is a descriptive study; no estimate below is causal.
Decision numbers (D001 …) refer to `docs/decisions.md`. Every step is reproduced by `run_all.sh`.

## A0. Three concepts (D029)
- **PRESENCE**: physical facilities. Mouza Census online commercial bank in or > 25 km from the mouza; RURAL scheduled-bank branches
  per 10,000 farms (branches coded "R" in the SBP list as on 30 June 2024 ÷ Ag Census 2024 farms; D034). All-branch density is a
  sensitivity only: it is dominated by urban branches (Lahore 190.4 vs 3.9 rural per 10,000 farms) and measures urbanization.
- **AVAILABILITY**: credit sources reported as available in the mouza (Mouza Census 2020): commercial bank, ZTBL, cooperative bank,
  microfinance bank, commission agent/arhti.
- **ALLOCATION**: who formal credit reaches. `small_farm_reach` = reported subsistence-holding borrower records per 1,000 farms under
  12.5 acres (SBP FY2023-24, by booking district; borrower records may not be unique individuals).

## A1. Data sources
All files were accessed on **31 October 2026** (`docs/download_log.csv` has URLs, sizes and SHA-256 checksums).

| Source | Content used | Unit | Vintage / reference period |
|---|---|---|---|
| PBS, Mouza Census 2020: mouza-level records (`mc2020.excel-1.rar`) and Punjab report | Mouza status; credit sources (Table 8.1); online commercial bank distance (8.2); wholesale markets (6.7); road type / distance (6.3) | Mouza → tehsil | Fieldwork Jan–Mar 2020 (Punjab: Jan 2020) |
| SBP, *District-wise Agri Credit FY24* (xlsx + DWS PDF) | Farm-sector disbursed borrower records and amounts by holding category | District (booking location) | FY2023-24 (Jul 2023–Jun 2024) |
| SBP, *Indicative Credit Limits … 2022-23* (CL1 Annex) | Holding thresholds, Table 2.7 | Province | 2022-23; thresholds from Ag Census 2010 |
| SBP, list of scheduled bank branches | Branch counts (PRESENCE) | Branch | As of 30 June 2024 |
| PBS, Agricultural Census 2024 (Punjab report; `Table_1_District.xls`, `Table_3_District.xls`) | Farms, farm area, cultivated area by size class; farms by tenure | District | Ag year 2023-24; fieldwork Sep 2024 and Jan–Feb 2025; **sample-based** (district design, 15% MoE at 95%) |
| PBS, Population Census 2023, Table 1 | Tehsil list (corroboration only) | District / tehsil | 2023 |
| OCHA COD-AB Pakistan (HDX) | ADM1–ADM3 polygons, p-codes | Province / district / tehsil | `valid_on` 2022-09-09 |
| ESA WorldCover 10 m 2021 v200 (doi:10.5281/zenodo.7254221), 7 tiles from ESA's AWS bucket | Cropland mask (class 40) | 10 m | 2021 |
| Malaria Atlas Project, Accessibility to Cities 2015 (Weiss et al. 2018) via MAP WCS | Modelled travel time to the nearest city | ~1 km | Nominal 2015 |
| **CONTEXT only:** Haq, Aslam et al. (IGC/NIBAF/PMN) 2013, *Who is the Arthi?* (https://www.theigc.org/sites/default/files/2014/09/Aslam-Et-Al-2013-Working-Paper.pdf) | Annualized implicit interest by crop (Table 11, p. 39); 8 market towns (Figure S3) | Crop (not location) | Interviews 2012; 18 arthis, purposive |
| **CONTEXT only:** PMN/MEDA 2019, *Warehouse Receipt Financing* (https://www.meda.org/wp-content/uploads/2019/12/PMN-Warehouse-Receipt-Financing-Case-Study-Nov-2019.pdf) | Reported markup ~180% from focus groups (pp. 19, 23); 2 focus-group towns | Focus group | 2018; non-representative |

## A2. Processing steps (in run order)
1. **`01_download.py`** downloads the sources to `data/raw/` (never modified; D001).
2. **`02_extract_archives.py`** extracts the RAR and shapefiles to `data/interim/` (D002). **`03_inspect_raw.py`** inspects the files.
3. **`04_extract_mouza.py`** filters to Punjab (26,462 mouzas; ICT excluded, D003). Rural populated = rural + partly urban + populated
   forest (D005). Counts per tehsil by PBS codes (148 census tehsils, D006). **Validation:** 9,628 / 9,628 published count cells of
   Tables 1.1, 6.3, 6.7, 8.1, 8.2 match. Jand and Pindi Gheb (Table 1.1), unreadable in the PDF text layer, were checked visually
   against rendered page images (PDF p. 79, all values match); human check pending (`docs/human_checklist.md`).
4. **`05_boundaries_join.py`** builds the crosswalks from automatic matching plus Ahmed's decisions (A4). Counts are summed per OCHA
   polygon and shares recomputed (never averaged). It builds Cholistan options A and B.
5. **`06_raster_context.py`**: cropland share and travel time (A3).
6. **`07_spatial_stats.py`**: Q1 spatial statistics at the gated unit, the MAUP comparison, Cholistan scenarios, three models (A6).
7. **`08_credit_allocation.py`**: SBP and Ag Census extraction, Q2 measures, data-quality screen, classifications, concentration
   curve, tenure and post-hoc association tables (A6).
8. **`09_figures.py`**: Figures 1–5, S1, S2, S4–S6. **`10_export_qgis.py`**: `outputs/arhti_project.gpkg` with field aliases.
9. **`11_literature_context.py`**: CONTEXT only. Geocodes published-study towns (OSM Nominatim), builds Figure S3 and a descriptive
   cluster-context table; no statistics on these points (D032–D033).
10. **`12_qgis_project.py`** (QGIS Python): `outputs/arhti_project.qgz` + `.qml` styles. **`13_reporting_geography.py`** and
   **`14_cost_context.py`**: holding classes, LQs, scorecard; lending rates and price ladder.
11. **`15_course_methods.py`**: EXPLORATORY extensions (A9). **`16_qgis_layouts.py`** (QGIS Python): Print Layouts for Figures 2–6,
   exported to `outputs/figures/*_qgis.{png,pdf}` and saved in the project.
12. **`17_key_numbers.py`**: every number in the text with its source file and row. **`18_export_web.py`** writes simplified web
   copies for the app (`app/data/`, with a checksum manifest). **`19_build_documents.py`**: the paper (`outputs/paper/arhti_paper.docx`)
   and the slides (`outputs/slides/arhti_slides.pptx`) from `docs/paper_draft.md` and `docs/slide_text.md`.

## A3. CRS, resolution and raster processing
- **Analysis CRS (D025):** custom Albers equal-area centred on Punjab, `+proj=aea +lat_1=28 +lat_2=33 +lat_0=30 +lon_0=72
  +datum=WGS84 +units=m`. It replaced ESRI:102028, which is centred at 125°E and rotated Punjab ~10.8° (Attock–Bahawalpur centroid
  distance 419 km vs 519 km geodesic). In the new CRS, 5 centroid distances agree with geodesic within 0.06%, unit areas are unchanged
  (both equal-area; max relative difference 1.3×10⁻⁵), and grid north is within 0.06° of true north (`outputs/tables/crs_verification.csv`).
- **Rasters** stay in native EPSG:4326 grids. Polygons are reprojected for zonal statistics only (D017).
- **Cropland:** WorldCover class 40 at 10 m, block-averaged 10×10 to ~100 m before zonal statistics. `cropland_share` = mean fraction
  over cells whose centre is in the polygon. It is a land-cover mask, not crop type, irrigation or farm area. Checks: 6 random
  ~100 m cells recomputed from the tiles matched exactly.
- **Travel time:** MAP ~1 km minutes. Cropland weights are an exact 10×10 aggregation of the ~100 m fraction.
  `tt_city_cropw_mean_min` = Σ(tᵢcᵢ)/Σcᵢ. This is modelled travel time to the nearest city, not to banks or markets, and not
  farmers' observed travel.

## A4. Crosswalks and administrative assignment
- **Match types (D024):** exact; normalized (generic rules); **spelling** (spelling/transliteration); **rename** (same unit, new
  official name; historical name kept); **parent_aggregation** (several census units summed into one OCHA polygon). Non-exact
  matches were decided by Ahmed (`docs/crosswalk_manual.csv`, `docs/crosswalk_manual_district.csv`). Each row keeps the source name,
  code and district, the OCHA name and p-code, decision, decided_by, date and historical name. Original names and codes are never overwritten.

| Crosswalk | Result |
|---|---|
| Mouza Census tehsils (148) → OCHA ADM3 (139) | exact 115, normalized 11, spelling 9, rename 2, parent_aggregation 8, unmatched 3 (Lahore's Model Town, Raiwind, Shalimar: 0 rural populated mouzas) |
| Mouza Census districts → OCHA ADM2 (36) | 35 normalized, Layyah → Leiah spelling; Cholistan assigned through its tehsils |
| SBP districts (36 excl. Islamabad) → OCHA ADM2 | 31 exact, 2 normalized, 3 spelling (D.G.Khan, Jehlum, Layyah) |
| Ag Census districts (36) → OCHA ADM2 | 35 normalized, 1 spelling (Layyah) |
| SBP branch list districts (36) → OCHA ADM2 | 33 exact, 1 normalized (Rajan Pur), 2 spelling (D.G.Khan, Layyah) |

- **Administrative assignment** (D027) = the share of rural populated mouzas assigned to a polygon: **23,130 / 23,130 (100%)**. This
  is not geographic precision. Polygons that aggregate several census units (Bahawalpur, Gujranwala, Tala Gang incl. Lawa, and the
  three Cholistan parents) conceal internal differences.
- **Integrity checks:** no source unit is assigned twice; no harmonized identifier is duplicated; harmonized totals reconcile to
  23,130 (option A) and 22,807 (option B).
- **Gate:** tehsil-level inference if administrative assignment ≥ 95%. Result: **GO**, so the Q1 unit is the **tehsil** (n = 137).
  The district level (n = 35) is reported as a labelled MAUP comparison; Q2 is at district level (n = 36).

## A5. ICT, Cholistan and the Q1 sample
- **Islamabad (ICT)** is excluded throughout (D003, D021).
- **Cholistan (D015):** option A (primary) sums the three census-only Cholistan tehsils (same PBS tehsil codes as Fort Abbas, Yazman,
  Liaquatpur; 323 rural populated mouzas) into those OCHA polygons. Maps note that these polygons combine desert and irrigated mouzas.
  Option B (exclude Cholistan) is a required sensitivity scenario from the same processed file. Every changed classification,
  LISA label and statistic is listed in `outputs/tables/cholistan_sensitivity.csv`. The Ag Census "Cholistan Area" (19,536 farms,
  0.4%) has no SBP counterpart and is excluded from Q2 denominators.
- **Q1 sample (D028):** units with zero rural populated mouzas (Lahore Cantt and Lahore City tehsils; Lahore district) have
  undefined shares and are excluded from Q1 but kept in Q2.

## A6. Statistical methods and settings
- **Spatial weights** (prespecified, D018): primary **Queen contiguity, row-standardised**; sensitivity **kNN-5 from geodesic
  centroid distances** (pyproj.Geod on WGS84; centroids computed in the analysis CRS; D026), row-standardised. **999 conditional
  permutations, seed 20261031.** LISA counts reported at p < 0.05, p < 0.01 and FDR(0.05); FDR survivors are outlined on maps. Every
  FDR count states its Benjamini–Hochberg p-value cutoff. When no p-value passes BH, no unit is FDR-significant and the cutoff is
  "none" (esda's α/n fallback is not used for labels; D036). No
  islands; one connected component.
- **Tests (Q1, tehsil; district as MAUP comparison; Cholistan A and B):** global Moran's I for `arhti_share` and `commercial_share`;
  LISA for `arhti_share`; bivariate global and local Moran's I (arhti at i vs spatial lag of commercial).
- **Regression (EXPLORATORY; D019-final):** `arhti_share ~ commercial_share + ztbl_share + onlinebank_over25km_share +
  tt_city_cropw_hours + cropland_share + road_metalled_share`. OLS with HC3 SEs and VIFs; spatial error model (ML, prespecified
  check); spatial lag model (ML, POST-HOC). LM diagnostics and residual Moran's I for all three; leave-one-out jackknife ranges
  (POST-HOC). No model is chosen on significance; all are reported in the appendix.
- **POST-HOC association table (D030):** Spearman correlations of `arhti_share` with a fixed list, raw and Benjamini–Hochberg
  p-values, at tehsil and district level, scenarios A and B.
- **Q2 (D021, D029, D030):** `small_farm_reach`; `tenant_share`, `owner_cum_tenant_share`; `large_farm_area_share` (concentration of
  *operated* area in farms ≥ 50 acres, not landownership). Average loan size is used only as a data-quality flag.
  - **Data-quality screen:** F1 = average loan size > 5× or < 0.2× the median; F2 = above-economic loans > 75% of farm-sector disbursement.
  - **Two classifications:** availability-based (commercial_share top half) and presence-based (RURAL branches per 10,000 farms
    top half), each combined with small_farm_reach in the bottom third; the all-branch version is reported as a sensitivity.
  - **Concentration curve and coefficient**; Global Moran's I of small_farm_reach (same weights).
  - **Tenure Spearman table** with BH; everything rerun excluding flagged districts.
- **Choropleth classes:** 5-class Fisher-Jenks unless a class holds < 3 units, else quantiles (Fig S1); bivariate tertiles.

## A7. Limitations
1. **Availability is enumerator-reported, not household borrowing.** It records informants' reports of available sources, not
   use, volume, terms or who is excluded within a mouza. Distances are approximations.
2. **SBP booking location.** Loans are recorded where they are booked. Amount shares are never mapped. Borrower records may not be
   unique individuals.
3. **Sample-based census denominators.** Ag Census 2024 district figures are weighted sample estimates (15% MoE at 95%); no
   confidence intervals are published.
4. **Vintage mismatch.** Mouza Census (Jan–Mar 2020), SBP (FY2023-24), Ag Census (2023-24, enumerated 2024–25), WorldCover (2021),
   MAP (2015) and OCHA boundaries (2022) are not contemporaneous.
5. **MAUP and tehsil-vs-district sensitivity.** Results are reported at both levels; aggregated polygons conceal internal
   differences; kNN and Queen weights give different local results.
6. **Endogenous bank and market location.** Banks, mandis and arhtis locate where agricultural activity already is. Co-location
   of reported sources across units cannot show substitution or complementarity at the borrower level.
7. **Travel time is to cities, not to banks.**
8. **Size-class alignment.** SBP "up to 12.5 / 12.5 to 50 / above 50 acres" (2010-based) and census classes share cut points but
   differ at the boundaries and in concept (borrower holding vs operated farm). The CL1 basis (owned vs operated) is unconfirmed.
9. **Cholistan.** Option A mixes desert and irrigated mouzas in three polygons. Results that change under option B are listed in
   `cholistan_sensitivity.csv`.
10. **Published-study locations are context only.** Their rates come from small, non-representative samples, are by crop (IGC) or from
    focus groups (PMN/MEDA), and are never used in statistics or mapped as local rates. Points are geocoded town centres (OSM Nominatim, D033).

## A8. Mouza-level co-occurrence (EXPLORATORY; prespecified in D035)
Rural populated mouzas (scenario A: 23,130; scenario B: 22,807), stratified by harmonized OCHA tehsil. Binary indicators per mouza:
arhti, commercial bank, ZTBL, online commercial bank in mouza. Mantel–Haenszel pooled odds ratios (arhti vs each), 95% CI,
Breslow–Day test of homogeneity (Tarone) and CMH test; tehsils whose 2×2 table has an empty row or column are uninformative and
dropped (count reported). Per tehsil: observed share reporting both arhti and commercial vs the share expected under independence,
mapped in fixed classes (Figure S4); not estimable if < 20 mouzas or zero in either source. Only tehsil aggregates and pooled
statistics are published. These are availability reports, not borrowing; an association across mouzas is not substitution or
complementarity in behaviour.

## A9. Course-method extensions (EXPLORATORY; D041)
All run on the Q1 tehsils (scenario A, n = 137) unless stated; 999 permutations, seed 20261031; FDR = Benjamini–Hochberg 0.05.
- **Weights sensitivity:** Queen; Rook (identical neighbour sets to Queen for these polygons); geodesic kNN-5; geodesic distance band
  (73.6 km = largest nearest-neighbour distance, so no unit lacks a neighbour); inverse distance (1/d, km) within that band. All
  row-standardised. Global Moran's I for each, and Geary's C (Queen). Table `course_weights_sensitivity.csv`.
- **Moran scatterplot** (Figure S7): z-scores of arhti_share against their Queen spatial lag; the OLS slope equals Moran's I.
- **Getis–Ord Gi\*** (Figure S8): Queen contiguity including each unit itself, binary weights; hot spot if z > 0 and pseudo p < 0.05;
  FDR survivors outlined. Cross-tabulated against LISA in `course_gistar_vs_lisa.csv`.
- **Trend surface** (Figure S9): OLS of arhti_share on centroid coordinates (analysis CRS, km from the mean centroid), first order
  (x, y) and second order (x, y, x², xy, y²); residual Moran's I with Queen weights. A global interpolator used for exploration only.
- **Index of dissimilarity** D = ½ Σ |aᵢ/A − bᵢ/B|: tehsils (mouzas reporting each credit source vs all rural populated mouzas) and
  districts (SBP subsistence-holding borrower records vs farms under 12.5 acres; rural and all scheduled-bank branches vs farms).
  Counts only (rule 11). Table `course_dissimilarity.csv`.
- **k-means typology** (Figure S10): 35 districts with all six variables (arhti_share, commercial_share, small_farm_reach, rural
  branches per 10,000 farms, tenant share, cropland share), z-scores; second specification adds standardised centroid x, y. k = 2–6,
  50 initialisations, seed 20261031; chosen k = highest silhouette among solutions whose smallest type has ≥ 3 districts. Types are
  numbered by descending median arhti_share. Silhouettes of 0.25–0.26 indicate weak separation.
- **Tissot indicatrix** (Figure S11): 40 km geodesic circles on a 1.5° grid drawn in ESRI:102028 and in the analysis CRS; distortion
  from `pyproj.Proj.get_factors` (`course_tissot_distortion.csv`).
- **Classification histograms** (Figure S12): equal interval, quantiles and Fisher–Jenks (k = 5) with GADF = 1 − ADCM / Σ|y − median|.
- **Dasymetric dots** (Figure 6): for each district, round(farms under 12.5 acres / 1,000) points sampled with replacement among
  WorldCover cells (~100 m) whose cropland fraction is ≥ 0.25, with probability proportional to cropland fraction, jittered within the
  cell (seed 20261031). Proportional circles: SBP subsistence-holding borrower records (counts), Flannery scaling (exponent 0.57),
  at each district's representative point.
- **Distance measures:** no Euclidean buffer of cities or markets is drawn (no mandi coordinates; OCHA lists only provincial capitals).
  The census distance bands to the nearest bank branch and grain market serve as multiple-ring buffer measures, and the MAP travel time
  (cost distance) as the time-based measure.
