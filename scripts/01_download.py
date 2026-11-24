"""01_download.py: download raw source files into data/raw/.

Run from anywhere:
    .venv/bin/python -I scripts/01_download.py

Behaviour
- Each file goes to data/raw/<source_folder>/<filename>. Files that already exist are never overwritten
  (data/raw is read-only once populated). They are logged as "already present" and the script moves on.
- One attempt per URL plus at most one retry. No endless retrying.
- A response counts as a failure if the HTTP status is not 200, or if the server returned an HTML page
  (a block page or login wall) when a binary file was expected.
- Results are appended to docs/download_log.csv (date, URL, path, status, bytes, sha256).
- Failures are written to docs/manual_downloads.md with the URL and the exact save path.
- The OCHA COD-AB resource URL is resolved at run time from the HDX CKAN API, because HDX resource
  IDs change when the dataset is updated.
"""

from __future__ import annotations

import csv
import datetime as dt
import hashlib
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
DOCS = ROOT / "docs"
LOG_CSV = DOCS / "download_log.csv"
MANUAL_MD = DOCS / "manual_downloads.md"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    ),
    "Accept": "*/*",
}
TIMEOUT = (20, 180)  # connect, read (seconds)
MAX_ATTEMPTS = 2

# (dataset label, subfolder, url). The filename is taken from the URL.
# FALLBACKS: if the primary URL fails, try these same-institution mirrors (logged as "downloaded (fallback)").
FILES = [
    # Mouza Census 2020
    ("Mouza Census 2020: Punjab report", "mouza_census_2020",
     "https://www.pbs.gov.pk/wp-content/uploads/2020/07/mouza_census_2020_punjab_report.pdf"),
    ("Mouza Census 2020: Excel tables (RAR)", "mouza_census_2020",
     "https://www.pbs.gov.pk/wp-content/uploads/2020/07/mc2020.excel-1.rar"),
    # SBP agricultural credit and banking
    ("SBP district-wise agri credit detail FY2023-24", "sbp",
     "https://archive.sbp.org.pk/acd/DistrictWise-Detail-Jul-Jun-2024.xlsx"),
    ("SBP district-wise agri credit summary FY2023-24 (PDF)", "sbp",
     "https://archive.sbp.org.pk/acd/DWS-Jul-Jun-2024.pdf"),
    ("SBP CL1 Annex (2022)", "sbp",
     "https://www.sbp.org.pk/acd/2022/CL1-Annex.pdf"),
    ("SBP bank branches list, Jun 2024", "sbp",
     "https://www.sbp.org.pk/assets/document/publications/Bank-Branches-Jun-2024.xlsx"),
    # Agricultural Census 2024
    ("Agricultural Census 2024: Punjab report", "ag_census_2024",
     "https://www.pbs.gov.pk/wp-content/uploads/2020/07/IAC-Punjab-Report-25-05-2026-1.pdf"),
    ("Agricultural Census 2024: Table 1 (district)", "ag_census_2024",
     "https://www.pbs.gov.pk/wp-content/uploads/2020/07/Table_1_District.xls"),
    ("Agricultural Census 2024: Table 3 (district)", "ag_census_2024",
     "https://www.pbs.gov.pk/wp-content/uploads/2020/07/Table_3_District.xls"),
    # SBP Monthly Statistical Bulletin: Table 3.33, average rates of return on agricultural advances (added 2026-10-31, D039).
    # The September 2026 edition gives 2012-13 to 2024-25; the June 2024 edition is kept to check the 2012-13 values.
    ("SBP Monthly Statistical Bulletin, September 2026", "sbp_bulletin",
     "https://www.sbp.org.pk/assets/documents/bulletin/MSB_September_2026.pdf"),
    ("SBP Monthly Statistical Bulletin, June 2024", "sbp_bulletin",
     "https://archive.sbp.org.pk/reports/stat_reviews/Bulletin/2024/Jun/MSB-Jun-24.pdf"),
    # Population Census 2023. Link found on https://www.pbs.gov.pk/result-excel/ under
    # "Table-1 Area, population by sex, sex ratio, population density, urban proportion,
    #  household size and annual growth rate" -> Punjab -> District Wise.
    ("Population Census 2023: Table 1, Punjab districts", "pop_census_2023",
     "https://www.pbs.gov.pk/wp-content/uploads/2020/07/table_1_punjab_districts.xlsx"),
]

FALLBACKS = {
    # www.sbp.org.pk redirects this URL to a Cloudflare-blocked circular search page (403, Oct 2026);
    # SBP's own archive domain serves a PDF at the same path. Ahmed to verify it is the intended document.
    "https://www.sbp.org.pk/acd/2022/CL1-Annex.pdf": "https://archive.sbp.org.pk/acd/2022/CL1-Annex.pdf",
}

