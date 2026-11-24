# Where the Bank Ends and the Arhti Begins: Geographic Access, Landholding Structure and the Allocation of Agricultural Credit in Punjab, Pakistan

Ahmed Raza Khan Lodhi and Hasnain Akram, PPHA 38520, University of Chicago. December 2026.

## Abstract

Agricultural credit in Punjab, Pakistan, is supplied through overlapping formal banking and informal commission-agent (arhti)
networks. Using village-level reports of credit availability from the Mouza Census 2020 (23,130 rural populated mouzas in 137
tehsils), State Bank of Pakistan (SBP) lending records for FY2023-24 and the Agricultural Census 2024 (36 districts), we test
three hypotheses: that arhti credit fills the gaps left by formal credit (H1), that formal credit reaches small farms in
proportion to their number and land (H2), and that formal lending is recorded where farmland is (H3). Reported arhti credit
availability is strongly clustered (Moran's I = 0.536) and follows cropland. Within tehsils it is modestly more likely to be
reported alongside commercial-bank credit (Mantel–Haenszel odds ratio 1.18) and is not associated with ZTBL or with any formal
source taken together; no formal source shows the negative association that gap-filling implies, although the relationship
varies widely across tehsils. Across the 36 districts, subsistence holdings account for 90.9% of recorded farm-sector borrower
records but 37.0% of disbursement, and borrower records are spread differently from small farms (index of dissimilarity 0.216).
Five city districts record 59.6% of above-economic disbursement with 13.3% of cultivated area. All results are descriptive.

## 1. Introduction and problem statement

Punjab's farmers borrow from two worlds. One is formal: commercial banks, the Zarai Taraqiati Bank (ZTBL), the Punjab
Provincial Cooperative Bank, microfinance banks and, since late 2024, a provincial interest-free card for small farmers. The
other is the arhti, the commission agent who sells farmers' crops in the grain market (mandi) and who, in many villages, also
advances them money before the harvest. Banks lend through branches, arhtis through markets. Where each system reaches, and whom
it reaches, shapes what farmers pay for credit, when they must sell, and how much bargaining power they keep at harvest.

**Thesis.** Agricultural credit in Punjab has distinct and uneven geographies. Arhti credit is spatially concentrated, follows
farmland and coexists with formal credit rather than filling its gaps, while recorded formal lending is concentrated by holding
size and in a few city districts.

Earlier work, notably the International Growth Centre study of arhtis (Haq et al. 2013), already found that farmers with bank
accounts keep borrowing from arhtis. Our contribution is to test how far that coexistence extends across a whole province, with
village-level census data and spatial statistics, and to compare where formal lending is recorded with where farms are.

We ask two research questions and test three hypotheses. The tests for H1 and H2 were fixed before the analysis was run and are
recorded in our project log; H3 and every other method in the paper are exploratory.

- **Q1 (tehsil level, geographic exclusion).** Is reported arhti credit availability associated with weaker formal credit
  availability, or does it concentrate where formal credit and farmland already are?
  - **H1 (gap-filling).** Arhti credit is reported where formal credit is not: a negative association between arhti and formal
    credit availability across tehsils and, within tehsils, an odds ratio below 1.
  - **H1-alt (coexistence).** Arhti credit follows farmland and is reported alongside formal credit (odds ratio of 1 or more),
    forming spatial clusters.
- **Q2 (district level, economic exclusion).** Does formal agricultural credit reach smallholders and tenant-heavy areas in
  proportion to their share of farms?
  - **H2 (proportional reach).** Small holdings' shares of SBP borrower records and disbursement match their shares of farms and
    operated area, and borrower records are spread across districts as small farms are (index of dissimilarity near 0).
  - **H3 (proportional reporting geography, exploratory).** District shares of recorded lending in each holding class match
    district shares of cultivated area (location quotients near 1).

Proportionality is a benchmark, not an optimum: larger farms need larger loans, so departures from it describe how lending is
distributed, not whether it is adequate. We use four public sources with different dates and units and never treat them as
contemporaneous. Throughout, we keep three ideas apart: *presence* is where bank facilities physically are; *availability* is
whether a credit source is reported as serving a village; *allocation* is whom formal credit reaches, as SBP records it.

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
through the same market. Haq and colleagues (2013) describe the arhti as the largest source of informal agricultural credit in
Punjab, operating from the province's 325 commodity markets. From a purposive sample (18 arhtis in 8 locations, interviews in
2012) they estimated implicit annualized interest, from input-price premiums and extra commission, of 61.9% for cotton, 71.48%
for maize, 80.7% for rice and 67.1% for wheat. The same study reports bank rates of 9 to 18 percent from the farmers it
interviewed, most of whom had bank accounts yet preferred arhtis because borrowing was easier. These are small studies whose
figures are given by crop; we treat them as context, not as local estimates.

