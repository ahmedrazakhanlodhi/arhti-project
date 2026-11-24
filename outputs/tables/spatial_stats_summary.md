# Spatial statistics summary: EXPLORATORY (2026-11-23)

Prespecified in D018. Administrative assignment 23,130/23,130 (100.0%) passes the 95% gate, so **Q1 unit = tehsil**. The other level is a labelled MAUP comparison. Scenario A = Cholistan merged into its parent tehsils (primary); B = Cholistan excluded (sensitivity, D015). Weights: Queen contiguity, row-standardised (primary); kNN-5 from geodesic centroid distances, row-standardised (sensitivity, D026). 999 permutations, seed 20261031. CRS: Albers equal-area centred on Punjab (lat_1 28, lat_2 33, lat_0 30, lon_0 72; WGS84). Data: Mouza Census 2020 (PBS, Jan-Mar 2020; enumerator-reported availability); ESA WorldCover 2021; MAP Accessibility to Cities 2015; OCHA COD-AB boundaries (valid_on 2022-09-09). Vintages differ.

## Samples (Q1 excludes units with zero rural populated mouzas, D028)

| level    | role            | scenario   | excluded_zero_rp          |   n |   arhti_mean |   arhti_median |   arhti_min |   arhti_max |   arhti_zero |   commercial_median |   arhti_pooled |   rp_mouzas |
|:---------|:----------------|:-----------|:--------------------------|----:|-------------:|---------------:|------------:|------------:|-------------:|--------------------:|---------------:|------------:|
| tehsil   | Q1 unit (gate)  | A          | Lahore Cantt; Lahore City | 137 |        0.289 |          0.192 |       0.000 |       1.000 |           15 |               0.374 |          0.315 |       23130 |
| tehsil   | Q1 unit (gate)  | B          | Lahore Cantt; Lahore City | 137 |        0.289 |          0.192 |       0.000 |       1.000 |           15 |               0.379 |          0.310 |       22807 |
| district | MAUP comparison | A          | Lahore                    |  35 |        0.309 |          0.246 |       0.002 |       0.860 |            0 |               0.382 |          0.315 |       23130 |
| district | MAUP comparison | B          | Lahore                    |  35 |        0.307 |          0.246 |       0.002 |       0.860 |            0 |               0.382 |          0.310 |       22807 |

## Weights

| level    | scenario   | weights          |   n | islands   |   components |   min_nb |   mean_nb |   max_nb |
|:---------|:-----------|:-----------------|----:|:----------|-------------:|---------:|----------:|---------:|
| tehsil   | A          | Queen            | 137 |           |            1 |        1 |     5.168 |       11 |
| tehsil   | A          | kNN-5 (geodesic) | 137 |           |            1 |        5 |     5.000 |        5 |
| tehsil   | B          | Queen            | 137 |           |            1 |        1 |     5.168 |       11 |
| tehsil   | B          | kNN-5 (geodesic) | 137 |           |            1 |        5 |     5.000 |        5 |
| district | A          | Queen            |  35 |           |            1 |        2 |     4.800 |        9 |
| district | A          | kNN-5 (geodesic) |  35 |           |            1 |        5 |     5.000 |        5 |
| district | B          | Queen            |  35 |           |            1 |        2 |     4.800 |        9 |
| district | B          | kNN-5 (geodesic) |  35 |           |            1 |        5 |     5.000 |        5 |

## Global Moran's I

| level    | role            | scenario   | variable         | weights          |   n |     I |     EI |   z_perm |   p_perm |
|:---------|:----------------|:-----------|:-----------------|:-----------------|----:|------:|-------:|---------:|---------:|
| tehsil   | Q1 unit (gate)  | A          | arhti_share      | Queen            | 137 | 0.536 | -0.007 |    9.941 |    0.001 |
| tehsil   | Q1 unit (gate)  | A          | commercial_share | Queen            | 137 | 0.297 | -0.007 |    5.592 |    0.001 |
| tehsil   | Q1 unit (gate)  | A          | arhti_share      | kNN-5 (geodesic) | 137 | 0.568 | -0.007 |   11.313 |    0.001 |
| tehsil   | Q1 unit (gate)  | A          | commercial_share | kNN-5 (geodesic) | 137 | 0.256 | -0.007 |    5.141 |    0.001 |
| tehsil   | Q1 unit (gate)  | B          | arhti_share      | Queen            | 137 | 0.543 | -0.007 |   10.105 |    0.001 |
| tehsil   | Q1 unit (gate)  | B          | commercial_share | Queen            | 137 | 0.327 | -0.007 |    6.152 |    0.001 |
| tehsil   | Q1 unit (gate)  | B          | arhti_share      | kNN-5 (geodesic) | 137 | 0.571 | -0.007 |   11.361 |    0.001 |
| tehsil   | Q1 unit (gate)  | B          | commercial_share | kNN-5 (geodesic) | 137 | 0.268 | -0.007 |    5.371 |    0.001 |
| district | MAUP comparison | A          | arhti_share      | Queen            |  35 | 0.429 | -0.029 |    4.385 |    0.001 |
| district | MAUP comparison | A          | commercial_share | Queen            |  35 | 0.128 | -0.029 |    1.477 |    0.080 |
| district | MAUP comparison | A          | arhti_share      | kNN-5 (geodesic) |  35 | 0.370 | -0.029 |    4.420 |    0.001 |
| district | MAUP comparison | A          | commercial_share | kNN-5 (geodesic) |  35 | 0.102 | -0.029 |    1.407 |    0.093 |
| district | MAUP comparison | B          | arhti_share      | Queen            |  35 | 0.428 | -0.029 |    4.375 |    0.001 |
| district | MAUP comparison | B          | commercial_share | Queen            |  35 | 0.151 | -0.029 |    1.704 |    0.057 |
| district | MAUP comparison | B          | arhti_share      | kNN-5 (geodesic) |  35 | 0.371 | -0.029 |    4.421 |    0.001 |
| district | MAUP comparison | B          | commercial_share | kNN-5 (geodesic) |  35 | 0.116 | -0.029 |    1.584 |    0.078 |

