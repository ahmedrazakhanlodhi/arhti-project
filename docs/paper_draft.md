# Where the Bank Ends and the Arhti Begins: Geographic Access, Landholding Structure and the Allocation of Agricultural Credit in Punjab, Pakistan

Ahmed Raza Khan Lodhi and Hasnain Akram, PPHA 38520, University of Chicago. December 2026.

## Abstract

Punjab's farmers borrow from banks and from arhtis, the commission agents of the grain markets. We map both systems with public
data: village-level reports of credit availability from the Mouza Census 2020 (23,130 rural populated mouzas in 137 tehsils),
State Bank of Pakistan (SBP) lending records for FY2023-24 and the Agricultural Census 2024 (36 districts). We test two
hypotheses. If arhtis fill the gaps left by banks, arhti availability should be lower where bank credit is reported (H1). If
formal credit reaches small farms in proportion, its distribution across districts and holding classes should match the
distribution of small farms (H2). Neither holds. Arhti credit is strongly clustered (Moran's I = 0.536) and, within tehsils,
slightly more likely to be reported where bank credit is also reported (odds ratio 1.18). Formal credit reaches small farms by
count (91.9% of borrower records) but not by amount (35.9% of disbursement), and borrower records are unevenly spread relative
to small farms across districts (index of dissimilarity 0.216). All results are descriptive associations.

## 1. Introduction and problem statement

Punjab's farmers borrow from two worlds. One is formal: commercial banks, the Zarai Taraqiati Bank (ZTBL), the Punjab
Provincial Cooperative Bank and, since late 2024, a provincial interest-free card for small farmers. The other is the arhti, the
commission agent who sells farmers' crops in the grain market (mandi) and who, in many villages, also advances them money before
the harvest. Both lend to agriculture, but they are organised around different places: banks lend through branches, arhtis
through markets. Where each system reaches, and whom it reaches, shapes what farmers pay for credit, when they must sell, and how
much bargaining power they keep at harvest.

**Thesis.** Agricultural finance in Punjab is organised around markets and towns more than around farms. Arhti credit is
clustered and is reported alongside formal credit rather than in its gaps, and formal credit reaches small farms in proportion
to their number but not to their share of land or loan value, with lending recorded disproportionately in a few city districts.

We test this thesis through two research questions and three hypotheses. The main tests for H1 and H2 were written down before
the analysis was run (project decisions D018 and D021); every other method in the paper is labelled exploratory.

- **Q1 (tehsil level, geographic exclusion).** Is reported arhti credit availability associated with weaker formal credit
  access, or does it concentrate where banks and markets already exist?
  - **H1 (gap-filling).** Arhti credit is reported where formal credit is not: a negative association between arhti and
    commercial-bank availability across tehsils (bivariate Moran's I < 0) and within tehsils (odds ratio < 1).
  - **H1-alt (co-location).** Arhti credit follows farmland and markets and is reported alongside bank credit (odds ratio ≥ 1),
    forming spatial clusters.
- **Q2 (district level, economic exclusion).** Does formal agricultural credit reach smallholders and tenant-heavy areas in
  proportion to their share of farms?
  - **H2 (proportional reach).** Small holdings' shares of SBP borrower records and of disbursement equal their shares of farms
    and of operated area, and borrower records are spread across districts as small farms are (index of dissimilarity ≈ 0).
  - **H3 (proportional reporting geography).** District shares of recorded lending match district shares of farmland
    (location quotients ≈ 1).

We use four public sources with different dates and units, and we never treat them as contemporaneous: the Mouza Census 2020
(January–March 2020), SBP lending data for FY2023-24 by district as SBP reports it, the Agricultural Census 2024 (sample-based)
and the SBP list of bank branches as on 30 June 2024. Throughout, we keep three ideas apart: *presence* is where bank facilities
physically are; *availability* is whether a credit source is reported as serving a village; *allocation* is whom formal credit
reaches. Section 2 reviews the literature, Section 3 sets out data and GIS methods, Section 4 reports results by hypothesis,
Section 5 checks robustness, and Sections 6 to 8 discuss, qualify and conclude.

## 2. Literature and background

**Why formal and informal lenders coexist.** Rural credit markets are shaped by imperfect information: lenders must screen
borrowers, enforce repayment and monitor the use of funds, and these problems are cheapest to solve for lenders who already know
the borrower (Hoff and Stiglitz 1990). One tradition reads high informal interest rates as the product of lender power over
dependent borrowers (Bhaduri 1977). A second reads them as the cost of lending under imperfect information. Aleem (1990) studied
informal lenders around the market town of Chambar in Sindh and found an average annual cost of informal commercial borrowing of
78.7 percent, against a bank rate of 12 percent. He found that lenders' charges were close to their average cost of lending,
and that lenders often required the farmer to market the harvest through them. Bell (1988) surveys such *interlinked*
transactions, in which credit is bundled with the sale of output or the supply of inputs. Smith, Stockbridge and Lohano (1999)
found trader credit in Sindh interlocked with input supply and crop purchase, and argued that competition among traders made it
behave more competitively than the exploitation view predicts.

**Arhtis in Punjab.** The arhti is the Punjabi form of the interlinked lender: a licensed commission agent in a grain market who
brokers the sale of farmers' crops and advances inputs or cash before the harvest, recovering the loan when the crop is sold
through the same market. Haq and colleagues (2013), in a study for the International Growth Centre (IGC), describe the arhti as
the largest source of informal agricultural credit in Punjab, operating from the province's 325 commodity markets. From a
purposive sample (18 arhtis in 8 locations, interviews in 2012) they estimated implicit annualized interest, from input-price
premiums and extra commission, of 61.9% for cotton, 71.48% for maize, 80.7% for rice and 67.1% for wheat. The same study reports
bank rates of 9 to 18 percent from the farmers it interviewed, most of whom had bank accounts yet preferred arhtis because
borrowing was easier. A later study of warehouse-receipt financing (PMN/MEDA 2019) reported focus-group statements of a markup of
about 180%. These are small studies whose figures are given by crop or come from focus groups; we treat them as context, not as
local estimates.

**Who formal credit reaches.** Pakistani evidence has long found formal credit skewed towards larger farms. Malik, Mushtaq and
Gill (1989) found that small farm households had limited access to institutional credit. Qureshi, Nabi and Faruqee (1996)
reported that fewer than a third of rural households borrowed, and only about a tenth of their loans came from institutional
sources. Khandker and Faruqee (2003) found that large landowners, about 4 percent of rural households, received 42 percent of
formal loans, while landless and subsistence households, more than 69 percent, received 23 percent. SBP now classifies
agricultural borrowers by holding size: subsistence (up to 12.5 acres), economic (above 12.5 to 50 acres) and above-economic
(above 50 acres). It publishes borrower records and disbursements by district and class, which lets us ask whether the skew
persists two decades later.

**The geography of finance.** Where banks are matters. Burgess and Pande (2005) show that India's rule forcing banks to open
branches in unbanked rural locations is associated with lower rural poverty. Mian (2006) shows that distance between a bank's
head office and its branches shapes lending in Pakistan. Leyshon, French and Signoretta (2008) map bank branch closures in
Britain and find them concentrated in poorer areas, an example of treating access to finance as an uneven geography. We follow
this tradition, but with two differences: we map *reported availability* of both formal and informal credit across every rural
village of a province, and we compare where formal lending is *recorded* with where farms are.

**Methods literature.** Tobler's (1970) first law, that near things are more related than distant things, motivates testing
for spatial autocorrelation. We use global and local Moran's I (Anselin 1995) and the Getis–Ord Gi* statistic (Getis and Ord
1992; Ord and Getis 1995), correcting local tests for multiple comparisons with the false discovery rate (Benjamini and Hochberg
1995). Because our units are administrative, results may depend on the units chosen, the modifiable areal unit problem (MAUP;
Openshaw and Taylor 1979; Openshaw 1984), and associations between areas need not hold for the individuals in them, the
ecological fallacy (Robinson 1950). We measure unevenness with the index of dissimilarity (Duncan and Duncan 1955).

**Post-period context.** In 2024 the Government of Punjab introduced the CM Kissan Card, an interest-free input loan for
holdings of 1 to 12.5 acres. Registration opened on 1 June 2024 and cards became operational on 15 October 2024, so it falls
after our FY2023-24 lending data apart from the last month of registration. The loan limit, Rs 30,000 per acre capped at
Rs 150,000 per season, is reached at 5 acres.

## 3. Data and GIS methods

**Data and units (Table 1).** The Mouza Census 2020 (Pakistan Bureau of Statistics, PBS) records, for every village (mouza),
which sources of credit the patwari and other local respondents said serve the mouza's residents. These are reports of
availability, not records of borrowing. We keep Punjab's 23,130 rural populated mouzas and aggregate them to 137 tehsils. From SBP
we take FY2023-24 farm-sector borrower records and disbursed amounts by district and holding class. From the Agricultural Census
2024 we take farms, operated (farm) area and cultivated area by size class, tenure and crop. From SBP's branch list we count all
and rural scheduled-bank branches. Rasters: ESA WorldCover 10 m 2021 (cropland; Zanaga et al. 2022) and the Malaria Atlas Project
travel time to cities, 2015 (Weiss et al. 2018).

**Table 1. Data, units, vintages and levels of measurement.**

| Variable | Source and vintage | Unit | Level of measurement | Map symbolization |
|---|---|---|---|---|
| arhti_share, commercial_share (share of rural populated mouzas reporting the source) | Mouza Census, Jan–Mar 2020 | 137 tehsils | Ratio (normalized count) | Choropleth, natural breaks (Fig 2) |
| Bivariate class (terciles of the two shares) | as above | tehsils | Ordinal × ordinal | 3 × 3 bivariate choropleth (Fig 3) |
| LISA / Gi* cluster type | derived | tehsils | Nominal | Qualitative colours (Fig 4, S8) |
| Small-farm reach (subsistence borrower records per 1,000 farms under 12.5 acres) | SBP FY2023-24; Ag Census 2024 | 36 districts | Ratio | Choropleth, quantiles (Fig 5) |
| Farms under 12.5 acres; borrower records (counts) | Ag Census 2024; SBP FY2023-24 | districts | Ratio (counts) | Dasymetric dots; proportional circles (Fig 6) |
| Location quotient (class disbursement share ÷ cultivated-area share) | SBP FY2023-24; Ag Census 2024 | districts | Ratio | Diverging choropleth, log-symmetric breaks (Fig R1) |
| Cropland share; travel time to cities | WorldCover 2021; MAP 2015 | tehsils, districts | Ratio | Zonal statistics (covariates) |

**Census geography and matching.** Pakistan's census geography nests province → division → district → tehsil → mouza, and PBS
codes each unit hierarchically, much as US FIPS/GEOID codes nest state, county and tract. OCHA's boundaries use their own
p-codes (for example PK60504 for Tala Gang). We matched the 148 census tehsils to the 139 OCHA tehsil polygons by code and name:
115 matched exactly, 11 after rule-based normalization, 9 after spelling review, 2 as renames, and 8 were summed into a parent
polygon (attribute join plus dissolve). Three Lahore tehsils with no rural populated mouzas have no polygon. Every non-exact
match was reviewed by hand. All 23,130 rural populated mouzas were assigned to a polygon. The district layer is a dissolve of
tehsils (36 districts, the pre-split units used by SBP and the census).

**Projection.** Punjab is a mid-latitude province elongated from north-east to south-west. We use an Albers equal-area conic
projection centred on the province (standard parallels 28°N and 33°N, central meridian 72°E). It is a secant conic, suited to a mid-latitude region, and
equal-area, which matters because choropleths and dot densities compare areas. An earlier choice, ESRI:102028, is also Albers but
centred at 125°E; it rotated Punjab by about 10° and distorted shapes. A Tissot indicatrix (Figure S11) shows maximum angular
distortion over the province of 29.68° in ESRI:102028 against 0.11° in our projection. k-nearest-neighbour weights use
geodesic distances, so they do not depend on the projection.

**Normalization and classification.** Every choropleth maps a ratio, never a raw count, because raw counts mostly track the size
of a unit: mouza counts become shares of rural populated mouzas, and borrower records become records per 1,000 small farms. Raw
counts appear only as dots and proportional circles (Figure 6). Class breaks follow a fixed rule: five Fisher–Jenks natural-break
classes unless a class would hold fewer than three units, in which case quantiles. Figure S12 shows the histogram of
arhti_share with equal-interval, quantile and natural-break schemes; natural breaks fit best (goodness of absolute deviation fit
0.818, against 0.781 for both alternatives). Figure S1 compares the resulting maps.

**Raster processing.** Cropland was computed from the 10 m WorldCover tiles as the fraction of cropland pixels in each block of
10 × 10 pixels (about 100 m), an average-based resampling that avoids the "winner takes all" loss of mixed pixels, and then
summarized by zonal statistics for each tehsil and district. Travel time to cities, a cost-distance surface, was summarized as a
cropland-weighted mean, so that it describes farmland rather than desert. The Mouza Census also reports the distance from each
mouza to the nearest bank branch and grain market in bands (in the mouza, 1–10, 11–25, 26–50, over 50 km), which work like
multiple-ring buffers measured by respondents.

**Spatial statistics.** Spatial weights are Queen contiguity, row-standardised (primary), with sensitivity runs using Rook
contiguity, geodesic k-nearest neighbours (k = 5), a geodesic distance band (73.6 km, the smallest distance that leaves no tehsil
without a neighbour) and inverse-distance weights within that band. All permutation tests use 999 permutations with seed
20261031. We report global Moran's I and Geary's C, the Moran scatterplot (Figure S7), local Moran's I (LISA) and Gi* at p < 0.05
and after false-discovery-rate correction (Benjamini–Hochberg cutoff 0.0117 for LISA), the bivariate Moran's I between a tehsil's
arhti share and its neighbours' commercial-bank share, and a global trend surface (OLS of arhti_share on centroid x, y and their
squares) with its residual map (Figure S9). Within villages we compute a Mantel–Haenszel odds ratio of reporting arhti credit
when commercial-bank credit is also reported, with tehsils as strata, and test homogeneity across tehsils (Breslow–Day).

