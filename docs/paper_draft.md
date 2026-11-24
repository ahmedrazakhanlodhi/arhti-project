# Where the Bank Ends and the Arhti Begins: Mapping Access, Allocation, and the Cost of Agricultural Credit in Punjab

Ahmed Raza Khan Lodhi and Hasnain Akram, PPHA 38520, University of Chicago. December 2026.

## 1. Introduction

Punjab's farmers borrow from two worlds. One is formal: commercial banks, the Zarai Taraqiati Bank (ZTBL), the Punjab
Provincial Cooperative Bank and, more recently, a provincial interest-free card for small farmers. The other is the arhti, the
commission agent who sells farmers' crops in the grain market and who, in many villages, also advances them money before the
harvest. Both systems lend to agriculture, but they are organised around different places. Banks lend through branches; arhtis
lend through markets. Where each system reaches, and whom it reaches, shapes what farmers pay for credit, when they must sell
their crops, and how much bargaining power they keep at harvest.

This paper asks whether the geography of agricultural finance corresponds to where farming happens and who farms. We look at it
through four lenses. **Access** asks where credit sources are reported as available to rural villages, and whether arhti credit
appears where formal credit does not. **Allocation** asks how formal credit is divided between small and large holdings, and how
far it reaches small farms across districts. **Reporting geography** asks where formal agricultural lending is recorded relative to
where farmland, farms and rural bank branches are. **Cost** places formal lending rates next to published estimates of what arhti
credit costs. A district scorecard brings the four lenses together for each of Punjab's districts.

We use public data from four sources with different dates and units: the Mouza Census 2020 for village-level availability, State
Bank of Pakistan (SBP) lending data for FY2023-24 by district, the Agricultural Census 2024 for farms, area and crops, and the SBP
list of bank branches as on 30 June 2024. All results are descriptive. Throughout, we keep three ideas apart: *presence* is where
bank facilities physically are; *availability* is whether a credit source is reported as serving a village; and *allocation* is who
formal credit actually reaches.

Our main finding, in one sentence: agricultural finance in Punjab does not follow farming evenly. Arhti credit is reported
alongside formal credit rather than mainly in its place; formal credit is spread across small farms by count but concentrated in
large holdings by amount; and the lending recorded in a handful of large-city districts far exceeds their share of farmland.

Section 2 gives background, Section 3 describes the data and methods, Section 4 presents the results for each lens and the
scorecard, Section 5 reports robustness checks, and Sections 6 to 8 discuss, qualify and conclude.

## 2. Background

### 2.1 Arhtis

An arhti (also written arthi) is a commission agent licensed to operate in a grain market (mandi). Arhtis broker the sale of
farmers' crops to traders and millers and take a commission on each sale. Many also advance cash or inputs before the harvest and
recover the loan when the crop is sold through the same market, so credit and marketing are bundled in a single relationship. The
arhti's place of business is the market town, not the village, but an arhti can serve many surrounding villages.

Published work suggests this credit is costly. Haq, Aslam and colleagues (2013), in a study for the International Growth Centre
(IGC), estimated implicit annualized interest from input-price premiums and extra commission at cotton 61.9%; maize 71.48%; rice
80.7%; wheat 67.1%, from a purposive sample (18 arthis in 8 locations, purposive, interviews 2012). The same study reports bank
rates of 9 to 18 percent from the farmers it interviewed, and that most of those farmers had bank accounts yet preferred to
borrow from arhtis because it was easier. A later study of warehouse-receipt financing (PMN/MEDA 2019) reported focus-group
statements of a markup of ~180% (non-representative: 400-farmer survey in 10 Punjab districts plus 4 FGDs, 2018). These are small
studies whose figures are given by crop or come from focus groups; we treat them as context, not as local estimates.

### 2.2 Formal agricultural credit

The State Bank of Pakistan regulates agricultural lending, sets annual lending targets and classifies borrowers by the size of
their holding: subsistence (up to 12.5 acres), economic (above 12.5 to 50 acres) and above-economic (above 50 acres). ZTBL and the
provincial cooperative bank specialise in agriculture; commercial banks lend through branch networks that are densest in cities
and district headquarters. SBP publishes disbursements and borrower records by district and holding class, and publishes average
rates of return on agricultural advances by institution. Because these data are administrative, they record where and to whom
loans were made as the banks report them, which is not necessarily where the financed land lies.

### 2.3 The Kissan Card as post-period context

