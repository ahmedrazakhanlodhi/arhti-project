# Validation: SBP FY2023-24 and Agricultural Census 2024 extraction (2026-11-24)

Written by `scripts/08_credit_allocation.py`. SBP, FY2023-24 (Jul 2023-Jun 2024), loans by booking district. Agricultural Census 2024 (PBS), sample-based, fieldwork 2024-25.

## SBP: published figures

| Check | Extracted | Published | Result |
|---|---|---|---|
| All Punjab total disbursed borrowers | 732,856.0 | 732,856.0 | PASS |
| All Punjab total disbursed amount (Rs mn) | 887,737.4 | 887,737.4 | PASS |
| All Punjab above-economic borrowers | 8,024.0 | 8,024.0 | PASS |
| All Punjab above-economic amount (Rs mn) | 438,386.5 | 438,386.5 | PASS |

The published All-Punjab row = sum of the 37 district rows ('Total': 658,362 borrowers, Rs 882,609.9 mn) + 'MFIs' (74,494 borrowers, Rs 5,127.5 mn, all in the subsistence columns, Punjab-wide only). **The MFI figures are not distributed to districts and are excluded from all district measures.** The 37 district rows include **Islamabad**, which is dropped from the analysis.

## SBP: internal consistency

- District rows sum to 'Total': PASS
- 'Total' + 'MFIs' = 'All Punjab': PASS
- Total columns = subsistence + economic + above-economic, every row and field: PASS. (The printed header '18=3+7+13' is a typo for 3+8+13; the data follow 3+8+13.)
- xlsx vs DWS PDF p. 1, every row × 20 columns (amounts at 0.1 mn): rows not found in PDF text: none; mismatches: 2
  - ('MFIs', 'sub_borrowers', 74494.0, 5127.5)
  - ('MFIs', 'sub_amount_mn', 5127.5, 74494.0)

## SBP holding thresholds (CL1-Annex, *Indicative Credit Limits and Eligible Items for Agriculture Financing 2022-23*, Table 2.7, PDF p. 11)

Extracted line: `1 Punjab Up to 12.5 90 64 12.5 to 50 9 23 Above 50 1 13`

| Category (Punjab) | Acres | % of farms | % of area |
|---|---|---|---|
| Subsistence holding | up to 12.5 | 90 | 64 |
| Economic holding | 12.5 to 50.0 | 9 | 23 |
| Above economic holding | above 50.0 | 1 | 13 |

Source: Pakistan Agricultural Census 2010, Pakistan Bureau of Statistics Government of Pakistan (GoP) The thresholds are from the **2010** census, and the table gives no irrigated/unirrigated split for Punjab. Whether borrowers are classified by land owned or land operated is not stated in Table 2.7 [CHECK].

## Agricultural Census 2024: extraction checks

- Size classes used by PBS: UNDER 1.0, 1.0 TO UNDER 2.5, 2.5 TO UNDER 5.0, 5.0 TO UNDER 7.5, 7.5 TO UNDER 12.5, 12.5 TO UNDER 25.0, 25.0 TO UNDER 50.0, 50.0 TO UNDER 100.0, 100.0 AND ABOVE (acres).
- Size classes sum to 'PRIVATE-FARMS TOTAL' (farms, farm area, cultivated area, tenant farms), all units: PASS
- Table_1 farms = Table_3 farms, every unit × class: PASS
- Owner + owner-cum-tenant + tenant = farms, every unit × class: PASS
- District/division/province totals vs report Table 1.1 (farms, farm area, cultivated area) and Table 1.3 (tenure): 46 units compared, 0 mismatches (±1); units not found in report text: ['DERA GHAZI KHAN DIVISION']

**Cholistan Area** (separate Ag Census unit, no SBP/OCHA counterpart): 19,536 farms (0.4% of Punjab), 284,651 acres (0.9%). Excluded from district denominators pending D015/D021.

## Size-class alignment (SBP vs Ag Census): reported, not forced

| SBP category | SBP acres | Closest Ag Census classes | Boundary difference |
|---|---|---|---|
| Subsistence | up to 12.5 | Under 1.0 … 7.5–<12.5 | SBP includes exactly 12.5 acres; the census puts 12.5 in 12.5–<25 |
| Economic | 12.5–50.0 | 12.5–<25, 25–<50 | SBP includes exactly 50 (and its lower bound overlaps 'up to 12.5'); the census puts 50 in 50–<100 |
| Above economic | above 50.0 | 50–<100, 100+ | farms of exactly 50 acres are 'economic' for SBP, 'large' in the census |

The cut points coincide (12.5 and 50 acres). The differences are at the two boundary points, and in the concept: the census measures **operated farm area** of a household's farm in 2023-24; SBP classifies **borrowers** (basis not stated). Farms reported at exactly 12.5 or 50 acres cannot be identified in the published classes, so their size is unknown.

