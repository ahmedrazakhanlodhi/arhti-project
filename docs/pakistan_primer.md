# Pakistan primer for the group (one page)

*Draft, 2026-10-31. Items marked **[CHECK]** still need confirming against a source before this goes to the group.*

## Administrative units (largest → smallest)
**Province** (Punjab is the most populous) → **division** (a grouping of districts, mostly administrative) → **district**
(the main unit for government statistics and for SBP lending data; Punjab has 36 in the 2023 Census and OCHA boundaries)
→ **tehsil** (a sub-district, the revenue and administrative unit below the district; roughly 140–150 in Punjab
depending on source and year) → **mouza** (a *revenue estate*: the smallest unit with surveyed boundaries in the
land-revenue record. A mouza is a land unit, not a village. It may contain one settlement, several, or none). Rule of
thumb: district ≈ US county, tehsil ≈ township, mouza ≈ cadastral parcel block. **[CHECK]** the analogy, and whether to
mention the patwar circle / qanungo halqa layers between tehsil and mouza.

Units change over time. Punjab created or announced new districts after 2020 (e.g., Murree, Talagang, Wazirabad, Kot
Addu, Taunsa) **[CHECK which are in force and when]**. So a "district" in a 2020, 2023, 2024 or 2025 dataset may not be
the same polygon.

## Arhtis
An **arhti** (*aarhti*, commission agent) is a licensed intermediary in a grain or produce **mandi** (wholesale market).
Arhtis sell farmers' crops for a commission, and many also **advance cash or inputs** before harvest. The loan is then
repaid out of the crop sold through that same arhti. The interest is often implicit, built into commission, prices or
deductions, so it does not appear as a stated rate. Arhti credit is informal in the sense that SBP does not record it.
**[CHECK]** the licensing framework (Punjab Agricultural Produce Markets law) and whether to describe the tying as
typical or universal. In the Mouza Census, the published report labels this category **"Commission Agent / Arthi"**
(Table 8.1), while the Excel file's column header calls it **"Broker"**. Same code (8), verified by matching totals.

## Formal lenders
- **ZTBL (Zarai Taraqiati Bank Ltd)** is a state-owned specialised agricultural bank (formerly the Agricultural Development
  Bank of Pakistan). Its branches are mostly rural (in Punjab, 262 of its 292 branches are coded rural in the SBP list
  of Jun 2024). **[CHECK]** the current ownership and SBP classification wording.
- **Commercial banks** (HBL, NBP, MCB, UBL, Allied …) do much of the agricultural lending in volume. SBP sets annual
  indicative agri-credit targets for them. **[CHECK]** how binding these targets are.
- **Microfinance banks** (Khushhali, NRSP, U-Bank …) make small loans and are listed separately in the SBP branch file.
- Cooperative banks, NGOs, Rural Support Programmes (RSPs) and government schemes are also Mouza Census categories.

## SBP land-holding categories (farm sector)
From SBP's *Indicative Credit Limits… 2022-23* (CL1 Annex, Table 2.7), for **Punjab**:
**Subsistence holding** = up to 12.5 acres; **Economic holding** = 12.5 to 50 acres; **Above economic** = over 50 acres.
Thresholds differ by province (Sindh 16 / 64 acres; Balochistan 32 / 64 acres), and SBP says they derive from the
**Agricultural Census 2010**. The Ag Census 2024 size classes break at "under 12.5" and "under 50", so they line up
closely with SBP's categories, though SBP's "up to 12.5" vs the Census's "under 12.5" differ at the edge. **[CHECK]**
whether a borrower's category is based on land owned or land operated. The non-farm sector (livestock, poultry,
fisheries) uses separate "small / large farm" classes based on animals or birds, not acres.

## What each dataset does and does not measure
| Dataset | Measures | Does **not** measure |
|---|---|---|
| **Mouza Census 2020** (PBS, Jan–Mar 2020) | Whether each mouza *reports* that a credit source (ZTBL, commercial bank, arhti …) is available. It also reports whether facilities (bank branch, markets, roads) are in the mouza or how many km away. Answers come from enumerators and local key informants. | How many people borrow, loan amounts, interest rates, or who is excluded *within* a mouza. "Available" means the informant said it is available. It is not observed use. |
| **SBP district-wise credit FY2023-24** | Number of borrowers and amounts disbursed, recovered and outstanding, by district and holding category, for formal lenders. | Informal credit (arhtis, landlords, shopkeepers). Where the land is: data are recorded where the loan is **booked**, so a branch in a district HQ may serve borrowers from other districts. Unique farmers: borrower counts may double-count across banks. **[CHECK]** |
| **SBP branch list Jun 2024** | Every bank and MFB/DFI branch, with district, tehsil, city, locality text and a rural/urban flag. | Coordinates (none in the file, so mapping needs geocoding or aggregation by tehsil field), branch size, or lending. |
| **Agricultural Census 2024** (PBS, sample-based; ag year 2023-24) | Number of farms and farm area by size class and by tenure (owner, owner-cum-tenant, tenant), by district. | Tehsil or mouza detail. Sampling was designed at district level, so the numbers are estimates with error. It says nothing about credit. |
| **Population Census 2023** | Population (total / rural / urban), area and households by district and tehsil. | Anything agricultural or financial. |
| **OCHA COD-AB boundaries** (valid 2022-09-09) | District and tehsil polygons with p-codes. | Mouza boundaries, or districts and tehsils created after Sep 2022. Its names may not match PBS or SBP spellings. |

**Vintages differ:** Mouza Census (Jan–Mar 2020), SBP (FY2023-24), Ag Census (2023-24 ag year, enumerated 2024-25),
Census (2023), boundaries (2022). They must never be presented as one point in time.