HDX_DATASET = "cod-ab-pak"
HDX_API = f"https://data.humdata.org/api/3/action/package_show?id={HDX_DATASET}"
HDX_WANTED_FORMATS = {"SHP", "XLSX"}  # boundaries shapefile + p-code gazetteer


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def looks_like_html(first_bytes: bytes) -> bool:
    head = first_bytes.lstrip()[:200].lower()
    return head.startswith(b"<!doctype html") or head.startswith(b"<html") or b"<head" in head


def download(url: str, dest: Path) -> tuple[str, int, str]:
    """Return (status, bytes, note). status in {"downloaded", "already present", "failed"}."""
    if dest.exists() and dest.stat().st_size > 0:
        return "already present", dest.stat().st_size, ""
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    note = ""
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            with requests.get(url, headers=HEADERS, timeout=TIMEOUT, stream=True,
                              allow_redirects=True) as r:
                if r.status_code != 200:
                    note = f"HTTP {r.status_code}"
                else:
                    with tmp.open("wb") as f:
                        for chunk in r.iter_content(1 << 16):
                            f.write(chunk)
                    with tmp.open("rb") as f:
                        first = f.read(512)
                    if looks_like_html(first) and not url.lower().endswith((".htm", ".html")):
                        note = "server returned an HTML page instead of the file (likely blocked)"
                        tmp.unlink(missing_ok=True)
                    elif tmp.stat().st_size == 0:
                        note = "empty response"
                        tmp.unlink(missing_ok=True)
                    else:
                        tmp.rename(dest)
                        return "downloaded", dest.stat().st_size, ""
        except requests.RequestException as e:
            note = f"{type(e).__name__}: {e}"[:300]
            tmp.unlink(missing_ok=True)
        if attempt < MAX_ATTEMPTS:
            time.sleep(3)
    return "failed", 0, note


def resolve_hdx() -> list[tuple[str, str, str]]:
    """Return FILES-style entries for the OCHA COD-AB resources, or an empty list (and a failure note)."""
    r = requests.get(HDX_API, headers=HEADERS, timeout=TIMEOUT)
    r.raise_for_status()
    res = r.json()["result"]
    out = []
    for item in res["resources"]:
        if (item.get("format") or "").upper() in HDX_WANTED_FORMATS:
            out.append((f"OCHA COD-AB Pakistan: {item['name']} (HDX modified {res.get('metadata_modified', '')[:10]})",
                        "boundaries", item["url"]))
    return out


def main() -> int:
    today = dt.date.today().isoformat()
    files = list(FILES)
    hdx_failure = None
    try:
        files += resolve_hdx()
    except Exception as e:  # noqa: BLE001 - we want to log any failure and continue
        hdx_failure = f"Could not query HDX API ({type(e).__name__}: {e})"

    rows, failures = [], []
    for label, sub, url in files:
        fname = url.rstrip("/").split("/")[-1].split("?")[0]
        dest = RAW / sub / fname
        status, nbytes, note = download(url, dest)
        if status == "failed" and url in FALLBACKS:
            primary_note = note
            status, nbytes, note = download(FALLBACKS[url], dest)
            if status != "failed":
                status = f"{status} (fallback)"
            note = f"primary failed ({primary_note}); fallback {FALLBACKS[url]}: {note or 'ok'}"
        digest = sha256(dest) if dest.exists() else ""
        rel = dest.relative_to(ROOT)
        print(f"[{status:15}] {nbytes:>12,d} B  {rel}  {note}")
        rows.append({"date": today, "dataset": label, "url": url, "path": str(rel),
                     "status": status, "bytes": nbytes, "sha256": digest, "note": note})
        if status == "failed":
            failures.append((label, url, dest, note))

    DOCS.mkdir(exist_ok=True)
    new_file = not LOG_CSV.exists()
    with LOG_CSV.open("a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        if new_file:
            w.writeheader()
        w.writerows(rows)

    lines = [
        "# Manual downloads needed",
        "",
        f"Written by `scripts/01_download.py` on {today}. Some government sites block automated downloads.",
        "Download each file below in a browser and save it at the exact path shown (create the folder if needed),",
        "then re-run `scripts/01_download.py`. It will log the file as \"already present\" and record its checksum.",
        "",
    ]
    if hdx_failure:
        lines += [f"- **OCHA COD-AB Pakistan boundaries.** {hdx_failure}. Go to https://data.humdata.org/dataset/cod-ab-pak,",
                  f"  download `pak_admin_boundaries.shp.zip` and `pak_admin_boundaries.xlsx`, and save both in",
                  f"  `{RAW / 'boundaries'}/`", ""]
    if not failures and not hdx_failure:
        lines.append("_None. All files downloaded automatically._")
    for label, url, dest, note in failures:
        lines += [f"- **{label}**", f"  - URL: {url}", f"  - Save as: `{dest}`", f"  - Reason: {note}", ""]
    MANUAL_MD.write_text("\n".join(lines) + "\n")

    print(f"\n{len(rows) - len(failures)} ok, {len(failures)} failed"
          + (" (+ HDX lookup failed)" if hdx_failure else ""))
    return 1 if failures or hdx_failure else 0


if __name__ == "__main__":
    sys.exit(main())