**Who formal credit reaches.** Pakistani evidence has long found formal credit skewed towards larger farms. Malik, Mushtaq and
Gill (1989) found that small farm households had limited access to institutional credit. Qureshi, Nabi and Faruqee (1996)
reported that fewer than a third of rural households borrowed, and only about a tenth of their loans came from institutional
sources. Khandker and Faruqee (2003) found that large landowners, about 4 percent of rural households, received 42 percent of
formal loans, while landless and subsistence households, more than 69 percent, received 23 percent. SBP now classifies
agricultural borrowers by holding size: subsistence (up to 12.5 acres), economic (above 12.5 to 50 acres) and above-economic
(above 50 acres), and publishes borrower records and disbursements by district and class.

**The geography of finance.** Where banks are matters. Burgess and Pande (2005) show that India's rule forcing banks to open
branches in unbanked rural locations is associated with lower rural poverty. Mian (2006) shows that distance between a bank's
head office and its branches shapes lending in Pakistan. Leyshon, French and Signoretta (2008) map bank branch closures in
Britain and find them concentrated in poorer areas, an example of treating access to finance as an uneven geography.

**Methods literature.** Tobler's (1970) first law, that near things are more related than distant things, motivates testing
for spatial autocorrelation. We use global and local Moran's I (Anselin 1995) and the Getis–Ord Gi* statistic (Getis and Ord
1992; Ord and Getis 1995), correcting local tests for multiple comparisons with the false discovery rate (Benjamini and Hochberg
1995). Because our units are administrative, results may depend on the units chosen, the modifiable areal unit problem (MAUP;
Openshaw and Taylor 1979; Openshaw 1984), and associations between areas need not hold for the individuals in them, the
ecological fallacy (Robinson 1950). We measure unevenness with the index of dissimilarity (Duncan and Duncan 1955).

**Post-period context.** In 2024 the Government of Punjab introduced the CM Kissan Card, an interest-free input loan for
holdings of 1 to 12.5 acres. Registration opened on 1 June 2024 and cards became operational on 15 October 2024, so it falls
after our FY2023-24 lending data apart from the last month of registration. Its initial loan limit, Rs 30,000 per acre capped at
Rs 150,000 per season, was reached at 5 acres; later changes to its terms are outside our period.

## 3. Data and GIS methods

**Data and units (Table 1).** The Mouza Census 2020 (Pakistan Bureau of Statistics, PBS) records, for every village (mouza),
which sources of credit the patwari and other local respondents said serve the mouza's residents. These are reports of
availability, not records of borrowing. We keep Punjab's 23,130 rural populated mouzas and aggregate them to tehsils. From SBP
we take FY2023-24 farm-sector borrower records and disbursed amounts by district and holding class; from the Agricultural Census
2024, farms, operated (farm) area and cultivated area by size class, tenure and crop; from SBP's branch list, all and rural
scheduled-bank branches. Rasters: ESA WorldCover 10 m 2021 (cropland; Zanaga et al. 2022) and the Malaria Atlas Project travel
time to cities, 2015 (Weiss et al. 2018).

**Table 1. Data, units, vintages and levels of measurement.**

