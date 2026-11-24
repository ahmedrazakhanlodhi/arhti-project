# Paper outline

**Where the Bank Ends and the Arhti Begins: Mapping Access, Allocation, and the Cost of Agricultural Credit in Punjab.**
Paper due Dec 9, 2026. Ahmed Raza Khan Lodhi and Hasnain Akram, PPHA 38520, University of Chicago.

**Central question:** does the geography of agricultural finance correspond to where farming happens and who farms?

Numbers come from `docs/key_numbers.md` (IDs in brackets). Rules (`docs/project_rules.md`): descriptive verbs only;
never "credit desert"; vintages stated; PRESENCE, AVAILABILITY and ALLOCATION kept separate. Every SBP district statistic is "district
as reported by SBP (attribution under verification)" until the attribution is confirmed (D039).

## 1. Introduction
## 2. Background
- 2.1 Arhtis: commission agents in grain markets; credit tied to crop sales; published cost estimates (CONTEXT).
- 2.2 Formal agricultural credit: SBP holding classes; ZTBL, cooperative bank, commercial banks; branch networks.
- 2.3 The Kissan Card as post-period context (registration from 1 Jun 2024; operational from 15 Oct 2024) [`kissan_terms`].
## 3. Data and methods
- Mouza Census 2020 (availability); SBP FY2023-24 (borrower records and amounts by district as reported); Agricultural Census
  2024 (farms, operated and cultivated area, crops); SBP branch list (30 Jun 2024); SBP Monthly Statistical Bulletin Table 3.33.
- Spatial statistics (Queen, row-standardised, [`permutations`] permutations, seed [`seed`]; FDR with BH cutoff); Mantel–Haenszel.
- Location quotients; holding-class shares; concentration coefficient; descriptive scorecard rule.
## 4. Results
### 4.1 Access (Figures 2, 3, 4)
- Availability [`arhti_pooled`]; clustering [`moran_arhti_queen`]; LISA counts; bivariate [`bv_queen`].
- Mouza OR [`mh_or`] ([`mh_lo`]–[`mh_hi`]); Breslow–Day [`bd_p`]; [`tehsils_ratio_above1`]/[`tehsils_ratio_below1`];
  cropland [`rho_cropland`] (exploratory); online commercial-bank branch in the village, a PRESENCE measure [`rho_onlinebank`] (exploratory).
### 4.2 Allocation (Figures A1, 5, S6)
- Holding-class shares [`hc_*`]; small-farm reach [`reach_min`]–[`reach_max`]; crop structure [`top_crop_wheat`],
  [`second_crop_*`]; concentration [`cc_all`]; tenure in one sentence [`rho_tenant`].
### 4.3 Reporting geography (Figures R1, R2)
- LQ maps [`lq_abv_lahore`], [`lq_sub_jhelum`] (flagged); five-city summary [`five_*`]; Lahore branches
  [`lahore_total_branches_10k`] vs [`lahore_rural_branches_10k`]; Islamabad [`isb_credit_share_tot`].
### 4.4 Cost (Figure P1; context)
- IGC arhti implicit costs [`lit_igc_rates`]; farmer-reported bank rates [`igc_bank_low`]–[`igc_bank_high`]; SBP Table 3.33 FY2012-13
  and FY2023-24 [`rate_*`]; Kissan Card; PMN/MEDA note [`lit_pmn_markup`] off the axis.
### 4.5 District scorecard (Table 1)
- Profile counts [`profile_*`]; districts listed by profile.
## 5. Robustness (one sentence each)
- kNN [`moran_arhti_knn`]; district level [`moran_arhti_district`]; Cholistan B [`moran_arhti_B`], [`mh_or_B`]; flagged-district
  exclusion [`cc_excl`], [`moran_reach_excl`].
## 6. Discussion
- Possible mechanisms from published work, not findings: interlinked marketing and credit; speed and collateral; branch networks and
  booking practices.
## 7. Limitations
## 8. Conclusion
## Appendix
- A1 Regressions (`models_arhti.csv`, `regression_diagnostics.csv`); A2 jackknife ranges; A3 full exploratory associations;
  A4 tenure correlations; A5 exclusion classifications (Figure S5); A6 classification comparison (S1); A7 district LISA (S2);
  A8 published-study locations (S3, CONTEXT); A9 village-level co-reporting by tehsil (S4, EXPLORATORY); A10 concentration curve (S6);
  A11 methods appendix, decisions, validation, human verification checklist.
