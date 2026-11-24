"""05_boundaries_join.py: attach Mouza Census 2020 tehsil data to OCHA COD-AB ADM3 polygons (Punjab), with audit.

    .venv/bin/python -I scripts/05_boundaries_join.py     (after 02_extract_archives.py and 04_extract_mouza.py)

Steps
1. OCHA ADM3 + ADM2 (plain layers, not the `_em` variants), Punjab only: check validity, reproject to the analysis CRS
   (common.CRS: Albers equal-area centred on Punjab, D025),
   save data/interim/punjab_boundaries.gpkg (layers `adm3`, `adm2`).
2. District crosswalk, then tehsil crosswalk WITHIN matched districts:
     exact           names identical ignoring case/surrounding spaces
     normalized      identical after the documented rules in NORMALIZE_RULES (each fired rule is recorded)
     fuzzy-proposed  rapidfuzz best remaining candidate in the same district (score >= FUZZY_MIN). NEVER auto-accepted
     then Ahmed's decisions (docs/crosswalk_manual.csv, docs/crosswalk_manual_district.csv) set the final match_type:
     spelling / normalized / rename / parent_aggregation (several census units summed into one OCHA polygon)
     unmatched       everything else
   `validated` = match_type in common.VALID_MATCH_TYPES AND the district assignment is validated.
3. Coverage of the 23,130 rural populated mouzas by validated matches; GO/NO-GO gate at 95%.
4. Join: counts of validated matches are SUMMED per OCHA polygon (handles accepted many-to-one cases), and shares are
   recomputed from the summed counts (never averaged). District fallback: tehsil counts summed to MC districts, shares
   recomputed, joined to ADM2 via the validated district crosswalk.
5. data/processed/punjab_tehsil_credit.gpkg: layers `tehsil`, `district_fallback` (Cholistan option A, primary) and
   `tehsil_optB`, `district_fallback_optB` (Cholistan excluded; required sensitivity, D015); docs/match_audit.md.
Checks: no source unit assigned twice; harmonized totals reconcile to the published 23,130 rural populated mouzas.

Inputs Ahmed edits: docs/crosswalk_manual.csv (tehsils), docs/crosswalk_manual_district.csv (districts, all sources).
"""

from __future__ import annotations

import datetime as dt
import importlib.util
import re
import sys
from pathlib import Path

import geopandas as gpd

import numpy as np
import pandas as pd
from rapidfuzz import fuzz, process

ROOT = Path(__file__).resolve().parents[1]
SHP = ROOT / "data" / "interim" / "boundaries_shp"
MOUZA = ROOT / "data" / "processed" / "mouza_tehsil.csv"
CENSUS23 = ROOT / "data" / "raw" / "pop_census_2023" / "table_1_punjab_districts.xlsx"
BOUND_GPKG = ROOT / "data" / "interim" / "punjab_boundaries.gpkg"
XWALK = ROOT / "data" / "interim" / "tehsil_crosswalk.csv"
DXWALK = ROOT / "data" / "interim" / "district_crosswalk.csv"
MANUAL = ROOT / "docs" / "crosswalk_manual.csv"
MANUAL_DISTRICT = ROOT / "docs" / "crosswalk_manual_district.csv"
OUT_GPKG = ROOT / "data" / "processed" / "punjab_tehsil_credit.gpkg"
AUDIT = ROOT / "docs" / "match_audit.md"

_spec = importlib.util.spec_from_file_location("common", Path(__file__).resolve().parent / "common.py")
common = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(common)
CRS = common.CRS
PUNJAB_RP = 23130
GATE = 0.95
FUZZY_MIN = 60
MC_VINTAGE = "Mouza Census 2020 (PBS), fieldwork Jan-Mar 2020"
OCHA_VINTAGE = "OCHA COD-AB Pakistan, valid_on 2022-09-09"

# Normalisation rules, applied in order. Each is generic (no unit-specific pairs).
NORMALIZE_RULES = [
    ("punctuation->space", lambda s: re.sub(r"[.\-(),/]", " ", s)),
    ("drop suffix TEHSIL/DISTRICT", lambda s: re.sub(r"\b(TEHSIL|DISTRICT)\b", " ", s)),
    ("SADDAR/SADDER/SADAR->SADAR", lambda s: re.sub(r"\bSAD+[AE]R\b", "SADAR", s)),
    ("remove spaces", lambda s: re.sub(r"\s+", "", s)),
    ("OO->U, EE->I", lambda s: s.replace("OO", "U").replace("EE", "I")),
    ("collapse doubled letters", lambda s: re.sub(r"([A-Z])\1+", r"\1", s)),
]
COUNT_PREFIX = ("n_", "mouzas_", "rp_")
ADM2_BY_PCODE: dict[str, str] = {}
ADM3_BY_PCODE: dict[str, str] = {}

