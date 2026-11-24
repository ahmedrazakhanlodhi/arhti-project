# Raster context run (2026-10-31)

Tiles: N27E069, N27E072, N30E069, N30E072, N30E075, N33E069, N33E072
Punjab grid: 69.3167–75.3833E, 27.7000–34.0250N; ~100 m grid 7280×7590; 1 km grid 728×759.
Sanity: travel time at Lahore city centre = 0 min; Punjab mean cropland fraction = 0.540.

| Step | Seconds |
|---|---|
| download / check | 0.1 |
| 10 m → ~100 m cropland fraction | 15.5 |
| 1 km weights + travel-time clip | 0.1 |
| zonal statistics (both levels) | 3.4 |
| TOTAL | 19.1 |

| File | MB |
|---|---|
| ESA_WorldCover_10m_2021_v200_N27E069_Map.tif | 105.0 |
| ESA_WorldCover_10m_2021_v200_N27E072_Map.tif | 108.8 |
| ESA_WorldCover_10m_2021_v200_N30E069_Map.tif | 150.6 |
| ESA_WorldCover_10m_2021_v200_N30E072_Map.tif | 122.8 |
| ESA_WorldCover_10m_2021_v200_N30E075_Map.tif | 102.5 |
| ESA_WorldCover_10m_2021_v200_N33E069_Map.tif | 155.7 |
| ESA_WorldCover_10m_2021_v200_N33E072_Map.tif | 153.2 |
| MAP_2015_travel_time_to_cities_69E76E_27N35N.tif | 4.2 |
| worldcover_cropland_frac_1200.tif | 77.7 |
| cropland_frac_120.tif | 1.6 |
| **total** | **982.1** |
