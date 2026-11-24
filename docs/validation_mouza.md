# Validation: Mouza Census 2020 tehsil extraction

Written by `scripts/04_extract_mouza.py` on 2026-10-31. Vintage: Mouza Census 2020 (PBS), fieldwork Jan-Mar 2020.

**Source used:** Excel mouza-level records from the RAR (aggregated by PBS district + tehsil codes). The RAR contains no pre-built tables. Published PDF tables were parsed only to validate.

## Scope

- Punjab mouza records: 26,462; ICT records excluded: 195 (ICT is a separate province in the Excel).
- Tehsils (unique district code + tehsil code): 148; of which Cholistan: 3; tehsils with 0 rural populated mouzas: 6.

## Check 1: Punjab totals vs published figures supplied

| Variable | Excel | Expected | Diff | Result |
|---|---|---|---|---|
| rp_mouzas | 23,130 | 23,130 | +0 | PASS |
| n_ztbl | 16,989 | 16,989 | +0 | PASS |
| n_coop | 5,753 | 5,753 | +0 | PASS |
| n_commercial | 8,832 | 8,832 | +0 | PASS |
| n_mfb | 3,526 | 3,526 | +0 | PASS |
| n_arhti | 7,290 | 7,290 | +0 | PASS |
| n_others | 5,184 | 9,418 | -4,234 | **FAIL** |

Note on `n_others`: the **detailed** Table 8.1 Punjab row (report p. 479) prints Others = 5,184. The summary Table 8.1 on report p. 54 prints 9,418. NGO + RSP + Govt + Others = 1,054 + 1,985 + 1,195 + 5,184 = 9,418. Those are counts of mouza-mentions, not mouzas (a mouza can report several), so 9,418 is not a mouza count. `n_others` is kept as the detailed-table 'Others' column. **Needs Ahmed's decision** on which 'others' definition to use.

## Check 2: Bahawalnagar district

| Variable | Excel | Expected | Diff | Result |
|---|---|---|---|---|
| rp_mouzas (Bahawalnagar) | 1,043 | 1,043 | +0 | PASS |

## Check 3: tehsils sum to district totals

- (a) Sum of Excel tehsil values vs **published** district rows: 1844 of 1844 district×variable cells match; 0 mismatches.
- (b) Internal consistency of the report: sum of published tehsil rows vs published district rows: 8 mismatching cells.

Mismatches (b):

| Table | District | Variable | Published tehsil sum | Published district | Reason |
|---|---|---|---|---|---|
| 1.1 | ATTOCK DISTRICT | mouzas_forest_unpopulated | 2 | 4.0 | tehsil row(s) unreadable in PDF text layer, so the published tehsil sum is incomplete |
| 1.1 | ATTOCK DISTRICT | mouzas_partly_urban | 7 | 11.0 | tehsil row(s) unreadable in PDF text layer, so the published tehsil sum is incomplete |
| 1.1 | ATTOCK DISTRICT | mouzas_rural | 260 | 394.0 | tehsil row(s) unreadable in PDF text layer, so the published tehsil sum is incomplete |
| 1.1 | ATTOCK DISTRICT | mouzas_total | 298 | 458.0 | tehsil row(s) unreadable in PDF text layer, so the published tehsil sum is incomplete |
| 1.1 | ATTOCK DISTRICT | mouzas_unpopulated | 10 | 27.0 | tehsil row(s) unreadable in PDF text layer, so the published tehsil sum is incomplete |
| 1.1 | ATTOCK DISTRICT | mouzas_urban | 19 | 22.0 | tehsil row(s) unreadable in PDF text layer, so the published tehsil sum is incomplete |
| 1.1 | ATTOCK DISTRICT | rp_mouzas | 267 | 405.0 | tehsil row(s) unreadable in PDF text layer, so the published tehsil sum is incomplete |
| 1.1 | LAHORE DISTRICT | rp_mouzas | 0 | nan | district cell printed blank (fully urban district) |

## Check 4: shares within [0, 1]

- Shares outside [0, 1]: 0 (PASS).
- Undefined shares (tehsil has 0 rural populated mouzas): 6 tehsils; shares left blank.

## Check 5: every published row (all levels), Excel vs PDF

| Table | Cells compared | Exact matches | Mismatches |
|---|---|---|---|
| 1.1 | 1544 | 1544 | 0 |
| 6.3 | 1692 | 1692 | 0 |
| 6.7 | 3384 | 3384 | 0 |
| 8.1 | 1880 | 1880 | 0 |
| 8.2 | 1128 | 1128 | 0 |

Cells printed blank in the PDF (rural-populated column of fully urban units in Table 1.1) and equal to 0 in the Excel: 7; blank in PDF but non-zero in Excel: 0.

Average-distance columns (published as rounded integers; Excel mean over mouzas *without* the facility, rounded; tolerance ±1 km): 916 of 940 cells within tolerance. Averages are **not** included in mouza_tehsil.csv.

Excel units with no parsed row in a published table (row unreadable in the PDF text layer; these cells were NOT validated against the PDF). Units with 0 rural populated mouzas (Lahore district's 5 tehsils, Bahawalpur City) are correctly absent from Tables 6.3-8.2 and not listed:

- Table 1.1: tehsil, ATTOCK DISTRICT / JAND
- Table 1.1: tehsil, ATTOCK DISTRICT / PINDI GHEB

## Data anomalies found in the mouza records (reported, not corrected)

- Table 6.3: 23 rural-populated mouzas have distance to metalled road = 0 (road types {'1': 20, '3': 3}); not placed in any band (the published table has no 0 band)

## PDF parsing problems

- T1.1 line 2416: numbers merged/unreadable, row NOT compared: JAND 3 38 80 64 1 1 - -14 65
- T1.1 line 2417: numbers merged/unreadable, row NOT compared: PINDI GHEB 5 37 80 70 2 3 -2 373