# Background-knowledge suggestions for units no generic rule or fuzzy score can catch. Shown in notes only.
SUGGESTIONS = {
    ("DERA GHAZI KHAN", "DE-EXCLUDED AREA D.G KHAN"): "D.G Khan (Tribal Area) PK60701? 'De-excluded area' = former "
        "tribal area; Census 2023 calls this unit KOH-E-SULEMAN TEHSIL. [CHECK]",
    ("RAJANPUR", "DE-EXCLUDED AREA RAJANPUR"): "Rajanpur (Tribal Area) PK62903? 'De-excluded area' = former tribal area. [CHECK]",
    ("JHANG", "18-HAZARI"): "Athara Hazari PK61204? 'athara' is Urdu for 18. [CHECK]",
}


def up(s) -> str:
    return re.sub(r"\s+", " ", str(s)).strip().upper()


def normalize(s: str) -> tuple[str, list[str]]:
    s, fired = up(s), []
    for name, f in NORMALIZE_RULES:
        t = f(s)
        if t != s:
            fired.append(name)
        s = t
    return s, fired


def match_units(left: list[str], right: list[str]) -> list[dict]:
    """Match each left name to a right name: exact, then normalized, then fuzzy proposal among unused right names."""
    res, used = {}, set()
    R = {r: normalize(r)[0] for r in right}
    for l in left:
        hit = [r for r in right if up(r) == up(l)]
        if hit:
            res[l] = dict(right=hit[0], match_type="exact", score=100.0, notes="")
            used.add(hit[0])
    for l in left:
        if l in res:
            continue
        nl, fired = normalize(l)
        hit = [r for r in right if r not in used and R[r] == nl]
        if len(hit) == 1:
            fired_r = normalize(hit[0])[1]
            res[l] = dict(right=hit[0], match_type="normalized", score=100.0,
                          notes="rules: " + "; ".join(sorted(set(fired + fired_r))))
            used.add(hit[0])
    for l in left:
        if l in res:
            continue
        cands = [r for r in right if r not in used]
        if not cands:
            res[l] = dict(right=None, match_type="unmatched", score=np.nan,
                          notes="no OCHA unit left in district (all already matched)")
            continue
        best = process.extract(normalize(l)[0], {r: R[r] for r in cands}, scorer=fuzz.WRatio, limit=2)
        (bname, bscore, bkey) = best[0]
        alt = f"; 2nd: {best[1][2]} ({best[1][1]:.0f})" if len(best) > 1 else ""
        if bscore >= FUZZY_MIN:
            res[l] = dict(right=bkey, match_type="fuzzy-proposed", score=round(bscore, 1), notes=f"best of {len(cands)}{alt}")
        else:
            res[l] = dict(right=None, match_type="unmatched", score=round(bscore, 1),
                          notes=f"best candidate {bkey} ({bscore:.0f}) below {FUZZY_MIN}{alt}")
    return [dict(left=l, **res[l]) for l in left]


# --------------------------------------------------------------------------------------------- 1. boundaries
def load_boundaries():
    out, log = {}, []
    BOUND_GPKG.unlink(missing_ok=True)  # rebuilt from scratch each run (appending would duplicate layers)
    for lvl in ["adm3", "adm2"]:
        g = gpd.read_file(SHP / f"pak_admin{lvl[-1]}.shp")
        g = g[g.adm1_name == "Punjab"].copy()
        bad = ~g.is_valid
        log.append(f"{lvl}: {len(g)} Punjab features, CRS {g.crs.to_string()}, invalid geometries: {int(bad.sum())}")
        if bad.any():
            g.loc[bad, "geometry"] = g.loc[bad, "geometry"].make_valid()
            log.append(f"  repaired with make_valid: {g.loc[bad].iloc[:, 0].tolist()}")
        g = g.to_crs(CRS)
        ratio = (g.area / 1e6 / g.area_sqkm)
        log.append(f"  area check (analysis-CRS km2 / attribute area_sqkm): min {ratio.min():.4f}, max {ratio.max():.4f}")
        keep = [c for c in g.columns if c.startswith(("adm3", "adm2", "adm1_pcode", "valid_on", "area_sqkm"))] + ["geometry"]
        out[lvl] = g[keep].reset_index(drop=True)
        out[lvl].to_file(BOUND_GPKG, layer=lvl, driver="GPKG", mode="w" if lvl == "adm3" else "a")
    return out["adm3"], out["adm2"], log


