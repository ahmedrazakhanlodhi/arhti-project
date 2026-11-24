# Match audit: Mouza Census 2020 tehsils → OCHA COD-AB ADM3 (Punjab)

Written by `scripts/05_boundaries_join.py` on 2026-10-31. Data: Mouza Census 2020 (PBS), fieldwork Jan-Mar 2020. Boundaries: OCHA COD-AB Pakistan, valid_on 2022-09-09. The boundaries post-date the census (not contemporaneous). Decisions: `docs/crosswalk_manual.csv`, `docs/crosswalk_manual_district.csv` (decided by Ahmed).

**Coverage language (D027):** *administrative assignment* = the share of rural populated mouzas assigned to a polygon. It is not geographic precision: polygons that aggregate several census units (parent_aggregation) conceal internal differences.

## Boundaries

- adm3: 139 Punjab features, CRS EPSG:4326, invalid geometries: 0
-   area check (analysis-CRS km2 / attribute area_sqkm): min 1.0000, max 1.0000
- adm2: 36 Punjab features, CRS EPSG:4326, invalid geometries: 0
-   area check (analysis-CRS km2 / attribute area_sqkm): min 1.0000, max 1.0000

## Tehsil assignments by match type

| Match type | Census tehsils | Rural populated mouzas | % of 23,130 |
|---|---|---|---|
| exact | 115 | 18,768 | 81.1% |
| normalized | 11 | 2,189 | 9.5% |
| parent_aggregation | 8 | 626 | 2.7% |
| rename | 2 | 352 | 1.5% |
| spelling | 9 | 1,195 | 5.2% |
| unmatched | 3 | 0 | 0.0% |

**Administrative assignment: 23,130 / 23,130 rural populated mouzas (100.0%).** Gate (≥ 95%): **GO: Q1 at tehsil level**.

## Integrity checks

- No census tehsil is assigned more than once (each `source_code` appears once): PASS.
- Harmonized totals reconcile: option A tehsil polygons 23,130, districts 23,130 (expected 23,130); option B tehsil 22,807, districts 22,807 (expected 23,130 − 323 Cholistan = 22,807).
- No harmonized polygon identifier is duplicated: PASS.
- Crosswalk rows without a final match type or decision: 0; unmatched rows with rural populated mouzas and no decision: 0.

## Every non-exact assignment (decided by Ahmed)

