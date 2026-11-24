"""10_export_qgis.py: export every final layer into one GeoPackage for QGIS, with field aliases.

    .venv/bin/python -I scripts/10_export_qgis.py      (after 09_figures.py)

Output: outputs/arhti_project.gpkg (all layers in the analysis CRS, common.CRS: Albers equal-area centred on Punjab). Field aliases are written to the GeoPackage
`gpkg_data_columns` table (GeoPackage schema extension). GDAL >= 3.3 reads its `name` column as the field
alternative name, which QGIS (>= 3.20) shows as the field alias. Each layer also carries a `vintage` field.
"""

from __future__ import annotations

import importlib.util
import sqlite3
import sys
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import pyogrio

ROOT = Path(__file__).resolve().parents[1]
P, T = ROOT / "data" / "processed", ROOT / "outputs" / "tables"
OUT = ROOT / "outputs" / "arhti_project.gpkg"
_cs = importlib.util.spec_from_file_location("common", ROOT / "scripts" / "common.py")
common = importlib.util.module_from_spec(_cs); _cs.loader.exec_module(common)
CRS = common.CRS

TEHSIL_FIELDS = {
    "adm3_pcode": "OCHA tehsil p-code", "adm3_name": "Tehsil (OCHA name)", "adm2_pcode": "OCHA district p-code",
    "adm2_name": "District (OCHA name)", "coverage_class": "Figure 1 class (crosswalk match type)", "match_types": "Match type(s)",
    "mouza_tehsil_uids": "Mouza Census tehsil key(s) summed into this polygon", "contains_cholistan": "Includes Cholistan desert mouzas",
    "rp_mouzas": "Rural populated mouzas (denominator)", "n_arhti": "Mouzas reporting commission agent/arhti credit",
    "n_ztbl": "Mouzas reporting ZTBL credit", "n_commercial": "Mouzas reporting commercial bank credit",
    "n_coop": "Mouzas reporting cooperative bank credit", "n_mfb": "Mouzas reporting microfinance bank credit",
    "arhti_share": "AVAILABILITY: share reporting arhti credit (Mouza Census 2020)",
    "commercial_share": "AVAILABILITY: share reporting commercial-bank credit (Mouza Census 2020)",
    "ztbl_share": "AVAILABILITY: share reporting ZTBL credit", "coop_share": "AVAILABILITY: share reporting cooperative bank credit",
    "mfb_share": "AVAILABILITY: share reporting microfinance bank credit",
    "onlinebank_in_mouza_share": "PRESENCE: share with online commercial bank in mouza",
    "onlinebank_over25km_share": "PRESENCE: share with nearest online bank > 25 km",
    "mkt_grain_in_mouza_share": "Share with grain market in mouza", "mkt_grain_51plus_share": "Share with grain market 51+ km away",
    "road_metalled_share": "Share on metalled road", "bivariate_class": "Figure 3 bivariate class (arhti tertile-commercial tertile)",
    "lisa_queen_p05": "LISA arhti_share, Queen, p<0.05", "lisa_queen_p01": "LISA arhti_share, Queen, p<0.01",
    "lisa_queen_fdr05": "LISA arhti_share, Queen, FDR 0.05", "lisa_queen_p": "LISA pseudo p (Queen, 999 perm, seed 20261031)",
    "lisa_knn5_p05": "LISA arhti_share, geodesic kNN-5, p<0.05",
    "cropland_share": "Cropland fraction (WorldCover 2021, class 40)",
    "tt_city_cropw_mean_min": "Modelled travel time to nearest city, cropland-weighted mean (min, MAP 2015)",
    "cooc_obs_exp_ratio": "EXPLORATORY: observed/expected share of mouzas reporting both arhti and commercial (Fig S4)",
    "cooc_ratio_class": "Figure S4 class (fixed; 'not estimable' if < 20 mouzas or zero in either source)",
    "scenario": "Cholistan scenario", "vintage": "Data vintage"}
