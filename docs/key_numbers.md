# Key numbers

Every number used in the main text, the app and the slides. Written by `scripts/17_key_numbers.py` from finished outputs; nothing here is computed anew. Source = file; Row = filter that selects the row; Column = field.

## Data

| ID | Number | Shown as | Source | Row | Column |
|---|---|---|---|---|---|
| `n_tehsils` | Tehsils in the Q1 analysis (rural populated mouzas > 0) | **137** | `outputs/tables/q1_descriptives.csv` | level = tehsil; scenario = A | `n` |
| `rp_mouzas` | Rural populated mouzas (denominator of every share) | **23,130** | `outputs/tables/q1_descriptives.csv` | level = tehsil; scenario = A | `rp_mouzas` |
| `excluded_tehsils` | Tehsils with no rural populated mouzas (not in the Q1 sample) | **Lahore Cantt; Lahore City** | `outputs/tables/q1_descriptives.csv` | level = tehsil; scenario = A | `excluded_zero_rp` |
| `n_districts_q2` | Districts with small-farm reach | **36** | `outputs/arhti_project.gpkg | layer q2_districts_credit_allocation` | all rows (count over 36 rows) | `small_farm_reach` |
| `xwalk_exact` | Census tehsils matched to OCHA polygons: exact | **115** | `data/interim/tehsil_crosswalk.csv` | match_type = exact (count over 115 rows) | `source_code` |
| `xwalk_normalized` | Census tehsils matched to OCHA polygons: normalized | **11** | `data/interim/tehsil_crosswalk.csv` | match_type = normalized (count over 11 rows) | `source_code` |
| `xwalk_spelling` | Census tehsils matched to OCHA polygons: spelling | **9** | `data/interim/tehsil_crosswalk.csv` | match_type = spelling (count over 9 rows) | `source_code` |
| `xwalk_rename` | Census tehsils matched to OCHA polygons: rename | **2** | `data/interim/tehsil_crosswalk.csv` | match_type = rename (count over 2 rows) | `source_code` |
| `xwalk_parent_aggregation` | Census tehsils matched to OCHA polygons: parent_aggregation | **8** | `data/interim/tehsil_crosswalk.csv` | match_type = parent_aggregation (count over 8 rows) | `source_code` |
| `xwalk_unmatched` | Census tehsils matched to OCHA polygons: unmatched | **3** | `data/interim/tehsil_crosswalk.csv` | match_type = unmatched (count over 3 rows) | `source_code` |
| `xwalk_total` | Census tehsils in the crosswalk | **148** | `data/interim/tehsil_crosswalk.csv` | all rows (count over 148 rows) | `source_code` |
| `n_tehsil_polygons` | OCHA tehsil polygons in Punjab (Q1 layer, incl. 2 with no rural populated mouzas) | **139** | `outputs/arhti_project.gpkg | layer q1_tehsils_mouza_census_2020` | all rows (count over 139 rows) | `adm3_pcode` |

## R1 Where

| ID | Number | Shown as | Source | Row | Column |
|---|---|---|---|---|---|
| `arhti_pooled` | Share of all rural populated mouzas reporting arhti credit (Punjab, pooled) | **31.5%** | `outputs/tables/q1_descriptives.csv` | level = tehsil; scenario = A | `arhti_pooled` |
| `arhti_median` | Median tehsil arhti_share | **19.2%** | `outputs/tables/q1_descriptives.csv` | level = tehsil; scenario = A | `arhti_median` |
| `arhti_min` | Lowest tehsil arhti_share | **0.0%** | `outputs/tables/q1_descriptives.csv` | level = tehsil; scenario = A | `arhti_min` |
| `arhti_max` | Highest tehsil arhti_share | **100.0%** | `outputs/tables/q1_descriptives.csv` | level = tehsil; scenario = A | `arhti_max` |
| `arhti_zero` | Tehsils where no rural populated mouza reports arhti credit | **15** | `outputs/tables/q1_descriptives.csv` | level = tehsil; scenario = A | `arhti_zero` |
| `commercial_median` | Median tehsil commercial_share (commercial-bank credit reported available) | **37.4%** | `outputs/tables/q1_descriptives.csv` | level = tehsil; scenario = A | `commercial_median` |

## R2 Clusters

| ID | Number | Shown as | Source | Row | Column |
|---|---|---|---|---|---|
| `moran_arhti_queen` | Global Moran's I, arhti_share, tehsils, Queen | **0.536** | `outputs/tables/moran_global.csv` | level = tehsil; scenario = A; variable = arhti_share; weights = Queen | `I` |
| `moran_arhti_queen_p` | Pseudo p-value (999 permutations) | **0.001** | `outputs/tables/moran_global.csv` | level = tehsil; scenario = A; variable = arhti_share; weights = Queen | `p_perm` |
| `moran_commercial_queen` | Global Moran's I, commercial_share, tehsils, Queen | **0.297** | `outputs/tables/moran_global.csv` | level = tehsil; scenario = A; variable = commercial_share; weights = Queen | `I` |
| `lisa_hh_p05` | LISA High-High tehsils, Queen, p < 0.05 | **25** | `outputs/tables/lisa_counts.csv` | level = tehsil; scenario = A; analysis = LISA arhti_share; weights = Queen; cluster = High-High | `p05` |
| `lisa_hh_p01` | LISA High-High tehsils, Queen, p < 0.01 | **14** | `outputs/tables/lisa_counts.csv` | level = tehsil; scenario = A; analysis = LISA arhti_share; weights = Queen; cluster = High-High | `p01` |
| `lisa_hh_fdr05` | LISA High-High tehsils, Queen, FDR 0.05 | **15** | `outputs/tables/lisa_counts.csv` | level = tehsil; scenario = A; analysis = LISA arhti_share; weights = Queen; cluster = High-High | `fdr05` |
| `lisa_ll_p05` | LISA Low-Low tehsils, Queen, p < 0.05 | **32** | `outputs/tables/lisa_counts.csv` | level = tehsil; scenario = A; analysis = LISA arhti_share; weights = Queen; cluster = Low-Low | `p05` |
| `lisa_ll_p01` | LISA Low-Low tehsils, Queen, p < 0.01 | **16** | `outputs/tables/lisa_counts.csv` | level = tehsil; scenario = A; analysis = LISA arhti_share; weights = Queen; cluster = Low-Low | `p01` |
| `lisa_ll_fdr05` | LISA Low-Low tehsils, Queen, FDR 0.05 | **17** | `outputs/tables/lisa_counts.csv` | level = tehsil; scenario = A; analysis = LISA arhti_share; weights = Queen; cluster = Low-Low | `fdr05` |
| `lisa_lh_p05` | LISA Low-High tehsils, Queen, p < 0.05 | **3** | `outputs/tables/lisa_counts.csv` | level = tehsil; scenario = A; analysis = LISA arhti_share; weights = Queen; cluster = Low-High | `p05` |
| `lisa_lh_p01` | LISA Low-High tehsils, Queen, p < 0.01 | **0** | `outputs/tables/lisa_counts.csv` | level = tehsil; scenario = A; analysis = LISA arhti_share; weights = Queen; cluster = Low-High | `p01` |
| `lisa_lh_fdr05` | LISA Low-High tehsils, Queen, FDR 0.05 | **0** | `outputs/tables/lisa_counts.csv` | level = tehsil; scenario = A; analysis = LISA arhti_share; weights = Queen; cluster = Low-High | `fdr05` |
| `lisa_hl_p05` | LISA High-Low tehsils, Queen, p < 0.05 | **0** | `outputs/tables/lisa_counts.csv` | level = tehsil; scenario = A; analysis = LISA arhti_share; weights = Queen; cluster = High-Low | `p05` |
| `lisa_hl_p01` | LISA High-Low tehsils, Queen, p < 0.01 | **0** | `outputs/tables/lisa_counts.csv` | level = tehsil; scenario = A; analysis = LISA arhti_share; weights = Queen; cluster = High-Low | `p01` |
| `lisa_hl_fdr05` | LISA High-Low tehsils, Queen, FDR 0.05 | **0** | `outputs/tables/lisa_counts.csv` | level = tehsil; scenario = A; analysis = LISA arhti_share; weights = Queen; cluster = High-Low | `fdr05` |
| `bh_cutoff_queen` | Benjamini-Hochberg cutoff (pseudo p) for FDR 0.05, LISA arhti, tehsils, Queen | **0.0117** | `outputs/tables/lisa_counts.csv` | level = tehsil; scenario = A; analysis = LISA arhti_share; weights = Queen; cluster = High-High | `bh_cutoff` |
| `permutations` | Permutations | **999** | `outputs/tables/moran_global.csv` | level = tehsil; scenario = A; variable = arhti_share; weights = Queen | `permutations` |
| `seed` | Random seed | **20261031** | `outputs/tables/moran_global.csv` | level = tehsil; scenario = A; variable = arhti_share; weights = Queen | `seed` |

## R3 Gap

| ID | Number | Shown as | Source | Row | Column |
|---|---|---|---|---|---|
| `bv_queen` | Bivariate Moran's I (arhti_share x lag commercial_share), tehsils, Queen | **0.112** | `outputs/tables/moran_bivariate.csv` | level = tehsil; scenario = A; weights = Queen | `I_bv` |
| `bv_queen_p` | Pseudo p-value, bivariate Moran, Queen | **0.062** | `outputs/tables/moran_bivariate.csv` | level = tehsil; scenario = A; weights = Queen | `p_perm` |
| `mh_or` | Mantel-Haenszel odds ratio, arhti x commercial-bank credit reported in the same mouza (tehsil strata) | **1.18** | `outputs/tables/mouza_cooccurrence.csv` | record = pooled (Mantel-Haenszel); scenario = A; pair = arhti x commercial | `mh_or` |
| `mh_lo` | 95% CI lower bound | **1.09** | `outputs/tables/mouza_cooccurrence.csv` | record = pooled (Mantel-Haenszel); scenario = A; pair = arhti x commercial | `ci95_low` |
| `mh_hi` | 95% CI upper bound | **1.27** | `outputs/tables/mouza_cooccurrence.csv` | record = pooled (Mantel-Haenszel); scenario = A; pair = arhti x commercial | `ci95_high` |
| `mh_n_mouzas` | Mouzas in the pooled odds ratio | **21,674** | `outputs/tables/mouza_cooccurrence.csv` | record = pooled (Mantel-Haenszel); scenario = A; pair = arhti x commercial | `n_mouzas` |
| `mh_strata` | Tehsil strata used | **120** | `outputs/tables/mouza_cooccurrence.csv` | record = pooled (Mantel-Haenszel); scenario = A; pair = arhti x commercial | `n_strata` |
| `bd_stat` | Breslow-Day-Tarone homogeneity statistic | **751.0** | `outputs/tables/mouza_cooccurrence.csv` | record = pooled (Mantel-Haenszel); scenario = A; pair = arhti x commercial | `breslow_day_tarone_stat` |
| `bd_p` | Breslow-Day-Tarone p-value | **< 0.001** | `outputs/tables/mouza_cooccurrence.csv` | record = pooled (Mantel-Haenszel); scenario = A; pair = arhti x commercial | `breslow_day_tarone_p` |
| `tehsils_estimable` | Tehsils with an estimable observed/expected ratio | **120** | `outputs/tables/mouza_cooccurrence.csv` | record = tehsil (arhti x commercial); scenario = A; estimable = True (count over 120 rows) | `pcode` |
| `tehsils_ratio_above1` | Tehsils where arhti and commercial-bank credit are co-reported MORE often than independence implies | **67** | `outputs/tables/mouza_cooccurrence.csv` | record = tehsil (arhti x commercial); scenario = A; obs_exp_ratio > 1 (count) | `obs_exp_ratio` |
| `tehsils_ratio_below1` | Tehsils where they are co-reported LESS often than independence implies | **53** | `outputs/tables/mouza_cooccurrence.csv` | record = tehsil (arhti x commercial); scenario = A; obs_exp_ratio < 1 (count) | `obs_exp_ratio` |
| `rho_cropland` | Spearman rho, arhti_share vs cropland share (POST-HOC EXPLORATORY) | **0.49** | `outputs/tables/exploratory_associations.csv` | level = tehsil; scenario = A; x = cropland_share | `rho` |
| `rho_cropland_pbh` | BH-adjusted p-value | **< 0.001** | `outputs/tables/exploratory_associations.csv` | level = tehsil; scenario = A; x = cropland_share | `p_bh` |
| `rho_onlinebank` | Spearman rho, arhti_share vs share of mouzas with an online commercial bank in the mouza (PRESENCE; POST-HOC EXPLORATORY) | **-0.40** | `outputs/tables/exploratory_associations.csv` | level = tehsil; scenario = A; x = onlinebank_in_mouza_share | `rho` |
| `rho_onlinebank_pbh` | BH-adjusted p-value | **< 0.001** | `outputs/tables/exploratory_associations.csv` | level = tehsil; scenario = A; x = onlinebank_in_mouza_share | `p_bh` |