| match_type | source_district | source_name | source_code | rp_mouzas | ocha_name | ocha_pcode | decision | historical_name | decision_note |
|---|---|---|---|---|---|---|---|---|---|
| normalized | BHAKKAR DISTRICT | BHAKKAR TEHSIL | PB-058-194 | 217 | Bhakkar | PK60401 | accept |  | rules: collapse doubled letters; drop suffix TEHSIL/DISTRICT; remove spaces |
| normalized | BHAKKAR DISTRICT | DARYA KHAN TEHSIL | PB-058-195 | 103 | Darya Khan | PK60402 | accept |  | rules: drop suffix TEHSIL/DISTRICT; remove spaces |
| normalized | BHAKKAR DISTRICT | KALUR KOT TEHSIL | PB-058-196 | 92 | Kalur Kot | PK60403 | accept |  | rules: drop suffix TEHSIL/DISTRICT; remove spaces |
| normalized | BHAKKAR DISTRICT | MANKERA TEHSIL | PB-058-197 | 104 | Mankera | PK60404 | accept |  | rules: drop suffix TEHSIL/DISTRICT; remove spaces |
| normalized | MIANWALI DISTRICT | ISA KHEL | PB-060-201 | 56 | Isakhel | PK62101 | accept |  | rules: remove spaces |
| normalized | SHEIKHUPURA DISTRICT | FEROZE WALA | PB-046-146 | 83 | Ferozewala | PK63301 | accept |  | rules: remove spaces |
| normalized | SIALKOT DISTRICT | DASKA TEHSIL | PB-042-133 | 244 | Daska | PK63401 | accept |  | rules: drop suffix TEHSIL/DISTRICT; remove spaces |
| normalized | SIALKOT DISTRICT | PASROOR TEHSIL | PB-042-134 | 543 | Pasrur | PK63402 | accept |  | rules: OO->U, EE->I; drop suffix TEHSIL/DISTRICT; remove spaces |
| normalized | SIALKOT DISTRICT | SAMBRIAL TEHSIL | PB-042-135 | 143 | Sambrial | PK63403 | accept |  | rules: drop suffix TEHSIL/DISTRICT; remove spaces |
| normalized | SIALKOT DISTRICT | SIALKOT TEHSIL | PB-042-136 | 474 | Sialkot | PK63404 | accept |  | rules: drop suffix TEHSIL/DISTRICT; remove spaces |
| normalized | TOBA TEK SINGH DISTRICT | PIRMAHAL | PB-036-115 | 130 | Pir Mahal | PK63504 | accept |  | rules: remove spaces |
| parent_aggregation | BAHAWALPUR DISTRICT | BAHAWALPUR SADDAR | PB-027-602 | 114 | Bahawalpur | PK60302 | accept |  | Bahawalpur Saddar + Bahawalpur City summed into OCHA Bahawalpur |
| parent_aggregation | BAHAWALPUR DISTRICT | BAHAWALPUR CITY | PB-027-075 | 0 | Bahawalpur | PK60302 | accept |  | Bahawalpur Saddar + Bahawalpur City summed into OCHA Bahawalpur |
| parent_aggregation | CHAKWAL DISTRICT | LAWA | PB-052-174 | 17 | Tala Gang | PK60504 | accept |  | Lawa (17 mouzas) summed into Tala Gang; OCHA polygon ~2,975 km2, consistent with the pre-split combined Talagang |
| parent_aggregation | CHOLISTAN | FORT ABBAS | PB-999-071 | 46 | Fort Abbas | PK60203 | accept |  | Cholistan option A: Cholistan Fort Abbas (PBS tehsil code 71) summed into OCHA Fort Abbas |
| parent_aggregation | CHOLISTAN | YAZMAN | PB-999-079 | 144 | Yazman | PK60305 | accept |  | Cholistan option A: Cholistan Yazman (PBS tehsil code 79) summed into OCHA Yazman |
| parent_aggregation | CHOLISTAN | LIAQUATPUR | PB-999-081 | 133 | Liaqatpur | PK62802 | accept |  | Cholistan option A: Cholistan Liaquatpur (PBS tehsil code 81) summed into OCHA Liaqatpur |
| parent_aggregation | GUJRANWALA DISTRICT | GUJRANWALA CITY | PB-037-117 | 4 | Gujranwala | PK60901 | accept |  | Gujranwala Saddar + Gujranwala City summed into OCHA Gujranwala |
| parent_aggregation | GUJRANWALA DISTRICT | GUJRANWALA SADDAR | PB-037-118 | 168 | Gujranwala | PK60901 | accept |  | Gujranwala Saddar + Gujranwala City summed into OCHA Gujranwala |
| rename | DERA GHAZI KHAN DISTRICT | DE-EXCLUDED AREA D.G KHAN | PB-029-084 | 330 | D.G Khan (Tribal Area) | PK60701 | accept | De-excluded Area D.G. Khan | also known as Koh-e-Suleman (Population Census 2023 name) |
| rename | RAJANPUR DISTRICT | DE-EXCLUDED AREA RAJANPUR | PB-032-095 | 22 | Rajanpur (Tribal Area) | PK62903 | accept | De-excluded Area Rajanpur |  |
| spelling | DERA GHAZI KHAN DISTRICT | KOT CHHUTTA | PB-029-086 | 100 | Kot Chatta | PK60703 | accept |  |  |
| spelling | FAISALABAD DISTRICT | SAMMUNDRI | PB-034-106 | 116 | Summundri | PK60805 | accept |  |  |
| spelling | JHANG DISTRICT | 18-HAZARI | PB-035-108 | 102 | Athara Hazari | PK61204 | accept |  |  |
| spelling | KASUR DISTRICT | KOT RADHA KISHON | PB-043-139 | 69 | Kot Radha Kishen | PK61403 | accept |  |  |
| spelling | KHUSHAB DISTRICT | NOWSHERA | PB-059-597 | 28 | Naushera | PK61602 | accept |  |  |
| spelling | LAYYAH DISTRICT | LAYYAH | PB-030-090 | 306 | Leiah | PK61803 | accept |  |  |
| spelling | MIANWALI DISTRICT | MAINWALI | PB-060-202 | 83 | Mianwali | PK62102 | accept |  |  |
| spelling | RAHIM YAR KHAN DISTRICT | LIAQUATPUR | PB-028-081 | 235 | Liaqatpur | PK62802 | accept |  |  |
| spelling | SHEIKHUPURA DISTRICT | SHEIKHUPRA | PB-046-150 | 156 | Sheikhupura | PK63305 | accept |  |  |
| unmatched | LAHORE DISTRICT | MODEL TOWN | PB-044-547 | 0 |  |  | leave_unmatched |  | 0 rural populated mouzas; no OCHA polygon |
| unmatched | LAHORE DISTRICT | RAIWIND | PB-044-548 | 0 |  |  | leave_unmatched |  | 0 rural populated mouzas; no OCHA polygon |
| unmatched | LAHORE DISTRICT | SHALIMAR | PB-044-549 | 0 |  |  | leave_unmatched |  | 0 rural populated mouzas; no OCHA polygon |

