# Credit allocation by holding size: district summary (DESCRIPTIVE, 2026-11-24)

Data: SBP, FY2023-24 (Jul 2023-Jun 2024), loans by booking district; Agricultural Census 2024 (PBS), sample-based, fieldwork 2024-25; Mouza Census 2020 (PBS), Jan-Mar 2020; branches: SBP list of scheduled bank branches as on 30 June 2024. Vintages differ and are not contemporaneous. Unit: OCHA ADM2 district (Q2 keeps all districts, including Lahore, which has no rural populated mouzas, D028). CRS: Albers equal-area centred on Punjab (lat_1 28, lat_2 33, lat_0 30, lon_0 72; WGS84).

**Concepts (D029, D034).** PRESENCE = physical facilities (RURAL branches per 10,000 farms; online bank in/near mouza; all-branch density only as a sensitivity). AVAILABILITY = credit sources reported in the Mouza Census (commercial_share, arhti_share, ...). ALLOCATION = who formal credit reaches: small_farm_reach = reported subsistence-holding borrower records per 1,000 farms under 12.5 acres (SBP FY2023-24, by booking district; borrower records may not be unique individuals).

## Province-level headline (single statistic; not mapped)

Above-economic holdings: 1.1% of farm-sector disbursed borrower records and 49.4% of farm-sector disbursement (All-Punjab row including MFIs; 8,024 of 732,856; Rs 438,386.5 of 887,737.4 mn). Bank district rows only (excl. MFIs, incl. Islamabad): 1.2% and 49.7%. SBP, FY2023-24 (Jul 2023-Jun 2024), loans by booking district.

## Coverage

Districts with small_farm_reach: 36 of 36 (all name matches decided by Ahmed, D022/D024).

## Distributions

|                                        |   count |    min |    25% |     50% |     75% |     max |
|:---------------------------------------|--------:|-------:|-------:|--------:|--------:|--------:|
| small_farm_reach                       |  36.000 | 21.593 | 71.298 | 118.545 | 165.821 | 298.969 |
| rural_branches_per_10k_farms           |  36.000 |  1.810 |  3.838 |   5.237 |   7.286 |  15.340 |
| all_branches_per_10k_farms_sensitivity |  36.000 |  3.559 |  8.584 |  12.813 |  19.143 | 190.447 |
| tenant_share                           |  36.000 |  0.008 |  0.042 |   0.059 |   0.088 |   0.189 |
| owner_cum_tenant_share                 |  36.000 |  0.008 |  0.043 |   0.058 |   0.090 |   0.134 |
| large_farm_area_share                  |  36.000 |  0.017 |  0.054 |   0.083 |   0.108 |   0.267 |
| small_farm_share_of_farms              |  36.000 |  0.891 |  0.930 |   0.940 |   0.954 |   0.992 |

*large_farm_area_share = concentration of OPERATED area in farms ≥ 50 acres (not landownership).*

## Results: all matched districts (n = 36)

- Spearman ρ, small_farm_reach vs arhti_share = 0.42 (p = 0.01, n = 35); vs commercial_share = 0.38 (p = 0.02, n = 35).

Global Moran's I, small_farm_reach (Queen and geodesic kNN-5, row-standardised; 999 permutations, seed 20261031). Small sample:

| weights          |   n | islands   |   components |     I |     EI |   z_perm |   p_perm |
|:-----------------|----:|:----------|-------------:|------:|-------:|---------:|---------:|
| Queen            |  36 | none      |            1 | 0.532 | -0.029 |    5.331 |    0.001 |
| kNN-5 (geodesic) |  36 | none      |            1 | 0.401 | -0.029 |    4.651 |    0.001 |

**High reported commercial-bank credit availability, low small-farm reach** (commercial_share ≥ median 0.382 AND small_farm_reach ≤ 33rd percentile 89.1; n classified = 35): Attock, Chiniot, Gujranwala, Sialkot. Consistent with barriers beyond physical distance; it does not identify them.

**High rural-branch presence, low small-farm reach** (rural_branches_per_10k_farms ≥ median 5.237 AND small_farm_reach ≤ 33rd percentile 83.9; n classified = 36): Attock, Chakwal, Gujrat, Jhelum, Mandi Bahauddin, Mianwali, Rawalpindi, Sialkot. Consistent with barriers beyond physical distance; it does not identify them.

**SENSITIVITY (all branches): high branch density, low small-farm reach** (all_branches_per_10k_farms_sensitivity ≥ median 12.813 AND small_farm_reach ≤ 33rd percentile 83.9; n classified = 36): Attock, Gujrat, Jhelum, Lahore, Mandi Bahauddin, Rawalpindi, Sialkot. Consistent with barriers beyond physical distance; it does not identify them.

