# Slide text

Numbers from `docs/key_numbers.md`; figures from `outputs/figures/`. `scripts/19_build_documents.py` builds the deck from this
file: each `## Slide` is one slide; `Headline:` is the takeaway line; `- ` lines are bullets; `Figures:` lists image files
(one or two per slide); `Notes:` is speaker notes.

## Slide 1. Where the Bank Ends and the Arhti Begins
Headline: Geographic access, landholding structure and the allocation of agricultural credit in Punjab, Pakistan
- Ahmed Raza Khan Lodhi and Hasnain Akram
- PPHA 38520, GIS Applications in the Social Sciences, University of Chicago, November 30, 2026
Figures: fig6_dasymetric_farms_borrowers_qgis.png
Notes: Two credit systems lend to Punjab's farmers: banks through branches, arhtis (commission agents) through grain markets. We ask where each reaches, and whom.

## Slide 2. Problem, thesis and hypotheses
Headline: Is agricultural finance organised around farms, or around markets and towns?
- Q1 (tehsils): is arhti credit reported where formal credit is weak, or where banks and markets already are?
- H1 gap-filling: arhti and bank credit negatively associated. H1-alt co-location: they cluster together with farmland.
- Q2 (districts): does formal credit reach small farms in proportion to their share of farms?
- H2 proportional reach (index of dissimilarity ≈ 0). H3 lending recorded in proportion to farmland (LQ ≈ 1).
- Thesis: finance follows markets and towns more than farms. Descriptive, not causal.
Notes: H1 and H2 tests were fixed before the analysis (decisions D018 and D021); everything else is labelled exploratory.

## Slide 3. What the literature says
Headline: Interlinked credit is old news; mapping it across a province is not
- Informal lenders tie credit to crop sales (Bell 1988; Aleem 1990: 78.7% average cost of informal borrowing near Chambar, Sindh).
- In Punjab the arhti is the largest informal source, working from 325 markets; implicit cost 62–80% by crop (Haq et al. 2013).
- Formal credit skews to large farms: 4% of households received 42% of formal loans (Khandker and Faruqee 2003).
- Bank geography matters (Burgess and Pande 2005; Mian 2006; Leyshon et al. 2008). Gap: no province-wide map of arhti credit.
Notes: Methods literature: Tobler 1970, Anselin 1995, Getis and Ord 1992, Openshaw 1984 (MAUP), Robinson 1950 (ecological fallacy), Duncan and Duncan 1955 (dissimilarity).

## Slide 4. Data and GIS workflow
Headline: Four sources, three vintages, one equal-area projection
- Mouza Census 2020: 23,130 rural populated mouzas → 137 tehsils (attribute join + dissolve; every non-exact match reviewed).
- SBP FY2023-24 borrower records and amounts by district and holding class; Agricultural Census 2024 farms, area, crops; branch list 30 Jun 2024.
- Rasters: WorldCover 2021 cropland (10 m → 100 m fraction, zonal statistics); MAP travel time (cost distance).
- Albers equal-area centred on Punjab (Tissot: 0.11° vs 29.68° max angular distortion in the old CRS). Ratios mapped, counts as dots.
Figures: figS11_tissot_indicatrix.png
Notes: Levels of measurement: shares and rates are ratio data (choropleths); LISA and Gi* classes are nominal; bivariate classes ordinal.

## Slide 5. H1: arhti credit is strongly clustered
Headline: Moran's I = 0.536; 25 High-High and 32 Low-Low tehsils
- 31.5% of rural populated mouzas report arhti credit; tehsil shares run from 0% to 100%.
- High-High: Sheikhupura–Gujranwala–Sialkot belt and Bahawalnagar; Low-Low: Rawalpindi, Attock, Jhelum, Chakwal.
- Gi* finds the same hot and cold spots (28 and 33); trend-surface residuals still cluster (I = 0.234).
Figures: fig2_arhti_share_tehsil_qgis.png, fig4_lisa_arhti_tehsil_qgis.png
Notes: Queen contiguity, row-standardised; 999 permutations, seed 20261031; FDR survivors 15 and 17 (Benjamini–Hochberg cutoff 0.0117).

