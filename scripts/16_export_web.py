"""16_export_web.py: copy the layers and tables the Streamlit app needs into app/data/ (no new analysis).

    .venv/bin/python -I scripts/16_export_web.py

- Layers are read from the FULL GeoPackage geometries, reprojected to EPSG:4326 and simplified with shapely.coverage_simplify
  (shared edges stay shared) until each file is < 3 MB. Only the fields the app shows are kept; feature counts are asserted.
- Tables: key numbers, map classes, figure numbers, holding-class shares, crop structure, reporting geography, scorecard,
  concentration curve, SBP lending rates; docs/price_ladder.csv and notes.
- app/data/manifest.json: source, counts, SHA-256, timestamp, analysis CRS.
Nothing mouza-level is exported; no loan sizes; district amount-based columns only in AMOUNT_OK tables.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import re
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd
import shapely

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
GPKG = ROOT / "outputs" / "arhti_project.gpkg"
T = ROOT / "outputs" / "tables"
OUT = ROOT / "app" / "data"
MAX_BYTES = 3 * 1024 * 1024

LAYERS = {  # web name: (gpkg layer, expected features, first tolerance in degrees, fields kept)
    "tehsils": ("q1_tehsils_mouza_census_2020", 139, 0.0005,
                ["adm3_pcode", "adm3_name", "adm2_name", "rp_mouzas", "arhti_share", "commercial_share", "lisa_queen_p05",
                 "lisa_queen_fdr05", "bivariate_class", "contains_cholistan", "vintage"]),
    "districts": ("q2_districts_credit_allocation", 36, 0.0005,
                  ["adm2_pcode", "adm2_name", "small_farm_reach", "sub_borrowers", "small_farms", "flagged", "vintage"]),
    "provinces": ("context_pakistan_provinces", 7, 0.005, ["adm1_pcode", "adm1_name"]),
    "punjab_outline": ("context_punjab_outline", 1, 0.002, ["adm1_name"]),
}
TABLES = ["key_numbers.csv", "classification_comparison.csv", "figure_numbers.csv", "holding_class_shares.csv",
          "crop_structure_district.csv", "reporting_geography.csv", "district_scorecard.csv", "concentration_curve.csv",
          "concentration_coefficients.csv", "sbp_agri_lending_rates.csv"]
DOC_FILES = ["price_ladder.csv", "price_ladder_notes.md"]            # from docs/
# District AMOUNT-based columns (shares of disbursement, LQs, credit per acre) are allowed only in these two tables, which the app
# shows on the reporting-geography page (maps) and the district-profile page (labelled table values) (D039).
AMOUNT_OK = {"reporting_geography.csv", "district_scorecard.csv", "holding_class_shares.csv"}
FORBIDDEN = re.compile(r"avg_loan|mouza_(name|code|id)|mauza|vil_", re.I)
AMOUNT = re.compile(r"amount", re.I)


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def export_layer(web, layer, n_exp, tol0, fields) -> dict:
    g = gpd.read_file(GPKG, layer=layer)[fields + ["geometry"]].to_crs(4326)
    assert len(g) == n_exp, (layer, len(g), n_exp)
    assert not [c for c in g.columns if FORBIDDEN.search(c)], layer
    path = OUT / f"{web}.geojson"
    tried = []
    for tol in [tol0 * f for f in (1, 2, 4, 6, 10, 20)]:
        s = g.copy()
        s["geometry"] = shapely.set_precision(shapely.coverage_simplify(s.geometry.values, tolerance=tol), 1e-5)
        s.to_file(path, driver="GeoJSON", COORDINATE_PRECISION=5)
        size = path.stat().st_size
        tried.append([tol, size])
        if size < MAX_BYTES and s.geometry.notna().all() and (~s.geometry.is_empty).all():
            back = gpd.read_file(path)
            assert len(back) == n_exp, (web, len(back))
            return dict(file=path.name, source=f"outputs/arhti_project.gpkg | layer {layer}", features=len(back), bytes=size,
                        simplify_tolerance_deg=tol, crs="EPSG:4326", sha256=sha(path), fields=fields)
    sys.exit(f"{web}: could not get under 3 MB: {tried}")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    for p in OUT.iterdir():
        p.unlink()
    layers = [export_layer(w, *v) for w, v in LAYERS.items()]
    tables = []
    for f in TABLES:
        df = pd.read_csv(T / f)
        assert not [c for c in df.columns if FORBIDDEN.search(c)], f
        assert f in AMOUNT_OK or not [c for c in df.columns if AMOUNT.search(c)], f
        (OUT / f).write_bytes((T / f).read_bytes())
        tables.append(dict(file=f, source=f"outputs/tables/{f}", rows=len(df), bytes=(OUT / f).stat().st_size, sha256=sha(OUT / f)))
    for f in DOC_FILES:
        src = ROOT / "docs" / f
        (OUT / f).write_bytes(src.read_bytes())
        tables.append(dict(file=f, source=f"docs/{f}", rows=(len(pd.read_csv(src)) if f.endswith(".csv") else None),
                           bytes=(OUT / f).stat().st_size, sha256=sha(OUT / f)))
    for r in layers:
        print(f"{r['file']:24s} {r['features']:4d} features  {r['bytes'] / 1e6:5.2f} MB  tol={r['simplify_tolerance_deg']}")
    man = dict(generated=dt.datetime.now().isoformat(timespec="seconds"), written_by="scripts/16_export_web.py",
               analysis_crs=common.CRS, web_crs="EPSG:4326 (display copies; statistics were computed in the analysis CRS)",
               layers=layers, tables=tables)
    (OUT / "manifest.json").write_text(json.dumps(man, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
