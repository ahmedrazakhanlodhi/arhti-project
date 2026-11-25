# Speaker script: Where the Bank Ends and the Arhti Begins

12 slides · 1,310 words · about 10.1 minutes at 130 words per minute. Built from the Notes in `docs/slide_text.md` by `scripts/19_build_documents.py`; the same text is in the deck's speaker notes.

## Slide 1. Where the Bank Ends and the Arhti Begins
*Ahmed · about 45 seconds · starts at 0:00*

Good afternoon. I'm Ahmed Raza Khan Lodhi, and this is joint work with Hasnain Akram. Our project is called Where the Bank Ends and the Arhti Begins. Farmers in Punjab borrow from two systems. Banks lend through branches. Arhtis, the commission agents who sell farmers' crops in the grain markets, lend against the harvest they will market. The map behind me shows both: each dot is a thousand small farms placed on cropland, and each circle is the number of small-farm borrower records the State Bank reports in a district. Our question is simple: where does each system reach, and whom?

## Slide 2. Problem, thesis and hypotheses
*Ahmed · about 45 seconds · starts at 0:46*

We ask two questions. First, across tehsils: is arhti credit found where formal credit is missing, or where banks, markets and farmland already are? If arhtis fill the gaps that banks leave, the two should be negatively associated. That is our first hypothesis, gap-filling. Second, across districts: does formal credit reach small farms in proportion to how many small farms there are? That is our second hypothesis, proportional reach. A third, exploratory hypothesis asks whether lending is recorded where the farmland is. We fixed the main tests before running them. Everything we show is descriptive: associations between places, not effects.

## Slide 3. What the literature says
*Ahmed · about 55 seconds · starts at 1:32*

The literature tells us this kind of lending is old. Lenders who tie credit to the sale of the crop are well documented: in Sindh, Aleem found that informal credit cost an average of 78.7 percent a year. In Punjab, a study for the International Growth Centre found the arhti to be the largest informal lender, working from 325 grain markets, with implicit interest of 62 to 80 percent depending on the crop. On the formal side, Khandker and Faruqee found that large landowners, 4 percent of rural households, received 42 percent of formal loans. What had not been done is to map arhti credit across the whole province, village by village. That is our contribution.

## Slide 4. Data and GIS workflow
*Ahmed · about 60 seconds · starts at 2:26*

We combine four public datasets. The Mouza Census of 2020 tells us, for every village, which credit sources are available: 23,130 rural populated villages, which we joined to 137 tehsil boundaries, checking by hand every name that did not match exactly. The State Bank of Pakistan gives us lending for FY2023-24 by district and farm size, and the Agricultural Census of 2024 gives us farms and land. We add satellite cropland from ESA WorldCover and travel time to cities. One GIS choice mattered: our first projection was centred far to the east and twisted Punjab, as the Tissot circles on the right show. We switched to an equal-area projection centred on Punjab, which keeps the circles round. We map rates as choropleths and raw counts only as dots.

## Slide 5. H1: arhti credit is strongly clustered
*Ahmed · about 40 seconds · starts at 3:25*

First result. Arhti credit is reported in 31.5 percent of rural villages, but it is far from even. Global Moran's I is 0.536, which is strong clustering. The cluster map on the right shows where: a high-high belt from Sheikhupura through Gujranwala to Sialkot, and in Bahawalnagar, and a low-low block in the Pothohar districts of Rawalpindi, Attock, Jhelum and Chakwal. In total there are 25 high-high and 32 low-low tehsils. A Getis-Ord hot-spot analysis finds the same places, and the clustering remains after we remove any smooth province-wide trend.

## Slide 6. H1 test: no significant negative association with any formal source
*Ahmed · about 80 seconds · starts at 4:06*