In 2024 the Government of Punjab introduced the CM Kissan Card, an interest-free input loan for small farmers. Registration
opened on 1 June 2024 and cards became operational on 15 October 2024, so the scheme falls after our FY2023-24 lending data, apart
from the last month of registration. Eligibility runs from 1 to 12.5 acres; the loan limit is Rs 30,000 per acre capped at
Rs 150,000 per season, which means the maximum is reached at 5 acres. We mention it only to place the cost results in time; none
of our lending data includes it.

## 3. Data and methods

**Access.** The Mouza Census 2020 (Pakistan Bureau of Statistics, fieldwork January–March 2020) records, for every village
(mouza), which sources of credit the patwari and other local respondents said serve the mouza's residents. These are reports of
availability, not records of borrowing, and they say nothing about how many households borrow, how much, or on what terms. We
restrict the data to Punjab's 23,130 rural populated mouzas and compute, for each of 137 tehsils, the share of mouzas reporting
arhti credit (`arhti_share`) and commercial-bank credit (`commercial_share`). Census tehsils were matched to OCHA administrative
boundaries (valid 2022) by code and name, and every non-exact match was reviewed by hand. We measure clustering with Moran's I and
local indicators of spatial association (LISA) using Queen contiguity, row-standardised, with 999 permutations (seed 20261031).
Local clusters are reported at p < 0.05, at p < 0.01, and after a false-discovery-rate correction whose Benjamini–Hochberg cutoff
here is 0.0117. Inside villages, we compute a Mantel–Haenszel odds ratio of reporting arhti credit when commercial-bank credit is
also reported, with tehsils as strata so that each comparison is between villages of the same tehsil, and test whether the odds
ratio is the same across tehsils (Breslow–Day).

**Allocation.** From SBP's FY2023-24 farm-sector data we take borrower records and disbursed amounts by holding class, and from the
Agricultural Census 2024 the number of farms and operated (farm) area in the matching census classes (under 12.5, 12.5 to under
50, and 50 acres and above). The class boundaries coincide, but farms of exactly 12.5 or 50 acres fall in different classes in the
two sources, and the census measures operated area, not owned land. Small-farm reach is the number of subsistence-holding borrower
records per 1,000 farms under 12.5 acres, by district; borrower records may not be unique people. Crop structure comes from the
census district tables of area under wheat, rice, cotton, maize and sugarcane.

**Reporting geography.** For each of 36 districts we compute a location quotient (LQ): the district's share of Punjab's
disbursement in a holding class divided by its share of Punjab's cultivated area. An LQ of 1 means lending is recorded in
proportion to farmland; above 1, more lending is recorded than farmland would suggest. SBP reports lending by district; whether
that district is the lending branch's or the financed farm's is being verified, so every district credit figure is labelled as
reported by SBP. Islamabad, which appears in SBP's district rows but has no Punjab farmland in the census, is reported separately,
and microfinance institutions, reported only for Punjab as a whole, are excluded from district ratios. We also count all
scheduled-bank branches and rural branches per 10,000 farms. The 36 districts are the units used by SBP and the census; Punjab has
since created further districts, which these data do not distinguish.

**Cost.** Formal rates come from SBP's Monthly Statistical Bulletin, Table 3.33 (average rate of return on agricultural advances,
simple average at June quarter end), for FY2012-13 and FY2023-24. The earlier year roughly matches the period of the IGC
interviews, which allows a loose comparison across the same era.

**Why several lenses.** No single source shows both where credit is available and who receives it. The Mouza Census covers every
village but records only availability; SBP records actual lending but only by district and holding class, and only for formal
institutions; the Agricultural Census tells us who farms and what they grow but nothing about credit. Reading the sources side by
side, while keeping their dates and units apart, is the only way to ask our question with public data. It also means that our
results are comparisons of patterns, not links between individual farmers and loans.

**Scorecard.** For each district we assemble farms, cultivated area, smallholder and tenant shares, main crops, availability of
arhti, commercial-bank and ZTBL credit, branches per farm, small-farm reach, credit per cultivated acre, LQs, the count of tehsils
in arhti clusters, and the SBP data-quality flag. A descriptive profile splits districts at the median of arhti availability and
the median of small-farm reach. These are groupings, not rankings, and we attach no label of need or neglect to them.

All four sources differ in date and unit, and we never treat them as contemporaneous.

## 4. Results

### 4.1 Access

