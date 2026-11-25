# Slide text

Numbers from `docs/key_numbers.md`; figures from `outputs/figures/`. `scripts/19_build_documents.py` builds the deck from this
file: each `## Slide` is one slide; `Headline:` is the takeaway line; `- ` lines are bullets; `Figures:` lists image files
(one or two per slide); `Notes:` is speaker notes.

## Slide 1. Where the Bank Ends and the Arhti Begins
Headline: Geographic access, landholding structure and the allocation of agricultural credit in Punjab, Pakistan
- Ahmed Raza Khan Lodhi and Hasnain Akram
- PPHA 38520, GIS Applications in the Social Sciences, University of Chicago, November 30, 2026
Figures: fig6_dasymetric_farms_borrowers_qgis.png
Notes: [Ahmed] Good afternoon. I'm Ahmed Raza Khan Lodhi, and this is joint work with Hasnain Akram. Our project is called Where the Bank Ends and the Arhti Begins. Farmers in Punjab borrow from two systems. Banks lend through branches. Arhtis, the commission agents who sell farmers' crops in the grain markets, lend against the harvest they will market. The map behind me shows both: each dot is a thousand small farms placed on cropland, and each circle is the number of small-farm borrower records the State Bank reports in a district. Our question is simple: where does each system reach, and whom?

## Slide 2. Problem, thesis and hypotheses
Headline: Does arhti credit fill the gaps banks leave, and does formal credit reach small farms?
- Q1 (tehsils): is arhti credit reported where formal credit is weak, or where formal credit, markets and farmland already are?
- H1 gap-filling: arhti and formal credit negatively associated. H1-alt coexistence: they appear together, near markets.
- Q2 (districts): does formal credit reach small farms in proportion to their share of farms?
- H2 proportional reach (index of dissimilarity near 0). H3 (exploratory): lending recorded where farmland is (LQ near 1).
- Thesis: arhti credit clusters near grain markets; its link to formal credit varies by institution and place. Descriptive, not causal.
Notes: [Ahmed] We ask two questions. First, across tehsils: is arhti credit found where formal credit is missing, or where banks, markets and farmland already are? If arhtis fill the gaps that banks leave, the two should be negatively associated. That is our first hypothesis, gap-filling. Second, across districts: does formal credit reach small farms in proportion to how many small farms there are? That is our second hypothesis, proportional reach. A third, exploratory hypothesis asks whether lending is recorded where the farmland is. We fixed the main tests before running them. Everything we show is descriptive: associations between places, not effects.

## Slide 3. What the literature says
Headline: Interlinked credit is old news; mapping it across a province is not
- Informal lenders tie credit to crop sales (Bell 1988; Aleem 1990: 78.7% average cost of informal borrowing near Chambar, Sindh).
- In Punjab the arhti is the largest informal source, working from 325 markets; implicit cost 62–80% by crop (Haq et al. 2013).
- Formal credit skews to large farms: 4% of households received 42% of formal loans (Khandker and Faruqee 2003).
- Bank geography matters (Burgess and Pande 2005; Mian 2006; Leyshon et al. 2008). Gap: no province-wide map of arhti credit.
Notes: [Ahmed] The literature tells us this kind of lending is old. Lenders who tie credit to the sale of the crop are well documented: in Sindh, Aleem found that informal credit cost an average of 78.7 percent a year. In Punjab, a study for the International Growth Centre found the arhti to be the largest informal lender, working from 325 grain markets, with implicit interest of 62 to 80 percent depending on the crop. On the formal side, Khandker and Faruqee found that large landowners, 4 percent of rural households, received 42 percent of formal loans. What had not been done is to map arhti credit across the whole province, village by village. That is our contribution.

## Slide 4. Data and GIS workflow
Headline: Four sources, three vintages, one equal-area projection
- Mouza Census 2020: 23,130 rural populated mouzas → 137 tehsils (attribute join + dissolve; every non-exact match reviewed).
- SBP FY2023-24 borrower records and amounts by district and holding class; Agricultural Census 2024 farms, area, crops; branch list 30 Jun 2024.
- Rasters: WorldCover 2021 cropland (10 m → 100 m fraction, zonal statistics); MAP travel time (cost distance).
- Albers equal-area centred on Punjab (Tissot: 0.11° vs 29.68° max angular distortion in the old CRS). Ratios mapped, counts as dots.
Figures: figS11_tissot_indicatrix.png
Notes: [Ahmed] We combine four public datasets. The Mouza Census of 2020 tells us, for every village, which credit sources are available: 23,130 rural populated villages, which we joined to 137 tehsil boundaries, checking by hand every name that did not match exactly. The State Bank of Pakistan gives us lending for FY2023-24 by district and farm size, and the Agricultural Census of 2024 gives us farms and land. We add satellite cropland from ESA WorldCover and travel time to cities. One GIS choice mattered: our first projection was centred far to the east and twisted Punjab, as the Tissot circles on the right show. We switched to an equal-area projection centred on Punjab, which keeps the circles round. We map rates as choropleths and raw counts only as dots.