Now the test of gap-filling. If arhtis filled the gaps banks leave, the villages without banks would be the ones with arhtis. That is not what we find. Comparing villages within the same tehsil, the odds that a village reports arhti credit are higher where commercial-bank credit is reported, an odds ratio of 1.18, and higher still for the cooperative bank and microfinance banks, 1.72 and 1.76. For ZTBL and for formal credit as a whole, the result is inconclusive. No formal source shows a significant negative association; 79.9 percent of villages that report arhti credit also report a formal source, though formal credit is common everywhere: 75.9 percent of the other villages report one too. What does go with arhti credit is closeness to markets: in a spatial error model, one standard deviation more villages within 10 kilometres of a grain market goes with 5.5 percentage points more arhti availability. The left map shows that market access; the right map shows the 3,810 villages that report neither source.

## Slide 7. H2: in proportion by count, not by amount
*Hasnain · about 55 seconds · starts at 5:24*

Thank you, Ahmed. I'm Hasnain Akram, and I'll take the second question: whom formal credit reaches. Across Punjab's 36 districts, holdings under 12.5 acres are 94.2 percent of farms. They hold 90.9 percent of borrower records, close to their share, but receive only 37.0 percent of the money. Per borrower record, a subsistence holding receives about 0.52 million rupees and an above-economic holding about 50.62 million, roughly 97 times as much. Across districts the picture is uneven too: the index of dissimilarity between borrower records and small farms is 0.216, so about a fifth of the records would have to move district to match where small farms are. So formal lending is disproportionate: small farms are in the records, but not in the money.

## Slide 8. H3: lending is recorded in city districts
*Hasnain · about 50 seconds · starts at 6:22*

Our third, exploratory question is where lending is recorded. Five city districts, Lahore, Rawalpindi, Multan, Faisalabad and Rahim Yar Khan, record 59.6 percent of large-farm lending but hold only 13.3 percent of cultivated land. Lahore's location quotient for large holdings is 14.06: about fourteen times its share of farmland. The pattern holds if we drop any one of these cities, and it holds if we instead take the five districts with the largest urban populations. One caution: the State Bank reports lending by district, and we have not confirmed whether that is where a loan was booked or where the land is. So this is the geography of recorded lending.

## Slide 9. Cost in context
*Hasnain · about 40 seconds · starts at 7:12*

Why does this matter? Cost. Published estimates put the implicit cost of arhti credit at 61.9 to 80.7 percent a year, against formal agricultural rates of 12.00 to 19.00 percent at the same time. These are not matched contracts, but the gap is large, which makes it notable that arhti credit persists right next to formal credit. The Punjab Kissan Card, an interest-free loan introduced in 2024, came after our data, and it initially required applicants to own land recorded in the provincial land records, which may leave tenants out.

## Slide 10. Robustness and the MAUP
*Hasnain · about 30 seconds · starts at 7:54*

We tested how robust this is. The clustering holds across five definitions of neighbours, with Moran's I between 0.470 and 0.568. Aggregation matters, as the modifiable areal unit problem predicts: at district level Moran's I falls to 0.429, and only one high-high and one low-low cluster survive the correction for multiple testing. Excluding the Cholistan desert villages hardly changes the results.

## Slide 11. Limits
*Hasnain · about 25 seconds · starts at 8:22*

Three limits. First, the census records whether a credit source is available, not whether anyone borrows. Second, our results are about places, not people: a village that reports both sources does not tell us that the same farmer uses both. Third, our sources come from different years, and we never treat them as the same moment.

## Slide 12. Conclusions
*Hasnain · about 75 seconds · starts at 8:48*

To conclude, three findings. First, arhti credit coexists with formal credit rather than filling its gaps: it clusters near grain markets, in the same places as formal credit. Second, formal lending is disproportionate: small holdings are in the records, 90.9 percent of them, but receive 37.0 percent of the money. Third, recorded lending is concentrated: five city districts record 59.6 percent of above-economic disbursement with 13.3 percent of the cultivated area. So our answer to the title is that the arhti does not begin where the bank ends; the two overlap. The sharpest contrasts in formal credit are not between places with and without it, but between small and large farms, and between where farms are and where loans are recorded. Reported availability alone is a poor guide to who receives formal money. The next steps are to confirm how the State Bank attributes loans, and to observe how farmers combine arhti, bank and Kissan Card credit. Thank you. We are happy to take questions.