## R4 Reach

| ID | Number | Shown as | Source | Row | Column |
|---|---|---|---|---|---|
| `reach_min` | Lowest district small-farm reach | **21.6** | `outputs/arhti_project.gpkg | layer q2_districts_credit_allocation` | all rows (min over 36 rows) | `small_farm_reach` |
| `reach_max` | Highest district small-farm reach | **299.0** | `outputs/arhti_project.gpkg | layer q2_districts_credit_allocation` | all rows (max over 36 rows) | `small_farm_reach` |
| `reach_median` | Median district small-farm reach | **118.5** | `outputs/arhti_project.gpkg | layer q2_districts_credit_allocation` | all rows (median over 36 rows) | `small_farm_reach` |
| `n_flagged` | Districts flagged in the SBP data-quality screen | **5** | `outputs/arhti_project.gpkg | layer q2_districts_credit_allocation` | flagged = 1 (count over 5 rows) | `adm2_name` |
| `flagged_names` | Flagged districts | **Chakwal, Faisalabad, Jhelum, Lahore, Rawalpindi** | `outputs/arhti_project.gpkg | layer q2_districts_credit_allocation` | flagged = 1 | `adm2_name` |
| `moran_reach` | Global Moran's I, small_farm_reach, districts, Queen | **0.532** | `outputs/tables/moran_small_farm_reach.csv` | weights = Queen; sample = all matched districts | `I` |
| `head_borrower_share` | Above-economic holdings (> 50 acres): share of farm-sector borrower records | **1.1%** | `outputs/tables/sbp_province_headline.csv` | scope = All Punjab (banks + MFIs) | `abv_borrower_share` |
| `head_amount_share` | Above-economic holdings (> 50 acres): share of farm-sector disbursed amount (province only) | **49.4%** | `outputs/tables/sbp_province_headline.csv` | scope = All Punjab (banks + MFIs) | `abv_amount_share` |
| `head_abv_borrowers` | Above-economic borrower records | **8,024** | `outputs/tables/sbp_province_headline.csv` | scope = All Punjab (banks + MFIs) | `abv_borrowers` |
| `head_tot_borrowers` | All farm-sector borrower records | **732,856** | `outputs/tables/sbp_province_headline.csv` | scope = All Punjab (banks + MFIs) | `tot_borrowers` |
| `moran_reach_p` | Pseudo p, Moran's I small_farm_reach (Queen) | **0.001** | `outputs/tables/moran_small_farm_reach.csv` | weights = Queen; sample = all matched districts | `p_perm` |

## Robustness

| ID | Number | Shown as | Source | Row | Column |
|---|---|---|---|---|---|
| `moran_arhti_knn` | Global Moran's I, arhti_share, tehsils, geodesic kNN-5 | **0.568** | `outputs/tables/moran_global.csv` | level = tehsil; scenario = A; variable = arhti_share; weights = kNN-5 (geodesic) | `I` |
| `moran_arhti_district` | Global Moran's I, arhti_share, districts (n = 35), Queen | **0.429** | `outputs/tables/moran_global.csv` | level = district; scenario = A; variable = arhti_share; weights = Queen | `I` |
| `moran_arhti_B` | Global Moran's I, arhti_share, tehsils, Queen, Cholistan scenario B | **0.543** | `outputs/tables/moran_global.csv` | level = tehsil; scenario = B; variable = arhti_share; weights = Queen | `I` |
| `mh_or_B` | Mantel-Haenszel odds ratio, arhti x commercial, scenario B | **1.20** | `outputs/tables/mouza_cooccurrence.csv` | record = pooled (Mantel-Haenszel); scenario = B; pair = arhti x commercial | `mh_or` |
| `mh_lo_B` | 95% CI lower bound, scenario B | **1.11** | `outputs/tables/mouza_cooccurrence.csv` | record = pooled (Mantel-Haenszel); scenario = B; pair = arhti x commercial | `ci95_low` |
| `mh_hi_B` | 95% CI upper bound, scenario B | **1.29** | `outputs/tables/mouza_cooccurrence.csv` | record = pooled (Mantel-Haenszel); scenario = B; pair = arhti x commercial | `ci95_high` |
| `n_districts_q1` | Districts in the Q1 MAUP comparison (rural populated mouzas > 0) | **35** | `outputs/tables/moran_global.csv` | level = district; scenario = A; variable = arhti_share; weights = Queen | `n` |

## Background

| ID | Number | Shown as | Source | Row | Column |
|---|---|---|---|---|---|
| `lit_igc_rates` | IGC 2013: annualized implicit interest by crop (Table 11; CONTEXT) | **cotton 61.9%; maize 71.48%; rice 80.7%; wheat 67.1%** | `docs/literature_evidence.csv` | study = Haq, Aslam et al. (IGC/NIBAF/PMN), "Who is the Arthi?"; location = Nankana Sahib | `value` |
| `lit_igc_sample` | IGC 2013: sample | **18 arthis in 8 locations, purposive, interviews 2012** | `docs/literature_evidence.csv` | study = Haq, Aslam et al. (IGC/NIBAF/PMN), "Who is the Arthi?"; location = Nankana Sahib | `sample` |
| `lit_pmn_markup` | PMN/MEDA 2019: reported markup (focus groups; CONTEXT) | **~180%** | `docs/literature_evidence.csv` | study = PMN/MEDA, "Warehouse Receipt Financing"; location = Bahawalpur | `value` |
| `lit_pmn_sample` | PMN/MEDA 2019: sample | **non-representative: 400-farmer survey in 10 Punjab districts plus 4 FGDs, 2018** | `docs/literature_evidence.csv` | study = PMN/MEDA, "Warehouse Receipt Financing"; location = Bahawalpur | `sample` |

## Allocation by class

| ID | Number | Shown as | Source | Row | Column |
|---|---|---|---|---|---|
| `hc_subsistence_farms` | subsistence holdings: share of farms (Punjab) | **94.1%** | `outputs/tables/holding_class_shares.csv` | holding_class = subsistence | `share_farms` |
| `hc_subsistence_operated_area` | subsistence holdings: share of operated farm area (Punjab) | **68.5%** | `outputs/tables/holding_class_shares.csv` | holding_class = subsistence | `share_operated_area` |
| `hc_subsistence_borrower_records` | subsistence holdings: share of SBP borrower records (Punjab) | **91.9%** | `outputs/tables/holding_class_shares.csv` | holding_class = subsistence | `share_borrower_records` |
| `hc_subsistence_disbursement` | subsistence holdings: share of SBP disbursement (Punjab) | **35.9%** | `outputs/tables/holding_class_shares.csv` | holding_class = subsistence | `share_disbursement` |
| `hc_economic_farms` | economic holdings: share of farms (Punjab) | **5.3%** | `outputs/tables/holding_class_shares.csv` | holding_class = economic | `share_farms` |
| `hc_economic_operated_area` | economic holdings: share of operated farm area (Punjab) | **22.8%** | `outputs/tables/holding_class_shares.csv` | holding_class = economic | `share_operated_area` |
| `hc_economic_borrower_records` | economic holdings: share of SBP borrower records (Punjab) | **7.0%** | `outputs/tables/holding_class_shares.csv` | holding_class = economic | `share_borrower_records` |
| `hc_economic_disbursement` | economic holdings: share of SBP disbursement (Punjab) | **14.7%** | `outputs/tables/holding_class_shares.csv` | holding_class = economic | `share_disbursement` |
| `hc_above_economic_farms` | above-economic holdings: share of farms (Punjab) | **0.5%** | `outputs/tables/holding_class_shares.csv` | holding_class = above_economic | `share_farms` |
| `hc_above_economic_operated_area` | above-economic holdings: share of operated farm area (Punjab) | **8.6%** | `outputs/tables/holding_class_shares.csv` | holding_class = above_economic | `share_operated_area` |
| `hc_above_economic_borrower_records` | above-economic holdings: share of SBP borrower records (Punjab) | **1.1%** | `outputs/tables/holding_class_shares.csv` | holding_class = above_economic | `share_borrower_records` |
| `hc_above_economic_disbursement` | above-economic holdings: share of SBP disbursement (Punjab) | **49.4%** | `outputs/tables/holding_class_shares.csv` | holding_class = above_economic | `share_disbursement` |

## Reporting geography

| ID | Number | Shown as | Source | Row | Column |
|---|---|---|---|---|---|
| `lahore_total_branches_10k` | Lahore: all scheduled-bank branches per 10,000 farms | **190.4** | `outputs/tables/reporting_geography.csv` | record_type = district; adm2_name = Lahore | `total_branches_per_10k_farms` |
| `lahore_rural_branches_10k` | Lahore: rural branches per 10,000 farms | **3.9** | `outputs/tables/reporting_geography.csv` | record_type = district; adm2_name = Lahore | `rural_branches_per_10k_farms` |
| `five_credit_share_tot` | Five city districts combined: share of disbursement, all holdings | **39.7%** | `outputs/tables/reporting_geography.csv` | record_type = summary; adm2_name = Five cities combined (Lahore, Rawalpindi, Multan, Faisalabad, Rahim Yar Khan) | `credit_share_tot` |
| `five_credit_share_abv` | Five city districts combined: share of above-economic disbursement | **59.6%** | `outputs/tables/reporting_geography.csv` | record_type = summary; adm2_name = Five cities combined (Lahore, Rawalpindi, Multan, Faisalabad, Rahim Yar Khan) | `credit_share_abv` |
| `five_credit_share_sub` | Five city districts combined: share of subsistence disbursement | **22.4%** | `outputs/tables/reporting_geography.csv` | record_type = summary; adm2_name = Five cities combined (Lahore, Rawalpindi, Multan, Faisalabad, Rahim Yar Khan) | `credit_share_sub` |
| `five_area_share` | Five city districts combined: share of cultivated area | **13.3%** | `outputs/tables/reporting_geography.csv` | record_type = summary; adm2_name = Five cities combined (Lahore, Rawalpindi, Multan, Faisalabad, Rahim Yar Khan) | `area_share` |
| `five_farm_share` | Five city districts combined: share of farms | **18.2%** | `outputs/tables/reporting_geography.csv` | record_type = summary; adm2_name = Five cities combined (Lahore, Rawalpindi, Multan, Faisalabad, Rahim Yar Khan) | `farm_share` |
| `five_rural_branch_share` | Five city districts combined: share of rural branches | **19.1%** | `outputs/tables/reporting_geography.csv` | record_type = summary; adm2_name = Five cities combined (Lahore, Rawalpindi, Multan, Faisalabad, Rahim Yar Khan) | `rural_branch_share` |
| `five_total_branch_share` | Five city districts combined: share of all branches | **43.5%** | `outputs/tables/reporting_geography.csv` | record_type = summary; adm2_name = Five cities combined (Lahore, Rawalpindi, Multan, Faisalabad, Rahim Yar Khan) | `total_branch_share` |
| `isb_credit_share_tot` | Islamabad: share of disbursement in SBP district rows incl. Islamabad | **3.9%** | `outputs/tables/reporting_geography.csv` | record_type = Islamabad (booked; not in area ratios) | `credit_share_tot` |
| `lq_abv_lahore` | Lahore: amount LQ, above-economic holdings | **14.06** | `outputs/tables/reporting_geography.csv` | record_type = district; adm2_name = Lahore | `lq_amount_abv` |
| `lq_abv_rawalpindi` | Rawalpindi: amount LQ, above-economic holdings | **7.44** | `outputs/tables/reporting_geography.csv` | record_type = district; adm2_name = Rawalpindi | `lq_amount_abv` |
| `lq_abv_jhelum` | Jhelum: amount LQ, above-economic holdings | **0.22** | `outputs/tables/reporting_geography.csv` | record_type = district; adm2_name = Jhelum | `lq_amount_abv` |
| `lq_abv_chakwal` | Chakwal: amount LQ, above-economic holdings | **0.09** | `outputs/tables/reporting_geography.csv` | record_type = district; adm2_name = Chakwal | `lq_amount_abv` |
| `lq_sub_lahore` | Lahore: amount LQ, subsistence holdings | **4.66** | `outputs/tables/reporting_geography.csv` | record_type = district; adm2_name = Lahore | `lq_amount_sub` |
| `lq_sub_rawalpindi` | Rawalpindi: amount LQ, subsistence holdings | **0.29** | `outputs/tables/reporting_geography.csv` | record_type = district; adm2_name = Rawalpindi | `lq_amount_sub` |
| `lq_sub_jhelum` | Jhelum: amount LQ, subsistence holdings | **6.47** | `outputs/tables/reporting_geography.csv` | record_type = district; adm2_name = Jhelum | `lq_amount_sub` |
| `lq_sub_chakwal` | Chakwal: amount LQ, subsistence holdings | **0.14** | `outputs/tables/reporting_geography.csv` | record_type = district; adm2_name = Chakwal | `lq_amount_sub` |