DISTRICT_FIELDS = {
    "adm2_pcode": "OCHA district p-code", "adm2_name": "District (OCHA name)", "sbp_district": "SBP district name",
    "agc_district": "Ag Census district name", "coverage_class": "Figure 1 class",
    "rp_mouzas": "Rural populated mouzas (Mouza Census 2020)", "arhti_share": "AVAILABILITY: share reporting arhti credit",
    "commercial_share": "AVAILABILITY: share reporting commercial-bank credit (Mouza Census 2020)",
    "lisa_queen_p05": "LISA arhti_share (district, MAUP comparison), Queen, p<0.05",
    "lisa_queen_fdr05": "LISA arhti_share (district), Queen, FDR 0.05", "lisa_queen_p": "LISA pseudo p (district, Queen)",
    "sub_borrowers": "SBP subsistence-holding borrower records (FY2023-24, booking district)",
    "eco_borrowers": "SBP economic-holding borrower records", "abv_borrowers": "SBP above-economic borrower records",
    "small_farms": "Farms < 12.5 acres (Ag Census 2024)", "farms": "All private farms (Ag Census 2024)",
    "small_farm_reach": "ALLOCATION: " + common.SFR_DEF,
    "branches_scheduled": "Scheduled-bank branches (SBP list, 30 Jun 2024)",
    "branches_rural": "Scheduled-bank branches coded rural (SBP list, 30 Jun 2024)",
    "rural_branches_per_10k_farms": "PRESENCE: rural scheduled-bank branches per 10,000 farms (SBP 30 Jun 2024 / Ag Census 2024)",
    "all_branches_per_10k_farms_sensitivity": "SENSITIVITY only: all scheduled-bank branches per 10,000 farms (dominated by urban branches)",
    "tenant_share": "Tenant farms / all farms", "owner_cum_tenant_share": "Owner-cum-tenant farms / all farms",
    "large_farm_area_share": "Operated area in farms >= 50 acres / all farm area (concentration of OPERATED area)",
    "class_availability": "Figure 5B: high reported commercial-bank credit availability, low small-farm reach",
    "class_presence": "Figure 5C: high rural-branch presence, low small-farm reach",
    "flagged": "Flagged in SBP data-quality screen (1/0)", "flag_reasons": "SBP data-quality flag reasons",
    "cropland_share": "Cropland fraction (WorldCover 2021)",
    "tt_city_cropw_mean_min": "Modelled travel time to nearest city, cropland-weighted (min, MAP 2015)", "vintage": "Data vintage"}


def tehsil_layer(layer="tehsil", scen="A"):
    t = gpd.read_file(P / "punjab_credit_context.gpkg", layer=layer)
    mt = t.match_types.fillna("")
    t["coverage_class"] = np.select([t.rp_mouzas.fillna(0) == 0, mt.str.contains("parent_aggregation"), mt.str.contains("spelling|rename")],
                                    ["No rural populated mouzas", "Parent aggregation (several census units summed)",
                                     "Spelling or rename (reviewed by Ahmed)"], "Exact or rule-normalized")
    ok = t.rp_mouzas > 0
    qa = t.loc[ok, "arhti_share"].quantile([1 / 3, 2 / 3]).values
    qc = t.loc[ok, "commercial_share"].quantile([1 / 3, 2 / 3]).values
    ra, rc = np.digitize(t.arhti_share, qa, right=True) + 1, np.digitize(t.commercial_share, qc, right=True) + 1
    t["bivariate_class"] = np.where(ok, [f"A{a}-C{c}" for a, c in zip(ra, rc)], None)
    L = pd.read_csv(T / "lisa_arhti.csv")
    L = L[(L.level == "tehsil") & (L.scenario == scen) & (L.analysis == "LISA arhti_share")]
    q, k = L[L.weights == "Queen"].set_index("pcode"), L[L.weights == "kNN-5 (geodesic)"].set_index("pcode")
    cc = pd.read_csv(T / "mouza_cooccurrence.csv")
    cc = cc[(cc.record == "tehsil (arhti x commercial)") & (cc.scenario == scen)].set_index("pcode")
    t["cooc_obs_exp_ratio"] = t.adm3_pcode.map(cc.obs_exp_ratio)
    t["cooc_ratio_class"] = t.adm3_pcode.map(cc.ratio_class).fillna("not estimable")
    for c, src in [("lisa_queen_p05", q.cluster_p05), ("lisa_queen_p01", q.cluster_p01), ("lisa_queen_fdr05", q.cluster_fdr05),
                   ("lisa_queen_p", q.p_sim), ("lisa_knn5_p05", k.cluster_p05)]:
        t[c] = t.adm3_pcode.map(src)
    return t[[c for c in TEHSIL_FIELDS if c in t] + ["geometry"]]