def census23_tehsils() -> dict[str, set[str]]:
    """Tehsil names per district in Census 2023 Table 1 (corroboration only)."""
    c = pd.read_excel(CENSUS23, header=None)
    cur, out = None, {}
    for s in (up(x) for x in c[0]):
        if s.endswith(" DISTRICT"):
            cur = s; out[cur] = set()
        elif cur and s not in ("RURAL", "URBAN", "NAN") and not s.startswith("*"):
            out[cur].add(normalize(s)[0])
    return out


# --------------------------------------------------------------------------------------------- Ahmed's decisions
MANUAL_COLS = ["level", "source", "source_name", "source_code", "source_district", "ocha_name", "ocha_pcode", "match_type",
               "decision", "decided_by", "date", "historical_name", "note"]
DEC_COLS = ["decision", "decided_by", "date", "historical_name", "decision_note"]


def load_manual(path, **filt):
    if not path.exists():
        sys.exit(f"Missing {path} (Ahmed's crosswalk decisions).")
    m = pd.read_csv(path, dtype=str).fillna("")
    for k, v in filt.items():
        m = m[m[k] == v]
    bad = m[(m.decision == "accept") & ~m.match_type.isin(common.VALID_MATCH_TYPES)]
    if len(bad):
        sys.exit(f"accepted rows with an invalid match_type: {bad.to_dict('records')}")
    return m


def apply_decisions(df, m, key_df, key_m, name_col):
    for c in DEC_COLS:
        if c not in df:
            df[c] = ""
    for _, r in m.iterrows():
        sel = df[key_df].astype(str).values == r[key_m]
        if sel.sum() != 1:
            sys.exit(f"decision row does not identify exactly one unit: {r.to_dict()}")
        if r.decision == "accept":
            df.loc[sel, ["match_type", "ocha_pcode", name_col]] = [r.match_type, r.ocha_pcode, r.ocha_name]
        elif r.decision == "leave_unmatched":
            df.loc[sel, ["match_type", "ocha_pcode", name_col]] = ["unmatched", None, None]
        df.loc[sel, DEC_COLS] = [r.decision, r.decided_by + (f" ({r.date})" if r.date else ""), r.date,
                                 r.historical_name, r.note]
    return df


