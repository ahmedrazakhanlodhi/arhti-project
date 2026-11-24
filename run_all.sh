#!/usr/bin/env bash
# run_all.sh: rebuild every output from raw data, in order.
# Usage (from anywhere):  bash run_all.sh            # full run (downloads only files that are missing)
#                         bash run_all.sh --from 04  # resume from script 04
set -euo pipefail
cd "$(dirname "$0")"

PY=".venv/bin/python"
if [[ ! -x "$PY" ]]; then
  echo "No .venv found. Create it first (Apple silicon, Python 3.11):"
  echo "  python3.11 -m venv .venv && .venv/bin/pip install -r requirements.txt"
  exit 1
fi

FROM="${2:-01}"
[[ "${1:-}" == "--from" ]] || FROM="01"

SCRIPTS=(
  01_download.py            # raw data → data/raw (network; skips files already present)
  02_extract_archives.py    # RAR / zip → data/interim
  03_inspect_raw.py         # docs/raw_inspection.md
  04_extract_mouza.py       # Mouza Census tehsil dataset + validation
  05_boundaries_join.py     # crosswalk, match audit, 95% gate, joined GeoPackage
  06_raster_context.py      # WorldCover cropland + MAP travel time (network on first run, ~1 GB)
  07_spatial_stats.py       # Moran's I, LISA, OLS / SEM (prespecified, D018)
  08_credit_allocation.py   # SBP × Ag Census district measures + screen (prespecified, D021)
  09_figures.py             # Figures 1–5, S1–S2, S4–S6 (matplotlib; PNG 300 dpi + PDF)
  10_export_qgis.py         # outputs/arhti_project.gpkg for QGIS
  11_literature_context.py  # CONTEXT only: published-study locations (geocoded), Fig S3, cluster-context table
)

run_py() {   # $1 = script file name; skipped when its number is below --from
  local n="${1:0:2}"
  if [[ "$n" < "$FROM" ]]; then return; fi
  echo "=== $1 ==="
  local start=$(date +%s)
  "$PY" -I "scripts/$1"
  echo "--- $1 done in $(( $(date +%s) - start )) s"
}
run_qgis() { # PyQGIS scripts run with QGIS's own Python; skipped if QGIS is not installed
  local n="${1:0:2}"
  if [[ "$n" < "$FROM" ]]; then return; fi
  if ls -d /Applications/QGIS*.app >/dev/null 2>&1; then
    echo "=== $1 (QGIS Python) ==="
    ( source scripts/qgis_env.sh && cd /tmp && "$QGIS_PY" -s "$OLDPWD/scripts/$1" ) 2>&1 \
      | grep -v -E "^ERROR 1: sqlite3|unable to open database|qt.qpa|PNG driver does not support|proj_uom_get_info" || true
  else
    echo "--- $1 skipped (QGIS not found); see docs/qgis_steps.md"
  fi
}

for s in "${SCRIPTS[@]}"; do run_py "$s"; done
run_qgis 12_qgis_project.py      # QGIS project + .qml styles
run_py   13_reporting_geography.py  # holding classes, crop structure, LQs, city summary, scorecard (D039)
run_py   14_cost_context.py      # SBP agricultural lending rates, price ladder, Figure P1 (context)
run_py   15_course_methods.py    # EXPLORATORY: weights sensitivity, Moran scatterplot, Gi*, trend surface, dissimilarity,
                                 #   k-means typology, Tissot indicatrix, classification histograms, dasymetric dots (D041)
run_qgis 16_qgis_layouts.py      # QGIS Print Layouts for Figures 2-6 -> outputs/figures/*_qgis.{png,pdf}
run_py   17_key_numbers.py       # every number used in text, app and slides, with source file and row
run_py   18_export_web.py        # simplified GeoJSON + tables + manifest for the Streamlit app (app/data/)
run_py   19_build_documents.py   # paper (.docx) and slides (.pptx) from docs/paper_draft.md and docs/slide_text.md
echo "All done. Review docs/match_audit.md, docs/validation_*.md and docs/crosswalk_manual*.csv."