## Cost (context)

| ID | Number | Shown as | Source | Row | Column |
|---|---|---|---|---|---|
| `rate_ztbl_prod_2012` | SBP Table 3.33, Zarai Taraqiati Bank Ltd. (ZTBL), production loans, 2012-13 (% p.a.) | **12.00** | `outputs/tables/sbp_agri_lending_rates.csv` | period = 2012-13; institution = Zarai Taraqiati Bank Ltd. (ZTBL); loan_type = production | `rate_pct` |
| `rate_ztbl_deve_2012` | SBP Table 3.33, Zarai Taraqiati Bank Ltd. (ZTBL), development loans, 2012-13 (% p.a.) | **13.80** | `outputs/tables/sbp_agri_lending_rates.csv` | period = 2012-13; institution = Zarai Taraqiati Bank Ltd. (ZTBL); loan_type = development | `rate_pct` |
| `rate_ppcb_prod_2012` | SBP Table 3.33, Punjab Provincial Cooperative Bank (PPCB), production loans, 2012-13 (% p.a.) | **19.00** | `outputs/tables/sbp_agri_lending_rates.csv` | period = 2012-13; institution = Punjab Provincial Cooperative Bank (PPCB); loan_type = production | `rate_pct` |
| `rate_ppcb_deve_2012` | SBP Table 3.33, Punjab Provincial Cooperative Bank (PPCB), development loans, 2012-13 (% p.a.) | **18.00** | `outputs/tables/sbp_agri_lending_rates.csv` | period = 2012-13; institution = Punjab Provincial Cooperative Bank (PPCB); loan_type = development | `rate_pct` |
| `rate_comm_prod_2012` | SBP Table 3.33, Commercial banks (5 big banks + 14 DPBs), production loans, 2012-13 (% p.a.) | **16.00** | `outputs/tables/sbp_agri_lending_rates.csv` | period = 2012-13; institution = Commercial banks (5 big banks + 14 DPBs); loan_type = production | `rate_pct` |
| `rate_comm_deve_2012` | SBP Table 3.33, Commercial banks (5 big banks + 14 DPBs), development loans, 2012-13 (% p.a.) | **16.00** | `outputs/tables/sbp_agri_lending_rates.csv` | period = 2012-13; institution = Commercial banks (5 big banks + 14 DPBs); loan_type = development | `rate_pct` |
| `rate_ztbl_prod_2023` | SBP Table 3.33, Zarai Taraqiati Bank Ltd. (ZTBL), production loans, 2023-24 (% p.a.) | **29.42** | `outputs/tables/sbp_agri_lending_rates.csv` | period = 2023-24; institution = Zarai Taraqiati Bank Ltd. (ZTBL); loan_type = production | `rate_pct` |
| `rate_ztbl_deve_2023` | SBP Table 3.33, Zarai Taraqiati Bank Ltd. (ZTBL), development loans, 2023-24 (% p.a.) | **29.42** | `outputs/tables/sbp_agri_lending_rates.csv` | period = 2023-24; institution = Zarai Taraqiati Bank Ltd. (ZTBL); loan_type = development | `rate_pct` |
| `rate_ppcb_prod_2023` | SBP Table 3.33, Punjab Provincial Cooperative Bank (PPCB), production loans, 2023-24 (% p.a.) | **20.67** | `outputs/tables/sbp_agri_lending_rates.csv` | period = 2023-24; institution = Punjab Provincial Cooperative Bank (PPCB); loan_type = production | `rate_pct` |
| `rate_ppcb_deve_2023` | SBP Table 3.33, Punjab Provincial Cooperative Bank (PPCB), development loans, 2023-24 (% p.a.) | **22.71** | `outputs/tables/sbp_agri_lending_rates.csv` | period = 2023-24; institution = Punjab Provincial Cooperative Bank (PPCB); loan_type = development | `rate_pct` |
| `rate_comm_prod_2023` | SBP Table 3.33, Commercial banks (5 big banks + 14 DPBs), production loans, 2023-24 (% p.a.) | **22.96** | `outputs/tables/sbp_agri_lending_rates.csv` | period = 2023-24; institution = Commercial banks (5 big banks + 14 DPBs); loan_type = production | `rate_pct` |
| `rate_comm_deve_2023` | SBP Table 3.33, Commercial banks (5 big banks + 14 DPBs), development loans, 2023-24 (% p.a.) | **22.94** | `outputs/tables/sbp_agri_lending_rates.csv` | period = 2023-24; institution = Commercial banks (5 big banks + 14 DPBs); loan_type = development | `rate_pct` |
| `igc_bank_low` | IGC 2013: lowest bank rate reported by interviewed farmers (% p.a.; supplied by Ahmed, checklist P3) | **9** | `docs/price_ladder.csv` | item = Bank rates reported by interviewed farmers | `rate_low` |
| `igc_bank_high` | IGC 2013: highest bank rate reported by interviewed farmers (% p.a.) | **18** | `docs/price_ladder.csv` | item = Bank rates reported by interviewed farmers | `rate_high` |
| `kissan_terms` | Punjab CM Kissan Card: terms and dates | **Eligibility: 1 to 12.5 acres; loan limit Rs 30,000 per acre capped at Rs 150,000 per season (i.e. sized on 5 acres) per the Punjab Portal. Registration opened 1 Jun 2024 (SMU page); cards operational 15 Oct 2024 (supplied by Ahmed). Both after the FY2023-24 SBP data period except the last month of registration.** | `docs/price_ladder.csv` | item = Punjab CM Kissan Card (interest-free) | `note` |

## Scorecard

| ID | Number | Shown as | Source | Row | Column |
|---|---|---|---|---|---|
| `profile_high_arhti_availability_low_smallfarm_reach` | Districts with profile 'high arhti availability + low small-farm reach' | **7** | `outputs/tables/district_scorecard.csv` | profile_type = high arhti availability + low small-farm reach (count over 7 rows) | `adm2_name` |
| `profile_high_arhti_availability_high_smallfarm_reach` | Districts with profile 'high arhti availability + high small-farm reach' | **10** | `outputs/tables/district_scorecard.csv` | profile_type = high arhti availability + high small-farm reach (count over 10 rows) | `adm2_name` |
| `profile_low_arhti_availability_low_smallfarm_reach` | Districts with profile 'low arhti availability + low small-farm reach' | **10** | `outputs/tables/district_scorecard.csv` | profile_type = low arhti availability + low small-farm reach (count over 10 rows) | `adm2_name` |
| `profile_low_arhti_availability_high_smallfarm_reach` | Districts with profile 'low arhti availability + high small-farm reach' | **8** | `outputs/tables/district_scorecard.csv` | profile_type = low arhti availability + high small-farm reach (count over 8 rows) | `adm2_name` |
| `profile_not_classified` | Districts with profile 'not classified' | **1** | `outputs/tables/district_scorecard.csv` | profile_type = not classified (count over 1 rows) | `adm2_name` |

## Allocation extras

| ID | Number | Shown as | Source | Row | Column |
|---|---|---|---|---|---|
| `cc_all` | Concentration coefficient of borrower records over small farms, all 36 districts | **0.297** | `outputs/tables/concentration_coefficients.csv` | sample = all matched districts | `concentration_coefficient` |
| `cc_excl` | Concentration coefficient, excluding the 5 flagged districts | **0.255** | `outputs/tables/concentration_coefficients.csv` | sample = excluding flagged districts | `concentration_coefficient` |
| `rho_tenant` | Spearman rho, small_farm_reach vs tenant share of farms (36 districts) | **0.39** | `outputs/tables/q2_tenure_associations.csv` | family = all districts (n = 36); x = tenant_share | `rho` |
| `rho_tenant_pbh` | BH-adjusted p, small_farm_reach vs tenant share | **0.018** | `outputs/tables/q2_tenure_associations.csv` | family = all districts (n = 36); x = tenant_share | `p_bh` |
| `moran_reach_excl` | Moran's I, small_farm_reach, Queen, excluding flagged districts (n = 31) | **0.428** | `outputs/tables/moran_small_farm_reach.csv` | weights = Queen; sample = excluding flagged districts | `I` |
| `top_crop_wheat` | Districts where wheat is the largest of the five tracked crops by area | **34** | `outputs/tables/crop_structure_district.csv` | top_crop = wheat (count over 34 rows) | `agc_district` |
| `top_crop_rice` | Districts where rice is the largest of the five tracked crops by area | **2** | `outputs/tables/crop_structure_district.csv` | top_crop = rice (count over 2 rows) | `agc_district` |
| `top_crop_cotton` | Districts where cotton is the largest of the five tracked crops by area | **0** | `outputs/tables/crop_structure_district.csv` | top_crop = cotton (count over 0 rows) | `agc_district` |
| `top_crop_sugarcane` | Districts where sugarcane is the largest of the five tracked crops by area | **0** | `outputs/tables/crop_structure_district.csv` | top_crop = sugarcane (count over 0 rows) | `agc_district` |
| `top_crop_maize` | Districts where maize is the largest of the five tracked crops by area | **0** | `outputs/tables/crop_structure_district.csv` | top_crop = maize (count over 0 rows) | `agc_district` |
| `second_crop_rice` | Districts where rice is the second-largest of the five tracked crops | **17** | `outputs/tables/crop_structure_district.csv` | second_crop = rice (count over 17 rows) | `agc_district` |
| `second_crop_cotton` | Districts where cotton is the second-largest of the five tracked crops | **9** | `outputs/tables/crop_structure_district.csv` | second_crop = cotton (count over 9 rows) | `agc_district` |
| `second_crop_sugarcane` | Districts where sugarcane is the second-largest of the five tracked crops | **3** | `outputs/tables/crop_structure_district.csv` | second_crop = sugarcane (count over 3 rows) | `agc_district` |
| `second_crop_maize` | Districts where maize is the second-largest of the five tracked crops | **5** | `outputs/tables/crop_structure_district.csv` | second_crop = maize (count over 5 rows) | `agc_district` |
| `second_crop_wheat` | Districts where wheat is the second-largest of the five tracked crops | **2** | `outputs/tables/crop_structure_district.csv` | second_crop = wheat (count over 2 rows) | `agc_district` |