## Slide 5. H1: arhti credit is strongly clustered
Headline: Moran's I = 0.536; 25 High-High and 32 Low-Low tehsils
- 31.5% of rural populated mouzas report arhti credit; tehsil shares run from 0% to 100%.
- High-High: Sheikhupura–Gujranwala–Sialkot belt and Bahawalnagar; Low-Low: Rawalpindi, Attock, Jhelum, Chakwal.
- Gi* finds the same hot and cold spots (28 and 33); trend-surface residuals still cluster (I = 0.234).
Figures: fig2_arhti_share_tehsil_qgis.png, fig4_lisa_arhti_tehsil_qgis.png
Notes: [Ahmed] First result. Arhti credit is reported in 31.5 percent of rural villages, but it is far from even. Global Moran's I is 0.536, which is strong clustering. The cluster map on the right shows where: a high-high belt from Sheikhupura through Gujranwala to Sialkot, and in Bahawalnagar, and a low-low block in the Pothohar districts of Rawalpindi, Attock, Jhelum and Chakwal. In total there are 25 high-high and 32 low-low tehsils. A Getis-Ord hot-spot analysis finds the same places, and the clustering remains after we remove any smooth province-wide trend.

## Slide 6. H1 test: no significant negative association with any formal source
Headline: Arhti credit appears alongside commercial, cooperative and microfinance credit; ZTBL and all-formal results inconclusive
- Within tehsils, odds ratios: commercial 1.18, cooperative 1.72, microfinance 1.76 (adjusted p < 0.001); ZTBL 0.98, any formal 0.95.
- Arhti availability is higher where more villages have a grain market within 10 km (ρ = 0.336) or 25 km (ρ = 0.377); holds in the spatial error model.
- +5.5 percentage points of arhti availability per one-SD more villages within 10 km of a market (spatial error model); cropland's link does not survive.
- 79.9% of arhti-reporting mouzas also report a formal source (75.9% of the rest do); 3,810 of 23,130 report neither.
Figures: fig7_markets_neither_tehsil_qgis.png
Notes: [Ahmed] Now the test of gap-filling. If arhtis filled the gaps banks leave, the villages without banks would be the ones with arhtis. That is not what we find. Comparing villages within the same tehsil, the odds that a village reports arhti credit are higher where commercial-bank credit is reported, an odds ratio of 1.18, and higher still for the cooperative bank and microfinance banks, 1.72 and 1.76. For ZTBL and for formal credit as a whole, the result is inconclusive. No formal source shows a significant negative association; 79.9 percent of villages that report arhti credit also report a formal source, though formal credit is common everywhere: 75.9 percent of the other villages report one too. What does go with arhti credit is closeness to markets: in a spatial error model, one standard deviation more villages within 10 kilometres of a grain market goes with 5.5 percentage points more arhti availability. The left map shows that market access; the right map shows the 3,810 villages that report neither source.

## Slide 7. H2: in proportion by count, not by amount
Headline: 36 districts: small holdings are 94.2% of farms, 90.9% of borrower records, 37.0% of disbursement
- Rs 0.52 million per borrower record for subsistence holdings vs Rs 50.62 million for above-economic holdings.
- Above-economic holdings: 2.35 times their farm share in records, 92.11 times in disbursement.
- Borrower records vs small farms across districts: D = 0.216 (0.182 without flagged districts).
Figures: fig5_small_farm_reach_qgis.png, fig6_dasymetric_farms_borrowers_qgis.png
Notes: [Hasnain] Thank you, Ahmed. I'm Hasnain Akram, and I'll take the second question: whom formal credit reaches. Across Punjab's 36 districts, holdings under 12.5 acres are 94.2 percent of farms. They hold 90.9 percent of borrower records, close to their share, but receive only 37.0 percent of the money. Per borrower record, a subsistence holding receives about 0.52 million rupees and an above-economic holding about 50.62 million, roughly 97 times as much. Across districts the picture is uneven too: the index of dissimilarity between borrower records and small farms is 0.216, so about a fifth of the records would have to move district to match where small farms are. So formal lending is disproportionate: small farms are in the records, but not in the money.