## Bivariate global Moran's I (arhti_share at i vs spatial lag of commercial_share)

| level    | role            | scenario   | weights          |   n |   I_bv |   z_perm |   p_perm |
|:---------|:----------------|:-----------|:-----------------|----:|-------:|---------:|---------:|
| tehsil   | Q1 unit (gate)  | A          | Queen            | 137 |  0.112 |    1.524 |    0.062 |
| tehsil   | Q1 unit (gate)  | A          | kNN-5 (geodesic) | 137 |  0.121 |    1.800 |    0.042 |
| tehsil   | Q1 unit (gate)  | B          | Queen            | 137 |  0.131 |    1.781 |    0.036 |
| tehsil   | Q1 unit (gate)  | B          | kNN-5 (geodesic) | 137 |  0.123 |    1.815 |    0.041 |
| district | MAUP comparison | A          | Queen            |  35 |  0.072 |    0.705 |    0.266 |
| district | MAUP comparison | A          | kNN-5 (geodesic) |  35 |  0.020 |    0.245 |    0.409 |
| district | MAUP comparison | B          | Queen            |  35 |  0.068 |    0.665 |    0.269 |
| district | MAUP comparison | B          | kNN-5 (geodesic) |  35 |  0.016 |    0.205 |    0.422 |

## LISA counts (p < 0.05, p < 0.01, FDR 0.05; `bh_cutoff` = Benjamini–Hochberg p-value cutoff for that run; `bh_fallback_bonferroni` = True if no p-value passed BH: cutoff shown as blank and no unit is FDR-significant)