## Course methods

| ID | Number | Shown as | Source | Row | Column |
|---|---|---|---|---|---|
| `moran_rook` | Global Moran's I, arhti_share, tehsils, Rook (same neighbour sets as Queen) | **0.536** | `outputs/tables/course_weights_sensitivity.csv` | statistic = Moran's I; weights = Rook | `value` |
| `moran_dband` | Global Moran's I, arhti_share, tehsils, Distance band (geodesic, 73.6 km) | **0.470** | `outputs/tables/course_weights_sensitivity.csv` | statistic = Moran's I; weights = Distance band (geodesic, 73.6 km) | `value` |
| `dband_km` | Distance band threshold (km, geodesic; smallest with no unit lacking a neighbour) | **73.6 km** | `outputs/tables/course_weights_sensitivity.csv` | statistic = Moran's I; weights = Distance band (geodesic, 73.6 km) | `weights` |
| `moran_invd` | Global Moran's I, arhti_share, tehsils, Inverse distance within 73.6 km | **0.491** | `outputs/tables/course_weights_sensitivity.csv` | statistic = Moran's I; weights = Inverse distance within 73.6 km | `value` |
| `geary_c` | Geary's C, arhti_share, tehsils, Queen (E[C] = 1; < 1 = positive autocorrelation) | **0.458** | `outputs/tables/course_weights_sensitivity.csv` | statistic = Geary's C | `value` |
| `geary_c_p` | Geary's C pseudo p-value | **0.001** | `outputs/tables/course_weights_sensitivity.csv` | statistic = Geary's C | `p_perm` |
| `gistar_hot_p05` | Gi* hot spots, p < 0.05 | **28** | `outputs/tables/course_gistar_counts.csv` | class = Hot spot | `p05` |
| `gistar_hot_fdr` | Gi* hot spots surviving FDR 0.05 | **15** | `outputs/tables/course_gistar_counts.csv` | class = Hot spot | `fdr05` |
| `gistar_cold_p05` | Gi* cold spots, p < 0.05 | **33** | `outputs/tables/course_gistar_counts.csv` | class = Cold spot | `p05` |
| `gistar_cold_fdr` | Gi* cold spots surviving FDR 0.05 | **18** | `outputs/tables/course_gistar_counts.csv` | class = Cold spot | `fdr05` |
| `trend1_r2` | Trend surface order 1: R² | **0.32** | `outputs/tables/course_trend_surface.csv` | order = 1 | `r2` |
| `trend1_resid_I` | Trend surface order 1: Moran's I of residuals (Queen) | **0.340** | `outputs/tables/course_trend_surface.csv` | order = 1 | `resid_moran_I` |
| `trend1_resid_p` | Trend surface order 1: residual Moran pseudo p | **0.001** | `outputs/tables/course_trend_surface.csv` | order = 1 | `resid_moran_p` |
| `trend2_r2` | Trend surface order 2: R² | **0.40** | `outputs/tables/course_trend_surface.csv` | order = 2 | `r2` |
| `trend2_resid_I` | Trend surface order 2: Moran's I of residuals (Queen) | **0.234** | `outputs/tables/course_trend_surface.csv` | order = 2 | `resid_moran_I` |
| `trend2_resid_p` | Trend surface order 2: residual Moran pseudo p | **0.002** | `outputs/tables/course_trend_surface.csv` | order = 2 | `resid_moran_p` |
| `D_arhti` | Index of dissimilarity: mouzas reporting arhti credit vs reference | **0.380** | `outputs/tables/course_dissimilarity.csv` | group = mouzas reporting arhti credit | `D` |
| `D_commercial` | Index of dissimilarity: mouzas reporting commercial-bank credit vs reference | **0.234** | `outputs/tables/course_dissimilarity.csv` | group = mouzas reporting commercial-bank credit | `D` |
| `D_ztbl` | Index of dissimilarity: mouzas reporting ZTBL credit vs reference | **0.115** | `outputs/tables/course_dissimilarity.csv` | group = mouzas reporting ZTBL credit | `D` |
| `D_sub_borrowers` | Index of dissimilarity: SBP subsistence-holding borrower records vs reference | **0.216** | `outputs/tables/course_dissimilarity.csv` | group = SBP subsistence-holding borrower records | `D` |
| `D_rural_branches` | Index of dissimilarity: rural scheduled-bank branches vs reference | **0.214** | `outputs/tables/course_dissimilarity.csv` | group = rural scheduled-bank branches | `D` |
| `D_all_branches` | Index of dissimilarity: all scheduled-bank branches vs reference | **0.356** | `outputs/tables/course_dissimilarity.csv` | group = all scheduled-bank branches | `D` |
| `kmeans_k_attr` | k-means types, attributes | **6** | `outputs/tables/course_kmeans_profiles.csv` | spec = attributes (count over 6 rows) | `type` |
| `kmeans_sil_attr` | Silhouette of the chosen k-means solution, attributes | **0.26** | `outputs/tables/course_kmeans_silhouette.csv` | spec = attributes (max over 5 rows) | `silhouette` |
| `kmeans_k_loc` | k-means types, attributes + location | **5** | `outputs/tables/course_kmeans_profiles.csv` | spec = attributes + location (count over 5 rows) | `type` |
| `kmeans_sil_loc` | Silhouette of the chosen k-means solution, attributes + location | **0.25** | `outputs/tables/course_kmeans_silhouette.csv` | spec = attributes + location (max over 5 rows) | `silhouette` |
| `tissot_angdist_old` | Maximum angular distortion over the Punjab grid (deg), ESRI:102028 (Albers, centred 125°E; previous analysis CRS) | **29.68** | `outputs/tables/course_tissot_distortion.csv` | crs = ESRI:102028 (Albers, centred 125°E; previous analysis CRS) (max over 25 rows) | `angular_distortion_deg` |
| `tissot_angdist_new` | Maximum angular distortion over the Punjab grid (deg), Analysis CRS (Albers, centred 72°E, 30°N; D025) | **0.11** | `outputs/tables/course_tissot_distortion.csv` | crs = Analysis CRS (Albers, centred 72°E, 30°N; D025) (max over 25 rows) | `angular_distortion_deg` |
| `gadf_ei` | GADF, arhti_share, 5 classes, Equal interval | **0.781** | `outputs/tables/course_classification_histograms.csv` | scheme = Equal interval | `gadf` |
| `gadf_q` | GADF, arhti_share, 5 classes, Quantiles | **0.781** | `outputs/tables/course_classification_histograms.csv` | scheme = Quantiles | `gadf` |
| `gadf_nb` | GADF, arhti_share, 5 classes, Natural breaks (Fisher-Jenks) | **0.818** | `outputs/tables/course_classification_histograms.csv` | scheme = Natural breaks (Fisher-Jenks) | `gadf` |
| `lisa_district_hh_p05` | LISA High-High districts, Queen, p < 0.05 (MAUP comparison) | **8** | `outputs/tables/lisa_counts.csv` | level = district; scenario = A; analysis = LISA arhti_share; weights = Queen; cluster = High-High | `p05` |
| `lisa_district_hh_fdr` | LISA High-High districts, Queen, FDR 0.05 (MAUP comparison) | **1** | `outputs/tables/lisa_counts.csv` | level = district; scenario = A; analysis = LISA arhti_share; weights = Queen; cluster = High-High | `fdr05` |
| `lisa_district_ll_p05` | LISA Low-Low districts, Queen, p < 0.05 (MAUP comparison) | **5** | `outputs/tables/lisa_counts.csv` | level = district; scenario = A; analysis = LISA arhti_share; weights = Queen; cluster = Low-Low | `p05` |
| `lisa_district_ll_fdr` | LISA Low-Low districts, Queen, FDR 0.05 (MAUP comparison) | **1** | `outputs/tables/lisa_counts.csv` | level = district; scenario = A; analysis = LISA arhti_share; weights = Queen; cluster = Low-Low | `fdr05` |
| `kmeans_t1_arhti` | k-means type 1 (attributes): median arhti_share | **63%** | `outputs/tables/course_kmeans_profiles.csv` | spec = attributes; type = 1 | `arhti_share` |
| `kmeans_t1_reach` | k-means type 1 (attributes): median small-farm reach | **106** | `outputs/tables/course_kmeans_profiles.csv` | spec = attributes; type = 1 | `small_farm_reach` |
| `kmeans_t2_reach` | k-means type 2 (attributes): median small-farm reach | **215** | `outputs/tables/course_kmeans_profiles.csv` | spec = attributes; type = 2 | `small_farm_reach` |
| `ws_moran_min` | Lowest Moran's I across five weighting specifications | **0.470** | `outputs/tables/course_weights_sensitivity.csv` | statistic = Moran's I (min over 5 rows) | `value` |
| `ws_moran_max` | Highest Moran's I across five weighting specifications | **0.568** | `outputs/tables/course_weights_sensitivity.csv` | statistic = Moran's I (max over 5 rows) | `value` |
| `dots_total` | Dasymetric dots (1 dot = 1,000 farms under 12.5 acres) | **4,738** | `outputs/tables/course_dasymetric_dots.csv` | all rows (sum over 36 rows) | `dots` |

## Literature (quoted)

| ID | Number | Shown as | Source | Row | Column |
|---|---|---|---|---|---|
| `lit_aleem_cost` | Literature: aleem_cost | **78.7%** | `docs/literature_numbers.csv` | id = aleem_cost | `display` |
| `lit_aleem_bank` | Literature: aleem_bank | **12 percent** | `docs/literature_numbers.csv` | id = aleem_bank | `display` |
| `lit_igc_markets` | Literature: igc_markets | **325** | `docs/literature_numbers.csv` | id = igc_markets | `display` |
| `lit_igc_range_low` | Literature: igc_range_low | **62** | `docs/literature_numbers.csv` | id = igc_range_low | `display` |
| `lit_igc_range_high` | Literature: igc_range_high | **80** | `docs/literature_numbers.csv` | id = igc_range_high | `display` |
| `lit_kf_large_hh` | Literature: kf_large_hh | **4 percent** | `docs/literature_numbers.csv` | id = kf_large_hh | `display` |
| `lit_kf_large_loans` | Literature: kf_large_loans | **42 percent** | `docs/literature_numbers.csv` | id = kf_large_loans | `display` |
| `lit_kf_small_hh` | Literature: kf_small_hh | **69 percent** | `docs/literature_numbers.csv` | id = kf_small_hh | `display` |
| `lit_kf_small_loans` | Literature: kf_small_loans | **23 percent** | `docs/literature_numbers.csv` | id = kf_small_loans | `display` |

## Allocation (36 districts)

