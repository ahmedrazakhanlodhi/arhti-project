# Key numbers

Every number used in the main text, the app and the slides. Written by `scripts/15_key_numbers.py` from finished outputs; nothing here is computed anew. Source = file; Row = filter that selects the row; Column = field.

## Data

| ID | Number | Shown as | Source | Row | Column |
|---|---|---|---|---|---|
| `n_tehsils` | Tehsils in the Q1 analysis (rural populated mouzas > 0) | **137** | `outputs/tables/q1_descriptives.csv` | level = tehsil; scenario = A | `n` |
| `rp_mouzas` | Rural populated mouzas (denominator of every share) | **23,130** | `outputs/tables/q1_descriptives.csv` | level = tehsil; scenario = A | `rp_mouzas` |
| `excluded_tehsils` | Tehsils with no rural populated mouzas (not in the Q1 sample) | **Lahore Cantt; Lahore City** | `outputs/tables/q1_descriptives.csv` | level = tehsil; scenario = A | `excluded_zero_rp` |
| `n_districts_q2` | Districts with small-farm reach | **36** | `outputs/arhti_project.gpkg | layer q2_districts_credit_allocation` | all rows (count over 36 rows) | `small_farm_reach` |

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

## Robustness

| ID | Number | Shown as | Source | Row | Column |
|---|---|---|---|---|---|
| `moran_arhti_knn` | Global Moran's I, arhti_share, tehsils, geodesic kNN-5 | **0.568** | `outputs/tables/moran_global.csv` | level = tehsil; scenario = A; variable = arhti_share; weights = kNN-5 (geodesic) | `I` |
| `moran_arhti_district` | Global Moran's I, arhti_share, districts (n = 35), Queen | **0.429** | `outputs/tables/moran_global.csv` | level = district; scenario = A; variable = arhti_share; weights = Queen | `I` |
| `moran_arhti_B` | Global Moran's I, arhti_share, tehsils, Queen, Cholistan scenario B | **0.543** | `outputs/tables/moran_global.csv` | level = tehsil; scenario = B; variable = arhti_share; weights = Queen | `I` |
| `mh_or_B` | Mantel-Haenszel odds ratio, arhti x commercial, scenario B | **1.20** | `outputs/tables/mouza_cooccurrence.csv` | record = pooled (Mantel-Haenszel); scenario = B; pair = arhti x commercial | `mh_or` |
| `mh_lo_B` | 95% CI lower bound, scenario B | **1.11** | `outputs/tables/mouza_cooccurrence.csv` | record = pooled (Mantel-Haenszel); scenario = B; pair = arhti x commercial | `ci95_low` |
| `mh_hi_B` | 95% CI upper bound, scenario B | **1.29** | `outputs/tables/mouza_cooccurrence.csv` | record = pooled (Mantel-Haenszel); scenario = B; pair = arhti x commercial | `ci95_high` |

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