| level    | role            | scenario   | analysis                               | weights          |   n | cluster         |   p05 |   p01 |   fdr05 |   bh_cutoff | bh_fallback_bonferroni   |
|:---------|:----------------|:-----------|:---------------------------------------|:-----------------|----:|:----------------|------:|------:|--------:|------------:|:-------------------------|
| tehsil   | Q1 unit (gate)  | A          | LISA arhti_share                       | Queen            | 137 | High-High       |    25 |    14 |      15 |       0.012 | False                    |
| tehsil   | Q1 unit (gate)  | A          | LISA arhti_share                       | Queen            | 137 | Low-Low         |    32 |    16 |      17 |       0.012 | False                    |
| tehsil   | Q1 unit (gate)  | A          | LISA arhti_share                       | Queen            | 137 | High-Low        |     0 |     0 |       0 |       0.012 | False                    |
| tehsil   | Q1 unit (gate)  | A          | LISA arhti_share                       | Queen            | 137 | Low-High        |     3 |     0 |       0 |       0.012 | False                    |
| tehsil   | Q1 unit (gate)  | A          | LISA arhti_share                       | Queen            | 137 | not significant |    77 |   107 |     105 |       0.012 | False                    |
| tehsil   | Q1 unit (gate)  | A          | Bivariate LISA arhti x lag(commercial) | Queen            | 137 | High-High       |     8 |     0 |       0 |     nan     | True                     |
| tehsil   | Q1 unit (gate)  | A          | Bivariate LISA arhti x lag(commercial) | Queen            | 137 | Low-Low         |    19 |    11 |       0 |     nan     | True                     |
| tehsil   | Q1 unit (gate)  | A          | Bivariate LISA arhti x lag(commercial) | Queen            | 137 | High-Low        |     2 |     1 |       0 |     nan     | True                     |
| tehsil   | Q1 unit (gate)  | A          | Bivariate LISA arhti x lag(commercial) | Queen            | 137 | Low-High        |     6 |     1 |       0 |     nan     | True                     |
| tehsil   | Q1 unit (gate)  | A          | Bivariate LISA arhti x lag(commercial) | Queen            | 137 | not significant |   102 |   124 |     137 |     nan     | True                     |
| tehsil   | Q1 unit (gate)  | A          | LISA arhti_share                       | kNN-5 (geodesic) | 137 | High-High       |    25 |    18 |      22 |       0.019 | False                    |
| tehsil   | Q1 unit (gate)  | A          | LISA arhti_share                       | kNN-5 (geodesic) | 137 | Low-Low         |    29 |    21 |      27 |       0.019 | False                    |
| tehsil   | Q1 unit (gate)  | A          | LISA arhti_share                       | kNN-5 (geodesic) | 137 | High-Low        |     0 |     0 |       0 |       0.019 | False                    |
| tehsil   | Q1 unit (gate)  | A          | LISA arhti_share                       | kNN-5 (geodesic) | 137 | Low-High        |     4 |     2 |       4 |       0.019 | False                    |
| tehsil   | Q1 unit (gate)  | A          | LISA arhti_share                       | kNN-5 (geodesic) | 137 | not significant |    79 |    96 |      84 |       0.019 | False                    |
| tehsil   | Q1 unit (gate)  | A          | Bivariate LISA arhti x lag(commercial) | kNN-5 (geodesic) | 137 | High-High       |     9 |     5 |       0 |       0.001 | False                    |
| tehsil   | Q1 unit (gate)  | A          | Bivariate LISA arhti x lag(commercial) | kNN-5 (geodesic) | 137 | Low-Low         |    15 |     8 |       3 |       0.001 | False                    |
| tehsil   | Q1 unit (gate)  | A          | Bivariate LISA arhti x lag(commercial) | kNN-5 (geodesic) | 137 | High-Low        |     3 |     0 |       0 |       0.001 | False                    |
| tehsil   | Q1 unit (gate)  | A          | Bivariate LISA arhti x lag(commercial) | kNN-5 (geodesic) | 137 | Low-High        |    10 |     1 |       0 |       0.001 | False                    |
| tehsil   | Q1 unit (gate)  | A          | Bivariate LISA arhti x lag(commercial) | kNN-5 (geodesic) | 137 | not significant |   100 |   123 |     134 |       0.001 | False                    |
| tehsil   | Q1 unit (gate)  | B          | LISA arhti_share                       | Queen            | 137 | High-High       |    25 |    15 |      15 |       0.012 | False                    |
| tehsil   | Q1 unit (gate)  | B          | LISA arhti_share                       | Queen            | 137 | Low-Low         |    32 |    16 |      17 |       0.012 | False                    |
| tehsil   | Q1 unit (gate)  | B          | LISA arhti_share                       | Queen            | 137 | High-Low        |     0 |     0 |       0 |       0.012 | False                    |
| tehsil   | Q1 unit (gate)  | B          | LISA arhti_share                       | Queen            | 137 | Low-High        |     3 |     0 |       0 |       0.012 | False                    |
| tehsil   | Q1 unit (gate)  | B          | LISA arhti_share                       | Queen            | 137 | not significant |    77 |   106 |     105 |       0.012 | False                    |
| tehsil   | Q1 unit (gate)  | B          | Bivariate LISA arhti x lag(commercial) | Queen            | 137 | High-High       |     9 |     2 |       0 |     nan     | True                     |
| tehsil   | Q1 unit (gate)  | B          | Bivariate LISA arhti x lag(commercial) | Queen            | 137 | Low-Low         |    19 |    10 |       0 |     nan     | True                     |
| tehsil   | Q1 unit (gate)  | B          | Bivariate LISA arhti x lag(commercial) | Queen            | 137 | High-Low        |     2 |     1 |       0 |     nan     | True                     |
| tehsil   | Q1 unit (gate)  | B          | Bivariate LISA arhti x lag(commercial) | Queen            | 137 | Low-High        |     6 |     1 |       0 |     nan     | True                     |
| tehsil   | Q1 unit (gate)  | B          | Bivariate LISA arhti x lag(commercial) | Queen            | 137 | not significant |   101 |   123 |     137 |     nan     | True                     |
| tehsil   | Q1 unit (gate)  | B          | LISA arhti_share                       | kNN-5 (geodesic) | 137 | High-High       |    25 |    18 |      22 |       0.019 | False                    |
| tehsil   | Q1 unit (gate)  | B          | LISA arhti_share                       | kNN-5 (geodesic) | 137 | Low-Low         |    29 |    21 |      27 |       0.019 | False                    |
| tehsil   | Q1 unit (gate)  | B          | LISA arhti_share                       | kNN-5 (geodesic) | 137 | High-Low        |     0 |     0 |       0 |       0.019 | False                    |
| tehsil   | Q1 unit (gate)  | B          | LISA arhti_share                       | kNN-5 (geodesic) | 137 | Low-High        |     4 |     2 |       4 |       0.019 | False                    |
| tehsil   | Q1 unit (gate)  | B          | LISA arhti_share                       | kNN-5 (geodesic) | 137 | not significant |    79 |    96 |      84 |       0.019 | False                    |
| tehsil   | Q1 unit (gate)  | B          | Bivariate LISA arhti x lag(commercial) | kNN-5 (geodesic) | 137 | High-High       |     9 |     5 |       0 |       0.001 | False                    |
| tehsil   | Q1 unit (gate)  | B          | Bivariate LISA arhti x lag(commercial) | kNN-5 (geodesic) | 137 | Low-Low         |    15 |     8 |       3 |       0.001 | False                    |
| tehsil   | Q1 unit (gate)  | B          | Bivariate LISA arhti x lag(commercial) | kNN-5 (geodesic) | 137 | High-Low        |     3 |     0 |       0 |       0.001 | False                    |
| tehsil   | Q1 unit (gate)  | B          | Bivariate LISA arhti x lag(commercial) | kNN-5 (geodesic) | 137 | Low-High        |     9 |     1 |       0 |       0.001 | False                    |
| tehsil   | Q1 unit (gate)  | B          | Bivariate LISA arhti x lag(commercial) | kNN-5 (geodesic) | 137 | not significant |   101 |   123 |     134 |       0.001 | False                    |
| district | MAUP comparison | A          | LISA arhti_share                       | Queen            |  35 | High-High       |     8 |     2 |       1 |       0.003 | False                    |
| district | MAUP comparison | A          | LISA arhti_share                       | Queen            |  35 | Low-Low         |     5 |     2 |       1 |       0.003 | False                    |
| district | MAUP comparison | A          | LISA arhti_share                       | Queen            |  35 | High-Low        |     0 |     0 |       0 |       0.003 | False                    |
| district | MAUP comparison | A          | LISA arhti_share                       | Queen            |  35 | Low-High        |     0 |     0 |       0 |       0.003 | False                    |
| district | MAUP comparison | A          | LISA arhti_share                       | Queen            |  35 | not significant |    22 |    31 |      33 |       0.003 | False                    |
| district | MAUP comparison | A          | Bivariate LISA arhti x lag(commercial) | Queen            |  35 | High-High       |     1 |     0 |       0 |     nan     | True                     |
| district | MAUP comparison | A          | Bivariate LISA arhti x lag(commercial) | Queen            |  35 | Low-Low         |     3 |     0 |       0 |     nan     | True                     |
| district | MAUP comparison | A          | Bivariate LISA arhti x lag(commercial) | Queen            |  35 | High-Low        |     0 |     0 |       0 |     nan     | True                     |
| district | MAUP comparison | A          | Bivariate LISA arhti x lag(commercial) | Queen            |  35 | Low-High        |     2 |     0 |       0 |     nan     | True                     |
| district | MAUP comparison | A          | Bivariate LISA arhti x lag(commercial) | Queen            |  35 | not significant |    29 |    35 |      35 |     nan     | True                     |
| district | MAUP comparison | A          | LISA arhti_share                       | kNN-5 (geodesic) |  35 | High-High       |     6 |     3 |       3 |       0.007 | False                    |
| district | MAUP comparison | A          | LISA arhti_share                       | kNN-5 (geodesic) |  35 | Low-Low         |     4 |     2 |       2 |       0.007 | False                    |
| district | MAUP comparison | A          | LISA arhti_share                       | kNN-5 (geodesic) |  35 | High-Low        |     1 |     0 |       0 |       0.007 | False                    |
| district | MAUP comparison | A          | LISA arhti_share                       | kNN-5 (geodesic) |  35 | Low-High        |     0 |     0 |       0 |       0.007 | False                    |
| district | MAUP comparison | A          | LISA arhti_share                       | kNN-5 (geodesic) |  35 | not significant |    24 |    30 |      30 |       0.007 | False                    |
| district | MAUP comparison | A          | Bivariate LISA arhti x lag(commercial) | kNN-5 (geodesic) |  35 | High-High       |     2 |     0 |       0 |     nan     | True                     |
| district | MAUP comparison | A          | Bivariate LISA arhti x lag(commercial) | kNN-5 (geodesic) |  35 | Low-Low         |     2 |     2 |       0 |     nan     | True                     |
| district | MAUP comparison | A          | Bivariate LISA arhti x lag(commercial) | kNN-5 (geodesic) |  35 | High-Low        |     0 |     0 |       0 |     nan     | True                     |
| district | MAUP comparison | A          | Bivariate LISA arhti x lag(commercial) | kNN-5 (geodesic) |  35 | Low-High        |     3 |     0 |       0 |     nan     | True                     |
| district | MAUP comparison | A          | Bivariate LISA arhti x lag(commercial) | kNN-5 (geodesic) |  35 | not significant |    28 |    33 |      35 |     nan     | True                     |
| district | MAUP comparison | B          | LISA arhti_share                       | Queen            |  35 | High-High       |     8 |     2 |       1 |       0.003 | False                    |
| district | MAUP comparison | B          | LISA arhti_share                       | Queen            |  35 | Low-Low         |     5 |     2 |       1 |       0.003 | False                    |
| district | MAUP comparison | B          | LISA arhti_share                       | Queen            |  35 | High-Low        |     0 |     0 |       0 |       0.003 | False                    |
| district | MAUP comparison | B          | LISA arhti_share                       | Queen            |  35 | Low-High        |     0 |     0 |       0 |       0.003 | False                    |
| district | MAUP comparison | B          | LISA arhti_share                       | Queen            |  35 | not significant |    22 |    31 |      33 |       0.003 | False                    |
| district | MAUP comparison | B          | Bivariate LISA arhti x lag(commercial) | Queen            |  35 | High-High       |     1 |     0 |       0 |     nan     | True                     |
| district | MAUP comparison | B          | Bivariate LISA arhti x lag(commercial) | Queen            |  35 | Low-Low         |     3 |     0 |       0 |     nan     | True                     |
| district | MAUP comparison | B          | Bivariate LISA arhti x lag(commercial) | Queen            |  35 | High-Low        |     0 |     0 |       0 |     nan     | True                     |
| district | MAUP comparison | B          | Bivariate LISA arhti x lag(commercial) | Queen            |  35 | Low-High        |     2 |     1 |       0 |     nan     | True                     |
| district | MAUP comparison | B          | Bivariate LISA arhti x lag(commercial) | Queen            |  35 | not significant |    29 |    34 |      35 |     nan     | True                     |
| district | MAUP comparison | B          | LISA arhti_share                       | kNN-5 (geodesic) |  35 | High-High       |     6 |     3 |       3 |       0.007 | False                    |
| district | MAUP comparison | B          | LISA arhti_share                       | kNN-5 (geodesic) |  35 | Low-Low         |     4 |     2 |       2 |       0.007 | False                    |
| district | MAUP comparison | B          | LISA arhti_share                       | kNN-5 (geodesic) |  35 | High-Low        |     1 |     0 |       0 |       0.007 | False                    |
| district | MAUP comparison | B          | LISA arhti_share                       | kNN-5 (geodesic) |  35 | Low-High        |     0 |     0 |       0 |       0.007 | False                    |
| district | MAUP comparison | B          | LISA arhti_share                       | kNN-5 (geodesic) |  35 | not significant |    24 |    30 |      30 |       0.007 | False                    |
| district | MAUP comparison | B          | Bivariate LISA arhti x lag(commercial) | kNN-5 (geodesic) |  35 | High-High       |     2 |     0 |       0 |     nan     | True                     |
| district | MAUP comparison | B          | Bivariate LISA arhti x lag(commercial) | kNN-5 (geodesic) |  35 | Low-Low         |     2 |     2 |       0 |     nan     | True                     |
| district | MAUP comparison | B          | Bivariate LISA arhti x lag(commercial) | kNN-5 (geodesic) |  35 | High-Low        |     0 |     0 |       0 |     nan     | True                     |
| district | MAUP comparison | B          | Bivariate LISA arhti x lag(commercial) | kNN-5 (geodesic) |  35 | Low-High        |     3 |     0 |       0 |     nan     | True                     |
| district | MAUP comparison | B          | Bivariate LISA arhti x lag(commercial) | kNN-5 (geodesic) |  35 | not significant |    28 |    33 |      35 |     nan     | True                     |