| Variable | Source and vintage | Unit | Level of measurement | Map symbolization |
|---|---|---|---|---|
| arhti_share and formal-source shares (share of rural populated mouzas reporting the source) | Mouza Census, Jan–Mar 2020 | 137 tehsils | Ratio (normalized count) | Choropleth, natural breaks (Fig 2) |
| Bivariate class (terciles of two shares) | as above | tehsils | Ordinal × ordinal | 3 × 3 bivariate choropleth (Fig 3) |
| LISA / Gi* cluster type | derived | tehsils | Nominal | Qualitative colours (Fig 4, S8) |
| Small-farm reach (subsistence borrower records per 1,000 farms under 12.5 acres) | SBP FY2023-24; Ag Census 2024 | 36 districts | Ratio | Choropleth, quantiles (Fig 5) |
| Farms under 12.5 acres; borrower records (counts) | Ag Census 2024; SBP FY2023-24 | districts | Ratio (counts) | Dasymetric dots; proportional circles (Fig 6) |
| Location quotient (class disbursement share ÷ cultivated-area share) | SBP FY2023-24; Ag Census 2024 | districts | Ratio | Diverging choropleth, log-symmetric breaks (Fig R1) |
| Cropland share; travel time to cities | WorldCover 2021; MAP 2015 | tehsils, districts | Ratio | Zonal statistics (covariates) |

**Census geography and matching.** Pakistan's census geography nests province → division → district → tehsil → mouza, and PBS
codes each unit hierarchically, much as US FIPS/GEOID codes nest state, county and tract. OCHA's boundaries use their own
p-codes. We matched the 148 census tehsils to OCHA's 139 tehsil polygons by code and name: 115 matched exactly, 11 after
rule-based normalization, 9 after spelling review, 2 as renames, and 8 census units were summed into a parent polygon (attribute
join plus dissolve). The 3 remaining census tehsils, in Lahore, have no rural populated mouzas and no separate polygon. Every
non-exact match was reviewed by hand, and all 23,130 rural populated mouzas were assigned to a polygon. Two of the 139 polygons
have no rural populated mouzas, which leaves 137 tehsils for Q1. The district layer (36 districts, the pre-split units used by
SBP and the census) is a dissolve of the tehsils.

**Projection.** We use an Albers equal-area conic projection centred on Punjab (standard parallels 28°N and 33°N, central
meridian 72°E; full definition `+proj=aea +lat_1=28 +lat_2=33 +lat_0=30 +lon_0=72 +datum=WGS84 +units=m`). It is a secant conic,
suited to a mid-latitude region, and equal-area, which matters because choropleths and dot densities compare areas. An earlier
choice, ESRI:102028, is also Albers but centred at 125°E: it rotated Punjab by about 10° and sheared its shapes. A Tissot
indicatrix (Figure S11) shows a maximum angular distortion over the province of 29.68° in ESRI:102028 against 0.11° in our
projection. k-nearest-neighbour weights use geodesic distances, so they do not depend on the projection.

**Normalization and classification.** Every choropleth maps a ratio, never a raw count, because raw counts mostly track the size
of a unit. Raw counts appear only as dots and proportional symbols (Figure 6). Class breaks follow a fixed rule: five
Fisher–Jenks natural-break classes unless a class would hold fewer than three units, in which case quantiles. Figure S12 shows
the histogram of arhti_share under equal-interval, quantile and natural-break schemes; natural breaks fit best on the goodness of
absolute deviation fit (0.818, against 0.781 for both alternatives). Figure S1 compares quantile and natural-break maps.

**Raster processing.** Cropland was computed from the 10 m WorldCover tiles as the fraction of cropland pixels in each block of
10 × 10 pixels (about 100 m), an average-based resampling that avoids the "winner takes all" loss of mixed pixels, then summarized
by zonal statistics for each tehsil and district. Travel time to cities, a cost-distance surface, was summarized as a
cropland-weighted mean. The Mouza Census also reports each mouza's distance to the nearest bank branch and grain market in bands
(in the mouza, 1–10, 11–25, 26–50, over 50 km), which work like multiple-ring buffers measured by respondents.