## SBP data-quality screen (D021: F1 loan size >5× or <0.2× Punjab median; F2 above-economic >75% of disbursement)

Punjab district medians (excl. Islamabad), Rs per disbursed borrower: subsistence 456,726; economic 2,585,109; above-economic 25,351,177.

| District (SBP name) | Subsistence avg (× median) | Economic avg (×) | Above-econ avg (×) | Above-econ share of amount | Flag reasons |
|---|---|---|---|---|---|
| Islamabad | 515,594 (1.1) | 108,926,444 (42.1) | 1,945,801,824 (76.8) | 97% | note: only 9 economic borrowers (ratio not flagged); note: only 17 above_economic borrowers (ratio not flagged); F2 above-economic = 97% of farm-sector disbursement |
| Rawalpindi | 552,110 (1.2) | 53,310,385 (20.6) | 2,033,653,300 (80.2) | 96% | note: only 13 economic borrowers (ratio not flagged); F1 above_economic disbursement per borrower record Rs 2,033,653,300 = 80.2x Punjab median (Rs 25,351,177); F2 above-economic = 96% of farm-sector disbursement |
| Lahore | 1,238,910 (2.7) | 4,540,322 (1.8) | 214,036,239 (8.4) | 78% | F1 above_economic disbursement per borrower record Rs 214,036,239 = 8.4x Punjab median (Rs 25,351,177); F2 above-economic = 78% of farm-sector disbursement |
| Faisalabad | 528,607 (1.2) | 3,052,784 (1.2) | 134,156,726 (5.3) | 67% | F1 above_economic disbursement per borrower record Rs 134,156,726 = 5.3x Punjab median (Rs 25,351,177) |
| Chakwal | 333,022 (0.7) | 378,309 (0.1) | 12,541,035 (0.5) | 39% | F1 economic disbursement per borrower record Rs 378,309 = 0.1x Punjab median (Rs 2,585,109) |
| Attock | 2,083,806 (4.6) | 5,444,925 (2.1) | 126,718,250 (5.0) | 12% | note: only 12 above_economic borrowers (ratio not flagged) |
| Jehlum | 17,689,384 (38.7) | 2,178,511 (0.8) | 122,017,667 (4.8) | 4% | F1 subsistence disbursement per borrower record Rs 17,689,384 = 38.7x Punjab median (Rs 456,726); note: only 9 above_economic borrowers (ratio not flagged) |

### Suspects named in the brief, and near misses (reported; thresholds NOT changed after seeing the data)

| District | Flagged | Subsistence × median | Economic × median | Above-econ × median | Above-econ share | Borrowers sub / eco / abv |
|---|---|---|---|---|---|---|
| Attock (near miss) | False | 4.6 | 2.1 | 5.0 | 12% | 4,901 / 93 / 12 |
| Faisalabad (flagged) | True | 1.2 | 1.2 | 5.3 | 67% | 20,308 / 1,366 / 226 |
| Islamabad (suspect) | True | 1.1 | 42.1 | 76.8 | 97% | 224 / 9 / 17 |
| Jehlum (suspect) | True | 38.7 | 0.8 | 4.8 | 4% | 1,410 / 47 / 9 |
| Lahore (suspect) | True | 2.7 | 1.8 | 8.4 | 78% | 5,934 / 174 / 134 |
| Mianwali (near miss) | False | 0.8 | 0.6 | 4.6 | 72% | 5,388 / 614 / 67 |
| Multan (suspect) | False | 2.5 | 2.3 | 3.2 | 55% | 24,708 / 1,866 / 601 |
| Rahimyar Khan (suspect) | False | 1.0 | 1.1 | 2.5 | 71% | 47,717 / 3,067 / 1,139 |
| Rawalpindi (suspect) | True | 1.2 | 20.6 | 80.2 | 96% | 3,389 / 13 / 30 |
| Sargodha (near miss) | False | 1.1 | 0.8 | 4.5 | 58% | 15,897 / 2,511 / 159 |

Near miss = above-economic share 65–75% or a loan-size ratio of 4–5×. Chakwal's F1 flag is on the LOW side: 1,158 'economic' borrowers averaging about a subsistence-sized loan. This could be holding-category misclassification, which would also understate its subsistence borrowers (interpretation; [CHECK]).

### Booking location
SBP records each loan where it is **booked**, i.e. the lending branch or office's district, not where the borrower's land is. Large farm-sector loans, especially above-economic holdings and corporate farming, are often booked at urban or head-office branches. Lahore, Rawalpindi/Islamabad, Multan and other divisional headquarters therefore record amounts (and some borrowers) whose land may lie elsewhere. Rural districts' figures understate lending to their land by the same amount. This is why amount shares are never mapped (rule 11), and why borrower counts, which are less affected but not immune, are used for `small_farm_reach`.