LISA arhti_share: significant tehsils (Queen, scenario A, p < 0.05; † = FDR survivor):

Kamoke (High-High†), Nowshera Virkan (High-High†), Hafizabad (High-High†), Shah Kot (High-High†), Ferozewala (High-High†), Sheikhupura (High-High†), Pasrur (High-High†), Pindi Bhattian (High-High†), Muridke (High-High†), Safdarabad (High-High†), Daska (High-High†), Yazman (High-High†), Gujranwala (High-High†), Sharak Pur (High-High†), Haroonabad (High-High†), Kot Radha Kishen (High-High), Pattoki (High-High), Wazirabad (High-High), Sangla Hill (High-High), Narowal (High-High), Nankana Sahib (High-High), Zafarwal (High-High), Chishtian (High-High), Fort Abbas (High-High), Chunian (High-High), Renala Khurd (Low-High), Shakargarh (Low-High), Sialkot (Low-High), Attock (Low-Low†), Fateh Jang (Low-Low†), Chakwal (Low-Low†), Rawalpindi (Low-Low†), Choa Saidan Shah (Low-Low†), Hasan Abdal (Low-Low†), Pindi Gheb (Low-Low†), Sohawa (Low-Low†), Gujar Khan (Low-Low†), Pind Dadan Khan (Low-Low†), Kahuta (Low-Low†), Khushab (Low-Low†), Kotli Sattian (Low-Low†), Jhelum (Low-Low†), Kallar Sayaddan (Low-Low†), Bhera (Low-Low†), Dina (Low-Low†), Bhalwal (Low-Low), Sargodha (Low-Low), Gojra (Low-Low), Kallar Kahar (Low-Low), Dera Ghazi Khan (Low-Low), Taxila (Low-Low), Shorkot (Low-Low), Toba Tek Singh (Low-Low), Shahpur (Low-Low), Jhang (Low-Low), Mandi Bahauddin (Low-Low), Pir Mahal (Low-Low), Sahiwal (Low-Low), Malakwal (Low-Low), Kamalia (Low-Low)