**Spatial statistics.** Spatial weights are Queen contiguity, row-standardised (primary), with sensitivity runs using Rook
contiguity (which gives the same neighbours for these polygons), geodesic k-nearest neighbours (k = 5; not symmetrized), a
geodesic distance band (73.6 km, the smallest distance that leaves no tehsil without a neighbour, so there are no islands) and
inverse-distance weights within that band. All permutation tests use 999 permutations with seed 20261031 and report one-sided
pseudo p-values in the direction of the observed statistic. We report global Moran's I and Geary's C, the Moran scatterplot
(Figure S7), local Moran's I (LISA) and Gi* (Queen contiguity including each tehsil itself, binary weights) at p < 0.05 and after
false-discovery-rate correction (Benjamini–Hochberg cutoff 0.0117 for LISA), and a second-order trend surface, the OLS fit of
arhti_share on centroid coordinates x, y, x², xy and y², with its residual map (Figure S9).

**Arhti and formal credit (H1).** For each formal source (commercial banks, ZTBL, cooperative bank, microfinance banks) we report
the same-tehsil Spearman correlation with arhti_share, the bivariate Moran's I between a tehsil's arhti share and its neighbours'
share for that source, and a within-tehsil Mantel–Haenszel odds ratio of a mouza reporting arhti credit when the formal source is
also reported, with tehsils as strata; we also do this for "any formal source". Tehsils whose 2 × 2 table has an empty row or
column carry no information and are dropped (for commercial banks, 1,456 mouzas). Breslow–Day tests whether the odds ratio is the
same across tehsils. An exploratory model relates arhti_share to cropland share, distance to grain markets (share of mouzas over
50 km away), commercial and ZTBL availability, distance to an online bank branch and travel time, with standardized predictors,
fitted by OLS, by a binomial model on mouza counts with quasi-binomial standard errors, and by a spatial error model (Table B3).

**Allocation and reporting geography (H2, H3).** Province comparisons use the 36 districts on both sides: SBP's 36 district rows
(banks; Islamabad and the 74,494 microfinance borrower records that SBP reports only for Punjab as a whole are excluded) against
the census's Punjab minus the Cholistan Area, which has no SBP counterpart. SBP's All Punjab row (732,856 records) is reported for
comparison. Small-farm reach is subsistence-holding borrower records per 1,000 farms under 12.5 acres, a borrower-record
intensity rather than an inclusion rate, since records may not be unique people. The index of dissimilarity D = ½ Σ |bᵢ/B − fᵢ/F|
is the share of borrower records that would have to be in other districts for their distribution to match that of small farms.
The concentration coefficient orders districts by reach, so it measures inequality in reach across districts relative to small
farms, not inequality between farmers. Location quotients divide a district's share of Punjab's disbursement in a class by its
share of cultivated area. SBP reports lending by district; whether that is the lending branch's district or the financed farm's
is being verified, so every district credit figure is "as reported by SBP". A data-quality screen flags districts where a class's
average loan is above 5 or below 0.2 times the Punjab median, or where above-economic loans exceed 75% of farm-sector
disbursement; the five flagged districts are marked, not dropped (Table B4).

**Typology.** As an exploratory complement to a median split, we group the 35 classifiable districts with k-means on six
standardized attributes, with and without location, choosing k from 2 to 6 by the silhouette score (Figure S10). All analysis is
in Python (GeoPandas, PySAL) and QGIS 4.2.3; the main maps (Figures 2–6) are QGIS Print Layouts.

## 4. Results

### 4.1 H1: arhti credit clusters, follows farmland and coexists with formal credit

Arhti credit is reported available in 31.5% of Punjab's rural populated mouzas (Figure 2). Tehsil shares span the full range,
from 0.0% to 100.0%, with a median of 19.2%, and 15 tehsils report none. Formal sources are reported more widely: ZTBL in 73.5% of
mouzas, commercial banks in 38.2%, the cooperative bank in 24.9% and microfinance banks in 15.2%.