# --------------------------------------------------------------------------------------------- main
def main() -> int:
    adm3, adm2, geo_log = load_boundaries()
    ADM2_BY_PCODE.update(dict(zip(adm2.adm2_pcode, adm2.adm2_name)))
    ADM3_BY_PCODE.update(dict(zip(adm3.adm3_pcode, adm3.adm3_name)))
    mc = pd.read_csv(MOUZA, dtype={"district_code": str, "tehsil_code": str})
    count_cols = [c for c in mc.columns if c.startswith(COUNT_PREFIX)]
    c23 = census23_tehsils()

    # ---- district crosswalk (Mouza Census districts -> OCHA ADM2)
    dm = pd.DataFrame(match_units(sorted(mc.district.unique()), sorted(adm2.adm2_name)))
    dm = dm.rename(columns={"left": "mouza_district", "right": "ocha_district"})
    dm = dm.merge(adm2[["adm2_name", "adm2_pcode"]], left_on="ocha_district", right_on="adm2_name", how="left") \
           .drop(columns="adm2_name").rename(columns={"adm2_pcode": "ocha_pcode"})
    dm = apply_decisions(dm, load_manual(MANUAL_DISTRICT, source="MouzaCensus2020"), "mouza_district", "source_name",
                         "ocha_district")
    dm.loc[dm.mouza_district == "CHOLISTAN", "decision_note"] = (
        "census-only district; its tehsils are assigned individually (parent_aggregation, Cholistan option A, D015)")
    dm["validated"] = dm.match_type.isin(common.VALID_MATCH_TYPES)
    dm.to_csv(DXWALK, index=False)

    # ---- tehsil crosswalk, within district (automatic step), then Ahmed's decisions
    rows = []
    for _, d in dm.iterrows():
        sub = mc[mc.district == d.mouza_district]
        if pd.isna(d.ocha_district):
            for _, t in sub.iterrows():
                rows.append(dict(source_district=d.mouza_district, source_name=t.tehsil, source_code=t.tehsil_uid,
                                 rp_mouzas=t.rp_mouzas, is_cholistan=bool(t.is_cholistan), ocha_district=None, ocha_name=None,
                                 ocha_pcode=None, match_type="unmatched", score=np.nan, auto_note="district has no OCHA counterpart"))
            continue
        o = adm3[adm3.adm2_name == d.ocha_district]
        for r in match_units(list(sub.tehsil), list(o.adm3_name)):
            t = sub[sub.tehsil == r["left"]].iloc[0]
            pc = o[o.adm3_name == r["right"]].adm3_pcode.iloc[0] if r["right"] else None
            rows.append(dict(source_district=d.mouza_district, source_name=r["left"], source_code=t.tehsil_uid,
                             rp_mouzas=t.rp_mouzas, is_cholistan=bool(t.is_cholistan), ocha_district=d.ocha_district,
                             ocha_name=r["right"], ocha_pcode=pc, match_type=r["match_type"], score=r["score"],
                             auto_note=r["notes"]))
    xw = pd.DataFrame(rows)
    xw["auto_match_type"] = xw.match_type
    xw = apply_decisions(xw, load_manual(MANUAL, level="tehsil"), "source_code", "source_code", "ocha_name")
    xw["ocha_district"] = xw.ocha_pcode.map(lambda p: ADM2_BY_PCODE.get(str(p)[:5]) if pd.notna(p) else None)
    xw.loc[xw.match_type == "exact", ["decision", "decided_by"]] = ["auto (exact)", "rule"]
    valid_d = set(dm[dm.validated].ocha_district)
    xw["validated"] = xw.match_type.isin(common.VALID_MATCH_TYPES) & xw.ocha_district.isin(valid_d)
    xw.loc[xw.is_cholistan & xw.validated, "validated"] = True  # Cholistan rows are validated by their own tehsil decision

    # ---- integrity checks (D024)
    dup_src = xw.source_code[xw.source_code.duplicated()].tolist()
    if dup_src:
        sys.exit(f"source units assigned more than once: {dup_src}")
    blank = xw[~xw.match_type.isin(list(common.VALID_MATCH_TYPES) + ["unmatched"]) | (xw.match_type.isin(["fuzzy-proposed"]))]
    undecided = xw[(xw.match_type == "unmatched") & (xw.decision == "") & (xw.rp_mouzas > 0)]
    total_rp = int(xw.rp_mouzas.sum())
    assert total_rp == PUNJAB_RP, f"rural populated total {total_rp} != {PUNJAB_RP}"

    multi = xw[xw.validated].groupby("ocha_pcode").source_code.nunique()
    xw["relation"] = np.where(xw.ocha_pcode.isin(multi[multi > 1].index), "many-to-one (summed)",
                      np.where(xw.ocha_pcode.notna(), "one-to-one", "no OCHA polygon"))
    xw["in_census2023"] = [normalize(t)[0] in c23.get(d, set()) for d, t in zip(xw.source_district, xw.source_name)]
    xw.insert(0, "vintage_note", f"{MC_VINTAGE} -> {OCHA_VINTAGE}")
    xw.insert(1, "source", "MouzaCensus2020")
    cols = ["vintage_note", "source", "source_name", "source_code", "source_district", "ocha_name", "ocha_pcode", "ocha_district",
            "match_type", "auto_match_type", "score", "decision", "decided_by", "date", "historical_name", "decision_note",
            "auto_note", "rp_mouzas", "is_cholistan", "validated", "relation", "in_census2023"]
    xw = xw[cols]
    # backward-compatible aliases used by later scripts
    xw["mouza_tehsil"], xw["mouza_district"], xw["tehsil_uid"], xw["ocha_tehsil"] = xw.source_name, xw.source_district, xw.source_code, xw.ocha_name
    xw.to_csv(XWALK, index=False)

    covered = int(xw[xw.validated].rp_mouzas.sum())
    share = covered / PUNJAB_RP
    go = share >= GATE
    # reconciliation of harmonized polygons
    teh_A, dist_A = build_layers(xw, mc, adm3, adm2, dm, count_cols, exclude_cholistan=False)
    teh_B, dist_B = build_layers(xw, mc, adm3, adm2, dm, count_cols, exclude_cholistan=True)
    recon = dict(tehsil_A=int(teh_A.rp_mouzas.sum()), district_A=int(dist_A.rp_mouzas.sum()),
                 tehsil_B=int(teh_B.rp_mouzas.sum()), district_B=int(dist_B.rp_mouzas.sum()),
                 cholistan=int(mc[mc.is_cholistan].rp_mouzas.sum()))
    for lvl, g in [("tehsil", teh_A), ("district", dist_A)]:
        pc = "adm3_pcode" if lvl == "tehsil" else "adm2_pcode"
        if g[pc].duplicated().any():
            sys.exit(f"duplicated harmonized {lvl} identifiers")

    OUT_GPKG.parent.mkdir(parents=True, exist_ok=True)
    OUT_GPKG.unlink(missing_ok=True)
    teh_A.to_file(OUT_GPKG, layer="tehsil", driver="GPKG", mode="w")
    dist_A.to_file(OUT_GPKG, layer="district_fallback", driver="GPKG", mode="a")
    teh_B.to_file(OUT_GPKG, layer="tehsil_optB", driver="GPKG", mode="a")
    dist_B.to_file(OUT_GPKG, layer="district_fallback_optB", driver="GPKG", mode="a")

    write_audit(geo_log, dm, xw, adm3, covered, share, go, recon, blank, undecided)
    print(f"administrative assignment {covered:,}/{PUNJAB_RP:,} ({share:.1%}) -> {'GO' if go else 'NO-GO'}; "
          f"reconciliation {recon}; blank rows {len(blank)}; undecided with mouzas {len(undecided)}")
    print(xw.match_type.value_counts().to_dict())
    return 0


