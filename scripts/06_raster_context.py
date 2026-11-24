"""06_raster_context.py: cropland share and modelled travel time to the nearest city, per district and tehsil.

    .venv/bin/python -I scripts/06_raster_context.py      (after 05_boundaries_join.py)

Sources (downloaded to data/raw/, never modified)
- ESA WorldCover 10 m 2021 v200 (Zanaga et al. 2022, doi:10.5281/zenodo.7254221). Zenodo only offers 60-degree
  macrotile zips (~27 GB for Punjab's two macrotiles), so the identical v200 3x3-degree tiles are taken from ESA's
  official public AWS bucket (esa-worldcover.s3.eu-central-1.amazonaws.com/v200/2021/map/). Only the 7 tiles
  intersecting Punjab are downloaded.
- Malaria Atlas Project, Accessibility to Cities 2015 (Weiss et al. 2018, Nature, doi:10.1038/nature25181). A clipped
  GeoTIFF (69-76E, 27-35N) is requested from MAP's public GeoServer WCS (coverage
  Accessibility__201501_Global_Travel_Time_to_Cities; the same server the malariaAtlas R package uses). No login.

Method (all in the rasters' native EPSG:4326 grids; only the vector polygons are reprojected)
1. WorldCover 10 m (1/12000 deg): cropland = class 40; valid = class != 0 (no data). Counted in 10x10 blocks →
   cropland fraction on a 1/1200-deg grid (~93 m N-S x ~80 m E-W at 30N). This is average resampling of the
   binary mask, done block-wise BEFORE any zonal statistics.
2. cropland_share per polygon = mean of the ~100 m fraction over cells whose centre lies in the polygon.
3. Travel time (1/120 deg, ~1 km, minutes). Cropland weight per 1 km cell = mean of the 10x10 ~100 m fraction cells
   it contains (grids nest exactly, so there is no resampling ambiguity). Per polygon (cell centre in polygon):
   unweighted mean and median, and cropland-weighted mean and median (weights = cropland fraction).
Outputs: data/interim/worldcover_cropland_frac_1200.tif, data/interim/cropland_frac_120.tif,
data/processed/raster_context_{district,tehsil}.csv, data/processed/punjab_credit_context.gpkg (layers district, tehsil = Cholistan
option A; district_optB, tehsil_optB = option B), docs/raster_context_run.md
"""

from __future__ import annotations

import csv
import datetime as dt
import hashlib
import math
import sys
import time
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
import requests
from rasterio.features import rasterize
from rasterio.transform import from_origin
from rasterio.windows import Window
from shapely.geometry import box

ROOT = Path(__file__).resolve().parents[1]
RAW_WC = ROOT / "data" / "raw" / "worldcover"
RAW_TT = ROOT / "data" / "raw" / "accessibility" / "MAP_2015_travel_time_to_cities_69E76E_27N35N.tif"
IN_GPKG = ROOT / "data" / "processed" / "punjab_tehsil_credit.gpkg"
OUT_GPKG = ROOT / "data" / "processed" / "punjab_credit_context.gpkg"
FRAC100 = ROOT / "data" / "interim" / "worldcover_cropland_frac_1200.tif"
FRAC1K = ROOT / "data" / "interim" / "cropland_frac_120.tif"
LOG_CSV = ROOT / "docs" / "download_log.csv"
RUN_MD = ROOT / "docs" / "raster_context_run.md"

WC_URL = "https://esa-worldcover.s3.eu-central-1.amazonaws.com/v200/2021/map/ESA_WorldCover_10m_2021_v200_{t}_Map.tif"
TT_URL = ("https://data.malariaatlas.org/geoserver/ows?service=WCS&version=2.0.1&request=GetCoverage"
          "&CoverageId=Accessibility__201501_Global_Travel_Time_to_Cities&format=image/geotiff"
          "&subset=Long(69,76)&subset=Lat(27,35)")