Q1D_FIELDS = {k: v for k, v in TEHSIL_FIELDS.items() if not k.startswith(("adm3", "coverage", "match_types", "mouza_tehsil",
                                                                            "contains_", "bivariate", "cooc_"))}
Q1D_FIELDS.update({"adm2_pcode": "OCHA district p-code", "adm2_name": "District (OCHA name)",
                   "lisa_queen_p05": "LISA arhti_share (district, MAUP comparison), Queen, p<0.05",
                   "lisa_queen_p01": "LISA arhti_share (district), Queen, p<0.01", "lisa_queen_fdr05": "LISA arhti_share (district), Queen, FDR 0.05",
                   "lisa_queen_p": "LISA pseudo p (district, Queen)", "lisa_knn5_p05": "LISA arhti_share (district), geodesic kNN-5, p<0.05"})


def q1_district_layer(layer, scen):
    d = gpd.read_file(P / "punjab_credit_context.gpkg", layer=layer)
    L = pd.read_csv(T / "lisa_arhti.csv")
    L = L[(L.level == "district") & (L.scenario == scen) & (L.analysis == "LISA arhti_share")]
    q, k = L[L.weights == "Queen"].set_index("pcode"), L[L.weights == "kNN-5 (geodesic)"].set_index("pcode")
    for c, src in [("lisa_queen_p05", q.cluster_p05), ("lisa_queen_p01", q.cluster_p01), ("lisa_queen_fdr05", q.cluster_fdr05),
                   ("lisa_queen_p", q.p_sim), ("lisa_knn5_p05", k.cluster_p05)]:
        d[c] = d.adm2_pcode.map(src)
    d["vintage"] = ("Mouza Census 2020 (PBS, Jan-Mar 2020), tehsil counts summed to districts (shares recomputed); MAUP comparison; "
                    "OCHA COD-AB valid_on 2022-09-09")
    return d[[c for c in Q1D_FIELDS if c in d] + ["geometry"]]


def district_layer():
    d = gpd.read_file(P / "district_credit_allocation.gpkg", layer="district")
    ctx = gpd.read_file(P / "punjab_credit_context.gpkg", layer="district")[["adm2_pcode", "cropland_share", "tt_city_cropw_mean_min"]]
    d = d.merge(ctx, on="adm2_pcode", how="left")
    L = pd.read_csv(T / "lisa_arhti.csv")
    q = L[(L.level == "district") & (L.scenario == "A") & (L.weights == "Queen") & (L.analysis == "LISA arhti_share")].set_index("pcode")
    d["lisa_queen_p05"], d["lisa_queen_fdr05"], d["lisa_queen_p"] = d.adm2_pcode.map(q.cluster_p05), d.adm2_pcode.map(q.cluster_fdr05), d.adm2_pcode.map(q.p_sim)
    ex = pd.read_csv(T / "two_kinds_of_exclusion.csv")
    ex = ex[ex["sample"] == "all matched districts"]
    for basis, col, var in [("availability", "class_availability", "commercial_share"), ("presence", "class_presence", "rural_branches_per_10k_farms")]:
        e = ex[ex.basis == basis]
        lab = e.classification.iloc[0] if len(e) else basis
        d[col] = np.select([d.adm2_name.isin(set(e.adm2_name)), d.small_farm_reach.notna() & d[var].notna()], [lab, "Other"], "Not classified")
    fl = pd.to_numeric(d.flagged, errors="coerce")
    d["coverage_class"] = np.where(fl == 1, "Matched, flagged (SBP screen)", "Matched")
    d["flagged"] = fl.astype("Int64")
    d["vintage"] = ("SBP FY2023-24 (booking district); Agricultural Census 2024 (sample-based, fieldwork 2024-25); "
                    "Mouza Census 2020; SBP branch list 30 Jun 2024; not contemporaneous")
    return d[[c for c in DISTRICT_FIELDS if c in d] + ["geometry"]]