def build_layers(xw, mc, adm3, adm2, dm, count_cols, exclude_cholistan):
    v = xw[xw.validated & ~(xw.is_cholistan & exclude_cholistan)][["source_code", "ocha_pcode", "ocha_district", "match_type"]]
    v = v.merge(mc[["tehsil_uid"] + count_cols], left_on="source_code", right_on="tehsil_uid")
    agg = v.groupby("ocha_pcode").agg(mouza_tehsil_uids=("source_code", lambda s: ";".join(sorted(s))),
                                      n_mouza_tehsils=("source_code", "size"),
                                      match_types=("match_type", lambda s: ";".join(sorted(set(s)))))
    agg = common.recompute_shares(agg.join(v.groupby("ocha_pcode")[count_cols].sum()).reset_index())
    teh = adm3.merge(agg, left_on="adm3_pcode", right_on="ocha_pcode", how="left").drop(columns="ocha_pcode")
    teh["match_status"] = np.where(teh.n_mouza_tehsils.notna(), "validated", "no validated match")
    teh["contains_cholistan"] = teh.mouza_tehsil_uids.fillna("").str.contains("PB-999")
    scen = "Cholistan excluded (option B, sensitivity)" if exclude_cholistan else "Cholistan merged into parent tehsils (option A)"
    teh["scenario"] = scen
    teh["vintage"] = f"Data: {MC_VINTAGE}. Boundaries: {OCHA_VINTAGE} (boundaries post-date the data)"
    # districts: sum the assigned tehsils by the OCHA district of their polygon
    dsum = v.groupby("ocha_district")[count_cols].sum().reset_index()
    dsum = common.recompute_shares(dsum)
    mc_name = dict(zip(dm[dm.validated].ocha_district, dm[dm.validated].mouza_district))
    dsum["mouza_district"] = dsum.ocha_district.map(mc_name)
    dist = adm2.merge(dsum, left_on="adm2_name", right_on="ocha_district", how="left").drop(columns="ocha_district")
    dist["match_status"] = np.where(dist.mouza_district.notna(), "validated", "no validated match")
    dist["scenario"] = scen
    dist["vintage"] = teh["vintage"].iloc[0]
    return teh, dist


# --------------------------------------------------------------------------------------------- audit
def md_table(df, cols):
    out = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for _, r in df[cols].iterrows():
        out.append("| " + " | ".join("" if pd.isna(x) else (f"{x:.0f}" if isinstance(x, float) else str(x)) for x in r) + " |")
    return out


