# Speaker script: Where the Bank Ends and the Arhti Begins

12 slides · 1,310 words · about 10.1 minutes at 130 words per minute. Built from the Notes in `docs/slide_text.md` by `scripts/19_build_documents.py`; the same text is in the deck's speaker notes.

## Slide 1. Where the Bank Ends and the Arhti Begins
*Ahmed · about 75 seconds · starts at 0:00*

Good afternoon. I'm Ahmed Raza Khan Lodhi, and this is joint work with Hasnain Akram. Let me start with a puzzle. One of us spent years supervising banks in Pakistan and kept meeting the same arrangement. A farmer takes a bag of fertilizer worth 3,000 rupees from an arhti, the commission agent who sells his crop, and owes 4,000 at harvest. Then he sells the crop to the same arhti. Walk him through the arithmetic and he is not troubled: his father and grandfather borrowed from the same family, and the arhti was there for every wedding. The bank, meanwhile, promises five days, but only once the paperwork is complete, and that can take months. The bank starts counting time when the documents are ready. The farmer starts counting time when the rain arrives. So our question is: where does each system reach, and whom? The map behind me shows small farms as dots and small-farm borrower records as circles.

## Slide 2. Problem, thesis and hypotheses
*Ahmed · about 40 seconds · starts at 1:13*

We ask two questions. Across tehsils: is arhti credit found where formal credit is missing, or where banks, markets and farmland already are? If arhtis fill the gaps banks leave, the two should be negatively associated; that is our gap-filling hypothesis. Across districts: does formal credit reach small farms in proportion to their number? A third, exploratory question asks whether lending is recorded where the farmland is. The main tests were fixed before we ran them, and everything is descriptive: associations between places, not effects.

## Slide 3. What the literature says
*Ahmed · about 45 seconds · starts at 1:53*

The story is not only ours. A study for the International Growth Centre found that nearly all the farmers it interviewed in Punjab had bank accounts, yet kept borrowing from arhtis, at an implicit 62 to 80 percent a year against bank rates of 9 to 18. Lenders who tie credit to the crop are well documented: Aleem found informal credit near Chambar cost 78.7 percent a year, close to the lenders' own costs. On the formal side, 4 percent of rural households once received 42 percent of formal loans. What was missing is a province-wide map, village by village.

## Slide 4. Data and GIS workflow
*Ahmed · about 45 seconds · starts at 2:39*

We combine four public datasets. The Mouza Census of 2020 reports, for each of 23,130 rural villages, which credit sources are available; we joined them to 137 tehsils and checked every inexact match by hand. The State Bank gives lending for FY2023-24 by district and farm size, and the Agricultural Census of 2024 gives farms and land. We add satellite cropland and travel time to cities. One GIS choice mattered: our first projection was centred far to the east and twisted Punjab, as the Tissot circles show, so we use an equal-area projection centred on Punjab.

## Slide 5. H1: arhti credit is strongly clustered
*Ahmed · about 35 seconds · starts at 3:23*

First result. Arhti credit is reported in 31.5 percent of rural villages, but it is far from even. Global Moran's I is 0.536, strong clustering. The cluster map shows where: a high-high belt from Sheikhupura through Gujranwala to Sialkot, and in Bahawalnagar, and a low-low block in Rawalpindi, Attock, Jhelum and Chakwal; 25 high-high and 32 low-low tehsils in all. A Getis-Ord hot-spot analysis finds the same places, and the clustering remains after removing any smooth province-wide trend.

## Slide 6. H1: the arhti is not simply a substitute for the bank
*Ahmed · about 75 seconds · starts at 3:59*

Now the test of gap-filling. If arhtis filled the gaps banks leave, the villages without banks would be the ones with arhtis. That is not what we find. Within the same tehsil, the odds that a village reports arhti credit are higher where commercial-bank credit is reported, an odds ratio of 1.18, and higher still for the cooperative bank and microfinance banks, 1.72 and 1.76. For ZTBL and for formal credit as a whole, the result is inconclusive. No formal source shows a significant negative association; 79.9 percent of villages that report arhti credit also report a formal source, though formal credit is common everywhere: 75.9 percent of the other villages report one too. What does go with arhti credit is closeness to markets: in a spatial error model, one standard deviation more villages within 10 kilometres of a grain market goes with 5.5 percentage points more arhti availability. The maps show market access and the 3,810 villages that report neither source.