Bivariate LISA arhti x lag(commercial): significant tehsils (Queen, scenario A, p < 0.05; † = FDR survivor):

Chishtian (High-High), Arif Wala (High-High), Hasilpur (High-High), Khanewal (High-High), Liaqatpur (High-High), Yazman (High-High), Sambrial (High-High), Bahawalnagar (High-High), Jampur (High-Low), Mianwali (High-Low), Sargodha (Low-High), Mailsi (Low-High), Vehari (Low-High), Multan Saddar (Low-High), Burewala (Low-High), Dunyapur (Low-High), Murree (Low-Low), Sohawa (Low-Low), Kahuta (Low-Low), Kallar Sayaddan (Low-Low), Pind Dadan Khan (Low-Low), Gujar Khan (Low-Low), Jhelum (Low-Low), Chakwal (Low-Low), Choa Saidan Shah (Low-Low), Kallar Kahar (Low-Low), D.G Khan (Tribal Area) (Low-Low), Dera Ghazi Khan (Low-Low), Rajanpur (Tribal Area) (Low-Low), Kotli Sattian (Low-Low), Mandi Bahauddin (Low-Low), Kot Chatta (Low-Low), Dina (Low-Low), Quaidabad (Low-Low), Athara Hazari (Low-Low)

## Regression (EXPLORATORY: OLS; spatial error = prespecified check; spatial lag = POST-HOC; none chosen on significance)

| ('diagnostic', '', '')       |   ('tehsil', 'Q1 unit (gate)', 'Queen') |   ('district', 'MAUP comparison', 'Queen') |
|:-----------------------------|----------------------------------------:|-------------------------------------------:|
| n                            |                                 137.000 |                                     35.000 |
| k                            |                                   7.000 |                                      7.000 |
| ols_r2                       |                                   0.134 |                                      0.261 |
| ols_adj_r2                   |                                   0.094 |                                      0.103 |
| ols_aic                      |                                  32.918 |                                      0.955 |
| ols_loglik                   |                                  -9.459 |                                      6.522 |
| resid_moran_I                |                                   0.411 |                                      0.223 |
| resid_moran_p_perm           |                                   0.001 |                                      0.016 |
| spreg_moran_z                |                                   8.107 |                                      3.083 |
| spreg_moran_p                |                                   0.000 |                                      0.002 |
| LM_error                     |                                  53.823 |                                      3.900 |
| LM_error_p                   |                                   0.000 |                                      0.048 |
| LM_lag                       |                                  63.667 |                                      7.518 |
| LM_lag_p                     |                                   0.000 |                                      0.006 |
| RLM_error                    |                                   1.601 |                                      3.102 |
| RLM_error_p                  |                                   0.206 |                                      0.078 |
| RLM_lag                      |                                  11.446 |                                      6.721 |
| RLM_lag_p                    |                                   0.001 |                                      0.010 |
| sem_loglik                   |                                  18.124 |                                     11.765 |
| sem_aic                      |                                 -22.248 |                                     -9.531 |
| sem_lambda                   |                                   0.715 |                                      0.806 |
| slm_loglik                   |                                  17.469 |                                     10.932 |
| slm_aic                      |                                 -18.937 |                                     -5.864 |
| slm_rho                      |                                   0.671 |                                      0.635 |
| sem_prespecified_trigger_met |                                   1.000 |                                      1.000 |
| max_vif                      |                                   3.148 |                                      3.086 |
| cond_number                  |                                  29.625 |                                     47.503 |
| sem_resid_moran_I            |                                  -0.034 |                                      0.016 |
| sem_resid_moran_p            |                                   0.335 |                                      0.304 |
| slm_resid_moran_I            |                                  -0.024 |                                      0.013 |
| slm_resid_moran_p            |                                   0.380 |                                      0.322 |