## Slide 8. H3: lending is recorded in city districts
Headline: Five city districts: 59.6% of above-economic disbursement, 13.3% of cultivated area
- Location quotient for above-economic lending: Lahore 14.06, Rawalpindi 7.44, Chakwal 0.09.
- Leave any one city out: still 4.41 to 5.65 times its area share. Five districts with the largest urban populations (2023 census): 43.5% with 11.2% of area.
- District = as reported by SBP (attribution under verification): booking place may differ from where the land is.
Figures: figR1_lq_maps.png
Notes: [Hasnain] Our third, exploratory question is where lending is recorded. Five city districts, Lahore, Rawalpindi, Multan, Faisalabad and Rahim Yar Khan, record 59.6 percent of large-farm lending but hold only 13.3 percent of cultivated land. Lahore's location quotient for large holdings is 14.06: about fourteen times its share of farmland. The pattern holds if we drop any one of these cities, and it holds if we instead take the five districts with the largest urban populations. One caution: the State Bank reports lending by district, and we have not confirmed whether that is where a loan was booked or where the land is. So this is the geography of recorded lending.

## Slide 9. Cost in context
Headline: Published arhti cost estimates sit far above formal rates
- IGC 2013: implicit arhti cost 61.9%–80.7% by crop vs SBP FY2012-13 averages of 12.00–19.00%.
- FY2023-24 formal averages 20.67%–29.42%.
- Kissan Card (0%, up to 12.5 acres) began after the data period; it initially required land in the applicant's name in the provincial land records.
Figures: figP1_price_ladder.png
Notes: [Hasnain] Why does this matter? Cost. Published estimates put the implicit cost of arhti credit at 61.9 to 80.7 percent a year, against formal agricultural rates of 12.00 to 19.00 percent at the same time. These are not matched contracts, but the gap is large, which makes it notable that arhti credit persists right next to formal credit. The Punjab Kissan Card, an interest-free loan introduced in 2024, came after our data, and it initially required applicants to own land recorded in the provincial land records, which may leave tenants out.

## Slide 10. Robustness and the MAUP
Headline: Clustering survives every weighting scheme; aggregation weakens it
- Moran's I: Queen/Rook 0.536, kNN-5 0.568, 73.6 km band 0.470, inverse distance 0.491 (all p = 0.001).
- Scale effect: 35 districts → I = 0.429; only 1 High-High and 1 Low-Low cluster survive FDR.
- Zoning effect: excluding Cholistan desert mouzas → I = 0.543, odds ratio 1.20.
Figures: figS7_moran_scatterplot.png
Notes: [Hasnain] We tested how robust this is. The clustering holds across five definitions of neighbours, with Moran's I between 0.470 and 0.568. Aggregation matters, as the modifiable areal unit problem predicts: at district level Moran's I falls to 0.429, and only one high-high and one low-low cluster survive the correction for multiple testing. Excluding the Cholistan desert villages hardly changes the results.

## Slide 11. Limits
Headline: Availability is not borrowing; districts are not farmers
- Mouza Census reports availability, not household borrowing. Borrower records may not be unique people.
- Ecological fallacy: area associations need not hold for the farmers in them.
- Different vintages (2020, FY2023-24, 2024); SBP district attribution under verification; 36 pre-split districts.
Notes: [Hasnain] Three limits. First, the census records whether a credit source is available, not whether anyone borrows. Second, our results are about places, not people: a village that reports both sources does not tell us that the same farmer uses both. Third, our sources come from different years, and we never treat them as the same moment.

## Slide 12. Conclusions
Headline: The arhti does not begin where the bank ends: the two overlap, and formal money concentrates
- H1: coexistence, not gap-filling. Arhti credit clusters near grain markets and alongside formal credit.
- H2: formal lending is disproportionate. Small holdings: 90.9% of records, 37.0% of disbursement.
- H3: recorded lending is concentrated. Five city districts: 59.6% of above-economic disbursement, 13.3% of cultivated area.
- Reported availability is a poor guide to who receives formal money: the sharpest contrasts are by farm size and by booking place.
- Next: confirm SBP attribution; observe how farmers combine arhti, bank and Kissan Card credit.
Notes: [Hasnain] To conclude, three findings. First, arhti credit coexists with formal credit rather than filling its gaps: it clusters near grain markets, in the same places as formal credit. Second, formal lending is disproportionate: small holdings are in the records, 90.9 percent of them, but receive 37.0 percent of the money. Third, recorded lending is concentrated: five city districts record 59.6 percent of above-economic disbursement with 13.3 percent of the cultivated area. So our answer to the title is that the arhti does not begin where the bank ends; the two overlap. The sharpest contrasts in formal credit are not between places with and without it, but between small and large farms, and between where farms are and where loans are recorded. Reported availability alone is a poor guide to who receives formal money. The next steps are to confirm how the State Bank attributes loans, and to observe how farmers combine arhti, bank and Kissan Card credit. Thank you. We are happy to take questions.
