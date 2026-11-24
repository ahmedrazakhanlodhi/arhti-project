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
Headline: Does arhti credit fill the gaps banks leave, and does formal credit reach small farms?
- Q1 (tehsils): is arhti credit reported where formal credit is weak, or where formal credit, markets and farmland already are?
- H1 gap-filling: arhti and formal credit negatively associated. H1-alt coexistence: they appear together, near markets.
- Q2 (districts): does formal credit reach small farms in proportion to their share of farms?
- H2 proportional reach (index of dissimilarity near 0). H3 (exploratory): lending recorded where farmland is (LQ near 1).
- Thesis: arhti credit clusters near grain markets; its link to formal credit varies by institution and place. Descriptive, not causal.
Notes: H1 and H2 tests were fixed before the analysis; everything else is exploratory. Proportionality is a benchmark, not an optimum.

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

## Slide 6. H1 test: no significant negative association with any formal source
Headline: Arhti credit appears alongside commercial, cooperative and microfinance credit; ZTBL and all-formal results inconclusive
- Within tehsils, odds ratios: commercial 1.18, cooperative 1.72, microfinance 1.76 (adjusted p < 0.001); ZTBL 0.98, any formal 0.95.
- Arhti availability is higher where more villages have a grain market within 10 km (ρ = 0.336) or 25 km (ρ = 0.377); holds in the spatial error model.
- Cropland's link (ρ = 0.49) does not survive spatial error modelling.
- 79.9% of arhti-reporting mouzas also report a formal source; 3,810 of 23,130 mouzas report neither.
Figures: fig7_markets_neither_tehsil_qgis.png
Notes: Odds ratios compare odds, not probabilities. Large heterogeneity across tehsils (Breslow–Day p < 0.001): 67 above independence, 53 below. Co-reporting is about availability, not which source a farmer uses.

## Slide 7. H2: in proportion by count, not by amount
Headline: 36 districts: small holdings are 94.2% of farms, 90.9% of borrower records, 37.0% of disbursement
- Rs 0.52 million per borrower record for subsistence holdings vs Rs 50.62 million for above-economic holdings.
- Above-economic holdings: 2.35 times their farm share in records, 92.11 times in disbursement.
- Borrower records vs small farms across districts: D = 0.216 (0.182 without flagged districts).
Figures: fig5_small_farm_reach_qgis.png, fig6_dasymetric_farms_borrowers_qgis.png
Notes: 36 district rows, banks only; the 74,494 microfinance records have no district. Census class areas below 12.5 acres are inconsistent, so we rely on farm counts.

## Slide 8. H3: lending is recorded in city districts
Headline: Five city districts: 59.6% of above-economic disbursement, 13.3% of cultivated area
- Location quotient for above-economic lending: Lahore 14.06, Rawalpindi 7.44, Chakwal 0.09.
- Leave any one city out: still 4.41 to 5.65 times its area share. Five most urban districts (2023 census): 43.5% with 11.2% of area.
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
Headline: Where the bank ends, the arhti has not simply begun: the two overlap
- H1 not supported: arhti credit clusters near markets and alongside formal credit; no significant negative association.
- H2 not supported: in proportion by count, not by amount, and uneven across districts.
- H3 not supported: lending recorded in a few city districts, robust to dropping any one of them.
- Next: confirm SBP attribution and counting rules; observe how farmers combine arhti, bank and Kissan Card credit.
