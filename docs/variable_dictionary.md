# Three concepts that must never be conflated (D029)

| Concept | Meaning | Variables | Source / vintage |
|---|---|---|---|
| **PRESENCE** | Physical facilities | `onlinebank_in_mouza_share`, `onlinebank_over25km_share` | Mouza Census 2020 |
| | | `rural_branches_per_10k_farms` = `branches_rural` (coded "R" in the list) / Ag Census `farms` × 10,000 (D034). `all_branches_per_10k_farms_sensitivity` = all branches / farms × 10,000, **sensitivity only**: dominated by urban branches (Lahore 190.4 vs 3.9 rural) | SBP branch list as on 30 June 2024; Ag Census 2024 |
| **AVAILABILITY** | Credit sources reported as available in the mouza | `commercial_share`, `ztbl_share`, `coop_share`, `mfb_share`, `arhti_share` | Mouza Census 2020 |
| **ALLOCATION** | Who formal credit reaches | `small_farm_reach` = reported subsistence-holding borrower records per 1,000 farms under 12.5 acres (SBP FY2023-24, by booking district; borrower records may not be unique individuals) | SBP FY2023-24 ÷ Ag Census 2024 |

Labels, legends and captions use these words. `commercial_share` is **availability**, never "bank presence".

# Variable dictionary: `data/processed/mouza_tehsil.csv`

**Vintage:** Mouza Census 2020, Pakistan Bureau of Statistics. Fieldwork Jan–Mar 2020; Punjab was covered in January 2020.
**Built by:** `scripts/04_extract_mouza.py` from the mouza-level Excel records (`Mouza Census-2020.xlsx`, in the
RAR). Every count was validated cell by cell against the published Punjab report (`docs/validation_mouza.md`).
**Unit:** one row per tehsil of Punjab, 148 rows. ICT is excluded (D003). Cholistan's 3 tehsils are separate, flagged rows (D004).

## How to read these data
- **These are availability reports, not borrowing.** Each mouza (a revenue estate, not a household) was recorded as
  having or not having a facility. The information comes from the enumerator, the patwari (village revenue official) and
  local knowledgeable respondents (report "Caution for readers", PDF p. 29, items d–e).
  "Credit source available" means respondents said that source serves the mouza's residents. It says nothing about
  how many households borrow, how much, on what terms, or who is excluded.
- **Distances are approximations** by enumerators and respondents (item d), recorded in whole km.
- **Credit sources are multiple-response.** One mouza can report ZTBL, a commercial bank *and* an arhti. Counts and
  shares across institutions **must not be added**. They do not partition the mouzas.