**Allocation and reporting geography.** For H2 we compare holding-class shares of SBP borrower records and disbursement with the
census shares of farms and operated area, compute small-farm reach by district, a concentration coefficient of borrower records
over small farms, and the index of dissimilarity D = ½ Σ |bᵢ/B − fᵢ/F|, the share of borrower records that would have to be in
other districts for their distribution to match that of small farms. For H3 we compute location quotients (a district's share of
Punjab's disbursement in a class divided by its share of Punjab's cultivated area). SBP reports lending by district; whether that
is the lending branch's district or the financed farm's is being verified, so every district credit figure is labelled "as
reported by SBP". Disbursement amounts are mapped only in the reporting-geography figures.

**Typology.** A district scorecard assembles the measures. As an exploratory complement to a median split, we group the 35
classifiable districts with k-means on six standardized attributes (arhti and commercial-bank availability, small-farm reach,
rural branches per farm, tenant share, cropland share), with and without location, choosing k from 2 to 6 by the silhouette
score (Figure S10). All analysis is in Python (GeoPandas, PySAL) and QGIS 4.2.3; the main maps (Figures 2–6) are QGIS Print
Layouts, and every script runs from the raw downloads in numbered order.

## 4. Results

### 4.1 H1: arhti credit clusters and sits alongside bank credit