| level    |   n | model                                  | term                      |   coef |    se |   stat |     p |     vif |
|:---------|----:|:---------------------------------------|:--------------------------|-------:|------:|-------:|------:|--------:|
| tehsil   | 137 | OLS (HC3)                              | const                     |  0.324 | 0.270 |  1.200 | 0.230 | nan     |
| tehsil   | 137 | OLS (HC3)                              | commercial_share          |  0.109 | 0.158 |  0.692 | 0.489 |   1.555 |
| tehsil   | 137 | OLS (HC3)                              | ztbl_share                | -0.013 | 0.136 | -0.093 | 0.926 |   1.517 |
| tehsil   | 137 | OLS (HC3)                              | onlinebank_over25km_share | -0.330 | 0.274 | -1.204 | 0.229 |   3.148 |
| tehsil   | 137 | OLS (HC3)                              | tt_city_cropw_hours       |  0.012 | 0.128 |  0.091 | 0.928 |   2.850 |
| tehsil   | 137 | OLS (HC3)                              | cropland_share            |  0.382 | 0.160 |  2.390 | 0.017 |   1.557 |
| tehsil   | 137 | OLS (HC3)                              | road_metalled_share       | -0.349 | 0.270 | -1.294 | 0.196 |   2.147 |
| tehsil   | 137 | Spatial error (ML; prespecified check) | const                     |  0.492 | 0.242 |  2.037 | 0.042 | nan     |
| tehsil   | 137 | Spatial error (ML; prespecified check) | commercial_share          |  0.193 | 0.096 |  2.009 | 0.045 | nan     |
| tehsil   | 137 | Spatial error (ML; prespecified check) | ztbl_share                | -0.065 | 0.086 | -0.756 | 0.450 | nan     |
| tehsil   | 137 | Spatial error (ML; prespecified check) | onlinebank_over25km_share | -0.442 | 0.211 | -2.094 | 0.036 | nan     |
| tehsil   | 137 | Spatial error (ML; prespecified check) | tt_city_cropw_hours       |  0.057 | 0.097 |  0.590 | 0.555 | nan     |
| tehsil   | 137 | Spatial error (ML; prespecified check) | cropland_share            | -0.070 | 0.140 | -0.502 | 0.615 | nan     |
| tehsil   | 137 | Spatial error (ML; prespecified check) | road_metalled_share       | -0.215 | 0.250 | -0.860 | 0.390 | nan     |
| tehsil   | 137 | Spatial error (ML; prespecified check) | lambda                    |  0.715 | 0.068 | 10.509 | 0.000 | nan     |
| tehsil   | 137 | Spatial lag (ML; POST-HOC)             | const                     |  0.162 | 0.194 |  0.835 | 0.404 | nan     |
| tehsil   | 137 | Spatial lag (ML; POST-HOC)             | commercial_share          |  0.154 | 0.094 |  1.627 | 0.104 | nan     |
| tehsil   | 137 | Spatial lag (ML; POST-HOC)             | ztbl_share                | -0.034 | 0.083 | -0.417 | 0.677 | nan     |
| tehsil   | 137 | Spatial lag (ML; POST-HOC)             | onlinebank_over25km_share | -0.350 | 0.231 | -1.513 | 0.130 | nan     |
| tehsil   | 137 | Spatial lag (ML; POST-HOC)             | tt_city_cropw_hours       |  0.051 | 0.091 |  0.564 | 0.573 | nan     |
| tehsil   | 137 | Spatial lag (ML; POST-HOC)             | cropland_share            |  0.030 | 0.099 |  0.308 | 0.758 | nan     |
| tehsil   | 137 | Spatial lag (ML; POST-HOC)             | road_metalled_share       | -0.138 | 0.201 | -0.686 | 0.493 | nan     |
| tehsil   | 137 | Spatial lag (ML; POST-HOC)             | rho                       |  0.671 | 0.073 |  9.167 | 0.000 | nan     |
| district |  35 | OLS (HC3)                              | const                     |  0.347 | 0.671 |  0.517 | 0.605 | nan     |
| district |  35 | OLS (HC3)                              | commercial_share          | -0.064 | 0.523 | -0.123 | 0.902 |   2.672 |
| district |  35 | OLS (HC3)                              | ztbl_share                |  0.206 | 0.458 |  0.450 | 0.653 |   2.362 |
| district |  35 | OLS (HC3)                              | onlinebank_over25km_share | -1.088 | 0.847 | -1.284 | 0.199 |   3.038 |
| district |  35 | OLS (HC3)                              | tt_city_cropw_hours       |  0.333 | 0.339 |  0.981 | 0.327 |   3.086 |
| district |  35 | OLS (HC3)                              | cropland_share            |  0.547 | 0.393 |  1.392 | 0.164 |   2.477 |
| district |  35 | OLS (HC3)                              | road_metalled_share       | -0.710 | 0.582 | -1.221 | 0.222 |   2.071 |
| district |  35 | Spatial error (ML; prespecified check) | const                     | -0.096 | 0.547 | -0.175 | 0.861 | nan     |
| district |  35 | Spatial error (ML; prespecified check) | commercial_share          |  0.199 | 0.250 |  0.796 | 0.426 | nan     |
| district |  35 | Spatial error (ML; prespecified check) | ztbl_share                |  0.127 | 0.213 |  0.598 | 0.550 | nan     |
| district |  35 | Spatial error (ML; prespecified check) | onlinebank_over25km_share | -0.512 | 0.576 | -0.889 | 0.374 | nan     |
| district |  35 | Spatial error (ML; prespecified check) | tt_city_cropw_hours       |  0.676 | 0.248 |  2.726 | 0.006 | nan     |
| district |  35 | Spatial error (ML; prespecified check) | cropland_share            |  0.084 | 0.280 |  0.300 | 0.764 | nan     |
| district |  35 | Spatial error (ML; prespecified check) | road_metalled_share       | -0.050 | 0.491 | -0.102 | 0.919 | nan     |
| district |  35 | Spatial error (ML; prespecified check) | lambda                    |  0.806 | 0.096 |  8.375 | 0.000 | nan     |
| district |  35 | Spatial lag (ML; POST-HOC)             | const                     | -0.117 | 0.472 | -0.247 | 0.805 | nan     |
| district |  35 | Spatial lag (ML; POST-HOC)             | commercial_share          | -0.034 | 0.283 | -0.119 | 0.906 | nan     |
| district |  35 | Spatial lag (ML; POST-HOC)             | ztbl_share                |  0.200 | 0.244 |  0.819 | 0.413 | nan     |
| district |  35 | Spatial lag (ML; POST-HOC)             | onlinebank_over25km_share | -1.033 | 0.655 | -1.576 | 0.115 | nan     |
| district |  35 | Spatial lag (ML; POST-HOC)             | tt_city_cropw_hours       |  0.482 | 0.245 |  1.972 | 0.049 | nan     |
| district |  35 | Spatial lag (ML; POST-HOC)             | cropland_share            |  0.269 | 0.240 |  1.122 | 0.262 | nan     |
| district |  35 | Spatial lag (ML; POST-HOC)             | road_metalled_share       | -0.249 | 0.439 | -0.568 | 0.570 | nan     |
| district |  35 | Spatial lag (ML; POST-HOC)             | rho                       |  0.635 | 0.143 |  4.447 | 0.000 | nan     |