## District crosswalks (SBP / Ag Census / branch list → OCHA ADM2)

| Source | Source name | OCHA | Match type | Score | Validated |
|---|---|---|---|---|---|
| AgCensus | ATTOCK DISTRICT | Attock | normalized | 100 | True |
| AgCensus | BAHAWALNAGAR DISTRICT | Bahawalnagar | normalized | 100 | True |
| AgCensus | BAHAWALPUR DISTRICT | Bahawalpur | normalized | 100 | True |
| AgCensus | BHAKKAR DISTRICT | Bhakkar | normalized | 100 | True |
| AgCensus | CHAKWAL DISTRICT | Chakwal | normalized | 100 | True |
| AgCensus | CHINIOT DISTRICT | Chiniot | normalized | 100 | True |
| AgCensus | DERA GHAZI KHAN DISTRICT | Dera Ghazi Khan | normalized | 100 | True |
| AgCensus | FAISALABAD DISTRICT | Faisalabad | normalized | 100 | True |
| AgCensus | GUJRANWALA DISTRICT | Gujranwala | normalized | 100 | True |
| AgCensus | GUJRAT DISTRICT | Gujrat | normalized | 100 | True |
| AgCensus | HAFIZABAD DISTRICT | Hafizabad | normalized | 100 | True |
| AgCensus | JHANG DISTRICT | Jhang | normalized | 100 | True |
| AgCensus | JHELUM DISTRICT | Jhelum | normalized | 100 | True |
| AgCensus | KASUR DISTRICT | Kasur | normalized | 100 | True |
| AgCensus | KHANEWAL DISTRICT | Khanewal | normalized | 100 | True |
| AgCensus | KHUSHAB DISTRICT | Khushab | normalized | 100 | True |
| AgCensus | LAHORE DISTRICT | Lahore | normalized | 100 | True |
| AgCensus | LAYYAH DISTRICT | Leiah | spelling | 60 | True |
| AgCensus | LODHRAN DISTRICT | Lodhran | normalized | 100 | True |
| AgCensus | MANDI BAHAUDDIN DISTRICT | Mandi Bahauddin | normalized | 100 | True |
| AgCensus | MIANWALI DISTRICT | Mianwali | normalized | 100 | True |
| AgCensus | MULTAN DISTRICT | Multan | normalized | 100 | True |
| AgCensus | MUZAFFARGARH DISTRICT | Muzaffargarh | normalized | 100 | True |
| AgCensus | NANKANA SAHIB DISTRICT | Nankana Sahib | normalized | 100 | True |
| AgCensus | NAROWAL DISTRICT | Narowal | normalized | 100 | True |
| AgCensus | OKARA DISTRICT | Okara | normalized | 100 | True |
| AgCensus | PAKPATTAN DISTRICT | Pakpattan | normalized | 100 | True |
| AgCensus | RAHIM YAR KHAN DISTRICT | Rahim Yar Khan | normalized | 100 | True |
| AgCensus | RAJANPUR DISTRICT | Rajanpur | normalized | 100 | True |
| AgCensus | RAWALPINDI DISTRICT | Rawalpindi | normalized | 100 | True |
| AgCensus | SAHIWAL DISTRICT | Sahiwal | normalized | 100 | True |
| AgCensus | SARGODHA DISTRICT | Sargodha | normalized | 100 | True |
| AgCensus | SHEIKHUPURA DISTRICT | Sheikhupura | normalized | 100 | True |
| AgCensus | SIALKOT DISTRICT | Sialkot | normalized | 100 | True |
| AgCensus | TOBA TEK SINGH DISTRICT | Toba Tek Singh | normalized | 100 | True |
| AgCensus | VEHARI DISTRICT | Vehari | normalized | 100 | True |
| BranchList | D.G.Khan | Dera Ghazi Khan | spelling | 72 | True |
| BranchList | Layyah | Leiah | spelling | 60 | True |
| BranchList | Rajan Pur | Rajanpur | normalized | 100 | True |
| SBP | D.G.Khan | Dera Ghazi Khan | spelling | 72 | True |
| SBP | Jehlum | Jhelum | spelling | 83 | True |
| SBP | Layyah | Leiah | spelling | 60 | True |
| SBP | Mandibahauddin | Mandi Bahauddin | normalized | 100 | True |
| SBP | Rahimyar Khan | Rahim Yar Khan | normalized | 100 | True |

Exact matches not listed. Decisions (decided by Ahmed) are in `docs/crosswalk_manual_district.csv`.