| ID | Number | Shown as | Source | Row | Column |
|---|---|---|---|---|---|
| `hc36_subsistence_farms` | subsistence: share_farms_36 (36 districts; banks; no Islamabad, no MFIs) | **94.2%** | `outputs/tables/holding_class_shares.csv` | holding_class = subsistence | `share_farms_36` |
| `hc36_subsistence_operated_area` | subsistence: share_operated_area_36 (36 districts; banks; no Islamabad, no MFIs) | **68.7%** | `outputs/tables/holding_class_shares.csv` | holding_class = subsistence | `share_operated_area_36` |
| `hc36_subsistence_borrower_records` | subsistence: share_borrower_records_36 (36 districts; banks; no Islamabad, no MFIs) | **90.9%** | `outputs/tables/holding_class_shares.csv` | holding_class = subsistence | `share_borrower_records_36` |
| `hc36_subsistence_disbursement` | subsistence: share_disbursement_36 (36 districts; banks; no Islamabad, no MFIs) | **37.0%** | `outputs/tables/holding_class_shares.csv` | holding_class = subsistence | `share_disbursement_36` |
| `hc36_subsistence_per_record` | subsistence: disbursement per borrower record, Rs million (36 districts) | **0.52** | `outputs/tables/holding_class_shares.csv` | holding_class = subsistence | `disbursement_per_record_mn_36` |
| `hc36_economic_farms` | economic: share_farms_36 (36 districts; banks; no Islamabad, no MFIs) | **5.3%** | `outputs/tables/holding_class_shares.csv` | holding_class = economic | `share_farms_36` |
| `hc36_economic_operated_area` | economic: share_operated_area_36 (36 districts; banks; no Islamabad, no MFIs) | **22.7%** | `outputs/tables/holding_class_shares.csv` | holding_class = economic | `share_operated_area_36` |
| `hc36_economic_borrower_records` | economic: share_borrower_records_36 (36 districts; banks; no Islamabad, no MFIs) | **7.8%** | `outputs/tables/holding_class_shares.csv` | holding_class = economic | `share_borrower_records_36` |
| `hc36_economic_disbursement` | economic: share_disbursement_36 (36 districts; banks; no Islamabad, no MFIs) | **15.2%** | `outputs/tables/holding_class_shares.csv` | holding_class = economic | `share_disbursement_36` |
| `hc36_economic_per_record` | economic: disbursement per borrower record, Rs million (36 districts) | **2.51** | `outputs/tables/holding_class_shares.csv` | holding_class = economic | `disbursement_per_record_mn_36` |
| `hc36_above_economic_farms` | above_economic: share_farms_36 (36 districts; banks; no Islamabad, no MFIs) | **0.5%** | `outputs/tables/holding_class_shares.csv` | holding_class = above_economic | `share_farms_36` |
| `hc36_above_economic_operated_area` | above_economic: share_operated_area_36 (36 districts; banks; no Islamabad, no MFIs) | **8.6%** | `outputs/tables/holding_class_shares.csv` | holding_class = above_economic | `share_operated_area_36` |
| `hc36_above_economic_borrower_records` | above_economic: share_borrower_records_36 (36 districts; banks; no Islamabad, no MFIs) | **1.2%** | `outputs/tables/holding_class_shares.csv` | holding_class = above_economic | `share_borrower_records_36` |
| `hc36_above_economic_disbursement` | above_economic: share_disbursement_36 (36 districts; banks; no Islamabad, no MFIs) | **47.8%** | `outputs/tables/holding_class_shares.csv` | holding_class = above_economic | `share_disbursement_36` |
| `hc36_above_economic_per_record` | above_economic: disbursement per borrower record, Rs million (36 districts) | **50.62** | `outputs/tables/holding_class_shares.csv` | holding_class = above_economic | `disbursement_per_record_mn_36` |
| `hc36_tot_records` | Farm-sector borrower records, 36 districts (banks) | **658,112** | `outputs/tables/holding_class_shares.csv` | holding_class = subsistence | `total_borrower_records_36` |
| `hc_allp_tot_records` | Farm-sector borrower records, SBP All Punjab row (incl. MFIs and Islamabad) | **732,856** | `outputs/tables/holding_class_shares.csv` | holding_class = subsistence | `total_borrower_records_all_punjab` |
| `hc_mfi_records` | MFI borrower records without a district (All Punjab row only) | **74,494** | `outputs/tables/holding_class_shares.csv` | holding_class = subsistence | `mfi_borrower_records` |
| `rep_subsistence_records` | subsistence: borrower-record share / farm share (36 districts) | **0.97** | `outputs/tables/holding_class_shares.csv` | holding_class = subsistence | `ratio_records_to_farms_36` |
| `rep_subsistence_disb` | subsistence: disbursement share / farm share (36 districts) | **0.39** | `outputs/tables/holding_class_shares.csv` | holding_class = subsistence | `ratio_disbursement_to_farms_36` |
| `rep_economic_records` | economic: borrower-record share / farm share (36 districts) | **1.48** | `outputs/tables/holding_class_shares.csv` | holding_class = economic | `ratio_records_to_farms_36` |
| `rep_economic_disb` | economic: disbursement share / farm share (36 districts) | **2.87** | `outputs/tables/holding_class_shares.csv` | holding_class = economic | `ratio_disbursement_to_farms_36` |
| `rep_above_economic_records` | above_economic: borrower-record share / farm share (36 districts) | **2.35** | `outputs/tables/holding_class_shares.csv` | holding_class = above_economic | `ratio_records_to_farms_36` |
| `rep_above_economic_disb` | above_economic: disbursement share / farm share (36 districts) | **92.11** | `outputs/tables/holding_class_shares.csv` | holding_class = above_economic | `ratio_disbursement_to_farms_36` |
| `hc36_abv_ratio_sub` | Above-economic disbursement per record / subsistence (36 districts) | **97** | `outputs/tables/holding_class_shares.csv` | holding_class = above_economic | `per_record_ratio_to_subsistence_36` |

## H1 by source

| ID | Number | Shown as | Source | Row | Column |
|---|---|---|---|---|---|
| `h1_com_or` | Mantel-Haenszel OR, arhti x commercial (within tehsils) | **1.18** | `outputs/tables/course_h1_by_source.csv` | source = commercial | `mh_or` |
| `h1_com_lo` | 95% CI low, arhti x commercial | **1.09** | `outputs/tables/course_h1_by_source.csv` | source = commercial | `mh_ci95_low` |
| `h1_com_hi` | 95% CI high, arhti x commercial | **1.27** | `outputs/tables/course_h1_by_source.csv` | source = commercial | `mh_ci95_high` |
| `h1_com_rho` | Spearman rho across tehsils, arhti_share vs commercial share | **0.245** | `outputs/tables/course_h1_by_source.csv` | source = commercial | `spearman_rho` |
| `h1_com_share` | Share of rural populated mouzas reporting commercial credit | **38.2%** | `outputs/tables/course_h1_by_source.csv` | source = commercial | `mouza_share_reporting` |
| `h1_com_bv` | Bivariate Moran's I, arhti vs neighbours' commercial share (Queen) | **0.112** | `outputs/tables/course_h1_by_source.csv` | source = commercial | `bivariate_moran_I` |
| `h1_com_bvp` | Pseudo p, bivariate Moran, commercial | **0.062** | `outputs/tables/course_h1_by_source.csv` | source = commercial | `bivariate_moran_p` |
| `h1_ztbl_or` | Mantel-Haenszel OR, arhti x ztbl (within tehsils) | **0.98** | `outputs/tables/course_h1_by_source.csv` | source = ztbl | `mh_or` |
| `h1_ztbl_lo` | 95% CI low, arhti x ztbl | **0.90** | `outputs/tables/course_h1_by_source.csv` | source = ztbl | `mh_ci95_low` |
| `h1_ztbl_hi` | 95% CI high, arhti x ztbl | **1.07** | `outputs/tables/course_h1_by_source.csv` | source = ztbl | `mh_ci95_high` |
| `h1_ztbl_rho` | Spearman rho across tehsils, arhti_share vs ztbl share | **0.166** | `outputs/tables/course_h1_by_source.csv` | source = ztbl | `spearman_rho` |
| `h1_ztbl_share` | Share of rural populated mouzas reporting ztbl credit | **73.5%** | `outputs/tables/course_h1_by_source.csv` | source = ztbl | `mouza_share_reporting` |
| `h1_ztbl_bv` | Bivariate Moran's I, arhti vs neighbours' ztbl share (Queen) | **0.170** | `outputs/tables/course_h1_by_source.csv` | source = ztbl | `bivariate_moran_I` |
| `h1_ztbl_bvp` | Pseudo p, bivariate Moran, ztbl | **0.004** | `outputs/tables/course_h1_by_source.csv` | source = ztbl | `bivariate_moran_p` |
| `h1_coop_or` | Mantel-Haenszel OR, arhti x coop (within tehsils) | **1.72** | `outputs/tables/course_h1_by_source.csv` | source = coop | `mh_or` |
| `h1_coop_lo` | 95% CI low, arhti x coop | **1.58** | `outputs/tables/course_h1_by_source.csv` | source = coop | `mh_ci95_low` |
| `h1_coop_hi` | 95% CI high, arhti x coop | **1.87** | `outputs/tables/course_h1_by_source.csv` | source = coop | `mh_ci95_high` |
| `h1_coop_rho` | Spearman rho across tehsils, arhti_share vs coop share | **0.391** | `outputs/tables/course_h1_by_source.csv` | source = coop | `spearman_rho` |
| `h1_coop_share` | Share of rural populated mouzas reporting coop credit | **24.9%** | `outputs/tables/course_h1_by_source.csv` | source = coop | `mouza_share_reporting` |
| `h1_coop_bv` | Bivariate Moran's I, arhti vs neighbours' coop share (Queen) | **0.156** | `outputs/tables/course_h1_by_source.csv` | source = coop | `bivariate_moran_I` |
| `h1_coop_bvp` | Pseudo p, bivariate Moran, coop | **0.017** | `outputs/tables/course_h1_by_source.csv` | source = coop | `bivariate_moran_p` |
| `h1_mfb_or` | Mantel-Haenszel OR, arhti x mfb (within tehsils) | **1.76** | `outputs/tables/course_h1_by_source.csv` | source = mfb | `mh_or` |
| `h1_mfb_lo` | 95% CI low, arhti x mfb | **1.60** | `outputs/tables/course_h1_by_source.csv` | source = mfb | `mh_ci95_low` |
| `h1_mfb_hi` | 95% CI high, arhti x mfb | **1.93** | `outputs/tables/course_h1_by_source.csv` | source = mfb | `mh_ci95_high` |
| `h1_mfb_rho` | Spearman rho across tehsils, arhti_share vs mfb share | **0.380** | `outputs/tables/course_h1_by_source.csv` | source = mfb | `spearman_rho` |
| `h1_mfb_share` | Share of rural populated mouzas reporting mfb credit | **15.2%** | `outputs/tables/course_h1_by_source.csv` | source = mfb | `mouza_share_reporting` |
| `h1_mfb_bv` | Bivariate Moran's I, arhti vs neighbours' mfb share (Queen) | **0.088** | `outputs/tables/course_h1_by_source.csv` | source = mfb | `bivariate_moran_I` |
| `h1_mfb_bvp` | Pseudo p, bivariate Moran, mfb | **0.106** | `outputs/tables/course_h1_by_source.csv` | source = mfb | `bivariate_moran_p` |
| `h1_any_or` | Mantel-Haenszel OR, arhti x any formal (within tehsils) | **0.95** | `outputs/tables/course_h1_by_source.csv` | source = any formal | `mh_or` |
| `h1_any_lo` | 95% CI low, arhti x any formal | **0.87** | `outputs/tables/course_h1_by_source.csv` | source = any formal | `mh_ci95_low` |
| `h1_any_hi` | 95% CI high, arhti x any formal | **1.04** | `outputs/tables/course_h1_by_source.csv` | source = any formal | `mh_ci95_high` |
| `h1_com_both` | Pooled 2x2, arhti x commercial: n_both_sources | **3,137** | `outputs/tables/course_h1_by_source.csv` | source = commercial | `n_both_sources` |
| `h1_any_both` | Pooled 2x2, arhti x any formal source: n_both_sources | **5,680** | `outputs/tables/course_h1_by_source.csv` | source = any formal | `n_both_sources` |
| `h1_com_arhti_only` | Pooled 2x2, arhti x commercial: n_arhti_only | **4,150** | `outputs/tables/course_h1_by_source.csv` | source = commercial | `n_arhti_only` |
| `h1_any_arhti_only` | Pooled 2x2, arhti x any formal source: n_arhti_only | **1,463** | `outputs/tables/course_h1_by_source.csv` | source = any formal | `n_arhti_only` |
| `h1_com_other_only` | Pooled 2x2, arhti x commercial: n_other_only | **5,468** | `outputs/tables/course_h1_by_source.csv` | source = commercial | `n_other_only` |
| `h1_any_other_only` | Pooled 2x2, arhti x any formal source: n_other_only | **10,937** | `outputs/tables/course_h1_by_source.csv` | source = any formal | `n_other_only` |
| `h1_com_neither` | Pooled 2x2, arhti x commercial: n_neither | **8,919** | `outputs/tables/course_h1_by_source.csv` | source = commercial | `n_neither` |
| `h1_any_neither` | Pooled 2x2, arhti x any formal source: n_neither | **3,046** | `outputs/tables/course_h1_by_source.csv` | source = any formal | `n_neither` |
| `h1_com_dropped` | Pooled 2x2, arhti x commercial: mouzas_in_dropped_strata | **1,456** | `outputs/tables/course_h1_by_source.csv` | source = commercial | `mouzas_in_dropped_strata` |
| `h1_any_dropped` | Pooled 2x2, arhti x any formal source: mouzas_in_dropped_strata | **2,004** | `outputs/tables/course_h1_by_source.csv` | source = any formal | `mouzas_in_dropped_strata` |
| `h1_any_rho` | Spearman rho across tehsils, arhti_share vs any-formal share | **0.136** | `outputs/tables/course_h1_by_source.csv` | source = any formal | `spearman_rho` |
| `h1_any_share` | Share of rural populated mouzas reporting any formal source | **77.2%** | `outputs/tables/course_h1_by_source.csv` | source = any formal | `mouza_share_reporting` |
| `h1_any_bv` | Bivariate Moran's I, arhti vs neighbours' any-formal share | **0.159** | `outputs/tables/course_h1_by_source.csv` | source = any formal | `bivariate_moran_I` |
| `h1_com_cmh_bh` | BH-adjusted CMH p (five within-tehsil comparisons), commercial | **< 0.001** | `outputs/tables/course_h1_by_source.csv` | source = commercial | `cmh_p_bh` |
| `h1_com_rho_bh` | BH-adjusted Spearman p, commercial | **0.006** | `outputs/tables/course_h1_by_source.csv` | source = commercial | `spearman_p_bh` |
| `h1_com_bv_bh` | BH-adjusted bivariate Moran p, commercial | **0.077** | `outputs/tables/course_h1_by_source.csv` | source = commercial | `bivariate_moran_p_bh` |
| `h1_ztbl_cmh_bh` | BH-adjusted CMH p (five within-tehsil comparisons), ztbl | **0.682** | `outputs/tables/course_h1_by_source.csv` | source = ztbl | `cmh_p_bh` |
| `h1_ztbl_rho_bh` | BH-adjusted Spearman p, ztbl | **0.065** | `outputs/tables/course_h1_by_source.csv` | source = ztbl | `spearman_p_bh` |
| `h1_ztbl_bv_bh` | BH-adjusted bivariate Moran p, ztbl | **0.015** | `outputs/tables/course_h1_by_source.csv` | source = ztbl | `bivariate_moran_p_bh` |
| `h1_coop_cmh_bh` | BH-adjusted CMH p (five within-tehsil comparisons), coop | **< 0.001** | `outputs/tables/course_h1_by_source.csv` | source = coop | `cmh_p_bh` |
| `h1_coop_rho_bh` | BH-adjusted Spearman p, coop | **< 0.001** | `outputs/tables/course_h1_by_source.csv` | source = coop | `spearman_p_bh` |
| `h1_coop_bv_bh` | BH-adjusted bivariate Moran p, coop | **0.028** | `outputs/tables/course_h1_by_source.csv` | source = coop | `bivariate_moran_p_bh` |
| `h1_mfb_cmh_bh` | BH-adjusted CMH p (five within-tehsil comparisons), mfb | **< 0.001** | `outputs/tables/course_h1_by_source.csv` | source = mfb | `cmh_p_bh` |
| `h1_mfb_rho_bh` | BH-adjusted Spearman p, mfb | **< 0.001** | `outputs/tables/course_h1_by_source.csv` | source = mfb | `spearman_p_bh` |
| `h1_mfb_bv_bh` | BH-adjusted bivariate Moran p, mfb | **0.106** | `outputs/tables/course_h1_by_source.csv` | source = mfb | `bivariate_moran_p_bh` |
| `h1_any_cmh_bh` | BH-adjusted CMH p (five within-tehsil comparisons), any formal | **0.283** | `outputs/tables/course_h1_by_source.csv` | source = any formal | `cmh_p_bh` |
| `h1_any_rho_bh` | BH-adjusted Spearman p, any formal | **0.114** | `outputs/tables/course_h1_by_source.csv` | source = any formal | `spearman_p_bh` |
| `h1_any_bv_bh` | BH-adjusted bivariate Moran p, any formal | **0.015** | `outputs/tables/course_h1_by_source.csv` | source = any formal | `bivariate_moran_p_bh` |