Arhti credit is reported available in 31.5% of Punjab's rural populated mouzas (Figure 2). Tehsil shares span the full range,
from 0.0% to 100.0%, with a median of 19.2%, and 15 tehsils report none. Commercial-bank credit is reported more widely, with a
median tehsil share of 37.4%.

The pattern is strongly clustered. Global Moran's I for arhti availability is 0.536 (p = 0.001), against 0.297 for
commercial-bank credit; Geary's C is 0.458 (p = 0.001), where values below 1 also indicate positive autocorrelation. The Moran
scatterplot (Figure S7) shows most tehsils in the High-High and Low-Low quadrants. The LISA map (Figure 4) identifies 25 High-High
and 32 Low-Low tehsils at p < 0.05, of which 15 and 17 survive the false-discovery-rate correction; 3 tehsils are Low-High
outliers. High-High clusters lie mainly in Sheikhupura, Gujranwala, Hafizabad, Sialkot and Nankana Sahib, with two in
Bahawalnagar and Bahawalpur; Low-Low clusters lie mainly in Rawalpindi, Attock, Jhelum and Chakwal. Gi* finds the same places
(Figure S8): 28 hot spots and 33 cold spots at p < 0.05 (15 and 18 after correction), and every LISA High-High tehsil is a Gi*
hot spot. A smooth province-wide gradient does not account for the clusters: a second-order trend surface on location reaches
R² = 0.40, and its residuals remain clustered (Moran's I = 0.234, p = 0.002). The geography of arhti credit is local.

Arhti availability is also less evenly spread than formal availability. The index of dissimilarity between mouzas reporting
arhti credit and all rural populated mouzas is 0.380, the share of arhti-reporting mouzas that would have to be in other
tehsils for arhti credit to be spread like villages. The index is 0.234 for commercial-bank credit and 0.115 for ZTBL credit.

**The H1 test.** Gap-filling predicts that arhti credit is reported where bank credit is not. Across tehsils, the bivariate map
(Figure 3) shows all nine combinations, with many tehsils where both are high and many where both are low, and the bivariate
Moran's I is 0.112 (p = 0.062): weak, uncertain, and not negative. Within tehsils, a mouza that reports commercial-bank credit is
slightly *more* likely also to report arhti credit: the Mantel–Haenszel odds ratio is 1.18 (95% CI 1.09–1.27), based on 21,674
mouzas in 120 tehsil strata. The average conceals large differences: the Breslow–Day test rejects a common odds ratio (statistic
751.0, p < 0.001), and of the 120 tehsils, 67 report both sources more often than independence implies and 53 less often. In
exploratory correlations, arhti availability is higher where more land is cropland (Spearman ρ = 0.49, adjusted p < 0.001) and
lower where more villages have an online commercial-bank branch, a measure of presence rather than availability (ρ = −0.40,
adjusted p < 0.001). **We therefore reject H1 in favour of H1-alt:** arhti credit clusters where farmland is, and is reported
alongside bank credit on average, although the relationship varies across tehsils.

### 4.2 H2: formal credit reaches small farms by count, not by amount

Formal credit is spread across small farms by count but not by amount (Figure A1). Subsistence holdings are 94.1% of Punjab's
farms and 68.5% of operated farm area; they account for 91.9% of farm-sector borrower records but 35.9% of the amount disbursed.
Economic holdings are 5.3% of farms and 22.8% of operated area, with 7.0% of borrower records and 14.7% of disbursement.
Above-economic holdings are 0.5% of farms and 8.6% of operated area, but 1.1% of borrower records and 49.4% of disbursement.
Larger holdings need larger loans, so some gap between farm and amount shares is expected; what stands out is the top, where
holdings with under a tenth of the operated area account for about half of the amount lent. The skew that Khandker and Faruqee
(2003) reported is still visible in the amounts.

Across districts, formal credit reaches small farms unevenly (Figure 5). Small-farm reach ranges from 21.6 to 299.0
subsistence-holding borrower records per 1,000 farms under 12.5 acres, with a median of 118.5 across 36 districts, and is itself
spatially clustered (Moran's I 0.532). The lowest values lie in the north (Rawalpindi, Jhelum, Chakwal, Gujrat); the highest in
the south and centre (Bahawalnagar, Bahawalpur, Okara, Lodhran, Hafizabad). Five districts flagged by our data-quality screen
(Chakwal, Faisalabad, Jhelum, Lahore, Rawalpindi) are marked rather than dropped. Figure 6 shows the same contrast without
ratios: 4,738 dots, each standing for 1,000 farms under 12.5 acres and placed only on cropland, show where small farms are,
and circles show where small-farm borrower records are reported. The index of dissimilarity between the two distributions is 0.216: about a fifth of
borrower records would have to be in other districts to match the distribution of small farms. Ordering districts by reach, the
concentration coefficient is 0.297 (Figure S6). Small-farm reach is higher where tenant farms are a larger share of farms
(Spearman ρ = 0.39, adjusted p 0.018), so tenant-heavy districts are not, on this measure, the least reached.

Crop structure varies less than credit. Wheat is the largest of the five tracked crops by area in 34 districts and rice in 2; the
second crop varies more (rice in 17 districts, cotton in 9, maize in 5, sugarcane in 3, wheat in 2). Differences in reach are
therefore not simply differences between wheat and non-wheat economies. **H2 is rejected:** proportional by count at the
province level, but not by amount, and not across districts.

### 4.3 H3: lending is recorded heavily in a few city districts

Where formal agricultural lending is recorded does not follow where farmland is (Figure R1). For above-economic holdings, the
location quotient is 14.06 in Lahore and 7.44 in Rawalpindi, and as low as 0.09 in Chakwal. For subsistence holdings the pattern
is flatter but still uneven: 4.66 in Lahore, 6.47 in Jhelum (a flagged district) and 0.29 in Rawalpindi. Five large-city
districts (Lahore, Rawalpindi, Multan, Faisalabad and Rahim Yar Khan) together record 39.7% of Punjab's farm-sector disbursement
and 59.6% of above-economic disbursement, but hold 13.3% of cultivated area and 18.2% of farms (Figure R2). For subsistence
holdings their share is 22.4%, close to their share of farms. Islamabad, outside the 36-district totals, records 3.9% of
disbursement in SBP's district rows. The five differ: Lahore and Rawalpindi have little farmland but large shares of
above-economic lending, while Multan and Rahim Yar Khan are major agricultural districts in their own right.

Bank branches show the same split. The five districts hold 43.5% of all scheduled-bank branches but 19.1% of rural branches,
close to their share of farms; the index of dissimilarity against farms is 0.356 for all branches and 0.214 for rural branches.
Lahore has 190.4 branches per 10,000 farms in total but 3.9 rural branches. **H3 is rejected for large holdings** and holds
roughly for small ones. Until SBP's district attribution is confirmed, a high location quotient in a city district may reflect
where loans are booked, for example at city branches lending to farms elsewhere, rather than where the financed land is.

### 4.4 Cost in context

Figure P1 places formal lending rates next to published arhti estimates. They are not matched contracts and should be read as
orders of magnitude. For about 2012-13, the IGC estimates of implicit arhti cost (61.9% to 80.7% by crop) sit far above both
the bank rates reported by interviewed farmers (9 to 18 percent) and SBP's institutional averages for FY2012-13: ZTBL 12.00
(production) and 13.80 (development), the Punjab Provincial Cooperative Bank 19.00 and 18.00, commercial banks 16.00 and 16.00
percent per annum. SBP's FY2023-24 averages are higher (ZTBL 29.42 and 29.42; cooperative bank 20.67 and 22.71; commercial
banks 22.96 and 22.94). The Kissan Card, at 0% for holdings up to 12.5 acres, began after the data period. The gap between the
two systems' prices is large, which makes the co-location found under H1 more striking: arhti credit persists where cheaper
formal credit is also reported.

### 4.5 District typology

A median split groups 10 districts as high arhti availability with high small-farm reach, 10 as low with low, 8 as low
availability with high reach and 7 as high availability with low reach (Lahore is not classified). The two measures are close
to independent. k-means on six standardized attributes gives the same message (Figure S10): the best solutions (k = 6 without
location, k = 5 with it) have silhouette scores of only 0.26 and 0.25, so districts do not fall into sharply separated types.
Three groups appear in both solutions: a north-eastern group of eight districts from Sheikhupura to Sialkot with much arhti
credit (median 63%) and middling reach (106), a south-eastern group (Bahawalnagar, Okara, Pakpattan) with the highest reach
(215), and a northern group around Rawalpindi, Jhelum, Chakwal and Gujrat with little arhti credit and the lowest reach. These are descriptive groupings, not rankings, and carry no label of need.

## 5. Robustness and the MAUP

The clustering of arhti credit does not depend on the weights: Moran's I is 0.536 with Rook contiguity (the same neighbours as
Queen for these polygons), 0.568 with geodesic k-nearest neighbours, 0.470 with the 73.6 km distance band and 0.491 with
inverse-distance weights, all with p = 0.001. **Scale effect:** aggregating tehsils to 35 districts lowers Moran's I to 0.429; at district level 8
High-High and 5 Low-Low clusters appear at p < 0.05 but only one of each survives the false-discovery-rate correction (Figure
S2), against 15 and 17 at tehsil level, as the MAUP predicts. **Zoning effect:** excluding the Cholistan desert mouzas, which
change how three southern polygons are drawn, gives Moran's I 0.543 and a within-village odds ratio of 1.20 (95% CI 1.11–1.29).
Excluding the five flagged districts, the concentration coefficient is 0.255 and Moran's I for small-farm reach is 0.428.