def write_aliases(layer_aliases: dict[str, dict[str, str]]):
    con = sqlite3.connect(OUT)
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS gpkg_data_columns (table_name TEXT NOT NULL, column_name TEXT NOT NULL,
                   name TEXT, title TEXT, description TEXT, mime_type TEXT, constraint_name TEXT,
                   CONSTRAINT pk_gdc PRIMARY KEY (table_name, column_name), CONSTRAINT gdc_tn UNIQUE (table_name, name))""")
    cur.execute("""CREATE TABLE IF NOT EXISTS gpkg_extensions (table_name TEXT, column_name TEXT, extension_name TEXT NOT NULL,
                   definition TEXT NOT NULL, scope TEXT NOT NULL, CONSTRAINT ge_tce UNIQUE (table_name, column_name, extension_name))""")
    for tbl in ["gpkg_data_columns", "gpkg_data_column_constraints"]:
        cur.execute("INSERT OR IGNORE INTO gpkg_extensions VALUES (?, NULL, 'gpkg_schema', "
                    "'http://www.geopackage.org/spec/#extension_schema', 'read-write')", (tbl,))
    cur.execute("""CREATE TABLE IF NOT EXISTS gpkg_data_column_constraints (constraint_name TEXT NOT NULL, constraint_type TEXT NOT NULL,
                   value TEXT, min NUMERIC, min_is_inclusive BOOLEAN, max NUMERIC, max_is_inclusive BOOLEAN, description TEXT,
                   CONSTRAINT gdcc_ntv UNIQUE (constraint_name, constraint_type, value))""")
    for layer, al in layer_aliases.items():
        for col, alias in al.items():
            cur.execute("INSERT OR REPLACE INTO gpkg_data_columns (table_name, column_name, name, title, description) "
                        "VALUES (?, ?, ?, ?, ?)", (layer, col, alias, alias, alias))
    con.commit()
    con.close()


def main() -> int:
    OUT.unlink(missing_ok=True)
    teh, dist = tehsil_layer(), district_layer()
    tehB = tehsil_layer("tehsil_optB", "B")
    adm1 = gpd.read_file(ROOT / "data" / "interim" / "boundaries_shp" / "pak_admin1.shp").to_crs(CRS)[["adm1_pcode", "adm1_name", "geometry"]]
    layers = {
        "q1_tehsils_mouza_census_2020": (teh, TEHSIL_FIELDS),
        "q1_tehsils_cholistan_excluded_optB": (tehB, TEHSIL_FIELDS),
        "q2_districts_credit_allocation": (dist, DISTRICT_FIELDS),
        "q1_districts_mouza_census_2020_MAUP": (q1_district_layer("district", "A"), Q1D_FIELDS),
        "q1_districts_cholistan_excluded_optB_MAUP": (q1_district_layer("district_optB", "B"), Q1D_FIELDS),
        "context_pakistan_provinces": (adm1, {"adm1_pcode": "OCHA province p-code", "adm1_name": "Province"}),
        "context_islamabad_ict_excluded": (adm1[adm1.adm1_name == "Islamabad"], {"adm1_name": "Excluded unit (ICT)"}),
        "context_punjab_outline": (adm1[adm1.adm1_name == "Punjab"], {"adm1_name": "Province"}),
    }
    for name, (g, _) in layers.items():
        pyogrio.write_dataframe(g.to_crs(CRS), OUT, layer=name, driver="GPKG", append=OUT.exists())
    tables = {"table_tehsil_crosswalk": pd.read_csv(ROOT / "data" / "interim" / "tehsil_crosswalk.csv"),
              "table_district_crosswalk_sbp_agc": pd.read_csv(ROOT / "data" / "interim" / "district_crosswalk_sbp_agc_branches.csv"),
              "table_moran_global": pd.read_csv(T / "moran_global.csv"),
              "table_lisa_counts": pd.read_csv(T / "lisa_counts.csv"),
              "table_cholistan_sensitivity": pd.read_csv(T / "cholistan_sensitivity.csv"),
              "table_exploratory_associations": pd.read_csv(T / "exploratory_associations.csv"),
              "table_q2_tenure_associations": pd.read_csv(T / "q2_tenure_associations.csv"),
              "table_sbp_province_headline": pd.read_csv(T / "sbp_province_headline.csv")}
    for name, df in tables.items():
        pyogrio.write_dataframe(df, OUT, layer=name, driver="GPKG", append=True)
    write_aliases({k: v for k, (_, v) in layers.items()})
    for l, _ in pyogrio.list_layers(OUT):
        i = pyogrio.read_info(OUT, layer=l)
        print(f"{l:40s} {i['features']:5d} features  {i['geometry_type'] or 'table':14s} {len(i['fields'])} fields")
    con = sqlite3.connect(OUT)
    print("aliases written:", con.execute("select count(*) from gpkg_data_columns").fetchone()[0])
    con.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