Same districts under both classifications: Attock, Sialkot; availability only: Chiniot, Gujranwala; presence only: Chakwal, Gujrat, Jhelum, Mandi Bahauddin, Mianwali, Rawalpindi. Rural-branch vs all-branch (sensitivity) presence classification: both Attock, Gujrat, Jhelum, Mandi Bahauddin, Rawalpindi, Sialkot; rural only Chakwal, Mianwali; all-branch only Lahore.

Concentration coefficient (districts ordered by small_farm_reach) = 0.297. Lowest-reach districts: Rawalpindi, Jhelum, Chakwal, Gujrat, Attock. Highest: Bahawalnagar, Bahawalpur, Okara, Lodhran, Hafizabad.

## Results: excluding flagged districts (n = 31)

- Spearman ρ, small_farm_reach vs arhti_share = 0.24 (p = 0.20, n = 31); vs commercial_share = 0.19 (p = 0.31, n = 31).

Global Moran's I, small_farm_reach (Queen and geodesic kNN-5, row-standardised; 999 permutations, seed 20261031). Small sample:

| weights          |   n | islands   |   components |     I |     EI |   z_perm |   p_perm |
|:-----------------|----:|:----------|-------------:|------:|-------:|---------:|---------:|
| Queen            |  31 | none      |            1 | 0.428 | -0.033 |    3.783 |    0.001 |
| kNN-5 (geodesic) |  31 | none      |            1 | 0.309 | -0.033 |    3.524 |    0.003 |

**High reported commercial-bank credit availability, low small-farm reach** (commercial_share ≥ median 0.447 AND small_farm_reach ≤ 33rd percentile 105.0; n classified = 31): Attock, Chiniot, Sialkot. Consistent with barriers beyond physical distance; it does not identify them.

**High rural-branch presence, low small-farm reach** (rural_branches_per_10k_farms ≥ median 4.862 AND small_farm_reach ≤ 33rd percentile 105.0; n classified = 31): Attock, Gujranwala, Gujrat, Mandi Bahauddin, Mianwali, Sheikhupura, Sialkot. Consistent with barriers beyond physical distance; it does not identify them.

**SENSITIVITY (all branches): high branch density, low small-farm reach** (all_branches_per_10k_farms_sensitivity ≥ median 12.068 AND small_farm_reach ≤ 33rd percentile 105.0; n classified = 31): Attock, Gujranwala, Gujrat, Mandi Bahauddin, Mianwali, Sheikhupura, Sialkot. Consistent with barriers beyond physical distance; it does not identify them.

Same districts under both classifications: Attock, Sialkot; availability only: Chiniot; presence only: Gujranwala, Gujrat, Mandi Bahauddin, Mianwali, Sheikhupura. Rural-branch vs all-branch (sensitivity) presence classification: both Attock, Gujranwala, Gujrat, Mandi Bahauddin, Mianwali, Sheikhupura, Sialkot; rural only none; all-branch only none.

Concentration coefficient (districts ordered by small_farm_reach) = 0.255. Lowest-reach districts: Gujrat, Attock, Khushab, Dera Ghazi Khan, Sialkot. Highest: Bahawalnagar, Bahawalpur, Okara, Lodhran, Hafizabad.

## Q2 tenure associations (Spearman; BH-adjusted within each family)

| family                               | x                      |   n |   rho |   p_raw |   p_bh |
|:-------------------------------------|:-----------------------|----:|------:|--------:|-------:|
| all districts (n = 36)               | tenant_share           |  36 | 0.392 |   0.018 |  0.018 |
| all districts (n = 36)               | owner_cum_tenant_share |  36 | 0.452 |   0.006 |  0.010 |
| all districts (n = 36)               | large_farm_area_share  |  36 | 0.445 |   0.007 |  0.010 |
| excluding flagged districts (n = 31) | tenant_share           |  31 | 0.241 |   0.192 |  0.192 |
| excluding flagged districts (n = 31) | owner_cum_tenant_share |  31 | 0.352 |   0.052 |  0.079 |
| excluding flagged districts (n = 31) | large_farm_area_share  |  31 | 0.474 |   0.007 |  0.021 |

## POST-HOC exploratory associations with arhti_share (BH-adjusted within each level × scenario)