## 6. Discussion

The four lenses show finance and farming sharing the map only partly. Several mechanisms are consistent with published work; we
present them as possibilities, not findings.

*Interlinked marketing and credit.* Arhtis lend against the crop they will market (Bell 1988; Aleem 1990; Haq et al. 2013).
Lending tied to crop sales would be expected to follow farmland and marketed surplus, consistent with the association between
arhti availability and cropland, and with arhti credit appearing in the same villages as bank credit. Under this reading the
arhti is less a substitute for a missing bank than a market agent whose lending travels with the harvest.

*Speed and collateral.* Most farmers interviewed by the IGC had bank accounts yet preferred arhtis because borrowing was easier.
If speed, flexible repayment and the absence of collateral matter more than the headline rate (Hoff and Stiglitz 1990), arhti
credit could persist next to formal credit despite costing several times more. The heterogeneity across tehsils would then
reflect local differences in how easy each source is to use.

*Branch networks and booking practices.* Formal lending passes through branches, which are densest in cities. If large loans are
arranged and recorded at city branches, the high location quotients in Lahore and Rawalpindi would follow (compare Mian 2006 on
distance within banks). Confirming SBP's district attribution is the first step in telling recording from use.

*Pattern, process and the ecological fallacy.* Our associations are between areas. That villages reporting bank credit are more
likely to report arhti credit does not mean that the same farmers use both (Robinson 1950); a tehsil-level pattern is consistent
with many household-level processes. Map design choices matter too: a different classification or unit would draw a different
picture, which is why we fix the classification rule in advance, show alternatives (Figures S1, S12) and report two unit sizes.

