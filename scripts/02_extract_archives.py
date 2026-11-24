"""02_extract_archives.py: extract raw archives into data/interim/ (data/raw is never modified).

    .venv/bin/python -I scripts/02_extract_archives.py

- Mouza Census 2020 RAR (RAR5) is extracted with macOS's built-in bsdtar (libarchive >= 3.6 reads RAR5),
  so no Homebrew tool is needed. If bsdtar fails, install `unar` (`brew install unar`) and re-run.
- OCHA COD-AB shapefile zip is extracted with Python's zipfile.
Each target folder is wiped and re-created, so the script is safe to re-run.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
INTERIM = ROOT / "data" / "interim"

JOBS = [
    (RAW / "mouza_census_2020" / "mc2020.excel-1.rar", INTERIM / "mouza_census_2020_excel"),
    (RAW / "boundaries" / "pak_admin_boundaries.shp.zip", INTERIM / "boundaries_shp"),
]


def extract(archive: Path, out: Path) -> None:
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    if archive.suffix == ".zip":
        with zipfile.ZipFile(archive) as z:
            for m in z.namelist():  # refuse path traversal
                if m.startswith("/") or ".." in Path(m).parts:
                    raise ValueError(f"unsafe member in {archive.name}: {m}")
            z.extractall(out)
    elif archive.suffix == ".rar":
        tar = shutil.which("bsdtar") or shutil.which("tar")
        unar = shutil.which("unar")
        if tar and subprocess.run([tar, "-xf", str(archive), "-C", str(out)]).returncode == 0:
            pass
        elif unar:
            subprocess.run([unar, "-q", "-o", str(out), str(archive)], check=True)
        else:
            raise RuntimeError("Cannot extract RAR: run `brew install unar` and re-run this script.")
    else:
        raise ValueError(f"unknown archive type: {archive}")


def main() -> int:
    for archive, out in JOBS:
        if not archive.exists():
            print(f"[missing] {archive.relative_to(ROOT)} (run 01_download.py first)")
            continue
        extract(archive, out)
        files = sorted(p for p in out.rglob("*") if p.is_file())
        print(f"[ok] {archive.name} -> {out.relative_to(ROOT)} ({len(files)} files)")
        for p in files:
            print(f"      {p.stat().st_size:>12,d}  {p.relative_to(out)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