## Leave-one-out jackknife ranges (POST-HOC)

| level    | model   | term                      |    min |    max | sign_changes   |   refits |
|:---------|:--------|:--------------------------|-------:|-------:|:---------------|---------:|
| tehsil   | OLS     | commercial_share          |  0.021 |  0.170 | False          |      137 |
| tehsil   | SEM     | commercial_share          |  0.114 |  0.230 | False          |      137 |
| tehsil   | SLM     | commercial_share          |  0.064 |  0.193 | False          |      137 |
| tehsil   | OLS     | ztbl_share                | -0.046 |  0.089 | True           |      137 |
| tehsil   | SEM     | ztbl_share                | -0.089 |  0.032 | True           |      137 |
| tehsil   | SLM     | ztbl_share                | -0.058 |  0.067 | True           |      137 |
| tehsil   | OLS     | onlinebank_over25km_share | -0.426 | -0.171 | False          |      137 |
| tehsil   | SEM     | onlinebank_over25km_share | -0.504 | -0.282 | False          |      137 |
| tehsil   | SLM     | onlinebank_over25km_share | -0.417 | -0.234 | False          |      137 |
| tehsil   | OLS     | tt_city_cropw_hours       | -0.059 |  0.078 | True           |      137 |
| tehsil   | SEM     | tt_city_cropw_hours       |  0.030 |  0.160 | False          |      137 |
| tehsil   | SLM     | tt_city_cropw_hours       |  0.023 |  0.113 | False          |      137 |
| tehsil   | OLS     | cropland_share            |  0.354 |  0.473 | False          |      137 |
| tehsil   | SEM     | cropland_share            | -0.117 |  0.116 | True           |      137 |
| tehsil   | SLM     | cropland_share            |  0.009 |  0.105 | False          |      137 |
| tehsil   | OLS     | road_metalled_share       | -0.446 | -0.260 | False          |      137 |
| tehsil   | SEM     | road_metalled_share       | -0.290 | -0.053 | False          |      137 |
| tehsil   | SLM     | road_metalled_share       | -0.210 | -0.049 | False          |      137 |
| tehsil   | SEM     | lambda                    |  0.694 |  0.742 | False          |      137 |
| tehsil   | SLM     | rho                       |  0.640 |  0.696 | False          |      137 |
| district | OLS     | commercial_share          | -0.437 |  0.076 | True           |       35 |
| district | SEM     | commercial_share          |  0.015 |  0.350 | False          |       35 |
| district | SLM     | commercial_share          | -0.334 |  0.100 | True           |       35 |
| district | OLS     | ztbl_share                |  0.059 |  0.525 | False          |       35 |
| district | SEM     | ztbl_share                |  0.030 |  0.226 | False          |       35 |
| district | SLM     | ztbl_share                |  0.072 |  0.436 | False          |       35 |
| district | OLS     | onlinebank_over25km_share | -1.584 | -0.812 | False          |       35 |
| district | SEM     | onlinebank_over25km_share | -0.996 | -0.225 | False          |       35 |
| district | SLM     | onlinebank_over25km_share | -1.418 | -0.777 | False          |       35 |
| district | OLS     | tt_city_cropw_hours       |  0.206 |  0.499 | False          |       35 |
| district | SEM     | tt_city_cropw_hours       |  0.513 |  1.063 | False          |       35 |
| district | SLM     | tt_city_cropw_hours       |  0.353 |  0.612 | False          |       35 |
| district | OLS     | cropland_share            |  0.375 |  0.765 | False          |       35 |
| district | SEM     | cropland_share            | -0.074 |  0.356 | True           |       35 |
| district | SLM     | cropland_share            |  0.176 |  0.425 | False          |       35 |
| district | OLS     | road_metalled_share       | -0.994 | -0.480 | False          |       35 |
| district | SEM     | road_metalled_share       | -0.430 |  0.281 | True           |       35 |
| district | SLM     | road_metalled_share       | -0.575 | -0.077 | False          |       35 |
| district | SEM     | lambda                    |  0.693 |  0.842 | False          |       35 |
| district | SLM     | rho                       |  0.518 |  0.687 | False          |       35 |

## Mouza-level co-occurrence (EXPLORATORY, D035; pooled statistics only)