## Market-access model

| ID | Number | Shown as | Source | Row | Column |
|---|---|---|---|---|---|
| `mm_ols_crop_p` | OLS (HC3): p-value, cropland_share | **0.039** | `outputs/tables/course_market_model.csv` | model = OLS (HC3); term = cropland_share | `p` |
| `mm_ols_mkt_p` | OLS (HC3): p-value, mkt_grain_51plus_share | **0.397** | `outputs/tables/course_market_model.csv` | model = OLS (HC3); term = mkt_grain_51plus_share | `p` |
| `mm_ols_com_p` | OLS (HC3): p-value, commercial_share | **0.712** | `outputs/tables/course_market_model.csv` | model = OLS (HC3); term = commercial_share | `p` |
| `mm_glm_crop_p` | Binomial GLM, quasi-binomial SEs (log-odds): p-value, cropland_share | **0.021** | `outputs/tables/course_market_model.csv` | model = Binomial GLM, quasi-binomial SEs (log-odds); term = cropland_share | `p` |
| `mm_glm_mkt_p` | Binomial GLM, quasi-binomial SEs (log-odds): p-value, mkt_grain_51plus_share | **0.061** | `outputs/tables/course_market_model.csv` | model = Binomial GLM, quasi-binomial SEs (log-odds); term = mkt_grain_51plus_share | `p` |
| `mm_glm_com_p` | Binomial GLM, quasi-binomial SEs (log-odds): p-value, commercial_share | **0.800** | `outputs/tables/course_market_model.csv` | model = Binomial GLM, quasi-binomial SEs (log-odds); term = commercial_share | `p` |
| `mm_sem_crop_p` | Spatial error (ML, Queen): p-value, cropland_share | **0.413** | `outputs/tables/course_market_model.csv` | model = Spatial error (ML, Queen); term = cropland_share | `p` |
| `mm_sem_mkt_p` | Spatial error (ML, Queen): p-value, mkt_grain_51plus_share | **0.417** | `outputs/tables/course_market_model.csv` | model = Spatial error (ML, Queen); term = mkt_grain_51plus_share | `p` |
| `mm_sem_com_p` | Spatial error (ML, Queen): p-value, commercial_share | **0.061** | `outputs/tables/course_market_model.csv` | model = Spatial error (ML, Queen); term = commercial_share | `p` |
| `mm_sem_lambda` | Spatial error model: lambda | **0.715** | `outputs/tables/course_market_model.csv` | model = Spatial error (ML, Queen); term = cropland_share | `fit` |
| `mm_glm_disp` | Quasi-binomial dispersion | **58.9** | `outputs/tables/course_market_model.csv` | model = Binomial GLM, quasi-binomial SEs (log-odds); term = cropland_share | `fit` |
| `mm_ols_r2` | OLS R² | **0.126** | `outputs/tables/course_market_model.csv` | model = OLS (HC3); term = cropland_share | `fit` |
| `rho_mkt51` | Spearman rho, arhti_share vs share of mouzas > 50 km from a grain market | **-0.25** | `outputs/tables/exploratory_associations.csv` | level = tehsil; scenario = A; x = mkt_grain_51plus_share | `rho` |
| `rho_mkt51_pbh` | BH-adjusted p-value | **0.009** | `outputs/tables/exploratory_associations.csv` | level = tehsil; scenario = A; x = mkt_grain_51plus_share | `p_bh` |
| `rho_mktin` | Spearman rho, arhti_share vs share of mouzas with a grain market in the mouza | **-0.03** | `outputs/tables/exploratory_associations.csv` | level = tehsil; scenario = A; x = mkt_grain_in_mouza_share | `rho` |
| `rho_mktin_pbh` | BH-adjusted p-value | **0.749** | `outputs/tables/exploratory_associations.csv` | level = tehsil; scenario = A; x = mkt_grain_in_mouza_share | `p_bh` |
| `mm_sem_aic` | Spatial error model fit (exploratory model) | **-22.2** | `outputs/tables/course_market_model.csv` | model = Spatial error (ML, Queen); term = cropland_share | `fit` |
| `mm_ols_aic` | OLS AIC (exploratory model) | **34.2** | `outputs/tables/course_market_model.csv` | model = Spatial error (ML, Queen); term = cropland_share | `fit` |
| `mm_ols_resid_I` | OLS residual Moran's I (exploratory model) | **0.418** | `outputs/tables/course_market_model.csv` | model = OLS (HC3); term = cropland_share | `fit` |
| `mm_sem_crop_coef` | Spatial error: cropland coefficient per SD | **-0.026** | `outputs/tables/course_market_model.csv` | model = Spatial error (ML, Queen); term = cropland_share | `coef_per_sd` |

## Neither source

