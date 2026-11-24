<!-- Text for the "Data and methods" page. The app looks sections up by exact heading text. -->

## Presence
Where bank facilities physically are: whether a village has an online commercial-bank branch, or how many rural bank
branches there are per farm in a district. Presence is about buildings and distance.

## Availability
Whether a source of credit was reported as serving a village. In the Mouza Census 2020, the patwari and local respondents
said which sources (commercial banks, ZTBL, cooperatives, microfinance banks, arhtis) serve each mouza. We report the share of
a tehsil's rural populated mouzas that name each source. Availability is not borrowing: it says nothing about how many
households borrow, how much, or on what terms.

## Allocation
Who formal credit actually reaches. Small-farm reach counts subsistence-holding borrower records in SBP's FY2023-24 data per
1,000 farms under 12.5 acres in the Agricultural Census 2024, by district.

## How the analysis was built
Every step is a numbered Python script that runs from the downloaded source files to the final maps, tables and this app
(`run_all.sh`). Extracted numbers were checked against the published totals in each report; census tehsils were matched to
OCHA boundaries by code and name, and every non-exact match was reviewed by hand and logged. Spatial statistics were set up
before they were run (weights, permutations and random seed are stated with every result). Maps were built in QGIS and with
geopandas, matplotlib, libpysal and esda; the app uses Streamlit, Folium and Plotly. Values that need checking against the
printed sources are listed in the verification checklist on this page.

## Code
Code and data: AHMED: add the GitHub link.