## Slide 6. H1 test: gap-filling is rejected
Headline: Arhti credit is reported alongside bank credit, not in its gaps
- Bivariate Moran's I = 0.112 (p = 0.062): weak, and not negative.
- Within tehsils, odds ratio 1.18 (95% CI 1.09–1.27): bank-credit villages slightly more likely to report arhti credit.
- Varies across tehsils (Breslow–Day p < 0.001): 67 above independence, 53 below.
- Arhti availability is higher where land is cropland (ρ = 0.49) and less even than bank credit (D = 0.380 vs 0.234).
Figures: fig3_bivariate_arhti_commercial_qgis.png
Notes: Co-reporting in a village is about availability, not about which source a farmer uses.

## Slide 7. H2: reach by count, not by amount
Headline: Small holdings: 94.1% of farms, 91.9% of borrower records, 35.9% of disbursement
- Above-economic holdings (> 50 acres): 0.5% of farms, 49.4% of disbursement.
- Small-farm reach ranges from 21.6 to 299.0 records per 1,000 small farms (median 118.5); clustered (I = 0.532).
- Dissimilarity between borrower records and small farms across districts: D = 0.216.
Figures: fig5_small_farm_reach_qgis.png, fig6_dasymetric_farms_borrowers_qgis.png
Notes: Dasymetric dots: 1 dot = 1,000 farms under 12.5 acres, placed only on cropland. Circles: borrower records with Flannery compensation.

## Slide 8. H3: lending is recorded in city districts
Headline: Five city districts: 59.6% of above-economic disbursement, 13.3% of cultivated area
- Location quotient for above-economic lending: Lahore 14.06, Rawalpindi 7.44, Chakwal 0.09.
- Same five districts: 43.5% of all bank branches but 19.1% of rural branches.
- District = as reported by SBP (attribution under verification): booking place may differ from where the land is.
Figures: figR1_lq_maps.png

## Slide 9. Cost in context
Headline: Published arhti cost estimates sit far above formal rates
- IGC 2013: implicit arhti cost 61.9%–80.7% by crop vs SBP FY2012-13 averages of 12.00–19.00%.
- FY2023-24 formal averages 20.67%–29.42%. Kissan Card (0%, up to 12.5 acres) began after the data period.
Figures: figP1_price_ladder.png
Notes: Orders of magnitude, not matched contracts; small, non-representative studies.

## Slide 10. Robustness and the MAUP
Headline: Clustering survives every weighting scheme; aggregation weakens it
- Moran's I: Queen/Rook 0.536, kNN-5 0.568, 73.6 km band 0.470, inverse distance 0.491 (all p = 0.001).
- Scale effect: 35 districts → I = 0.429; only 1 High-High and 1 Low-Low cluster survive FDR.
- Zoning effect: excluding Cholistan desert mouzas → I = 0.543, odds ratio 1.20.
Figures: figS7_moran_scatterplot.png

## Slide 11. Limits
Headline: Availability is not borrowing; districts are not farmers
- Mouza Census reports availability, not household borrowing. Borrower records may not be unique people.
- Ecological fallacy: area associations need not hold for the farmers in them.
- Different vintages (2020, FY2023-24, 2024); SBP district attribution under verification; 36 pre-split districts.

## Slide 12. Conclusions
Headline: Finance follows markets and towns more than farms
- H1 rejected: arhti credit clusters with cropland and alongside bank credit.
- H2 rejected: reach by count, not by amount, and uneven across districts.
- H3 rejected for large holdings: lending recorded in a few city districts.
- Next: confirm SBP attribution; observe how farmers combine arhti, bank and Kissan Card credit.