| record                   | scenario   | pair                        |   n_mouzas |   n_strata |   strata_dropped_zero_margin |   mh_or |   ci95_low |   ci95_high |   breslow_day_tarone_stat |   breslow_day_tarone_p |   cmh_stat |   cmh_p |
|:-------------------------|:-----------|:----------------------------|-----------:|-----------:|-----------------------------:|--------:|-----------:|------------:|--------------------------:|-----------------------:|-----------:|--------:|
| pooled (Mantel-Haenszel) | A          | arhti x commercial          |      21674 |    120.000 |                       17.000 |   1.176 |      1.092 |       1.267 |                   750.956 |                  0.000 |     19.215 |   0.000 |
| pooled (Mantel-Haenszel) | A          | arhti x ztbl                |      21521 |    118.000 |                       19.000 |   0.982 |      0.903 |       1.068 |                   798.523 |                  0.000 |      0.168 |   0.682 |
| pooled (Mantel-Haenszel) | A          | arhti x onlinebank_in_mouza |      21971 |    120.000 |                       17.000 |   0.985 |      0.831 |       1.167 |                   237.812 |                  0.000 |      0.019 |   0.891 |
| pooled (Mantel-Haenszel) | B          | arhti x commercial          |      21351 |    120.000 |                       17.000 |   1.196 |      1.110 |       1.289 |                   743.407 |                  0.000 |     22.836 |   0.000 |
| pooled (Mantel-Haenszel) | B          | arhti x ztbl                |      21198 |    118.000 |                       19.000 |   1.015 |      0.931 |       1.108 |                   734.734 |                  0.000 |      0.110 |   0.740 |
| pooled (Mantel-Haenszel) | B          | arhti x onlinebank_in_mouza |      21648 |    120.000 |                       17.000 |   0.983 |      0.829 |       1.166 |                   237.556 |                  0.000 |      0.025 |   0.875 |

## Cholistan sensitivity (B vs A): 23 changed items (`cholistan_sensitivity.csv`)

| level    | unit              | pcode   | item                                                                    | option_A        | option_B        |   arhti_A |   arhti_B |
|:---------|:------------------|:--------|:------------------------------------------------------------------------|:----------------|:----------------|----------:|----------:|
| tehsil   | Fort Abbas        | PK60203 | arhti_share value                                                       | 0.735           | 0.822           |     0.735 |     0.822 |
| tehsil   | Fort Abbas        | PK60203 | arhti_share map class (option-A breaks)                                 | 4               | 5               |     0.735 |     0.822 |
| tehsil   | Yazman            | PK60305 | arhti_share value                                                       | 0.676           | 0.743           |     0.676 |     0.743 |
| tehsil   | Yazman            | PK60305 | bivariate class (option-A tertiles)                                     | A3-C2           | A3-C3           |     0.676 |     0.743 |
| tehsil   | Liaqatpur         | PK62802 | arhti_share value                                                       | 0.63            | 0.46            |     0.630 |     0.460 |
| tehsil   | Liaqatpur         | PK62802 | arhti_share map class (option-A breaks)                                 | 4               | 3               |     0.630 |     0.460 |
| tehsil   | Liaqatpur         | PK62802 | bivariate class (option-A tertiles)                                     | A3-C2           | A3-C3           |     0.630 |     0.460 |
| tehsil   | Haroonabad        | PK60204 | LISA arhti_share | Queen | cluster_p01                                  | not significant | High-High       |     0.629 |     0.629 |
| tehsil   | Bahawalnagar      | PK60201 | Bivariate LISA arhti x lag(commercial) | Queen | cluster_p05            | High-High       | not significant |     0.574 |     0.574 |
| tehsil   | Haroonabad        | PK60204 | Bivariate LISA arhti x lag(commercial) | Queen | cluster_p05            | not significant | High-High       |     0.629 |     0.629 |
| tehsil   | Khairpur Tamewali | PK60304 | Bivariate LISA arhti x lag(commercial) | Queen | cluster_p05            | not significant | High-High       |     0.848 |     0.848 |
| tehsil   | Chishtian         | PK60202 | Bivariate LISA arhti x lag(commercial) | Queen | cluster_p01            | not significant | High-High       |     0.637 |     0.637 |
| tehsil   | Hasilpur          | PK60303 | Bivariate LISA arhti x lag(commercial) | Queen | cluster_p01            | not significant | High-High       |     0.792 |     0.792 |
| tehsil   | Murree            | PK63005 | Bivariate LISA arhti x lag(commercial) | Queen | cluster_p01            | Low-Low         | not significant |     0.000 |     0.000 |
| tehsil   | Jahanian          | PK61501 | Bivariate LISA arhti x lag(commercial) | kNN-5 (geodesic) | cluster_p05 | Low-High        | not significant |     0.093 |     0.093 |
| district | Bahawalnagar      | PK602   | arhti_share value                                                       | 0.635           | 0.644           |     0.635 |     0.644 |
| district | Bahawalnagar      | PK602   | bivariate class (option-A tertiles)                                     | A3-C2           | A3-C3           |     0.635 |     0.644 |
| district | Bahawalpur        | PK603   | arhti_share value                                                       | 0.519           | 0.499           |     0.519 |     0.499 |
| district | Bahawalpur        | PK603   | bivariate class (option-A tertiles)                                     | A3-C2           | A3-C3           |     0.519 |     0.499 |
| district | Rahim Yar Khan    | PK628   | arhti_share value                                                       | 0.322           | 0.249           |     0.322 |     0.249 |
| district | Lodhran           | PK619   | Bivariate LISA arhti x lag(commercial) | Queen | cluster_p01            | not significant | Low-High        |     0.092 |     0.092 |
| district | Lodhran           | PK619   | Bivariate LISA arhti x lag(commercial) | kNN-5 (geodesic) | cluster_p05 | not significant | Low-High        |     0.092 |     0.092 |
| district | Vehari            | PK636   | Bivariate LISA arhti x lag(commercial) | kNN-5 (geodesic) | cluster_p05 | Low-High        | not significant |     0.111 |     0.111 |