Arhti credit is reported available in 31.5% of Punjab's rural populated mouzas (Figure 2). Tehsil shares span the full range, from
0.0% to 100.0%, with a median of 19.2%, and 15 tehsils report none. Commercial-bank credit is reported more widely, with a median
tehsil share of 37.4%. The contrast between neighbouring tehsils is often sharp, which is the first hint that arhti credit follows
something more local than the general spread of rural settlement.

The pattern is strongly clustered. The global Moran's I for arhti availability is 0.536 (p = 0.001), compared with 0.297 for
commercial-bank credit. The LISA map (Figure 4) identifies 25 High-High and 32 Low-Low tehsils at p < 0.05, 14 and 16 at p < 0.01,
and 15 and 17 after the false-discovery-rate correction; 3 tehsils are Low-High outliers. Most clusters therefore survive the
correction. High-High clusters lie mainly in Sheikhupura, Gujranwala, Hafizabad, Sialkot and Nankana Sahib districts, with two in
Bahawalnagar and Bahawalpur; Low-Low clusters lie mainly in Rawalpindi, Attock, Jhelum and Chakwal.

Does arhti credit appear where formal credit does not? Across tehsils there is no clear pattern. The bivariate map (Figure 3)
shows all nine combinations of thirds, including many tehsils where both are high and many where both are low, and the bivariate
Moran's I between a tehsil's arhti share and its neighbours' commercial-bank share is 0.112 (p = 0.062): weak, uncertain, and not
the negative association that gap-filling would imply.

Inside villages, a mouza that reports commercial-bank credit is slightly more likely also to report arhti credit. Comparing mouzas
within the same tehsil, the Mantel–Haenszel odds ratio is 1.18 (95% CI 1.09–1.27), based on 21,674 mouzas in 120 tehsil strata
(Cholistan desert mouzas merged into their parent tehsils). The average conceals large differences between tehsils: the
Breslow–Day test rejects a common odds ratio (statistic 751.0, p < 0.001), and of the 120 tehsils where the comparison can be made,
67 report both sources more often than independence implies and 53 less often. In some places arhti and bank credit are reported
together; in others they are reported apart.

Two exploratory correlations add texture. Arhti availability is higher where more land is cropland (Spearman ρ = 0.49,
Benjamini–Hochberg-adjusted p < 0.001) and lower where more villages have an online commercial-bank branch in the village, a measure
of physical presence rather than availability (ρ = −0.40, adjusted p < 0.001). Availability and presence therefore tell somewhat
different stories, and we keep them apart. None of these results shows what farmers do: two credit sources reported in the same
village describe what is available there, not substitution or complementarity in borrowing.

### 4.2 Allocation

Formal credit is spread across small farms by count but not by amount (Figure A1). Subsistence holdings are 94.1% of Punjab's farms
and 68.5% of operated farm area; they account for 91.9% of farm-sector borrower records but 35.9% of the amount disbursed. Economic
holdings are 5.3% of farms and 22.8% of operated area, with 7.0% of borrower records and 14.7% of disbursement. Above-economic
holdings are 0.5% of farms and 8.6% of operated area, but 1.1% of borrower records and 49.4% of disbursement. Larger holdings need
larger loans, so some gap between farm and amount shares is expected; what stands out is the size of the gap at the top, where
holdings with under a tenth of the operated area account for about half of the amount lent.

Across districts, formal credit reaches small farms very unevenly (Figure 5). Small-farm reach ranges from 21.6 to 299.0
subsistence-holding borrower records per 1,000 farms under 12.5 acres, with a median of 118.5 across 36 districts, and it is itself
spatially clustered (Moran's I 0.532). Five districts flagged by our data-quality screen (Chakwal, Faisalabad, Jhelum, Lahore,
Rawalpindi) are marked rather than dropped. The lowest values lie in the north, in Rawalpindi, Jhelum,
Chakwal and Gujrat; the highest lie in the south and centre, in
Bahawalnagar, Bahawalpur, Okara, Lodhran and Hafizabad. Because the measure counts borrower records rather than people, a district
where farmers take several loans a year would show higher reach than one where each farmer takes one, and because SBP's districts
are as reported, reach in a district whose farmers borrow from branches elsewhere would be understated. Ordering districts from lowest to highest reach, the concentration coefficient of
borrower records over small farms is 0.297 (Figure S6): borrower records are concentrated in a subset of districts relative to
where small farms are. Small-farm reach is also higher where tenant farms are a larger share of farms (Spearman ρ = 0.39, adjusted
p 0.018).