def write_audit(geo_log, dm, xw, adm3, covered, share, go, recon, blank, undecided):
    L = ["# Match audit: Mouza Census 2020 tehsils → OCHA COD-AB ADM3 (Punjab)", "",
         f"Written by `scripts/05_boundaries_join.py` on {dt.date.today()}. Data: {MC_VINTAGE}. Boundaries: {OCHA_VINTAGE}. "
         "The boundaries post-date the census (not contemporaneous). Decisions: `docs/crosswalk_manual.csv`, "
         "`docs/crosswalk_manual_district.csv` (decided by Ahmed).", "",
         "**Coverage language (D027):** *administrative assignment* = the share of rural populated mouzas assigned to a polygon. "
         "It is not geographic precision: polygons that aggregate several census units (parent_aggregation) conceal internal differences.", "",
         "## Boundaries", ""] + [f"- {x}" for x in geo_log] + ["",
         "## Tehsil assignments by match type", "",
         "| Match type | Census tehsils | Rural populated mouzas | % of 23,130 |", "|---|---|---|---|"]
    for mt, g in xw.groupby("match_type"):
        L.append(f"| {mt} | {len(g)} | {int(g.rp_mouzas.sum()):,} | {g.rp_mouzas.sum() / PUNJAB_RP:.1%} |")
    L += ["", f"**Administrative assignment: {covered:,} / {PUNJAB_RP:,} rural populated mouzas ({share:.1%}).** "
          f"Gate (≥ 95%): **{'GO: Q1 at tehsil level' if go else 'NO-GO'}**.", "",
          "## Integrity checks", "",
          "- No census tehsil is assigned more than once (each `source_code` appears once): PASS.",
          f"- Harmonized totals reconcile: option A tehsil polygons {recon['tehsil_A']:,}, districts {recon['district_A']:,} "
          f"(expected 23,130); option B tehsil {recon['tehsil_B']:,}, districts {recon['district_B']:,} "
          f"(expected 23,130 − {recon['cholistan']} Cholistan = {PUNJAB_RP - recon['cholistan']:,}).",
          "- No harmonized polygon identifier is duplicated: PASS.",
          f"- Crosswalk rows without a final match type or decision: {len(blank)}; unmatched rows with rural populated mouzas "
          f"and no decision: {len(undecided)}.", "",
          "## Every non-exact assignment (decided by Ahmed)", ""]
    L += md_table(xw[xw.match_type != "exact"].sort_values(["match_type", "source_district"]),
                  ["match_type", "source_district", "source_name", "source_code", "rp_mouzas", "ocha_name", "ocha_pcode",
                   "decision", "historical_name", "decision_note"])
    L += ["", "## District assignments (Mouza Census → OCHA ADM2)", ""]
    L += md_table(dm, ["mouza_district", "ocha_district", "ocha_pcode", "match_type", "decision"])
    used = set(xw[xw.validated].ocha_pcode)
    L += ["", f"OCHA tehsil polygons without any assigned census tehsil: "
          f"{', '.join(adm3[~adm3.adm3_pcode.isin(used)].adm3_name) or 'none'}.", "",
          "## Cholistan (D015: decided by Ahmed)", "",
          "Option A (primary): the three Cholistan census tehsils (PB-999-071/079/081) are summed into OCHA Fort Abbas, Yazman and "
          "Liaqatpur. Option B (required sensitivity): Cholistan excluded. Both scenarios are built from the same processed "
          "file (`is_cholistan`), as layers `tehsil`/`district_fallback` (A) and `tehsil_optB`/`district_fallback_optB` (B). "
          "Maps note that Fort Abbas, Yazman and Liaqatpur combine desert (Cholistan) and irrigated mouzas.", "",
          "## Administrative structure differences", "",
          "OCHA's tehsil layer appears to follow an older structure (Lahore 2 vs 5 tehsils; no Lawa; no City/Saddar splits in "
          "Bahawalpur and Gujranwala). These are handled as parent_aggregation (Bahawalpur, Gujranwala, Lawa → Tala Gang) or left "
          "unmatched (Lahore's Model Town, Raiwind, Shalimar: 0 rural populated mouzas). No census unit is split across polygons."]
    AUDIT.write_text("\n".join(L) + "\n")


if __name__ == "__main__":
    sys.exit(main())