These possibilities raise questions for further research: how grain markets are organised in high-arhti clusters; how farmers
combine bank, arhti and Kissan Card credit across a season; whether the 5-acre cap shapes who uses the card; and how banks decide
where agricultural loans are booked. Answering them requires household borrowing data and loan records placed on the land they
finance.

## 7. Limitations

The Mouza Census records whether respondents report a credit source as serving the village, not whether households borrow or on
what terms. Our sources differ in date and unit: January–March 2020 (mouzas and tehsils), FY2023-24 (districts as reported by
SBP), the Agricultural Census 2024 (sample-based, so district figures carry sampling error) and the branch list of
30 June 2024. SBP's district attribution is under verification, and borrower records may not be unique people. SBP's "up to 12.5
acres" and the census's "under 12.5 acres" differ at the boundary, as do the definitions at 50 acres. Our 36 districts are the
pre-split units, not the current administrative map. The boundaries post-date the census, and a few tehsils rest on few
rural populated mouzas. Spatial statistics depend on units and weights; we report five weighting schemes and two unit sizes.
Dots in Figure 6 are placed at random on cropland and show density, not farm locations. Published estimates of arhti cost come
from small, non-representative studies. All results are descriptive associations.

## 8. Conclusion

Agricultural finance in Punjab does not map neatly onto farming. **H1 (gap-filling) is rejected:** arhti credit is clustered
(Moran's I 0.536, robust to five weighting schemes), is spread less evenly than bank credit (D = 0.380 against 0.234), and is
reported slightly more often where bank credit is also reported (odds ratio 1.18), consistent with credit that travels with the
harvest. **H2 (proportional reach) is rejected:** small holdings receive 91.9% of borrower records but 35.9% of disbursement, and
borrower records are unevenly spread relative to small farms across districts (D = 0.216). **H3 is rejected for large holdings:**
five city districts record 59.6% of above-economic disbursement with 13.3% of cultivated area. Published estimates suggest arhti
credit costs several times more than formal credit, yet it persists in the same places. Confirming where SBP attributes loans,
and observing how farmers actually borrow, are the next steps for understanding why.

## References

Aleem, I. (1990). Imperfect information, screening, and the costs of informal lending: A study of a rural credit market in
Pakistan. *The World Bank Economic Review*, 4(3), 329–349.

Anselin, L. (1995). Local indicators of spatial association—LISA. *Geographical Analysis*, 27(2), 93–115.

Bell, C. (1988). Credit markets and interlinked transactions. In H. Chenery & T. N. Srinivasan (Eds.), *Handbook of Development
Economics* (Vol. 1, pp. 763–830). Elsevier.

Benjamini, Y., & Hochberg, Y. (1995). Controlling the false discovery rate: A practical and powerful approach to multiple testing.
*Journal of the Royal Statistical Society: Series B*, 57(1), 289–300.

Bhaduri, A. (1977). On the formation of usurious interest rates in backward agriculture. *Cambridge Journal of Economics*, 1(4),
341–352.

Burgess, R., & Pande, R. (2005). Do rural banks matter? Evidence from the Indian social banking experiment. *American Economic
Review*, 95(3), 780–795.

Duncan, O. D., & Duncan, B. (1955). A methodological analysis of segregation indexes. *American Sociological Review*, 20(2),
210–217.

Getis, A., & Ord, J. K. (1992). The analysis of spatial association by use of distance statistics. *Geographical Analysis*,
24(3), 189–206.

Haq, A., Aslam, A., Chaudhry, A. A., Naseer, A., Muhammad, K., Mushtaq, K., & Farooqi, M. S. (2013). *Who is the "arthi":
Understanding the commission agent's role in the agriculture supply chain* (Working paper). International Growth Centre.

Hoff, K., & Stiglitz, J. E. (1990). Introduction: Imperfect information and rural credit markets—Puzzles and policy perspectives.
*The World Bank Economic Review*, 4(3), 235–250.

Khandker, S. R., & Faruqee, R. R. (2003). The impact of farm credit in Pakistan. *Agricultural Economics*, 28(3), 197–213.

Leyshon, A., French, S., & Signoretta, P. (2008). Financial exclusion and the geography of bank and building society branch
closure in Britain. *Transactions of the Institute of British Geographers*, 33(4), 447–465.

Malik, S. J., Mushtaq, M., & Gill, M. A. (1989). Differential access and the rural credit market in Pakistan: Some recent evidence.
*The Pakistan Development Review*, 28(4), 709–716.

Mian, A. (2006). Distance constraints: The limits of foreign lending in poor economies. *The Journal of Finance*, 61(3),
1465–1505.

Openshaw, S. (1984). *The modifiable areal unit problem* (Concepts and Techniques in Modern Geography No. 38). Geo Books.

Openshaw, S., & Taylor, P. J. (1979). A million or so correlation coefficients: Three experiments on the modifiable areal unit
problem. In N. Wrigley (Ed.), *Statistical applications in the spatial sciences* (pp. 127–144). Pion.

Ord, J. K., & Getis, A. (1995). Local spatial autocorrelation statistics: Distributional issues and an application.
*Geographical Analysis*, 27(4), 286–306.

Qureshi, S., Nabi, I., & Faruqee, R. (1996). *Rural finance for growth and poverty alleviation* (Policy Research Working Paper
No. 1593). World Bank.

Robinson, W. S. (1950). Ecological correlations and the behavior of individuals. *American Sociological Review*, 15(3), 351–357.

Smith, L. E. D., Stockbridge, M., & Lohano, H. R. (1999). Facilitating the provision of farm credit: The role of interlocking
transactions between traders and zamindars in crop marketing systems in Sindh. *World Development*, 27(2), 403–418.

Tobler, W. R. (1970). A computer movie simulating urban growth in the Detroit region. *Economic Geography*, 46(Suppl.), 234–240.

Weiss, D. J., Nelson, A., Gibson, H. S., et al. (2018). A global map of travel time to cities to assess inequalities in
accessibility in 2015. *Nature*, 553(7688), 333–336.

Zanaga, D., Van De Kerchove, R., Daems, D., et al. (2022). *ESA WorldCover 10 m 2021 v200* [Data set]. Zenodo.
https://doi.org/10.5281/zenodo.7254221

Data: Pakistan Bureau of Statistics, Mouza Census 2020 and Agricultural Census 2024; State Bank of Pakistan, district-wise
agricultural credit FY2023-24, bank branch list (30 June 2024), Monthly Statistical Bulletin Table 3.33; OCHA COD-AB Pakistan
boundaries (valid_on 2022-09-09); PMN/MEDA (2019) warehouse-receipt financing study. Full source list with URLs:
`docs/references.md` and `docs/data_inventory.md`.

## Appendix (list)

- Figures S1 (classification comparison), S2 (district LISA, MAUP), S4 (village-level co-reporting by tehsil), S5 (three-panel
  Figure 5), S6 (concentration curve), R2 (city shares), S7 (Moran scatterplot), S8 (Gi*), S9 (trend surface), S10 (k-means
  typology), S11 (Tissot indicatrix), S12 (classification histograms).
- A1. Regressions of arhti availability (OLS, spatial error, spatial lag) and diagnostics; A2. jackknife ranges; A3. exploratory
  associations; A4. small-farm reach and tenure correlations; A5. published-study locations (context only, Figure S3).
- Methods appendix, decisions log, validation reports, key-numbers table and human verification checklist (repository `docs/`).
