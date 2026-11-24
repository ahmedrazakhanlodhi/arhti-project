"""common.py: definitions shared by the numbered scripts (loaded with importlib; not run on its own).

- CRS: the analysis CRS (docs/project_rules.md rule 7, D025): custom Albers equal-area centred on Punjab.
- geodesic_knn: k-nearest-neighbour weights from GEODESIC distances between unit centroids (D026).
- recompute_shares: shares from summed counts (never averaged).
- Concept labels (D029): PRESENCE vs AVAILABILITY vs ALLOCATION.
"""

from __future__ import annotations

import numpy as np
from libpysal.weights import W
from pyproj import Geod

CRS = "+proj=aea +lat_1=28 +lat_2=33 +lat_0=30 +lon_0=72 +datum=WGS84 +units=m +no_defs"
CRS_LABEL = "Albers equal-area centred on Punjab (lat_1 28, lat_2 33, lat_0 30, lon_0 72; WGS84)"
GEOD = Geod(ellps="WGS84")
VALID_MATCH_TYPES = ("exact", "normalized", "spelling", "rename", "parent_aggregation")

SFR_DEF = ("reported subsistence-holding borrower records per 1,000 farms under 12.5 acres (SBP FY2023-24, by booking "
           "district; borrower records may not be unique individuals)")
CONCEPTS = {
    "presence": "PRESENCE: physical facilities (online bank branch in/near mouza; RURAL scheduled-bank branches per 10,000 farms)",
    "availability": "AVAILABILITY: credit sources reported as available in the mouza (Mouza Census 2020)",
    "allocation": "ALLOCATION: who formal credit reaches (SBP borrower records vs Ag Census farms)",
}


def centroid_lonlat(gdf):
    """Centroids computed in the analysis CRS, returned as lon/lat (EPSG:4326)."""
    c = gdf.to_crs(CRS).geometry.centroid
    ll = c.to_crs(4326)
    return np.column_stack([ll.x.values, ll.y.values])


def geodesic_distance_matrix(lonlat):
    n = len(lonlat)
    d = np.zeros((n, n))
    for i in range(n):
        _, _, dist = GEOD.inv(np.full(n, lonlat[i, 0]), np.full(n, lonlat[i, 1]), lonlat[:, 0], lonlat[:, 1])
        d[i] = dist
    return d


def geodesic_knn(gdf, k=5, ids=None):
    """libpysal W with each unit's k nearest neighbours by ellipsoidal distance (ties broken by stable index order)."""
    ll = centroid_lonlat(gdf)
    d = geodesic_distance_matrix(ll)
    np.fill_diagonal(d, np.inf)
    ids = list(range(len(gdf))) if ids is None else list(ids)
    neigh = {ids[i]: [ids[j] for j in np.argsort(d[i], kind="stable")[:k]] for i in range(len(gdf))}
    return W(neigh, silence_warnings=True)


def recompute_shares(t):
    rp = t["rp_mouzas"].replace(0, np.nan)
    for s in ["arhti", "ztbl", "commercial", "coop", "mfb"]:
        t[f"{s}_share"] = t[f"n_{s}"] / rp
    for pre in ["onlinebank", "mkt_grain", "mkt_livestock", "mkt_fruitveg"]:
        t[f"{pre}_in_mouza_share"] = t[f"n_{pre}_in_mouza"] / rp
        t[f"{pre}_51plus_share"] = t[f"n_{pre}_51plus"] / rp
    t["onlinebank_over25km_share"] = (t["n_onlinebank_26_50"] + t["n_onlinebank_51plus"]) / rp
    t["road_metalled_share"] = t["n_road_metalled"] / rp
    t["road_mud_share"] = t["n_road_mud"] / rp
    t["metroad_51plus_share"] = t["n_metroad_51plus"] / rp
    return t


def choose_scheme(values, k=5, min_count=3):
    """Classification rule (D023): Fisher-Jenks k=5 unless a class holds < min_count units, else quantiles."""
    import mapclassify
    import pandas as pd
    v = pd.Series(values).dropna().values
    q, j = mapclassify.Quantiles(v, k=k), mapclassify.FisherJenks(v, k=k)
    return (j if int(min(j.counts)) >= min_count else q), q, j
