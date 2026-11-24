# Where the Bank Ends and the Arhti Begins

The geography of arhti credit in rural Punjab, Pakistan. PPHA 38520 (GIS Applications in the Social Sciences), University of
Chicago. Ahmed Raza Khan Lodhi and Hasnain Akram. **Descriptive, not causal.**

**Thesis:** agricultural credit in Punjab has distinct and overlapping geographies. Arhti credit clusters near grain markets
and is reported alongside formal credit rather than in its gaps (H1, gap-filling: not supported); formal credit reaches small
farms in proportion by count but not by amount (H2, proportional reach: not supported); recorded lending concentrates in a few
city districts, above all for large holdings (H3: not supported). Data: Mouza Census 2020 (137 rural tehsils); SBP FY2023-24
lending records and the Agricultural Census 2024 (36 districts); separate datasets and periods, never treated as contemporaneous.

## Deliverables
| File | Contents |
|---|---|
| `outputs/paper/arhti_paper.docx` | The paper (built from `docs/paper_draft.md` by `scripts/19_build_documents.py`) |
| `outputs/slides/arhti_slides.pptx` | Presentation, Nov 30 (built from `docs/slide_text.md`; speaker notes included) |
| `outputs/arhti_project.qgz` | QGIS project: every layer styled, plus Print Layouts for Figures 2–6 (Project → Layout Manager) |

## Read first
| File | Contents |
|---|---|
| `docs/paper_draft.md` | The paper text |
| `docs/references.md` | References, with what each one supports |
| `docs/key_numbers.md` | Every number used in the paper, app and slides, with its source file and row |
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
Scripts are numbered in run order (`scripts/01_download.py` … `scripts/19_build_documents.py`) and never modify `data/raw/`.
Scripts 12 and 16 run with QGIS's own Python (`run_all.sh` does this automatically when QGIS is in `/Applications`).

## App
`.venv/bin/streamlit run app/app.py` (add `?present=1` for presentation mode). Seven pages (Overview, Access, Allocation, Reporting geography, Cost, District profiles, Data and methods); it displays finished outputs only
(`app/data/`, written by `scripts/18_export_web.py`). Text: `app/content/`. Deployment: `docs/deploy.md`. Screenshots:
`docs/app_screenshots/`.

## Figures
Main maps are QGIS Print Layouts (`*_qgis.png/pdf`, `scripts/16_qgis_layouts.py`); charts and appendix maps are matplotlib.

| Figure | File | Where |
|---|---|---|
| 1. Study area and matching to boundaries | `fig1_study_area_coverage` | Data and methods |
| 2. Arhti credit availability by tehsil | `fig2_arhti_share_tehsil_qgis` | H1 |
| 3. Bivariate map, arhti × commercial-bank credit availability | `fig3_bivariate_arhti_commercial_qgis` | H1 test |
| 4. LISA clusters of arhti credit availability | `fig4_lisa_arhti_tehsil_qgis` | H1 |
| 5. Small-farm reach by district | `fig5_small_farm_reach_qgis` | H2 |
| 6. Dasymetric dots of small farms and proportional circles of borrower records | `fig6_dasymetric_farms_borrowers_qgis` | H2 |
| A1, R1, P1. Holding-class shares; location quotients; price ladder | `figA1_…`, `figR1_…`, `figP1_…` | H2, H3, cost |
| S1–S13. Classification comparison; district LISA; published-study locations (context); village co-reporting; three-panel Figure 5; concentration curve; Moran scatterplot; Gi*; trend surface; k-means typology; Tissot indicatrix; classification histograms; mouzas reporting neither source | `figS1_…` – `figS13_…` | Appendix |

## Other documents
`docs/methods_appendix.md` (methods), `docs/decisions.md` (every data and geography decision), `docs/variable_dictionary.md`,
`docs/validation_mouza.md`, `docs/validation_sbp.md`, `docs/match_audit.md` (checks against published figures),
`docs/human_checklist.md` (values to verify by hand), `docs/data_inventory.md` (sources and links), `docs/figure_numbers.md`,
`docs/qgis_steps.md` (the QGIS GUI steps behind each layout).

## Data vintages (never contemporaneous)
Mouza Census Jan–Mar 2020 · SBP FY2023-24 (by loan-booking district) · Agricultural Census 2024 (sample-based) ·
ESA WorldCover 2021 · MAP travel time to cities 2015 · OCHA boundaries valid 2022-09-09.