## District assignments (Mouza Census → OCHA ADM2)

| mouza_district | ocha_district | ocha_pcode | match_type | decision |
|---|---|---|---|---|
| ATTOCK DISTRICT | Attock | PK601 | normalized |  |
| BAHAWALNAGAR DISTRICT | Bahawalnagar | PK602 | normalized |  |
| BAHAWALPUR DISTRICT | Bahawalpur | PK603 | normalized |  |
| BHAKKAR DISTRICT | Bhakkar | PK604 | normalized |  |
| CHAKWAL DISTRICT | Chakwal | PK605 | normalized |  |
| CHINIOT DISTRICT | Chiniot | PK606 | normalized |  |
| CHOLISTAN |  |  | unmatched |  |
| DERA GHAZI KHAN DISTRICT | Dera Ghazi Khan | PK607 | normalized |  |
| FAISALABAD DISTRICT | Faisalabad | PK608 | normalized |  |
| GUJRANWALA DISTRICT | Gujranwala | PK609 | normalized |  |
| GUJRAT DISTRICT | Gujrat | PK610 | normalized |  |
| HAFIZABAD DISTRICT | Hafizabad | PK611 | normalized |  |
| JHANG DISTRICT | Jhang | PK612 | normalized |  |
| JHELUM DISTRICT | Jhelum | PK613 | normalized |  |
| KASUR DISTRICT | Kasur | PK614 | normalized |  |
| KHANEWAL DISTRICT | Khanewal | PK615 | normalized |  |
| KHUSHAB DISTRICT | Khushab | PK616 | normalized |  |
| LAHORE DISTRICT | Lahore | PK617 | normalized |  |
| LAYYAH DISTRICT | Leiah | PK618 | spelling | accept |
| LODHRAN DISTRICT | Lodhran | PK619 | normalized |  |
| MANDI BAHAUDDIN DISTRICT | Mandi Bahauddin | PK620 | normalized |  |
| MIANWALI DISTRICT | Mianwali | PK621 | normalized |  |
| MULTAN DISTRICT | Multan | PK622 | normalized |  |
| MUZAFFARGARH DISTRICT | Muzaffargarh | PK623 | normalized |  |
| NANKANA SAHIB DISTRICT | Nankana Sahib | PK624 | normalized |  |
| NAROWAL DISTRICT | Narowal | PK625 | normalized |  |
| OKARA DISTRICT | Okara | PK626 | normalized |  |
| PAKPATTAN DISTRICT | Pakpattan | PK627 | normalized |  |
| RAHIM YAR KHAN DISTRICT | Rahim Yar Khan | PK628 | normalized |  |
| RAJANPUR DISTRICT | Rajanpur | PK629 | normalized |  |
| RAWALPINDI DISTRICT | Rawalpindi | PK630 | normalized |  |
| SAHIWAL DISTRICT | Sahiwal | PK631 | normalized |  |
| SARGODHA DISTRICT | Sargodha | PK632 | normalized |  |
| SHEIKHUPURA DISTRICT | Sheikhupura | PK633 | normalized |  |
| SIALKOT DISTRICT | Sialkot | PK634 | normalized |  |
| TOBA TEK SINGH DISTRICT | Toba Tek Singh | PK635 | normalized |  |
| VEHARI DISTRICT | Vehari | PK636 | normalized |  |

OCHA tehsil polygons without any assigned census tehsil: none.

## Cholistan (D015: decided by Ahmed)

Option A (primary): the three Cholistan census tehsils (PB-999-071/079/081) are summed into OCHA Fort Abbas, Yazman and Liaqatpur. Option B (required sensitivity): Cholistan excluded. Both scenarios are built from the same processed file (`is_cholistan`), as layers `tehsil`/`district_fallback` (A) and `tehsil_optB`/`district_fallback_optB` (B). Maps note that Fort Abbas, Yazman and Liaqatpur combine desert (Cholistan) and irrigated mouzas.

## Administrative structure differences

OCHA's tehsil layer appears to follow an older structure (Lahore 2 vs 5 tehsils; no Lawa; no City/Saddar splits in Bahawalpur and Gujranwala). These are handled as parent_aggregation (Bahawalpur, Gujranwala, Lawa → Tala Gang) or left unmatched (Lahore's Model Town, Raiwind, Shalimar: 0 rural populated mouzas). No census unit is split across polygons.
