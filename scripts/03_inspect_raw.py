"""03_inspect_raw.py: describe every raw/extracted file. Read-only; writes docs/raw_inspection.md.

    .venv/bin/python -I scripts/03_inspect_raw.py

- Excel: every sheet's dimensions and its first N rows read with header=None, so the true header rows are visible.
- PDF: page count and the first lines of text on page 1.
- Shapefiles: feature count, CRS, and field names for each layer.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import pdfplumber
import pyogrio

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
INTERIM = ROOT / "data" / "interim"
OUT = ROOT / "docs" / "raw_inspection.md"
N_ROWS = 12  # enough to show multi-row headers plus ~5 data rows

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 40)
pd.set_option("display.max_colwidth", 28)


def excel_section(path: Path) -> list[str]:
    engine = "xlrd" if path.suffix == ".xls" else "openpyxl"
    lines = [f"## {path.relative_to(ROOT)}", ""]
    xl = pd.ExcelFile(path, engine=engine)
    lines.append(f"Sheets ({len(xl.sheet_names)}): {xl.sheet_names}")
    lines.append("")
    for sh in xl.sheet_names:
        df = pd.read_excel(xl, sheet_name=sh, header=None, nrows=N_ROWS, dtype=str)
        if engine == "openpyxl":
            ws = xl.book[sh]
            dims = f"{ws.max_row} rows x {ws.max_column} cols"
        else:
            ws = xl.book.sheet_by_name(sh)
            dims = f"{ws.nrows} rows x {ws.ncols} cols"
        lines += [f"### Sheet `{sh}` ({dims})", "", "```",
                  df.dropna(how="all", axis=1).fillna("").to_string(), "```", ""]
    return lines


def pdf_section(path: Path) -> list[str]:
    with pdfplumber.open(path) as pdf:
        n = len(pdf.pages)
        txt = (pdf.pages[0].extract_text() or "").strip().splitlines()[:12]
    return [f"## {path.relative_to(ROOT)}", "", f"Pages: **{n}**", "", "Page 1 text (first lines):", "```",
            *txt, "```", ""]


def shp_section(folder: Path) -> list[str]:
    lines = [f"## {folder.relative_to(ROOT)} (shapefiles)", ""]
    for shp in sorted(folder.glob("*.shp")):
        info = pyogrio.read_info(shp)
        lines.append(f"- `{shp.name}`: {info['features']} features, {info['geometry_type']}, "
                     f"CRS {info['crs']}; fields: {', '.join(info['fields'])}")
    return lines + [""]


def main() -> int:
    out = ["# Raw data inspection", "", "Written by `scripts/03_inspect_raw.py`. Rows read with header=None; "
           "row index 0 = first spreadsheet row.", ""]
    files = sorted(RAW.rglob("*")) + sorted(INTERIM.rglob("*.xlsx"))
    for p in files:
        if not p.is_file():
            continue
        print("inspecting", p.relative_to(ROOT), flush=True)
        try:
            if p.suffix in (".xls", ".xlsx"):
                out += excel_section(p)
            elif p.suffix == ".pdf":
                out += pdf_section(p)
        except Exception as e:  # noqa: BLE001
            out += [f"## {p.relative_to(ROOT)}", "", f"**Could not read:** {type(e).__name__}: {e}", ""]
    shp_dir = INTERIM / "boundaries_shp"
    if shp_dir.exists():
        out += shp_section(shp_dir)
    OUT.write_text("\n".join(out) + "\n")
    print("wrote", OUT.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