The pattern is strongly clustered. Global Moran's I for arhti availability is 0.536 (p = 0.001), against 0.297 for
commercial-bank credit, and Geary's C is 0.458 (p = 0.001). The Moran scatterplot (Figure S7) places most tehsils in the
High-High and Low-Low quadrants. The LISA map (Figure 4) identifies 25 High-High and 32 Low-Low tehsils at p < 0.05, of which 15
and 17 survive the false-discovery-rate correction; 3 tehsils are Low-High outliers. High-High clusters lie mainly in Sheikhupura,
Gujranwala, Hafizabad, Sialkot and Nankana Sahib, with two in Bahawalnagar and Bahawalpur; Low-Low clusters lie mainly in
Rawalpindi, Attock, Jhelum and Chakwal. Gi* finds the same places (Figure S8): 28 hot spots and 33 cold spots at p < 0.05 (15 and
18 after correction), and every LISA High-High tehsil is a Gi* hot spot. A smooth province-wide gradient does not account for the
clusters: a second-order trend surface reaches R² = 0.40, and its residuals remain clustered (Moran's I = 0.234, p = 0.002), so
there is significant spatial autocorrelation beyond the fitted trend. Arhti availability is also less evenly spread than formal
availability: the index of dissimilarity between arhti-reporting mouzas and all rural populated mouzas is 0.380, against 0.234
for commercial banks and 0.115 for ZTBL.

**The H1 test (Tables B1, B2).** Gap-filling predicts negative associations. None appears for any formal source. Across tehsils,
arhti_share correlates positively with commercial-bank (ρ = 0.245), ZTBL (ρ = 0.166), cooperative (ρ = 0.391) and microfinance
(ρ = 0.380) availability. The bivariate Moran's I between a tehsil's arhti share and its neighbours' commercial-bank share is
0.112 (p = 0.062) and is positive for ZTBL (0.170, p = 0.004) and the cooperative bank (0.156, p = 0.017). Within tehsils, the odds
that a mouza reports arhti credit are 18% higher where commercial-bank credit is also reported (odds ratio 1.18, 95% CI
1.09–1.27; 21,674 mouzas in 120 tehsils), and higher still where cooperative (1.72) or microfinance (1.76) credit is reported.
Against ZTBL (0.98, 95% CI 0.90–1.07) and against any formal source (0.95, 95% CI 0.87–1.04) there is no association. Of the
mouzas in Table B2, 3,046 report neither arhti credit nor any formal source. The average conceals large differences: for
commercial banks the Breslow–Day test rejects a common odds ratio (p < 0.001), and of the 120 informative tehsils 67 report the
two sources together more often than independence implies and 53 less often.

**What arhti availability follows.** Arhti availability is higher where more land is cropland (Spearman ρ = 0.49, adjusted
p < 0.001) and lower where more villages have an online commercial-bank branch, a measure of presence (ρ = −0.40). It is lower
where more mouzas are over 50 km from a grain market (ρ = −0.25, adjusted p = 0.009), but not related to having a market in the
village itself (ρ = −0.03). In the exploratory model (Table B3), cropland is the one predictor associated with arhti availability
in both the OLS fit (p = 0.039) and the quasi-binomial fit (p = 0.021); distance to grain markets is negative but uncertain
(p = 0.061 in the quasi-binomial fit), and formal availability adds little once cropland is included. In the spatial error model
no predictor is clearly associated (λ = 0.715), so most of the pattern is local structure that these covariates do not capture.
**H1 is not supported:** no formal source shows the negative association gap-filling implies. The evidence fits H1-alt on
average, with substitution and coexistence both possible in different local markets.

### 4.2 H2: small holdings appear in borrower records in proportion, but not in disbursement

On the 36-district basis (Figure A1), subsistence holdings are 94.2% of farms and account for 90.9% of farm-sector borrower
records but 37.0% of the amount disbursed. Above-economic holdings are 0.5% of farms, with 1.2% of borrower records and 47.8% of
disbursement. Disbursement per borrower record is Rs 0.52 million for subsistence holdings and Rs 50.62 million for
above-economic holdings; this is not the average loan, since records may count repeat transactions. SBP's All Punjab row, which
adds microfinance records and Islamabad, gives the same picture (91.9% of records, 35.9% of disbursement for subsistence holdings;
49.4% of disbursement for above-economic holdings). The census also reports subsistence holdings' share of operated area (68.7%),
but its class areas are questionable: in three classes below 12.5 acres the published area implies an average farm larger than
the class limit, so we treat area shares as indicative and rely on farm counts. The concentration is consistent with earlier
evidence of skewed formal credit (Khandker and Faruqee 2003), although the measures are not directly comparable.

Across districts, the intensity of small-farm borrower records varies widely (Figure 5). Small-farm reach ranges from 21.6 to
299.0 subsistence-holding borrower records per 1,000 farms under 12.5 acres, with a median of 118.5 across 36 districts, and is
spatially clustered (Moran's I 0.532). The lowest values lie in the north (Rawalpindi, Jhelum, Chakwal, Gujrat); the highest in
the south and centre (Bahawalnagar, Bahawalpur, Okara, Lodhran, Hafizabad). Five districts flagged by the data-quality screen
(Chakwal, Faisalabad, Jhelum, Lahore, Rawalpindi) are marked rather than dropped. Figure 6 shows the contrast without ratios: 4,738
dots, each standing for 1,000 farms under 12.5 acres in the 36 districts and placed only on cropland, show where small farms are
(a synthetic redistribution, not farm locations), and perceptually scaled circles show where small-farm borrower records are
reported. The index of dissimilarity between the two distributions is 0.216. Ordering districts by reach, the concentration
coefficient is 0.297 (Figure S6). Small-farm reach is higher where tenant farms are a larger share of farms (Spearman ρ = 0.39,
adjusted p 0.018); this describes districts, not tenants, whose own borrowing these data cannot show. Crop structure varies less
than credit: wheat is the largest of the five tracked crops by area in 34 districts and rice in 2. **H2 is not supported:** small
holdings are close to proportionally represented in borrower records but receive a much smaller share of disbursement, and
borrower records are spread unevenly relative to small farms.

### 4.3 H3: recorded lending concentrates in city districts, above all for large holdings

Where formal agricultural lending is recorded does not follow where farmland is (Figure R1). For above-economic holdings the
location quotient is 14.06 in Lahore and 7.44 in Rawalpindi, and as low as 0.09 in Chakwal. For subsistence holdings it is 4.66 in
Lahore, 6.47 in Jhelum (a flagged district) and 0.29 in Rawalpindi. Five large-city districts (Lahore, Rawalpindi, Multan,
Faisalabad and Rahim Yar Khan) together record 39.7% of Punjab's farm-sector disbursement and 59.6% of above-economic disbursement,
but hold 13.3% of cultivated area (Figure R2). Their share of subsistence disbursement, 22.4%, is also well above their share of
cultivated area, though far below their share of large-holding lending. Islamabad, outside the 36-district totals, records 3.9% of
disbursement in SBP's district rows. Lahore and Rawalpindi have little farmland but large shares of above-economic lending, while
Multan and Rahim Yar Khan are major agricultural districts in their own right. The same five districts hold 43.5% of all
scheduled-bank branches but 19.1% of rural branches; the index of dissimilarity against farms is 0.356 for all branches and 0.214
for rural branches. **H3 is not supported:** recorded lending is concentrated in city districts for every class, most strongly for
large holdings. Until SBP's district attribution is confirmed, a high location quotient in a city district may reflect where loans
are booked rather than where the financed land is; Rawalpindi's above-economic records, for example, average far above the Punjab
median (Table B4).

### 4.4 Cost in context

Figure P1 places formal lending rates next to published arhti estimates; they are not matched contracts. For about 2012-13, the
IGC estimates of implicit arhti cost (61.9% to 80.7% by crop) sit far above both the bank rates reported by interviewed farmers
(9 to 18 percent) and SBP's institutional averages for FY2012-13: ZTBL 12.00 (production) and 13.80 (development), the Punjab
Provincial Cooperative Bank 19.00 and 18.00, commercial banks 16.00 and 16.00 percent per annum. SBP's FY2023-24 averages are
higher (ZTBL 29.42 and 29.42; cooperative bank 20.67 and 22.71; commercial banks 22.96 and 22.94). The Kissan Card, at 0% for
holdings up to 12.5 acres, began after the data period. The sampled studies document much higher implicit costs for arhti credit,
which makes its coexistence with cheaper formal credit, found under H1, notable.

### 4.5 District typology

A median split groups 10 districts as high arhti availability with high small-farm reach, 10 as low with low, 8 as low
availability with high reach and 7 as high availability with low reach (Lahore is not classified): the two measures are close to
independent. k-means (Figure S10) separates the districts only weakly (silhouette 0.26 without location, 0.25 with it), so we
treat its groups as illustrations, not regions.

## 5. Robustness and the MAUP

The clustering of arhti credit holds across five weighting specifications: Moran's I is 0.536 with Queen or Rook contiguity
(identical neighbours), 0.568 with geodesic k-nearest neighbours, 0.470 with the 73.6 km distance band and 0.491 with inverse
distance, all with p = 0.001. **Scale effect:** aggregating tehsils to 35 districts lowers Moran's I to 0.429; 8 High-High and 5
Low-Low districts appear at p < 0.05 but only one of each survives the false-discovery-rate correction (Figure S2), against 15 and
17 at tehsil level. Part of that loss reflects aggregation and part the smaller number of units. **Zoning effect:** excluding the
Cholistan desert mouzas, which changes how three southern polygons are drawn, gives Moran's I 0.543 and a within-village odds ratio
of 1.20 (95% CI 1.11–1.29). Excluding the five flagged districts, the concentration coefficient is 0.255 and Moran's I for
small-farm reach is 0.428.

## 6. Discussion

The lenses show finance and farming sharing the map only partly. Several mechanisms are consistent with published work; we
present them as possibilities, not findings.

*Interlinked marketing and credit.* Arhtis lend against the crop they will market (Bell 1988; Aleem 1990; Haq et al. 2013).
Lending tied to crop sales would be expected to follow farmland and marketed surplus, consistent with the association with
cropland and with arhti credit appearing in villages that also report formal credit. Under this reading the arhti is less a
substitute for a missing bank than a market agent whose lending travels with the harvest.

*Speed and collateral.* Most farmers interviewed by the IGC had bank accounts yet preferred arhtis because borrowing was easier.
If speed, flexible repayment and the absence of collateral matter more than the headline rate (Hoff and Stiglitz 1990), arhti
credit could persist next to formal credit despite costing more. The heterogeneity across tehsils would then reflect local
differences in how easy each source is to use.

*Branch networks and booking practices.* Formal lending passes through branches, which are densest in cities. If large loans are
arranged and recorded at city branches, high location quotients in Lahore and Rawalpindi would follow (compare Mian 2006 on
distance within banks). Confirming SBP's district attribution and counting rules is the first step in telling recording from use.

*Pattern, process and the ecological fallacy.* Our associations are between areas. That villages reporting bank credit are more
likely to report arhti credit does not mean that the same farmers use both (Robinson 1950). Map design choices matter too, which
is why we fix the classification rule in advance, show alternatives (Figures S1, S12) and report two unit sizes.

**Policy implications.** Read with these limits, the patterns suggest several directions. Because arhti credit coexists with formal
credit, expanding branch networks alone may not reduce reliance on informal finance; products that match farmers' cash flows and
harvest timing may matter as much as proximity. Because arhti credit clusters around farmland and markets, pilots of
market-linked formal products, such as warehouse-receipt or value-chain finance, could be placed in the high-arhti clusters.
Because recorded lending concentrates in city districts, better location reporting by SBP (lending branch and financed farm) would
make district targeting possible. Products that do not rely solely on land ownership would be relevant where tenant farms are
common. Finally, our FY2023-24 baseline predates the Kissan Card and can serve as a reference point for later changes.

## 7. Limitations

The Mouza Census records whether respondents report a credit source as serving the village, not whether households borrow or on
what terms. Our sources differ in date and unit: January–March 2020 (mouzas and tehsils), FY2023-24 (districts as reported by
SBP), the Agricultural Census 2024 (sample-based, so district figures carry sampling error) and the branch list of 30 June 2024.
SBP's district attribution is under verification; borrower records may not be unique people; microfinance records have no
district and are excluded from district measures. The census's class areas below 12.5 acres are internally inconsistent, so
area-based shares are indicative. SBP's "up to 12.5 acres" and the census's "under 12.5 acres" differ at the boundary, as do the
definitions at 50 acres. Our 36 districts are the pre-split units. The boundaries post-date the census, and a few tehsils rest on
few rural populated mouzas. Pooled odds ratios assume independence across mouzas, which spatial dependence may violate. Dots in
Figure 6 are a synthetic redistribution. Published cost estimates come from small, non-representative studies. All results are
descriptive associations.

## 8. Conclusion

Agricultural credit in Punjab has distinct and uneven geographies. **H1 is not supported:** arhti credit is clustered (Moran's I
0.536 across five weighting specifications), follows cropland, and shows no negative association with any formal source; within
tehsils it is modestly more likely where commercial-bank credit is reported (odds ratio 1.18) and unrelated to ZTBL or to formal
credit as a whole, with wide local variation. **H2 is not supported:** small holdings hold 90.9% of borrower records but 37.0% of
disbursement in the 36 districts, and borrower records are spread unevenly relative to small farms (D = 0.216). **H3 is not
supported:** five city districts record 59.6% of above-economic disbursement with 13.3% of cultivated area, and more than their
share for small holdings too. Where the bank ends, the arhti has not simply begun: the two systems overlap. Confirming where SBP
attributes loans, and observing how farmers combine sources, are the next steps for understanding why.

**Data and code availability.** All data are public; sources, access dates and checksums, and the scripts that rebuild every
number, table and figure from the raw downloads, are at https://github.com/ahmedrazakhanlodhi/arhti-project.

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
https://www.theigc.org/sites/default/files/2014/09/Haq-Et-Al-2013-Working-Paper.pdf

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

Pakistan Bureau of Statistics. *Mouza Census 2020*, Punjab report and mouza-level records.
https://www.pbs.gov.pk/wp-content/uploads/2020/07/mouza_census_2020_punjab_report.pdf (accessed 31 October 2026).

Pakistan Bureau of Statistics. *Agricultural Census 2024*, Punjab report and district tables.
https://www.pbs.gov.pk/wp-content/uploads/2020/07/IAC-Punjab-Report-25-05-2026-1.pdf (accessed 31 October 2026).

State Bank of Pakistan. District-wise agricultural credit disbursement, FY2023-24.
https://archive.sbp.org.pk/acd/DistrictWise-Detail-Jul-Jun-2024.xlsx (accessed 31 October 2026). Also: list of bank branches as
on 30 June 2024; *Monthly Statistical Bulletin*, Table 3.33 (June 2024 and September 2026 editions).

OCHA. Pakistan subnational administrative boundaries (COD-AB), valid_on 2022-09-09. https://data.humdata.org/dataset/cod-ab-pak
(accessed 31 October 2026).

## Appendix (list)

- Tables B1 (arhti against each formal source), B2 (mouzas by reported sources), B3 (exploratory model of arhti availability),
  B4 (districts flagged by the SBP data-quality screen) and B5 (prespecified regressions).
- Figures S1 to S12 and R2: classification comparison; district LISA; published-study locations (context only); village-level
  co-reporting; three-panel Figure 5; concentration curve; Moran scatterplot; Gi*; trend surface; k-means typology; Tissot
  indicatrix; classification histograms; city-district shares.