## Slide 7. H2: counting borrowers is not the same as counting rupees
*Hasnain · about 55 seconds · starts at 5:14*

Thank you, Ahmed. I'm Hasnain Akram, and I'll take the second question: whom formal credit reaches. Across Punjab's 36 districts, holdings under 12.5 acres are 94.2 percent of farms. They hold 90.9 percent of borrower records, close to their share, but receive only 37.0 percent of the money. Per borrower record, a subsistence holding receives about 0.52 million rupees and an above-economic holding about 50.62 million, roughly 97 times as much. Across districts the picture is uneven too: the index of dissimilarity between borrower records and small farms is 0.216, so about a fifth of the records would have to move district to match where small farms are. So formal lending is disproportionate: small farms are in the records, but not in the money.

## Slide 8. H3: where is agricultural lending recorded?
*Hasnain · about 50 seconds · starts at 6:11*

Our third, exploratory question is where lending is recorded. Five city districts, Lahore, Rawalpindi, Multan, Faisalabad and Rahim Yar Khan, record 59.6 percent of large-farm lending but hold only 13.3 percent of cultivated land. Lahore's location quotient for large holdings is 14.06: about fourteen times its share of farmland. The pattern holds if we drop any one of these cities, and it holds if we instead take the five districts with the largest urban populations. One caution: the State Bank reports lending by district, and we have not confirmed whether that is where a loan was booked or where the land is. So this is the geography of recorded lending.

## Slide 9. The economics of an expensive loan
*Hasnain · about 55 seconds · starts at 7:02*

So why pay so much more? Published estimates put the implicit cost of arhti credit at 61.9 to 80.7 percent a year, against formal rates of 12.00 to 19.00 percent at the time. The literature and our own observations suggest what the farmer is buying: credit tied to the sale of his crop, no collateral, repayment that can wait for a better harvest, and a lender who knows him. For farmers who object to interest, a higher deferred price for fertilizer is permissible trade. The same relationship can also tie the farmer to one buyer. Punjab's interest-free Kissan Card came after our data, and it initially required land in the applicant's name, which may leave tenants out.

## Slide 10. Robustness and the MAUP
*Hasnain · about 30 seconds · starts at 7:56*

We tested how robust this is. The clustering holds across five definitions of neighbours, with Moran's I between 0.470 and 0.568. Aggregation matters, as the modifiable areal unit problem predicts: at district level Moran's I falls to 0.429, and only one high-high and one low-low cluster survive the correction for multiple testing. Excluding the Cholistan desert villages hardly changes anything.

## Slide 11. Limits
*Hasnain · about 30 seconds · starts at 8:24*

Three limits. First, the census records whether a credit source is available, not whether anyone borrows. Second, our results are about places, not people: a village that reports both sources does not tell us that the same farmer uses both. Third, our sources come from different years, and we never treat them as the same moment. And the opening story is one person's professional experience, not a sample.

## Slide 12. Conclusions
*Hasnain · about 70 seconds · starts at 8:55*

To conclude, three findings. First, arhti credit coexists with formal credit rather than filling its gaps: it clusters near grain markets. Second, formal lending is disproportionate: small holdings are 90.9 percent of borrower records but receive 37.0 percent of the money. Third, recorded lending is concentrated: five city districts record 59.6 percent of above-economic disbursement with 13.3 percent of the cultivated area. So the arhti does not begin where the bank ends. Remember the farmer with the fertilizer: he was not comparing two loans. He was comparing a bank product with a relationship built on trust, flexible repayment and, for many, a contract they see as permissible. The test of financial inclusion is not how many branches a regulator can count, but whether that farmer has a credible alternative when the arhti sets the terms. Next: how the State Bank attributes loans, and how farmers combine their sources. Thank you.