| level    | scenario   | x                            |   n |    rho |   p_raw |   p_bh | note                                                                         |
|:---------|:-----------|:-----------------------------|----:|-------:|--------:|-------:|:-----------------------------------------------------------------------------|
| tehsil   | A          | onlinebank_in_mouza_share    | 137 | -0.403 |   0.000 |  0.000 |                                                                              |
| tehsil   | A          | onlinebank_over25km_share    | 137 | -0.212 |   0.013 |  0.023 |                                                                              |
| tehsil   | A          | commercial_share             | 137 |  0.245 |   0.004 |  0.009 |                                                                              |
| tehsil   | A          | ztbl_share                   | 137 |  0.166 |   0.052 |  0.078 |                                                                              |
| tehsil   | A          | mkt_grain_in_mouza_share     | 137 | -0.028 |   0.749 |  0.749 |                                                                              |
| tehsil   | A          | mkt_grain_51plus_share       | 137 | -0.249 |   0.003 |  0.009 |                                                                              |
| tehsil   | A          | cropland_share               | 137 |  0.486 |   0.000 |  0.000 |                                                                              |
| tehsil   | A          | tt_city_cropw_hours          | 137 | -0.115 |   0.180 |  0.231 |                                                                              |
| tehsil   | A          | road_metalled_share          | 137 |  0.028 |   0.747 |  0.749 |                                                                              |
| tehsil   | B          | onlinebank_in_mouza_share    | 137 | -0.385 |   0.000 |  0.000 |                                                                              |
| tehsil   | B          | onlinebank_over25km_share    | 137 | -0.238 |   0.005 |  0.009 |                                                                              |
| tehsil   | B          | commercial_share             | 137 |  0.262 |   0.002 |  0.006 |                                                                              |
| tehsil   | B          | ztbl_share                   | 137 |  0.199 |   0.019 |  0.029 |                                                                              |
| tehsil   | B          | mkt_grain_in_mouza_share     | 137 | -0.019 |   0.825 |  0.825 |                                                                              |
| tehsil   | B          | mkt_grain_51plus_share       | 137 | -0.251 |   0.003 |  0.007 |                                                                              |
| tehsil   | B          | cropland_share               | 137 |  0.488 |   0.000 |  0.000 |                                                                              |
| tehsil   | B          | tt_city_cropw_hours          | 137 | -0.114 |   0.186 |  0.240 |                                                                              |
| tehsil   | B          | road_metalled_share          | 137 |  0.062 |   0.469 |  0.527 |                                                                              |
| district | A          | onlinebank_in_mouza_share    |  35 | -0.553 |   0.001 |  0.006 |                                                                              |
| district | A          | onlinebank_over25km_share    |  35 | -0.294 |   0.086 |  0.216 |                                                                              |
| district | A          | rural_branches_per_10k_farms |  35 |  0.090 |   0.606 |  0.674 | PRESENCE (rural branches); district only (farms are not available by tehsil) |
| district | A          | commercial_share             |  35 |  0.171 |   0.325 |  0.464 |                                                                              |
| district | A          | ztbl_share                   |  35 |  0.201 |   0.247 |  0.412 |                                                                              |
| district | A          | mkt_grain_in_mouza_share     |  35 |  0.032 |   0.853 |  0.853 |                                                                              |
| district | A          | mkt_grain_51plus_share       |  35 | -0.521 |   0.001 |  0.007 |                                                                              |
| district | A          | cropland_share               |  35 |  0.404 |   0.016 |  0.054 |                                                                              |
| district | A          | tt_city_cropw_hours          |  35 | -0.230 |   0.183 |  0.367 |                                                                              |
| district | A          | road_metalled_share          |  35 | -0.124 |   0.478 |  0.597 |                                                                              |
| district | B          | onlinebank_in_mouza_share    |  35 | -0.529 |   0.001 |  0.007 |                                                                              |
| district | B          | onlinebank_over25km_share    |  35 | -0.287 |   0.094 |  0.235 |                                                                              |
| district | B          | rural_branches_per_10k_farms |  35 |  0.084 |   0.630 |  0.700 | PRESENCE (rural branches); district only (farms are not available by tehsil) |
| district | B          | commercial_share             |  35 |  0.204 |   0.241 |  0.344 |                                                                              |
| district | B          | ztbl_share                   |  35 |  0.245 |   0.156 |  0.312 |                                                                              |
| district | B          | mkt_grain_in_mouza_share     |  35 |  0.051 |   0.771 |  0.771 |                                                                              |
| district | B          | mkt_grain_51plus_share       |  35 | -0.521 |   0.001 |  0.007 |                                                                              |
| district | B          | cropland_share               |  35 |  0.404 |   0.016 |  0.054 |                                                                              |
| district | B          | tt_city_cropw_hours          |  35 | -0.228 |   0.188 |  0.313 |                                                                              |
| district | B          | road_metalled_share          |  35 | -0.086 |   0.623 |  0.700 |                                                                              |

## Flagged districts (excluded in the sensitivity run): Chakwal, Faisalabad, Jhelum, Lahore, Rawalpindi

See `docs/validation_sbp.md` for reasons.

## PRESENCE: scheduled-bank branches (SBP list of scheduled bank branches as on 30 June 2024; rural = coded 'R' in the list)

Punjab rows in the list: 9,003 branches (sheet 'Banks', i.e. scheduled banks; microfinance banks and DFIs are on a separate sheet and not counted). One row coded Lahore has a Lower Dir (KP) address (decisions.md O4); it is counted as listed. No second source for this date was checked, so no cross-source total comparison is made.