CROPLAND = 40
WC_RES = 1 / 12000          # WorldCover pixel (deg)
AGG = 10                    # 10x10 → 1/1200 deg (~100 m)
TT_RES = 1 / 120            # travel-time pixel (deg)
CHUNK = 1200                # 10 m rows per read (multiple of AGG)
WC_VINTAGE = "ESA WorldCover 2021 v200 (10 m)"
TT_VINTAGE = "MAP Accessibility to Cities, nominal year 2015 (~1 km)"


def log_download(label, url, path, status, note=""):
    h = hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else ""
    row = dict(date=dt.date.today().isoformat(), dataset=label, url=url, path=str(path.relative_to(ROOT)),
               status=status, bytes=path.stat().st_size if path.exists() else 0, sha256=h, note=note)
    new = not LOG_CSV.exists()
    with LOG_CSV.open("a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(row))
        if new:
            w.writeheader()
        w.writerow(row)


def fetch(url, dest, label):
    if dest.exists() and dest.stat().st_size > 0:
        return "already present"
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(".part")
    for attempt in (1, 2):
        try:
            with requests.get(url, stream=True, timeout=(20, 300)) as r:
                r.raise_for_status()
                with tmp.open("wb") as f:
                    for chunk in r.iter_content(1 << 20):
                        f.write(chunk)
            with tmp.open("rb") as f:
                if f.read(4) not in (b"II*\x00", b"MM\x00*"):
                    raise ValueError("not a GeoTIFF")
            tmp.rename(dest)
            log_download(label, url, dest, "downloaded")
            return "downloaded"
        except Exception as e:  # noqa: BLE001
            tmp.unlink(missing_ok=True)
            if attempt == 2:
                log_download(label, url, dest, "failed", str(e)[:200])
                sys.exit(f"Download failed: {url}\n{e}\nSave the file manually to {dest} and re-run.")
            time.sleep(3)


def punjab_tiles(bounds, union):
    out = []
    for lat in range(int(math.floor(bounds[1] / 3) * 3), int(bounds[3]) + 1, 3):
        for lon in range(int(math.floor(bounds[0] / 3) * 3), int(bounds[2]) + 1, 3):
            if union.intersects(box(lon, lat, lon + 3, lat + 3)):
                out.append((f"N{lat:02d}E{lon:03d}", lon, lat))
    return out


def build_cropland_fraction(tiles, x0, y1, W, H):
    """Fill crop/valid counts (0-100 per ~100 m cell) on the Punjab 1/1200-deg grid from 10 m tiles."""
    crop = np.zeros((H, W), np.uint8)
    valid = np.zeros((H, W), np.uint8)
    res100 = WC_RES * AGG
    for tname, lon, lat in tiles:
        with rasterio.open(RAW_WC / f"ESA_WorldCover_10m_2021_v200_{tname}_Map.tif") as src:
            assert abs(src.res[0] - WC_RES) < 1e-12 and src.crs.to_epsg() == 4326
            # intersection of tile and Punjab grid, in degrees (both are multiples of 1/1200)
            ix0, ix1 = max(lon, x0), min(lon + 3, x0 + W * res100)
            iy1, iy0 = min(lat + 3, y1), max(lat, y1 - H * res100)
            if ix1 <= ix0 or iy1 <= iy0:
                continue
            c0 = round((ix0 - src.bounds.left) / WC_RES); c1 = round((ix1 - src.bounds.left) / WC_RES)
            r0 = round((src.bounds.top - iy1) / WC_RES); r1 = round((src.bounds.top - iy0) / WC_RES)
            oc0 = round((ix0 - x0) / res100); or0 = round((y1 - iy1) / res100)
            for rr in range(r0, r1, CHUNK):
                nr = min(CHUNK, r1 - rr)
                a = src.read(1, window=Window(c0, rr, c1 - c0, nr))
                h, w = a.shape[0] // AGG, a.shape[1] // AGG
                a = a[: h * AGG, : w * AGG].reshape(h, AGG, w, AGG)
                orow = or0 + (rr - r0) // AGG
                crop[orow:orow + h, oc0:oc0 + w] += (a == CROPLAND).sum(axis=(1, 3)).astype(np.uint8)
                valid[orow:orow + h, oc0:oc0 + w] += (a != 0).sum(axis=(1, 3)).astype(np.uint8)
    return crop, valid


def weighted_median(v, w):
    o = np.argsort(v)
    v, w = v[o], w[o]
    c = np.cumsum(w)
    return float(v[np.searchsorted(c, 0.5 * c[-1])]) if c[-1] > 0 else np.nan


def zonal(layer, id_col, frac100, t100, tt, wt1k, t1k):
    g = layer.to_crs(4326).reset_index(drop=True)
    ids = np.arange(1, len(g) + 1, dtype=np.int32)
    z100 = rasterize(zip(g.geometry, ids), out_shape=frac100.shape, transform=t100, fill=0, dtype="int32")
    z1k = rasterize(zip(g.geometry, ids), out_shape=tt.shape, transform=t1k, fill=0, dtype="int32")
    rows = []
    for i, uid in zip(ids, g[id_col]):
        f = frac100[(z100 == i) & ~np.isnan(frac100)]
        m = (z1k == i) & (tt != -9999)
        v, w = tt[m].astype(float), wt1k[m]
        ok = ~np.isnan(w)
        rows.append({id_col: uid,
                     "cropland_share": f.mean() if f.size else np.nan,
                     "n_cells_100m": int(f.size),
                     "tt_city_mean_min": v.mean() if v.size else np.nan,
                     "tt_city_median_min": float(np.median(v)) if v.size else np.nan,
                     "tt_city_cropw_mean_min": np.average(v[ok], weights=w[ok]) if ok.any() and w[ok].sum() > 0 else np.nan,
                     "tt_city_cropw_median_min": weighted_median(v[ok], w[ok]) if ok.any() else np.nan,
                     "n_cells_1km": int(v.size)})
    return pd.DataFrame(rows)


def main() -> int:
    T = {}
    t0 = time.perf_counter()
    dist = gpd.read_file(IN_GPKG, layer="district_fallback")
    teh = gpd.read_file(IN_GPKG, layer="tehsil")
    g4326 = dist.to_crs(4326)
    b = g4326.total_bounds
    # Punjab grid snapped outward to the 1/120-deg travel-time grid (which is also a multiple of 1/1200).
    x0, y0 = math.floor(b[0] * 120) / 120, math.floor(b[1] * 120) / 120
    x1, y1 = math.ceil(b[2] * 120) / 120, math.ceil(b[3] * 120) / 120
    tiles = punjab_tiles(b, g4326.union_all())

    for tname, _, _ in tiles:
        fetch(WC_URL.format(t=tname), RAW_WC / f"ESA_WorldCover_10m_2021_v200_{tname}_Map.tif",
              f"ESA WorldCover 2021 v200 tile {tname}")
    fetch(TT_URL, RAW_TT, "MAP Accessibility to Cities 2015, WCS clip 69-76E 27-35N")
    T["download / check"] = time.perf_counter() - t0

    t1 = time.perf_counter()
    res100 = WC_RES * AGG
    W, H = round((x1 - x0) / res100), round((y1 - y0) / res100)
    crop, valid = build_cropland_fraction(tiles, x0, y1, W, H)
    with np.errstate(invalid="ignore", divide="ignore"):
        frac100 = np.where(valid > 0, crop / np.maximum(valid, 1), np.nan).astype(np.float32)
    t100 = from_origin(x0, y1, res100, res100)
    prof = dict(driver="GTiff", dtype="float32", count=1, crs="EPSG:4326", compress="deflate", tiled=True,
                nodata=np.nan, predictor=3)
    with rasterio.open(FRAC100, "w", width=W, height=H, transform=t100, **prof) as dst:
        dst.write(frac100, 1)
    T["10 m → ~100 m cropland fraction"] = time.perf_counter() - t1

    # 1 km cropland weight: exact 10x10 aggregation of the ~100 m counts
    t2 = time.perf_counter()
    h1, w1 = H // AGG, W // AGG
    c1 = crop[: h1 * AGG, : w1 * AGG].reshape(h1, AGG, w1, AGG).sum(axis=(1, 3), dtype=np.int64)
    v1 = valid[: h1 * AGG, : w1 * AGG].reshape(h1, AGG, w1, AGG).sum(axis=(1, 3), dtype=np.int64)
    wt1k = np.where(v1 > 0, c1 / np.maximum(v1, 1), np.nan).astype(np.float32)
    t1k = from_origin(x0, y1, TT_RES, TT_RES)
    with rasterio.open(FRAC1K, "w", width=w1, height=h1, transform=t1k, **prof) as dst:
        dst.write(wt1k, 1)

    with rasterio.open(RAW_TT) as src:
        assert src.crs.to_epsg() == 4326 and abs(src.res[0] - TT_RES) < 1e-12
        win = src.window(x0, y0, x1, y1)
        win = Window(round(win.col_off), round(win.row_off), w1, h1)
        tt = src.read(1, window=win)
        assert abs(src.window_transform(win).c - x0) < 1e-9 and abs(src.window_transform(win).f - y1) < 1e-9
        lahore = list(src.sample([(74.3436, 31.5497)]))[0][0]   # sanity: Lahore city centre should be ~0 min
    T["1 km weights + travel-time clip"] = time.perf_counter() - t2

    t3 = time.perf_counter()
    zd = zonal(dist, "adm2_pcode", frac100, t100, tt, wt1k, t1k)
    zt = zonal(teh, "adm3_pcode", frac100, t100, tt, wt1k, t1k)
    for z in (zd, zt):
        z["vintage_cropland"] = WC_VINTAGE
        z["vintage_travel_time"] = TT_VINTAGE
    zd.to_csv(ROOT / "data" / "processed" / "raster_context_district.csv", index=False)
    zt.to_csv(ROOT / "data" / "processed" / "raster_context_tehsil.csv", index=False)
    OUT_GPKG.unlink(missing_ok=True)
    dist.merge(zd, on="adm2_pcode").to_file(OUT_GPKG, layer="district", driver="GPKG")
    teh.merge(zt, on="adm3_pcode").to_file(OUT_GPKG, layer="tehsil", driver="GPKG", mode="a")
    # Cholistan option B (sensitivity, D015): same polygons, so the same raster statistics
    gpd.read_file(IN_GPKG, layer="district_fallback_optB").merge(zd, on="adm2_pcode").to_file(
        OUT_GPKG, layer="district_optB", driver="GPKG", mode="a")
    gpd.read_file(IN_GPKG, layer="tehsil_optB").merge(zt, on="adm3_pcode").to_file(
        OUT_GPKG, layer="tehsil_optB", driver="GPKG", mode="a")
    T["zonal statistics (both levels)"] = time.perf_counter() - t3
    T["TOTAL"] = time.perf_counter() - t0

    disk = {p.name: p.stat().st_size for p in sorted(RAW_WC.glob("*.tif"))}
    disk[RAW_TT.name] = RAW_TT.stat().st_size
    disk[FRAC100.name] = FRAC100.stat().st_size
    disk[FRAC1K.name] = FRAC1K.stat().st_size
    punjab_crop = np.nanmean(frac100[rasterize([(g4326.union_all(), 1)], out_shape=frac100.shape, transform=t100) == 1])
    L = [f"# Raster context run ({dt.date.today()})", "", f"Tiles: {', '.join(t for t, _, _ in tiles)}",
         f"Punjab grid: {x0:.4f}–{x1:.4f}E, {y0:.4f}–{y1:.4f}N; ~100 m grid {W}×{H}; 1 km grid {w1}×{h1}.",
         f"Sanity: travel time at Lahore city centre = {lahore} min; Punjab mean cropland fraction = {punjab_crop:.3f}.", "",
         "| Step | Seconds |", "|---|---|"] + [f"| {k} | {v:.1f} |" for k, v in T.items()] + [
         "", "| File | MB |", "|---|---|"] + [f"| {k} | {v / 1e6:.1f} |" for k, v in disk.items()] + [
         f"| **total** | **{sum(disk.values()) / 1e6:.1f}** |"]
    RUN_MD.write_text("\n".join(L) + "\n")
    print("\n".join(L))
    return 0


if __name__ == "__main__":
    sys.exit(main())