- **Denominator:** every share uses `rp_mouzas`, the number of rural populated mouzas (D005). Tehsils with
  `rp_mouzas = 0` have blank shares (6 tehsils: Lahore district's 5 and Bahawalpur City). Very small denominators
  (Faisalabad City 2, Gujranwala City 4, Lawa 17, De-excluded Area Rajanpur 22) give unstable shares.
- Report page numbers below are the printed page numbers that open each table in the Punjab report.

## Identifiers
| Variable | Definition |
|---|---|
| `division_code`, `division` | PBS division code and name (whitespace-normalised, D006) |
| `district_code`, `district` | PBS district code and name. `CHOLISTAN` = code 999, a census-only district (D004) |
| `tehsil_code`, `tehsil` | PBS tehsil code (unique only within district) and name |
| `tehsil_uid` | `PB-<district_code 3 digits>-<tehsil_code 3 digits>`, the unique key. Use it for joins, never the name |
| `is_cholistan` | True for the 3 Cholistan tehsils (Fort Abbas, Yazman, Liaquatpur; same names as tehsils in Bahawalnagar, Bahawalpur and Rahim Yar Khan) |
| `vintage` | Constant: "Mouza Census 2020 (PBS), fieldwork Jan-Mar 2020" |

## Table 1.1: Mouzas by status (report p. 57). Excel `P1Q09` (status), `P1Q10` (settlements)
| Variable | Definition |
|---|---|
| `mouzas_total` | All mouzas in the tehsil |
| `mouzas_rural`, `mouzas_urban`, `mouzas_partly_urban` | Status 1, 2, 3 |
| `mouzas_forest_populated` / `mouzas_forest_unpopulated` | Status 4 with ≥1 / 0 settlements |
| `mouzas_unpopulated` | Status 5 |
| `rp_mouzas` | **Rural populated mouzas** = rural + partly urban + forest populated. Denominator for every share |

## AVAILABILITY. Table 8.1: Credit facility by type of institution (report p. 479). Excel `P8Q011`–`P8Q019`, multiple response
Each `n_*` counts rural populated mouzas reporting that the source is available.
| Variable | Excel | Source |
|---|---|---|
| `n_ztbl` | P8Q011 | Zarai Taraqiati Bank Ltd |
| `n_coop` | P8Q012 | Cooperative bank |
| `n_commercial` | P8Q013 | Commercial bank |
| `n_mfb` | P8Q014 | Microfinance bank |
| `n_ngo` | P8Q015 | NGO |
| `n_rsp` | P8Q016 | Rural Support Programme |
| `n_govt` | P8Q017 | Government |
| `n_arhti` | P8Q018 | **Commission agent / arhti** (label in the published table; the Excel header calls it "Broker") |
| `n_others` | P8Q019 | Others, as in the detailed Table 8.1. Not the 9,418 of the summary table (D007) |
| `arhti_share`, `ztbl_share`, `commercial_share`, `coop_share`, `mfb_share` | n / `rp_mouzas` | Share of rural populated mouzas reporting the source available. **Not additive across sources** |

## PRESENCE. Table 8.2: Online commercial banking facility (report p. 487). Excel `P8Q021` (1 yes / 2 no), `P8Q022` (km if no)
| Variable | Definition |
|---|---|
| `n_onlinebank_in_mouza` | Mouzas with an online commercial bank branch inside the mouza |
| `n_onlinebank_1_10`, `_11_25`, `_26_50`, `_51plus` | Mouzas without one, by reported distance (km) to the nearest. Bands are the report's |
| `n_onlinebank_unclassified` | Yes/no or distance missing/invalid (0 in Punjab, kept as a check) |
| `onlinebank_in_mouza_share` | `n_onlinebank_in_mouza` / `rp_mouzas` |
| `onlinebank_51plus_share` | `n_onlinebank_51plus` / `rp_mouzas`, the share beyond the farthest band (51 km or more) |

In-mouza + the four bands + unclassified = `rp_mouzas` (exclusive categories, so these *can* be summed).
"Online" refers to a networked commercial-bank branch, as the questionnaire item is worded. **[CHECK]** the
report's definitions section for its exact meaning.

## Table 6.7: Wholesale markets (report p. 362). Excel `P6Q1311/1312` livestock, `P6Q1321/1322` grain, `P6Q1331/1332` fruit/veg
For each prefix `mkt_livestock`, `mkt_grain`, `mkt_fruitveg`:
| Variable | Definition |
|---|---|
| `n_<prefix>_in_mouza` | Mouzas with that wholesale market (mandi) inside the mouza |
| `n_<prefix>_1_10` … `_51plus` | Mouzas without one, by reported km to the nearest |
| `n_<prefix>_unclassified` | Missing/invalid (0 in Punjab) |
| `<prefix>_in_mouza_share`, `<prefix>_51plus_share` | As for Table 8.2 |

The grain market is where arhtis operate, so `mkt_grain_*` is the market-access variable most relevant to Q1.

## Table 6.3: Road facility and distance from metalled road (report p. 302). Excel `P6Q041` (road type), `P6Q042` (km)
| Variable | Definition |
|---|---|
| `n_road_metalled`, `n_road_cemented`, `n_road_bricked`, `n_road_mud` | Type of road reaching the mouza (codes 1, 2, 3, 4). Mutually exclusive; they sum to `rp_mouzas` |
| `n_metroad_1_10` … `_51plus` | Distance to the nearest metalled road. In the data (and the published table), distance is recorded only for **mud-road** mouzas, so the bands sum to `n_road_mud`, not to `rp_mouzas` |
| `road_metalled_share`, `road_mud_share` | n / `rp_mouzas` |
| `metroad_51plus_share` | `n_metroad_51plus` / `rp_mouzas` |

23 mouzas with distance 0 km (non-mud roads) are in no band (D008).

## Not included
- **Average distances** published in Tables 6.3, 6.7 and 8.2: the Excel reproduces 916 of 940 published averages within
  ±1 km, but not all of them, so they are left out of the analysis file. Rebuilding them is possible if needed.
- Post office, conciliatory committee and police station (also in Table 8.2) are not extracted.

## `data/processed/mouza_tehsil_long.csv` (for checking)
One row per published cell: `table`, `level` (tehsil/district/division/province), `division_key`, `district_key`,
`unit`, `tehsil_uid` (tehsil rows), `variable` (as printed, e.g. `rp_mouzas__mkt_grain` = the rural-populated column of the
grain-market row), `variable_std`, `excel` (value from the records), `published` (parsed from the PDF), `diff`, `match`, `vintage`.

---

# Raster context variables (`data/processed/raster_context_{district,tehsil}.csv`; layers in `punjab_credit_context.gpkg`)
Built by `scripts/06_raster_context.py` (D017). Keyed by `adm2_pcode` / `adm3_pcode` (OCHA polygons).

| Variable | Definition | Vintage |
|---|---|---|
| `cropland_share` | Mean ~100 m cropland fraction over cells whose centre is in the polygon. The fraction is the share of valid 10 m pixels in WorldCover class 40 ("Cropland"). **Class 40 is a land-cover mask: it says nothing about crop type, irrigation, farm area or farm size, and it is not comparable to Agricultural Census "cultivated area".** | ESA WorldCover 2021 v200 |
| `n_cells_100m` | Number of ~100 m cells in the polygon | |
| `tt_city_mean_min`, `tt_city_median_min` | Mean / median **modelled travel time to the nearest city** (minutes) over ~1 km cells in the polygon. These are model outputs from a friction surface, as defined by Weiss et al. (2018). **They are not farmers' travel times, and not access to banks, mandis or arhtis.** | MAP Accessibility to Cities, nominal 2015 |
| `tt_city_cropw_mean_min`, `tt_city_cropw_median_min` | Same, weighted by each 1 km cell's 2021 cropland fraction: Σ(t·c)/Σc. This is modelled travel time from where cropland is (not where people live). Mixes a 2015 surface with 2021 land cover | MAP 2015 × WorldCover 2021 |
| `n_cells_1km` | Number of ~1 km cells in the polygon | |

## Derived variables (`scripts/common.py: recompute_shares`, `07`)
| Variable | Definition |
|---|---|
| `onlinebank_over25km_share` | **PRESENCE.** (`n_onlinebank_26_50` + `n_onlinebank_51plus`) / `rp_mouzas`: share of rural populated mouzas reporting the nearest online commercial bank as more than 25 km away (enumerator approximation; Mouza Census 2020) |
| `tt_city_cropw_hours` | `tt_city_cropw_mean_min` / 60 |

---

# District credit-allocation variables (`outputs/tables/district_credit_allocation.csv`; `data/processed/district_credit_allocation.gpkg`)
Built by `scripts/08_credit_allocation.py` (D021/D022). One row per OCHA ADM2 district (36). Islamabad excluded.

| Variable | Definition | Vintage / caveat |
|---|---|---|
| `sub_borrowers`, `eco_borrowers`, `abv_borrowers`, `tot_borrowers` | SBP farm-sector **disbursed borrowers** by holding category, district rows (banks; MFIs excluded because they are Punjab-wide only) | SBP FY2023-24; **booking district**; a farmer borrowing from 2 banks counts twice [CHECK SBP definition] |
| `sub_amount_mn` | Subsistence-holding disbursed amount (Rs million). **Do not map amount shares** (rule 11) | SBP FY2023-24 |
| `avg_loan_<category>_rs` | Disbursed amount × 10⁶ / disbursed borrowers. **Data-quality flag only**, not an analysis variable | SBP FY2023-24 |
| `abv_amount_share` | Above-economic amount / farm-sector amount. Flag F2 only; never mapped | SBP FY2023-24 |
| `flagged`, `flag_reasons` | Data-quality screen (D021: F1, F2) | |
| `farms`, `farm_area_ac`, `cultivated_ac` | Ag Census private farms, operated farm area, cultivated area (acres), all sizes | Ag Census 2024, sample-based estimates |
| `owner`, `owner_cum_tenant`, `tenant` | Farms by tenure (number of farms) | Ag Census 2024 |
| `small_farms` | Farms < 12.5 acres (5 classes) | Ag Census 2024 |
| `small_farm_reach` | **ALLOCATION.** `sub_borrowers` / `small_farms` × 1,000 = reported subsistence-holding borrower records per 1,000 farms under 12.5 acres (SBP FY2023-24, by booking district; borrower records may not be unique individuals). **A ratio of two different sources and years, not a share of farms reached.** SBP "up to 12.5 acres" vs census "under 12.5" differ at the boundary | SBP FY2023-24 ÷ Ag Census 2024 |
| `tenant_share`, `owner_cum_tenant_share`, `owner_share` | Farms by tenure / all farms | Ag Census 2024 |
| `large_farm_area_share` | Farm area of farms ≥ 50 acres / all farm area. **Concentration of OPERATED area, not landownership inequality** | Ag Census 2024 |
| `small_farm_share_of_farms` | `small_farms` / `farms` | Ag Census 2024 |
| `arhti_share`, `commercial_share`, `rp_mouzas` | Mouza Census district aggregates (tehsil counts summed, shares recomputed) | Mouza Census Jan–Mar 2020 |
| `branches_scheduled`, `branches_rural`, `branches_ztbl` | Count of scheduled-bank branches in the SBP list (sheet "Banks"), all / coded rural / ZTBL. **Context only** | SBP branch list as on 30 June 2024 |
| `rural_branches_per_10k_farms` | **PRESENCE.** `branches_rural` / `farms` × 10,000 | SBP branch list (30 Jun 2024) ÷ Ag Census 2024 |
| `all_branches_per_10k_farms_sensitivity` | SENSITIVITY only: `branches_scheduled` / `farms` × 10,000 (measures urbanization more than farm access) | as above |
| `class_availability` | Figure 5B: "High reported commercial-bank credit availability, low small-farm reach" = `commercial_share` ≥ median AND `small_farm_reach` ≤ 33rd percentile | Mouza Census 2020; SBP; Ag Census |
| `class_presence` | Figure 5C: "High rural-branch presence, low small-farm reach" = `rural_branches_per_10k_farms` ≥ median AND `small_farm_reach` ≤ 33rd percentile | SBP branch list; SBP; Ag Census |


# Cholistan and Q1 sample flags (D015, D028)
| Variable | Definition |
|---|---|
| `is_cholistan` (`mouza_tehsil.csv`) | True for the three Cholistan census tehsils (PB-999-071/079/081); kept as separate records so option B runs from the same file |
| `contains_cholistan` (tehsil layers) | True for the OCHA polygons Fort Abbas, Yazman and Liaqatpur under option A (they combine desert and irrigated mouzas) |
| `scenario` | "Cholistan merged into parent tehsils (option A)" or "Cholistan excluded (option B, sensitivity)" |
| `match_types` | Crosswalk match type(s) of the census tehsils summed into the polygon: exact, normalized, spelling, rename, parent_aggregation |
| Q1 sample | Units with zero rural populated mouzas (Lahore Cantt, Lahore City; Lahore district) have undefined shares and are excluded from Q1, kept in Q2 |


# CONTEXT ONLY: published-study locations (`literature_evidence` layer; `docs/literature_evidence.csv`; D032–D033)
**Not analysis data.** These points are never used in statistics, joins to analysis tables, or choropleths, and their rates are never
coloured, interpolated or aggregated to polygons.

| Field | Definition |
|---|---|
| `study`, `year`, `url`, `page` | Haq, Aslam et al. (IGC/NIBAF/PMN) 2013 "Who is the Arthi?" (Table 11, p. 39); PMN/MEDA 2019 "Warehouse Receipt Financing" (pp. 19, 23) |
| `location`, `location_type` | Town; grain market (IGC) or focus group (PMN/MEDA) |
| `district` | District as given in the literature table (OCHA name) |
| `crops` | Crops at the location as given in the brief (blank if not given; not inferred) |
| `metric`, `value`, `basis`, `sample` | As published. IGC: annualized implicit interest **by crop** (cotton 61.9%, maize 71.48%, rice 80.7%, wheat 67.1%), the same values in every IGC row because **rates are by crop, not by location**. PMN/MEDA: reported markup ~180% from focus groups, not an annualized rate |
| `location_precision` | "town centre, approximate" |
| `geocode_source`, `osm_display_name` | OSM Nominatim object and display name (retrieved 2026-10-31) |
| `ocha_tehsil`, `ocha_district`, `district_check` | Spatial join to OCHA ADM3 (analysis CRS); check against `district` |
| `verified_by_ahmed` | Blank until Ahmed checks the row against the publication |

# EXPLORATORY: mouza-level co-occurrence (`outputs/tables/mouza_cooccurrence.csv`; Figure S4; D035)
Built from mouza-level records but published **only as tehsil aggregates and pooled statistics** (no mouza names or codes).
| Field | Definition |
|---|---|
| `record` | "pooled (Mantel-Haenszel)" or "tehsil (arhti x commercial)" |
| `scenario` | A (Cholistan merged into parents) or B (Cholistan excluded) |
| `pair`, `mh_or`, `ci95_low`, `ci95_high` | Mantel–Haenszel pooled odds ratio of arhti vs commercial / ZTBL / online bank in mouza, stratified by tehsil (within-tehsil comparisons only), with 95% CI |
| `breslow_day_tarone_stat`, `breslow_day_tarone_p` | Breslow–Day test of homogeneity of the odds ratio across tehsils (Tarone-adjusted); a small p means the tehsil ORs differ |
| `cmh_stat`, `cmh_p` | Cochran–Mantel–Haenszel test of OR = 1 |
| `n_mouzas`, `n_strata`, `strata_dropped_zero_margin` | Mouzas and tehsils used; tehsils dropped because a row or column of their 2×2 table is empty |
| `observed_both`, `expected_both_independence`, `obs_exp_ratio` | Per tehsil: share reporting both; share(arhti) × share(commercial); their ratio |
| `estimable`, `ratio_class` | False / "not estimable" if < 20 rural populated mouzas or zero mouzas reporting arhti or commercial; fixed classes otherwise |
| `cooc_obs_exp_ratio`, `cooc_ratio_class` (tehsil layers) | The same per-tehsil ratio and class on the map layers |

# ALLOCATION by holding class, REPORTING GEOGRAPHY, crop structure, COST (`scripts/13_reporting_geography.py`, `scripts/14_cost_context.py`; D039-D040)

**District attribution:** every SBP district figure below is "district as reported by SBP (attribution under verification)".

| Variable | Definition | Source / vintage |
|---|---|---|
| `share_farms`, `share_operated_area`, `share_cultivated_area` (holding_class_shares.csv) | Punjab share of farms / farm (operated) area / cultivated area in the census classes matched to SBP's holding classes | Ag Census 2024 (PUNJAB total, incl. Cholistan Area) |
| `share_borrower_records`, `share_disbursement` | Share of SBP farm-sector borrower records / disbursed amount in the class; All-Punjab row (banks + MFIs). `*_banks_only` = district rows incl. Islamabad, no MFIs | SBP FY2023-24 |
| `credit_share_h` (h = sub, eco, abv, tot) | District share of the 36-district total of class-h disbursement (Islamabad and MFIs excluded) | SBP FY2023-24 |
| `area_share`, `farm_share` | District share of the 36-district cultivated area / farms | Ag Census 2024 |
| `lq_amount_h` | **Location quotient** = `credit_share_h` / `area_share`. 1 = proportional to farmland; > 1 = more lending recorded than farmland. Amount-based; mapped only in Figure R1 | SBP FY2023-24 ÷ Ag Census 2024 |
| `lq_borrowers_h` | District share of class-h borrower records / district share of class-h farms (census classes as above) | SBP FY2023-24 ÷ Ag Census 2024 |
| `credit_per_cultivated_acre_rs` | Total farm-sector disbursement (Rs) / cultivated acres | SBP FY2023-24 ÷ Ag Census 2024 |
| `total_branches_per_10k_farms`, `rural_branches_per_10k_farms` | All scheduled-bank branches / branches coded R, per 10,000 farms (PRESENCE) | SBP branch list 30 Jun 2024 ÷ Ag Census 2024 |
| `rural_branch_share`, `total_branch_share` | Summary rows: share of the 36-district total of rural / all branches | SBP branch list 30 Jun 2024 |
| `<crop>_area_ac`, `<crop>_share_of_cropped` (crop_structure_district.csv) | Area under wheat, rice, cotton, maize, sugarcane (acres) and its share of total cropped area; `top2_crops` = the two largest of these five | Ag Census 2024, Tables 6.1, 6.9-6.13 |
| `profile_type` (district_scorecard.csv) | Descriptive grouping: arhti_share above/below the district median × small_farm_reach above/below the median; Lahore not classified. Not a ranking | Mouza Census 2020; SBP FY2023-24 ÷ Ag Census 2024 |
| `tehsils_hh_p05`, `tehsils_ll_p05`, `tehsils_hh_fdr05`, `tehsils_ll_fdr05` | Number of the district's tehsils in High-High / Low-Low LISA clusters of arhti_share (Queen, scenario A) at p < 0.05 / FDR 0.05 | Mouza Census 2020 |
| `rate_pct` (sbp_agri_lending_rates.csv) | Average rate of return on agricultural advances, % per annum, by institution and loan type; simple average at June quarter end | SBP Monthly Statistical Bulletin Table 3.33 (Sep 2026 edition) |
| `docs/price_ladder.csv` | Dated rates on one axis: IGC 2013 arhti implicit annualized cost by crop; IGC farmer-reported bank rates (supplied by Ahmed); SBP Table 3.33 FY2012-13 and FY2023-24; Kissan Card 0% | see `source` column |