| ID | Number | Shown as | Source | Row | Column |
|---|---|---|---|---|---|
| `all_com_both` | All rural populated mouzas, arhti x commercial: n_both_sources | **3,138** | `outputs/tables/mouza_cooccurrence.csv` | record = all mouzas (descriptive); scenario = A; pair = arhti x commercial | `n_both_sources` |
| `all_com_arhti_only` | All rural populated mouzas, arhti x commercial: n_arhti_only | **4,152** | `outputs/tables/mouza_cooccurrence.csv` | record = all mouzas (descriptive); scenario = A; pair = arhti x commercial | `n_arhti_only` |
| `all_com_other_only` | All rural populated mouzas, arhti x commercial: n_other_only | **5,694** | `outputs/tables/mouza_cooccurrence.csv` | record = all mouzas (descriptive); scenario = A; pair = arhti x commercial | `n_other_only` |
| `all_com_neither` | All rural populated mouzas, arhti x commercial: n_neither | **10,146** | `outputs/tables/mouza_cooccurrence.csv` | record = all mouzas (descriptive); scenario = A; pair = arhti x commercial | `n_neither` |
| `all_com_n` | All rural populated mouzas, arhti x commercial: n_mouzas | **23,130** | `outputs/tables/mouza_cooccurrence.csv` | record = all mouzas (descriptive); scenario = A; pair = arhti x commercial | `n_mouzas` |
| `all_any_both` | All rural populated mouzas, arhti x any formal (commercial, ZTBL, cooperative or MFB): n_both_sources | **5,825** | `outputs/tables/mouza_cooccurrence.csv` | record = all mouzas (descriptive); scenario = A; pair = arhti x any formal (commercial, ZTBL, cooperative or MFB) | `n_both_sources` |
| `all_any_arhti_only` | All rural populated mouzas, arhti x any formal (commercial, ZTBL, cooperative or MFB): n_arhti_only | **1,465** | `outputs/tables/mouza_cooccurrence.csv` | record = all mouzas (descriptive); scenario = A; pair = arhti x any formal (commercial, ZTBL, cooperative or MFB) | `n_arhti_only` |
| `all_any_other_only` | All rural populated mouzas, arhti x any formal (commercial, ZTBL, cooperative or MFB): n_other_only | **12,030** | `outputs/tables/mouza_cooccurrence.csv` | record = all mouzas (descriptive); scenario = A; pair = arhti x any formal (commercial, ZTBL, cooperative or MFB) | `n_other_only` |
| `all_any_neither` | All rural populated mouzas, arhti x any formal (commercial, ZTBL, cooperative or MFB): n_neither | **3,810** | `outputs/tables/mouza_cooccurrence.csv` | record = all mouzas (descriptive); scenario = A; pair = arhti x any formal (commercial, ZTBL, cooperative or MFB) | `n_neither` |
| `all_any_n` | All rural populated mouzas, arhti x any formal (commercial, ZTBL, cooperative or MFB): n_mouzas | **23,130** | `outputs/tables/mouza_cooccurrence.csv` | record = all mouzas (descriptive); scenario = A; pair = arhti x any formal (commercial, ZTBL, cooperative or MFB) | `n_mouzas` |
| `neither_median` | Median tehsil share of mouzas reporting neither arhti nor any formal source | **9.8%** | `outputs/tables/course_neither_source_tehsil.csv` | all rows (median over 137 rows) | `share_neither` |
| `neither_max` | Highest tehsil share reporting neither | **100.0%** | `outputs/tables/course_neither_source_tehsil.csv` | all rows (max over 137 rows) | `share_neither` |
| `all_any_unadj_or` | Province-wide unadjusted odds ratio, arhti x any formal source (all mouzas, no strata) | **1.26** | `outputs/tables/mouza_cooccurrence.csv` | record = all mouzas (descriptive); scenario = A; pair = arhti x any formal (commercial, ZTBL, cooperative or MFB) | `unadjusted_or` |
| `all_any_overlap` | Share of arhti-reporting mouzas that also report a formal source | **79.9%** | `outputs/tables/mouza_cooccurrence.csv` | record = all mouzas (descriptive); scenario = A; pair = arhti x any formal (commercial, ZTBL, cooperative or MFB) | `share_arhti_mouzas_with_other` |
| `all_any_either` | Share of mouzas reporting arhti or a formal source | **83.5%** | `outputs/tables/mouza_cooccurrence.csv` | record = all mouzas (descriptive); scenario = A; pair = arhti x any formal (commercial, ZTBL, cooperative or MFB) | `share_either` |
| `all_any_arhti_only_share` | Share of mouzas reporting arhti credit only | **6.3%** | `outputs/tables/mouza_cooccurrence.csv` | record = all mouzas (descriptive); scenario = A; pair = arhti x any formal (commercial, ZTBL, cooperative or MFB) | `share_arhti_only` |
| `all_any_neither_share` | Share of mouzas reporting neither | **16.5%** | `outputs/tables/mouza_cooccurrence.csv` | record = all mouzas (descriptive); scenario = A; pair = arhti x any formal (commercial, ZTBL, cooperative or MFB) | `share_neither_all` |

## Market bands

| ID | Number | Shown as | Source | Row | Column |
|---|---|---|---|---|---|
| `mb_w10_mean` | Share of mouzas: mkt_grain_within10_share | **40.4%** | `outputs/tables/course_market_bands.csv` | band = mkt_grain_within10_share | `mean_share` |
| `mb_w10_rho` | Spearman rho, arhti_share vs mkt_grain_within10_share | **0.336** | `outputs/tables/course_market_bands.csv` | band = mkt_grain_within10_share | `spearman_rho` |
| `mb_w10_rho_bh` | BH-adjusted p, mkt_grain_within10_share | **< 0.001** | `outputs/tables/course_market_bands.csv` | band = mkt_grain_within10_share | `spearman_p_bh` |
| `mb_w10_ols_p` | ols p-value of the market term (mkt_grain_within10_share) | **0.002** | `outputs/tables/course_market_bands.csv` | band = mkt_grain_within10_share | `ols_p` |
| `mb_w10_glm_p` | glm p-value of the market term (mkt_grain_within10_share) | **< 0.001** | `outputs/tables/course_market_bands.csv` | band = mkt_grain_within10_share | `glm_p` |
| `mb_w10_sem_p` | sem p-value of the market term (mkt_grain_within10_share) | **0.013** | `outputs/tables/course_market_bands.csv` | band = mkt_grain_within10_share | `sem_p` |
| `mb_w25_mean` | Share of mouzas: mkt_grain_within25_share | **81.1%** | `outputs/tables/course_market_bands.csv` | band = mkt_grain_within25_share | `mean_share` |
| `mb_w25_rho` | Spearman rho, arhti_share vs mkt_grain_within25_share | **0.377** | `outputs/tables/course_market_bands.csv` | band = mkt_grain_within25_share | `spearman_rho` |
| `mb_w25_rho_bh` | BH-adjusted p, mkt_grain_within25_share | **< 0.001** | `outputs/tables/course_market_bands.csv` | band = mkt_grain_within25_share | `spearman_p_bh` |
| `mb_w25_ols_p` | ols p-value of the market term (mkt_grain_within25_share) | **0.001** | `outputs/tables/course_market_bands.csv` | band = mkt_grain_within25_share | `ols_p` |
| `mb_w25_glm_p` | glm p-value of the market term (mkt_grain_within25_share) | **< 0.001** | `outputs/tables/course_market_bands.csv` | band = mkt_grain_within25_share | `glm_p` |
| `mb_w25_sem_p` | sem p-value of the market term (mkt_grain_within25_share) | **0.028** | `outputs/tables/course_market_bands.csv` | band = mkt_grain_within25_share | `sem_p` |
| `mb_o50_mean` | Share of mouzas: mkt_grain_51plus_share | **3.2%** | `outputs/tables/course_market_bands.csv` | band = mkt_grain_51plus_share | `mean_share` |
| `mb_o50_rho` | Spearman rho, arhti_share vs mkt_grain_51plus_share | **-0.249** | `outputs/tables/course_market_bands.csv` | band = mkt_grain_51plus_share | `spearman_rho` |
| `mb_o50_rho_bh` | BH-adjusted p, mkt_grain_51plus_share | **0.003** | `outputs/tables/course_market_bands.csv` | band = mkt_grain_51plus_share | `spearman_p_bh` |
| `mb_o50_ols_p` | ols p-value of the market term (mkt_grain_51plus_share) | **0.397** | `outputs/tables/course_market_bands.csv` | band = mkt_grain_51plus_share | `ols_p` |
| `mb_o50_glm_p` | glm p-value of the market term (mkt_grain_51plus_share) | **0.061** | `outputs/tables/course_market_bands.csv` | band = mkt_grain_51plus_share | `glm_p` |
| `mb_o50_sem_p` | sem p-value of the market term (mkt_grain_51plus_share) | **0.417** | `outputs/tables/course_market_bands.csv` | band = mkt_grain_51plus_share | `sem_p` |
| `mb_w10_sem_coef` | Spatial error coefficient per SD (mkt_grain_within10_share) | **0.055** | `outputs/tables/course_market_bands.csv` | band = mkt_grain_within10_share | `sem_coef_per_sd` |
| `mb_w10_sem_lo` | Spatial error 95% CI low (mkt_grain_within10_share) | **0.012** | `outputs/tables/course_market_bands.csv` | band = mkt_grain_within10_share | `sem_ci95_low` |
| `mb_w10_sem_hi` | Spatial error 95% CI high (mkt_grain_within10_share) | **0.098** | `outputs/tables/course_market_bands.csv` | band = mkt_grain_within10_share | `sem_ci95_high` |
| `mb_w10_sem_bh` | BH-adjusted spatial error p across three bands (mkt_grain_within10_share) | **0.039** | `outputs/tables/course_market_bands.csv` | band = mkt_grain_within10_share | `sem_p_bh` |
| `mb_w10_sem_holm` | Holm-adjusted spatial error p across three bands (mkt_grain_within10_share) | **0.039** | `outputs/tables/course_market_bands.csv` | band = mkt_grain_within10_share | `sem_p_holm` |
| `mb_w10_sem_lambda` | Spatial error lambda (mkt_grain_within10_share) | **0.703** | `outputs/tables/course_market_bands.csv` | band = mkt_grain_within10_share | `sem_lambda` |
| `mb_w10_sem_resid_I` | Moran's I of filtered residuals (mkt_grain_within10_share) | **-0.032** | `outputs/tables/course_market_bands.csv` | band = mkt_grain_within10_share | `sem_resid_moran_I` |
| `mb_w25_sem_coef` | Spatial error coefficient per SD (mkt_grain_within25_share) | **0.052** | `outputs/tables/course_market_bands.csv` | band = mkt_grain_within25_share | `sem_coef_per_sd` |
| `mb_w25_sem_lo` | Spatial error 95% CI low (mkt_grain_within25_share) | **0.006** | `outputs/tables/course_market_bands.csv` | band = mkt_grain_within25_share | `sem_ci95_low` |
| `mb_w25_sem_hi` | Spatial error 95% CI high (mkt_grain_within25_share) | **0.099** | `outputs/tables/course_market_bands.csv` | band = mkt_grain_within25_share | `sem_ci95_high` |
| `mb_w25_sem_bh` | BH-adjusted spatial error p across three bands (mkt_grain_within25_share) | **0.042** | `outputs/tables/course_market_bands.csv` | band = mkt_grain_within25_share | `sem_p_bh` |
| `mb_w25_sem_holm` | Holm-adjusted spatial error p across three bands (mkt_grain_within25_share) | **0.056** | `outputs/tables/course_market_bands.csv` | band = mkt_grain_within25_share | `sem_p_holm` |
| `mb_w25_sem_lambda` | Spatial error lambda (mkt_grain_within25_share) | **0.701** | `outputs/tables/course_market_bands.csv` | band = mkt_grain_within25_share | `sem_lambda` |
| `mb_w25_sem_resid_I` | Moran's I of filtered residuals (mkt_grain_within25_share) | **-0.032** | `outputs/tables/course_market_bands.csv` | band = mkt_grain_within25_share | `sem_resid_moran_I` |
| `mb_o50_sem_coef` | Spatial error coefficient per SD (mkt_grain_51plus_share) | **-0.018** | `outputs/tables/course_market_bands.csv` | band = mkt_grain_51plus_share | `sem_coef_per_sd` |
| `mb_o50_sem_lo` | Spatial error 95% CI low (mkt_grain_51plus_share) | **-0.063** | `outputs/tables/course_market_bands.csv` | band = mkt_grain_51plus_share | `sem_ci95_low` |
| `mb_o50_sem_hi` | Spatial error 95% CI high (mkt_grain_51plus_share) | **0.026** | `outputs/tables/course_market_bands.csv` | band = mkt_grain_51plus_share | `sem_ci95_high` |
| `mb_o50_sem_bh` | BH-adjusted spatial error p across three bands (mkt_grain_51plus_share) | **0.417** | `outputs/tables/course_market_bands.csv` | band = mkt_grain_51plus_share | `sem_p_bh` |
| `mb_o50_sem_holm` | Holm-adjusted spatial error p across three bands (mkt_grain_51plus_share) | **0.417** | `outputs/tables/course_market_bands.csv` | band = mkt_grain_51plus_share | `sem_p_holm` |
| `mb_o50_sem_lambda` | Spatial error lambda (mkt_grain_51plus_share) | **0.715** | `outputs/tables/course_market_bands.csv` | band = mkt_grain_51plus_share | `sem_lambda` |
| `mb_o50_sem_resid_I` | Moran's I of filtered residuals (mkt_grain_51plus_share) | **-0.037** | `outputs/tables/course_market_bands.csv` | band = mkt_grain_51plus_share | `sem_resid_moran_I` |
| `mb_w10_sem_pp` | Spatial error coefficient, within 10 km, in percentage points of arhti_share per SD | **5.5** | `outputs/tables/course_market_bands.csv` | band = mkt_grain_within10_share | `sem_coef_per_sd` |