Crop structure differs less across districts than credit does. Wheat is the largest of the five tracked crops by area in 34
districts and rice in 2. The second-largest crop varies more: rice in 17 districts, cotton in 9, maize in 5, sugarcane in 3 and
wheat in 2. In other words, almost every district grows wheat as its main crop, so differences in credit reach are not simply
differences between a wheat economy and a non-wheat economy; the crop maps in the companion app show the shares district by
district.

### 4.3 Reporting geography

Where formal agricultural lending is recorded does not follow where farmland is (Figure R1). For above-economic holdings, the LQ is
14.06 in Lahore and 7.44 in Rawalpindi, and as low as 0.09 in Chakwal. For subsistence holdings the pattern is flatter but still
uneven: the LQ is 4.66 in Lahore, 6.47 in Jhelum (a flagged district) and 0.29 in Rawalpindi.

Five large-city districts (Lahore, Rawalpindi, Multan, Faisalabad and Rahim Yar Khan) stand out together (Figure R2). Combined, they
record 39.7% of Punjab's farm-sector disbursement and 59.6% of above-economic disbursement, but hold 13.3% of cultivated area and
18.2% of farms. For subsistence holdings their combined share of disbursement is 22.4%, much closer to their share of farms.
Islamabad, outside the 36-district totals, records 3.9% of disbursement in SBP's district rows when it is included.
The five cities differ among themselves. Lahore and Rawalpindi have little farmland but record large shares of above-economic
lending; Multan and Rahim Yar Khan combine sizeable farmland with even larger shares of lending; Faisalabad records lending closer to its share of farmland than the others. The city pattern is therefore not one of urban lending
alone: two of the five are major agricultural districts in their own right, and much of what they record may be lending to their own
farms.

Bank branches show the same split between total and rural networks. The five districts hold 43.5% of all scheduled-bank branches
but 19.1% of rural branches, close to their share of farms. Lahore is the extreme case: 190.4 branches per 10,000 farms in total, but
3.9 rural branches per 10,000 farms. The total branch network follows cities; the rural network follows farms more closely.

These figures describe where SBP records lending, by district as SBP reports it. Until the attribution is confirmed, an LQ above 1
in a city district may reflect where loans are recorded, for example at city branches lending to farms elsewhere, rather than where
the financed land is. The large-holding pattern is the one most exposed to this question, because large loans are the ones most
likely to be arranged at head offices or city branches.

### 4.4 Cost

Figure P1 places formal lending rates next to published arhti estimates. These are not matched contracts and should be read as
orders of magnitude. In panel (a), for about 2012-13, the IGC implicit annualized cost of arhti credit (cotton 61.9%; maize
71.48%; rice 80.7%; wheat 67.1%) sits far above both the bank rates reported by the interviewed farmers (9 to 18 percent) and
SBP's institutional averages for FY2012-13: ZTBL 12.00 (production loans) and 13.80 (development loans), the Punjab Provincial
Cooperative Bank 19.00 and 18.00, and commercial banks 16.00 and 16.00 percent per annum. In panel (b), SBP's averages for FY2023-24
are higher: ZTBL 29.42 and 29.42, the cooperative bank 20.67 and 22.71, and commercial banks 22.96 and 22.94 percent. The Kissan
Card, at 0% for holdings up to 12.5 acres, is marked separately because it began after the data period. The PMN/MEDA focus-group
markup of ~180% is not an annualized rate and is kept off the rate axis.

The arhti figures come from a purposive sample interviewed in 2012 and are given by crop, not by place; the SBP figures are simple
averages at June quarter end by institution. The comparison shows that the gap between formal and informal prices reported in the
literature is large relative to formal rates, not what any particular farmer paid, and not whether the gap has changed since.

### 4.5 District scorecard

Table 1 groups districts by two descriptive splits. Ten districts combine high arhti availability with high small-farm reach, 10
combine low availability with low reach, 8 combine low availability with high reach, and 7 combine high availability with low
reach; Lahore, with no rural populated mouzas, is not classified. The two splits are close to independent of each other: districts
with much arhti credit are about as likely to have high as low small-farm reach. The full scorecard row for each district, with its
caveats, is in the companion app.

**Table 1. District profiles (descriptive groupings at the median; not rankings).**

