# Where the Bank Ends and the Arhti Begins

The geography of arhti credit in rural Punjab, Pakistan. PPHA 38520 (GIS Applications in the Social Sciences), University of
Chicago. Ahmed Raza Khan Lodhi and Hasnain Akram. **Descriptive, not causal.**

**Main question:** Where is arhti credit available in rural Punjab, and how does its geography compare with formal banking?
Main analysis: Mouza Census 2020, 137 rural tehsils. Second lens (separate dataset and period): SBP FY2023-24 lending
records and the Agricultural Census 2024, 36 districts.

## Read first
| File | Contents |
|---|---|
| `docs/paper_draft.md` | The paper |
| `docs/slide_text.md` | Presentation text |
| `docs/key_numbers.md` | Every number used in the paper, app and slides, with its source file and row |
| `docs/paper_outline.md` | Structure of the paper and appendix |
| `docs/project_rules.md` | Data, language and mapping rules for the project |

## Reproduce everything
Python 3.11 (native arm64 on Apple silicon), internet for the first run (~1 GB of rasters). Optional: QGIS; if present,
`run_all.sh` also builds the styled QGIS project.
```bash
python3.11 -m venv .venv
.venv/bin/pip install -r requirements.txt
bash run_all.sh                     # or: bash run_all.sh --from 09   to resume
.venv/bin/python -I -m pytest tests -q
```
Scripts are numbered in run order (`scripts/01_download.py` … `scripts/16_export_web.py`) and never modify `data/raw/`.

## App
`.venv/bin/streamlit run app/app.py` (add `?present=1` for presentation mode). Seven pages (Overview, Access, Allocation, Reporting geography, Cost, District profiles, Data and methods); it displays finished outputs only
(`app/data/`, written by `scripts/16_export_web.py`). Text: `app/content/`. Deployment: `docs/deploy.md`. Screenshots:
`docs/app_screenshots/`.

## Figures
| Figure | File | Where |
|---|---|---|
| 1. Study area and matching to boundaries | `fig1_study_area_coverage` | Data and methods |
| 2. Arhti credit availability by tehsil | `fig2_arhti_share_tehsil` | Result 1 |
| 3. Bivariate map, arhti × commercial-bank credit availability | `fig3_bivariate_arhti_commercial` | Result 3 |
| 4. LISA clusters of arhti credit availability | `fig4_lisa_arhti_tehsil` | Result 2 |
| 5. Small-farm reach by district, with the province headline | `fig5_small_farm_reach` | Result 4 |
| S1–S6. Classification comparison; district LISA; published-study locations (context); village-level co-reporting (exploratory); three-panel Figure 5; concentration curve | `figS1_…` – `figS6_…` | Appendix |

## Other documents
`docs/methods_appendix.md` (methods), `docs/decisions.md` (every data and geography decision), `docs/variable_dictionary.md`,
`docs/validation_mouza.md`, `docs/validation_sbp.md`, `docs/match_audit.md` (checks against published figures),
`docs/human_checklist.md` (values to verify by hand), `docs/data_inventory.md` (sources and links), `docs/figure_numbers.md`.

## Data vintages (never contemporaneous)
Mouza Census Jan–Mar 2020 · SBP FY2023-24 (by loan-booking district) · Agricultural Census 2024 (sample-based) ·
ESA WorldCover 2021 · MAP travel time to cities 2015 · OCHA boundaries valid 2022-09-09.