## Prespecified models

| ID | Number | Shown as | Source | Row | Column |
|---|---|---|---|---|---|
| `b5_sem_com_coef` | Prespecified spatial error model: commercial_share coefficient | **0.193** | `outputs/tables/models_arhti.csv` | level = tehsil; model = Spatial error (ML; prespecified check); term = commercial_share | `coef` |
| `b5_sem_com_p` | Prespecified spatial error model: commercial_share p | **0.045** | `outputs/tables/models_arhti.csv` | level = tehsil; model = Spatial error (ML; prespecified check); term = commercial_share | `p` |
| `b5_sem_ob25_coef` | Prespecified spatial error model: onlinebank_over25km_share coefficient | **-0.442** | `outputs/tables/models_arhti.csv` | level = tehsil; model = Spatial error (ML; prespecified check); term = onlinebank_over25km_share | `coef` |
| `b5_sem_ob25_p` | Prespecified spatial error model: onlinebank_over25km_share p | **0.036** | `outputs/tables/models_arhti.csv` | level = tehsil; model = Spatial error (ML; prespecified check); term = onlinebank_over25km_share | `p` |
| `b5_sem_crop_coef` | Prespecified spatial error model: cropland_share coefficient | **-0.070** | `outputs/tables/models_arhti.csv` | level = tehsil; model = Spatial error (ML; prespecified check); term = cropland_share | `coef` |
| `b5_sem_crop_p` | Prespecified spatial error model: cropland_share p | **0.615** | `outputs/tables/models_arhti.csv` | level = tehsil; model = Spatial error (ML; prespecified check); term = cropland_share | `p` |
| `b5_sem_ztbl_coef` | Prespecified spatial error model: ztbl_share coefficient | **-0.065** | `outputs/tables/models_arhti.csv` | level = tehsil; model = Spatial error (ML; prespecified check); term = ztbl_share | `coef` |
| `b5_sem_ztbl_p` | Prespecified spatial error model: ztbl_share p | **0.450** | `outputs/tables/models_arhti.csv` | level = tehsil; model = Spatial error (ML; prespecified check); term = ztbl_share | `p` |
| `b5_ols_com_p` | Prespecified OLS: commercial_share p | **0.489** | `outputs/tables/models_arhti.csv` | level = tehsil; model = OLS (HC3); term = commercial_share | `p` |
| `b5_lag_com_p` | Post-hoc spatial lag: commercial_share p | **0.104** | `outputs/tables/models_arhti.csv` | level = tehsil; model = Spatial lag (ML; POST-HOC); term = commercial_share | `p` |
| `b5_ols_ob25_p` | Prespecified OLS: onlinebank_over25km_share p | **0.229** | `outputs/tables/models_arhti.csv` | level = tehsil; model = OLS (HC3); term = onlinebank_over25km_share | `p` |
| `b5_lag_ob25_p` | Post-hoc spatial lag: onlinebank_over25km_share p | **0.130** | `outputs/tables/models_arhti.csv` | level = tehsil; model = Spatial lag (ML; POST-HOC); term = onlinebank_over25km_share | `p` |

## Coverage reconciliation

| ID | Number | Shown as | Source | Row | Column |
|---|---|---|---|---|---|
| `rc_d36_records` | Borrower records: 36 districts (banks) | **658,112** | `outputs/tables/sbp_coverage_reconciliation.csv` | scope = 36 districts (banks) | `tot_borrowers` |
| `rc_d36_bn` | Disbursement, Rs billion: 36 districts (banks) | **848.4** | `outputs/tables/sbp_coverage_reconciliation.csv` | scope = 36 districts (banks) | `tot_amount_bn` |
| `rc_isl_records` | Borrower records: Islamabad row (banks) | **250** | `outputs/tables/sbp_coverage_reconciliation.csv` | scope = Islamabad row (banks) | `tot_borrowers` |
| `rc_isl_bn` | Disbursement, Rs billion: Islamabad row (banks) | **34.2** | `outputs/tables/sbp_coverage_reconciliation.csv` | scope = Islamabad row (banks) | `tot_amount_bn` |
| `rc_mfi_records` | Borrower records: MFIs (Punjab-wide, no district) | **74,494** | `outputs/tables/sbp_coverage_reconciliation.csv` | scope = MFIs (Punjab-wide, no district) | `tot_borrowers` |
| `rc_mfi_bn` | Disbursement, Rs billion: MFIs (Punjab-wide, no district) | **5.1** | `outputs/tables/sbp_coverage_reconciliation.csv` | scope = MFIs (Punjab-wide, no district) | `tot_amount_bn` |
| `rc_allp_records` | Borrower records: SBP All Punjab row | **732,856** | `outputs/tables/sbp_coverage_reconciliation.csv` | scope = SBP All Punjab row | `tot_borrowers` |
| `rc_allp_bn` | Disbursement, Rs billion: SBP All Punjab row | **887.7** | `outputs/tables/sbp_coverage_reconciliation.csv` | scope = SBP All Punjab row | `tot_amount_bn` |

## Census area check

| ID | Number | Shown as | Source | Row | Column |
|---|---|---|---|---|---|
| `agc_c25_avg` | Implied average farm area (acres), class 2.5 TO UNDER 5.0 | **5.38** | `outputs/tables/agc_class_area_check.csv` | size_class = 2.5 TO UNDER 5.0 | `implied_avg_farm_area_ac` |
| `agc_c5_avg` | Implied average farm area (acres), class 5.0 TO UNDER 7.5 | **9.08** | `outputs/tables/agc_class_area_check.csv` | size_class = 5.0 TO UNDER 7.5 | `implied_avg_farm_area_ac` |
| `agc_c75_avg` | Implied average farm area (acres), class 7.5 TO UNDER 12.5 | **15.02** | `outputs/tables/agc_class_area_check.csv` | size_class = 7.5 TO UNDER 12.5 | `implied_avg_farm_area_ac` |

## H2/H3 sensitivity

| ID | Number | Shown as | Source | Row | Column |
|---|---|---|---|---|---|
| `sv_ex_D` | Excluding flagged: dissimilarity, borrower records vs small farms | **0.182** | `outputs/tables/course_h2_h3_sensitivity.csv` | sample = excluding the 5 flagged districts | `D_sub_borrowers_vs_small_farms` |
| `sv_ex_sub_disb` | Excluding flagged: subsistence share of disbursement | **39.7%** | `outputs/tables/course_h2_h3_sensitivity.csv` | sample = excluding the 5 flagged districts | `sub_share_of_disbursement` |
| `sv_ex_abv_disb` | Excluding flagged: above-economic share of disbursement | **42.0%** | `outputs/tables/course_h2_h3_sensitivity.csv` | sample = excluding the 5 flagged districts | `abv_share_of_disbursement` |
| `sv_ur_group` | Five districts with the largest urban populations (Population Census 2023) | **Lahore, Faisalabad, Rawalpindi, Gujranwala, Multan** | `outputs/tables/course_h2_h3_sensitivity.csv` | sample = all 36 districts; five districts with the largest urban populations (Population Census 2023) | `group` |
| `sv_ur_abv` | Five districts with the largest urban populations: share of above-economic disbursement | **43.5%** | `outputs/tables/course_h2_h3_sensitivity.csv` | sample = all 36 districts; five districts with the largest urban populations (Population Census 2023) | `group_abv_disbursement_share` |
| `sv_ur_cult` | Five districts with the largest urban populations: share of cultivated area | **11.2%** | `outputs/tables/course_h2_h3_sensitivity.csv` | sample = all 36 districts; five districts with the largest urban populations (Population Census 2023) | `group_cultivated_share` |
| `sv_ur_sub` | Five districts with the largest urban populations: share of subsistence disbursement | **17.3%** | `outputs/tables/course_h2_h3_sensitivity.csv` | sample = all 36 districts; five districts with the largest urban populations (Population Census 2023) | `group_sub_disbursement_share` |
| `sv_al_abv_ratio` | Five city districts: above-economic disbursement share / cultivated share | **4.49** | `outputs/tables/course_h2_h3_sensitivity.csv` | sample = all 36 districts | `group_abv_ratio_to_cultivated` |
| `sv_al_sub_ratio` | Five city districts: subsistence disbursement share / cultivated share | **1.69** | `outputs/tables/course_h2_h3_sensitivity.csv` | sample = all 36 districts | `group_sub_ratio_to_cultivated` |
| `sv_al_abv_cls` | Five city districts: above-economic disbursement share / share of farms of 50+ acres | **3.32** | `outputs/tables/course_h2_h3_sensitivity.csv` | sample = all 36 districts | `group_abv_ratio_to_class_farms` |
| `sv_al_sub_cls` | Five city districts: subsistence disbursement share / share of farms under 12.5 acres | **1.22** | `outputs/tables/course_h2_h3_sensitivity.csv` | sample = all 36 districts | `group_sub_ratio_to_class_farms` |
| `sv_loo_abv_min` | Leave one city out: lowest above-economic ratio to cultivated share | **4.41** | `outputs/tables/course_h2_h3_sensitivity.csv` | kind = leave-one-out (min over 5 rows) | `group_abv_ratio_to_cultivated` |
| `sv_loo_abv_max` | Leave one city out: highest above-economic ratio to cultivated share | **5.65** | `outputs/tables/course_h2_h3_sensitivity.csv` | kind = leave-one-out (max over 5 rows) | `group_abv_ratio_to_cultivated` |
| `sv_loo_sub_min` | Leave one city out: lowest subsistence ratio to cultivated share | **1.33** | `outputs/tables/course_h2_h3_sensitivity.csv` | kind = leave-one-out (min over 5 rows) | `group_sub_ratio_to_cultivated` |
| `sv_loo_sub_max` | Leave one city out: highest subsistence ratio to cultivated share | **1.97** | `outputs/tables/course_h2_h3_sensitivity.csv` | kind = leave-one-out (max over 5 rows) | `group_sub_ratio_to_cultivated` |
| `urban_rank1` | Rank 1 district by urban population, 2023 | **Lahore** | `outputs/tables/course_urban_population_top.csv` | rank = 1 | `district` |
| `urban_rank1_pop` | Urban population 2023, rank 1 | **13,004,135** | `outputs/tables/course_urban_population_top.csv` | rank = 1 | `urban_pop` |
| `urban_rank2` | Rank 2 district by urban population, 2023 | **Faisalabad** | `outputs/tables/course_urban_population_top.csv` | rank = 2 | `district` |
| `urban_rank2_pop` | Urban population 2023, rank 2 | **4,392,979** | `outputs/tables/course_urban_population_top.csv` | rank = 2 | `urban_pop` |
| `urban_rank3` | Rank 3 district by urban population, 2023 | **Rawalpindi** | `outputs/tables/course_urban_population_top.csv` | rank = 3 | `district` |
| `urban_rank3_pop` | Urban population 2023, rank 3 | **4,210,785** | `outputs/tables/course_urban_population_top.csv` | rank = 3 | `urban_pop` |
| `urban_rank4` | Rank 4 district by urban population, 2023 | **Gujranwala** | `outputs/tables/course_urban_population_top.csv` | rank = 4 | `district` |
| `urban_rank4_pop` | Urban population 2023, rank 4 | **3,593,971** | `outputs/tables/course_urban_population_top.csv` | rank = 4 | `urban_pop` |
| `urban_rank5` | Rank 5 district by urban population, 2023 | **Multan** | `outputs/tables/course_urban_population_top.csv` | rank = 5 | `district` |
| `urban_rank5_pop` | Urban population 2023, rank 5 | **2,499,871** | `outputs/tables/course_urban_population_top.csv` | rank = 5 | `urban_pop` |