| Profile | Districts |
|---|---|
| High arhti availability + high small-farm reach | 10 |
| Low arhti availability + low small-farm reach | 10 |
| Low arhti availability + high small-farm reach | 8 |
| High arhti availability + low small-farm reach | 7 |
| Not classified (no rural populated mouzas) | 1 |

## 5. Robustness

With geodesic k-nearest-neighbour weights, Moran's I for arhti availability is 0.568. At district level, Moran's I is 0.429.
Excluding the Cholistan desert mouzas, Moran's I is 0.543 and the within-village odds ratio is 1.20 (95% CI 1.11–1.29). Excluding the
five flagged districts, the concentration coefficient is 0.255 and Moran's I for small-farm reach is 0.428.

## 6. Discussion

Taken together, the four lenses show finance and farming sharing the map only partly. Arhti credit clusters and often sits next to
bank credit; formal credit reaches many small farms but most of its amount goes to large holdings; and lending is recorded heavily
in a few city districts. Several possible mechanisms are consistent with published work. We present them as possibilities, not as
findings of this study.

*Interlinked marketing and credit.* Arhtis lend against the crop they will market. Lending tied to crop sales would be expected to
follow farmland and marketed surplus, which is consistent with the positive association between arhti availability and cropland,
and with arhti credit appearing in the same villages as bank credit rather than only where banks are absent. Under this reading, the
arhti is less a substitute for a missing bank than a market agent whose lending travels with the harvest.

*Speed and collateral.* The IGC study reports that most interviewed farmers had bank accounts yet preferred arhtis because borrowing
was easier. If speed, flexible repayment and the absence of collateral matter more to farmers than the headline rate, arhti credit
could persist next to formal credit despite costing several times more, as the price ladder suggests. The heterogeneity across
tehsils would then reflect local differences in how easy each source is to use, not only whether it exists.

*Branch networks and booking practices.* Formal lending passes through branches, and the branch network is densest in cities. If
large loans are arranged and recorded at city branches, the high LQs in Lahore and Rawalpindi, and the gap between all branches and
rural branches, would follow. Confirming SBP's district attribution is the first step in telling recording from use.

These possibilities raise questions for further research: how grain markets are organised in high-arhti clusters and how many
arhtis compete in each; how farmers combine bank, arhti and now Kissan Card credit across a season; whether the 5-acre loan cap
shapes who uses the card among holdings up to 12.5 acres; and how banks decide where agricultural loans are booked. Answering them
requires household borrowing data and loan-level records that place each loan on the land it finances.

## 7. Limitations

The Mouza Census records whether respondents report a credit source as serving the village, not whether households borrow or on
what terms. Our sources differ in date and unit: January–March 2020 (mouzas and tehsils), FY2023-24 (districts as reported by SBP),
the Agricultural Census 2024 (sample-based districts) and the branch list of 30 June 2024. SBP's district attribution is under
verification, and borrower records may not be unique people. SBP's "up to 12.5 acres" and the census's "under 12.5 acres" differ at
the boundary, as do the two definitions at 50 acres. Our 36 districts are the pre-split units used by SBP and the census, not the
current administrative map. The administrative boundaries post-date the census, and a few tehsils have very few rural populated
mouzas, so their shares rest on small denominators. Spatial statistics depend on the units and weights chosen; we report two
weighting schemes and a district-level comparison. Published estimates of arhti cost come from small, non-representative studies.
All results are descriptive associations.

## 8. Conclusion

Agricultural finance in Punjab does not map neatly onto farming. Arhti credit is widespread, clustered and often reported next to
formal credit; formal credit reaches small farms in number but concentrates its amount in large holdings; and the lending recorded
in a few city districts far exceeds their farmland. The published cost estimates suggest that arhti credit is much more expensive
than formal credit, yet it persists in the same places. Confirming where SBP attributes loans, and observing how farmers actually
borrow, are the next steps for understanding why.

## Appendix (list)

- A1. Regressions of arhti availability (OLS, spatial error, spatial lag) and diagnostics.
- A2. Jackknife ranges.
- A3. Full table of exploratory (post-hoc) associations.
- A4. Small-farm reach and tenure / operated-area correlations.
- A5. Exclusion classifications (availability-based and presence-based), Figure S5.
- A6. Classification comparison, Figure S1. A7. District-level LISA (MAUP comparison), Figure S2.
- A8. Published-study locations (context only), Figure S3. A9. Village-level co-reporting by tehsil (exploratory), Figure S4.
- A10. Methods appendix, decisions log, validation reports and human verification checklist.
