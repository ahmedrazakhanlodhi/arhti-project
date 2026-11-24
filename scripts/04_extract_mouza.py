"""04_extract_mouza.py: tehsil-level dataset from the Punjab Mouza Census 2020.

    .venv/bin/python -I scripts/04_extract_mouza.py      (run 02_extract_archives.py first)

Source
- PRIMARY: mouza-level records in `Mouza Census-2020.xlsx` (inside data/raw/mouza_census_2020/mc2020.excel-1.rar,
  extracted to data/interim/ by 02_extract_archives.py). The RAR holds record-level data, not pre-built tables, so the
  report's tables are rebuilt here by counting mouzas per tehsil.
- VALIDATION: the published Punjab report PDF (data/raw/...punjab_report.pdf). Tables 1.1, 6.3, 6.7, 8.1 and 8.2 are
  parsed from its text layer for every admin row (province/division/district/tehsil) and compared with the Excel counts.

Outputs
- data/processed/mouza_tehsil.csv       one row per tehsil (Punjab only; ICT excluded; Cholistan rows flagged)
- data/processed/mouza_tehsil_long.csv  long format, all admin levels, Excel value vs published value
- data/interim/mouza_report_text.txt    text layer of the PDF (cache, re-created each run)
- data/interim/mouza_published_rows.csv parsed published rows
- docs/validation_mouza.md              validation report

Definitions (see docs/variable_dictionary.md)
- Rural populated mouza (the report's denominator) = status Rural (1) or Partly urban (3), or Forest (4) with >= 1
  settlement. This reproduces the published Punjab total of 23,130 exactly.
- Unit keys are PBS codes (dist_code, teh_code). Names are only whitespace-normalised (strip + collapse spaces), never
  fuzzy-matched.
"""

from __future__ import annotations

import datetime as dt
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pypdfium2 as pdfium

ROOT = Path(__file__).resolve().parents[1]
XLSX = ROOT / "data" / "interim" / "mouza_census_2020_excel" / "Mouza Census-2020.xlsx"
PDF = ROOT / "data" / "raw" / "mouza_census_2020" / "mouza_census_2020_punjab_report.pdf"
OUT_WIDE = ROOT / "data" / "processed" / "mouza_tehsil.csv"
OUT_LONG = ROOT / "data" / "processed" / "mouza_tehsil_long.csv"
TXT_CACHE = ROOT / "data" / "interim" / "mouza_report_text.txt"
PUB_CSV = ROOT / "data" / "interim" / "mouza_published_rows.csv"
VAL_MD = ROOT / "docs" / "validation_mouza.md"
VINTAGE = "Mouza Census 2020 (PBS), fieldwork Jan-Mar 2020"

# Published figures supplied by Ahmed for the mandatory checks.
EXPECTED_PUNJAB = {"rp_mouzas": 23130, "n_ztbl": 16989, "n_coop": 5753, "n_commercial": 8832, "n_mfb": 3526,
                   "n_arhti": 7290, "n_others": 9418}
EXPECTED_BAHAWALNAGAR_RP = 1043

BANDS = ["1_10", "11_25", "26_50", "51plus"]


def norm(s) -> str:
    return re.sub(r"\s+", " ", str(s)).strip().upper()


def band(km: float) -> str | None:
    if pd.isna(km) or km < 1:
        return None
    return "1_10" if km <= 10 else "11_25" if km <= 25 else "26_50" if km <= 50 else "51plus"


# --------------------------------------------------------------------------------------------- Excel (primary)
def load_excel() -> pd.DataFrame:
    if not XLSX.exists():
        sys.exit(f"Missing {XLSX}. Run scripts/02_extract_archives.py first.")
    codes = pd.read_excel(XLSX, header=None, skiprows=2, nrows=1, dtype=str).iloc[0].tolist()
    df = pd.read_excel(XLSX, header=None, skiprows=3, dtype=str)
    df.columns = codes
    for c in ["prv_desc", "div_desc", "dist_desc", "teh_desc", "vil_desc"]:
        df[c] = df[c].map(norm)
    return df


def mouza_indicators(p: pd.DataFrame, anomalies: list) -> pd.DataFrame:
    """One row per Punjab mouza with 0/1 indicators for every published category."""
    num = lambda c: pd.to_numeric(p[c], errors="coerce")
    status, settl = p["P1Q09"], num("P1Q10")
    m = pd.DataFrame(index=p.index)
    m["mouzas_total"] = 1
    m["mouzas_rural"] = (status == "1").astype(int)
    m["mouzas_urban"] = (status == "2").astype(int)
    m["mouzas_partly_urban"] = (status == "3").astype(int)
    m["mouzas_forest_populated"] = ((status == "4") & (settl > 0)).astype(int)
    m["mouzas_forest_unpopulated"] = ((status == "4") & ~(settl > 0)).astype(int)
    m["mouzas_unpopulated"] = (status == "5").astype(int)
    rp = m["mouzas_rural"] + m["mouzas_partly_urban"] + m["mouzas_forest_populated"]
    m["rp_mouzas"] = rp
    bad = status[~status.isin(list("12345"))]
    if len(bad):
        anomalies.append(f"{len(bad)} mouzas have status P1Q09 outside 1-5: {bad.value_counts(dropna=False).to_dict()}")

    # Table 8.1: multiple-response; column holds its own code when ticked, blank otherwise.
    credit = {"n_ztbl": ("P8Q011", "1"), "n_coop": ("P8Q012", "2"), "n_commercial": ("P8Q013", "3"),
              "n_mfb": ("P8Q014", "4"), "n_ngo": ("P8Q015", "5"), "n_rsp": ("P8Q016", "6"),
              "n_govt": ("P8Q017", "7"), "n_arhti": ("P8Q018", "8"), "n_others": ("P8Q019", "9")}
    for var, (col, code) in credit.items():
        v = p[col]
        odd = v[v.notna() & (v != code) & (rp == 1)]
        if len(odd):
            anomalies.append(f"{col} ({var}): {len(odd)} rural-populated mouzas hold a value other than '{code}': "
                             f"{odd.value_counts().to_dict()}")
        m[var] = (v.notna() & (rp == 1)).astype(int)

    # Tables 8.2 / 6.7: yes(1) / no(2) + distance in km when "no".
    def yes_no_distance(prefix, yn_col, km_col, label):
        yn, km = p[yn_col], num(km_col)
        r = rp == 1
        m[f"n_{prefix}_in_mouza"] = ((yn == "1") & r).astype(int)
        for b in BANDS:
            m[f"n_{prefix}_{b}"] = ((yn == "2") & r & (km.map(band) == b)).astype(int)
        m[f"_{prefix}_km_no"] = np.where((yn == "2") & r, km, np.nan)
        miss = r & ~yn.isin(["1", "2"])
        no_bad_km = r & (yn == "2") & ~(km >= 1)
        yes_km = r & (yn == "1") & (km > 0)
        m[f"n_{prefix}_unclassified"] = (miss | no_bad_km).astype(int)
        if miss.sum():
            anomalies.append(f"{label}: {int(miss.sum())} rural-populated mouzas with yes/no blank or invalid "
                             f"({yn[miss].value_counts(dropna=False).to_dict()})")
        if no_bad_km.sum():
            anomalies.append(f"{label}: {int(no_bad_km.sum())} mouzas answered 'No' but distance is blank or < 1 km "
                             f"({km[no_bad_km].value_counts(dropna=False).to_dict()})")
        if yes_km.sum():
            anomalies.append(f"{label}: {int(yes_km.sum())} mouzas answered 'Yes' but give a distance > 0 km")

    yes_no_distance("onlinebank", "P8Q021", "P8Q022", "Table 8.2 online commercial bank")
    yes_no_distance("mkt_livestock", "P6Q1311", "P6Q1312", "Table 6.7 livestock market")
    yes_no_distance("mkt_grain", "P6Q1321", "P6Q1322", "Table 6.7 grain market")
    yes_no_distance("mkt_fruitveg", "P6Q1331", "P6Q1332", "Table 6.7 fruit/vegetable market")

    # Table 6.3: road type to mouza (1 metalled, 2 cemented, 3 bricked, 4 mud/kacha) + km to metalled road.
    road, km = p["P6Q041"], num("P6Q042")
    r = rp == 1
    for var, code in [("n_road_mud", "4"), ("n_road_bricked", "3"), ("n_road_cemented", "2"), ("n_road_metalled", "1")]:
        m[var] = ((road == code) & r).astype(int)
    for b in BANDS:
        m[f"n_metroad_{b}"] = (r & (km.map(band) == b)).astype(int)
    m["_metroad_km"] = np.where(r & (km >= 1), km, np.nan)
    odd = r & ~road.isin(list("1234"))
    if odd.sum():
        anomalies.append(f"Table 6.3: {int(odd.sum())} rural-populated mouzas with road type blank/invalid")
    nonmud_km = r & (road != "4") & (km >= 1)
    if nonmud_km.sum():
        anomalies.append(f"Table 6.3: {int(nonmud_km.sum())} non-mud-road mouzas report a distance to metalled road")
    zero_km = r & (km == 0)
    if zero_km.sum():
        anomalies.append(f"Table 6.3: {int(zero_km.sum())} rural-populated mouzas have distance to metalled road = 0 "
                         f"(road types {road[zero_km].value_counts().to_dict()}); not placed in any band "
                         f"(the published table has no 0 band)")
    return m


ID = ["division_code", "division", "district_code", "district", "tehsil_code", "tehsil"]


def aggregate(p: pd.DataFrame, m: pd.DataFrame) -> pd.DataFrame:
    ids = pd.DataFrame({"division_code": p["div_code"], "division": p["div_desc"], "district_code": p["dist_code"],
                        "district": p["dist_desc"], "tehsil_code": p["teh_code"], "tehsil": p["teh_desc"]})
    d = pd.concat([ids, m], axis=1)
    keys = ["division_code", "district_code", "tehsil_code"]
    # Names must be unique per code after whitespace normalisation.
    for k, name in [(["division_code"], "division"), (["division_code", "district_code"], "district"), (keys, "tehsil")]:
        multi = d.groupby(k)[name].nunique()
        if (multi > 1).any():
            sys.exit(f"Code {k} maps to several {name} names: {multi[multi > 1]}")
    sums = [c for c in m.columns if not c.startswith("_")]
    g = d.groupby(keys)
    out = g[sums].sum()
    for c in [c for c in m.columns if c.startswith("_")]:
        out["avg" + c] = g[c].mean()  # mean km among mouzas without the facility (for comparison with published avg)
    names = g[["division", "district", "tehsil"]].first()
    return names.join(out).reset_index()[ID + sums + [c for c in out.columns if c.startswith("avg_")]]


# --------------------------------------------------------------------------------------------- PDF (validation)
def pdf_lines() -> list[str]:
    doc = pdfium.PdfDocument(str(PDF))
    text = "".join(f"\n=====PAGE {i + 1}=====\n" + doc[i].get_textpage().get_text_range() for i in range(len(doc)))
    TXT_CACHE.write_text(text)
    return text.splitlines()


def section(lines, start_pat, end_pat):
    """Lines from the page holding the table's first title to the page before the next table's first title.
    In this PDF's text layer a page's data rows come BEFORE its title block, so cut at page markers."""
    page_start = lambda i: max(k for k in range(i + 1) if lines[k].startswith("=====PAGE"))
    s = page_start(next(i for i, l in enumerate(lines) if re.match(start_pat, l)))
    e = page_start(next(i for i, l in enumerate(lines[s:], s) if re.match(end_pat, l)))
    return lines[s:e], s


NUMTOK = re.compile(r"^(\d[\d,]*|-)$")


def nums(tokens):
    return [0 if t == "-" else int(t.replace(",", "")) for t in tokens]


OTHER_PROVINCES = ("PAKISTAN", "KHYBER PAKHTUNKHWA", "SINDH", "BALOCHISTAN")


def classify(name, state):
    """Track hierarchy; return level. Rows under another province's header (the Punjab PDF reprints Sindh and
    Balochistan pages inside Table 8.2) and ICT rows are tagged and later excluded."""
    if name == "PUNJAB":
        state.update(division=None, district=None, skip=False); return "province"
    if name in OTHER_PROVINCES:
        state.update(division=None, district=name, skip=True); return "other_province"
    if name.startswith("ISLAMABAD"):
        state.update(division=None, district="ISLAMABAD", skip=True); return "ict"
    if state.get("skip"):
        return "other_province"
    if name.endswith(" DIVISION"):
        state.update(division=name, district=None); return "division"
    if name.endswith(" DISTRICT") or name == "CHOLISTAN":
        state["district"] = name; return "district"
    return "tehsil"


TABLE_SPECS = {
    # table: (start regex, end regex, columns after the name)
    "1.1": (r"^TABLE 1\.1 :", r"^TABLE 1\.2 :",
            ["qanungo_circles", "patwar_circles", "mouzas_total", "mouzas_rural", "mouzas_urban", "mouzas_partly_urban",
             "mouzas_forest_populated", "mouzas_forest_unpopulated", "mouzas_unpopulated", "rp_mouzas"]),
    "6.3": (r"^TABLE 6\.3:", r"^TABLE 6\.4:",
            ["rp_mouzas", "n_road_mud", "n_road_bricked", "n_road_cemented", "n_road_metalled", "avg_metroad_km",
             "n_metroad_1_10", "n_metroad_11_25", "n_metroad_26_50", "n_metroad_51plus"]),
    "8.1": (r"^TABLE 8\.1 :", r"^TABLE 8\.2 :",
            ["rp_mouzas", "n_ztbl", "n_coop", "n_commercial", "n_mfb", "n_ngo", "n_rsp", "n_govt", "n_arhti", "n_others"]),
}
FAC_SPECS = {
    "6.7": (r"^TABLE 6\.7:", r"^TABLE 6\.8 :",
            {"LIVESTOCK MARKET": "mkt_livestock", "GRAINS MARKET": "mkt_grain", "FRUITS/VEGETABLE": "mkt_fruitveg"}),
    "8.2": (r"^TABLE 8\.2 :", r"^TABLE 8\.3 :",
            {"POST OFFICE": "postoffice", "CONCILITORY COMMITTEE": "conciliatory", "POLICE STATION / POST/ CHOWKI": "police",
             "ON-LINE COMMERCIAL BANK": "onlinebank"}),
}


def parse_published(lines) -> tuple[pd.DataFrame, list[str]]:
    rows, problems = [], []
    for tab, (sp, ep, cols) in TABLE_SPECS.items():
        sec, off = section(lines, sp, ep)
        state = {"division": None, "district": None}
        for j, line in enumerate(sec):
            toks = line.split()
            if tab == "1.1":
                k = len(toks)
                while k and NUMTOK.match(toks[k - 1]):
                    k -= 1
                name, vals = norm(" ".join(toks[:k])), toks[k:]
                if not name or name.startswith("PAKISTAN BUREAU") or not re.search(r"\d", line):
                    continue
                if len(vals) < 9:
                    # Rows whose numbers are glued together in the text layer (e.g. "-14", "-2 373") end up here.
                    if len(toks) - k >= 3 or re.search(r"\s-\d|\d-\s", line):
                        problems.append(f"T{tab} line {off + j + 1}: numbers merged/unreadable, row NOT compared: {line[:100]}")
                    continue
                level = classify(name, state)
                if level != "tehsil":    # province/division/district/ICT rows carry "number of districts" first
                    vals = vals[1:]
                if len(vals) == 9:       # fully urban unit: the rural-populated column is printed blank
                    vals = vals + [None]
                if len(vals) != 10:
                    problems.append(f"T{tab} line {off + j + 1}: unexpected {len(vals)} numbers: {line[:100]}")
                    continue
                for c, v in zip(cols, vals):
                    rows.append(dict(table=tab, level=level, division=state["division"], district=state["district"],
                                     unit=name, variable=c, published=None if v is None else nums([v])[0]))
                continue
            else:
                if " NUMBER " not in f" {line} ":
                    continue
                name, rest = line.split(" NUMBER ", 1) if " NUMBER " in line else ("", line)
                name, vals = norm(name), rest.split()
                level = classify(name, state) if name else ("other_province" if state.get("skip") else "tehsil")
                if level in ("ict", "other_province"):
                    continue
                if not name or len(vals) != len(cols) or not all(NUMTOK.match(v) for v in vals):
                    problems.append(f"T{tab} line {off + j + 1}: cannot parse: {line[:120]}"); continue
            for c, v in zip(cols, nums(vals)):
                rows.append(dict(table=tab, level=level, division=state["division"], district=state["district"],
                                 unit=name, variable=c, published=v))
    for tab, (sp, ep, facs) in FAC_SPECS.items():
        sec, off = section(lines, sp, ep)
        state = {"division": None, "district": None}
        pat = re.compile(r"^(?P<name>.*?)\s*(?P<fac>" + "|".join(re.escape(f) for f in facs) + r")\s+NUMBER\s+(?P<n>.+)$")
        for j, line in enumerate(sec):
            mm = pat.match(line.strip())
            if not mm:
                if " NUMBER " in line and not state.get("skip"):
                    problems.append(f"T{tab} line {off + j + 1}: cannot parse: {line[:120]}")
                continue
            if mm["name"].strip():
                state["level"] = classify(norm(mm["name"]), state)
                state["unit"] = norm(mm["name"])
            if state.get("level") in ("ict", "other_province", None):
                continue
            vals = mm["n"].split()
            if len(vals) != 7 or not all(NUMTOK.match(v) for v in vals):
                problems.append(f"T{tab} line {off + j + 1}: bad numbers: {line[:120]}"); continue
            pre = facs[mm["fac"]]
            cols = ["rp_mouzas", f"n_{pre}_in_mouza", f"avg_{pre}_km_no"] + [f"n_{pre}_{b}" for b in BANDS]
            for c, v in zip(cols, nums(vals)):
                if c == "rp_mouzas":
                    c = f"rp_mouzas__{pre}"
                rows.append(dict(table=tab, level=state["level"], division=state["division"], district=state["district"],
                                 unit=state["unit"], variable=c, published=v))
    pub = pd.DataFrame(rows)
    pub.loc[pub.level.isin(["division", "province"]), "district"] = None
    pub.loc[pub.level == "province", "division"] = None
    # Duplicate keys within a table would mean the parser mis-tracked the hierarchy.
    dup = pub.duplicated(["table", "level", "district", "unit", "variable"], keep=False)
    if dup.any():
        problems.append(f"{dup.sum()} duplicated published keys, e.g. {pub[dup].head(3).to_dict('records')}")
    return pub, problems


# --------------------------------------------------------------------------------------------- main
def main() -> int:
    anomalies: list[str] = []
    df = load_excel()
    n_ict = int((df.prv_desc == "ISLAMABAD CAPITAL TERRITORY").sum())
    p = df[df.prv_desc == "PUNJAB"].copy()
    m = mouza_indicators(p, anomalies)
    teh = aggregate(p, m)

    count_cols = [c for c in teh.columns if c.startswith(("n_", "mouzas_", "rp_"))]
    avg_cols = [c for c in teh.columns if c.startswith("avg_")]

    # Aggregate levels from the same mouza records (sum of tehsils).
    dist = teh.groupby(["division", "district"], as_index=False)[count_cols].sum()
    div = teh.groupby(["division"], as_index=False)[count_cols].sum()
    prov = teh[count_cols].sum().to_frame().T
    ids = pd.DataFrame({"district": p.dist_desc, "division": p.div_desc})
    md = pd.concat([ids, m[[c for c in m.columns if c.startswith("_")]]], axis=1)
    for c in [c for c in m.columns if c.startswith("_")]:
        dist = dist.merge(md.groupby(["division", "district"])[c].mean().rename("avg" + c).reset_index(), how="left")
        div = div.merge(md.groupby("division")[c].mean().rename("avg" + c).reset_index(), how="left")
        prov["avg" + c] = md[c].mean()

    # Shares (denominator = rural populated mouzas). Never summed across institutions.
    def add_shares(t):
        rp = t["rp_mouzas"].replace(0, np.nan)
        for s in ["arhti", "ztbl", "commercial", "coop", "mfb"]:
            t[f"{s}_share"] = t[f"n_{s}"] / rp
        for pre in ["onlinebank", "mkt_grain", "mkt_livestock", "mkt_fruitveg"]:
            t[f"{pre}_in_mouza_share"] = t[f"n_{pre}_in_mouza"] / rp
            t[f"{pre}_51plus_share"] = t[f"n_{pre}_51plus"] / rp
        t["road_metalled_share"] = t["n_road_metalled"] / rp
        t["road_mud_share"] = t["n_road_mud"] / rp
        t["metroad_51plus_share"] = t["n_metroad_51plus"] / rp
        return t

    teh = add_shares(teh)
    share_cols = [c for c in teh.columns if c.endswith("_share")]
    teh.insert(6, "tehsil_uid", "PB-" + teh.district_code.str.zfill(3) + "-" + teh.tehsil_code.str.zfill(3))
    teh.insert(7, "is_cholistan", teh.district.eq("CHOLISTAN"))
    teh["vintage"] = VINTAGE

    # ---------------- published tables
    pub, parse_problems = parse_published(pdf_lines())
    pub.to_csv(PUB_CSV, index=False)

    # Excel values in long form, all levels
    def melt(t, level, unit_col, dist_col=None, div_col=None):
        x = t.copy()
        x["level"], x["unit"] = level, (x[unit_col] if unit_col else "PUNJAB")
        x["district_key"] = x[dist_col] if dist_col else None
        x["division_key"] = x[div_col] if div_col else None
        keep = ["level", "unit", "district_key", "division_key"] + (["tehsil_uid"] if "tehsil_uid" in x else [])
        return x[keep + count_cols + avg_cols].melt(id_vars=keep, var_name="variable", value_name="excel")

    ex = pd.concat([melt(teh, "tehsil", "tehsil", "district", "division"),
                    melt(dist, "district", "district", None, "division"),
                    melt(div, "division", "division"), melt(prov, "province", None)], ignore_index=True)

    # Published rows: expand the per-facility RP column back to rp_mouzas for the 6.7/8.2 checks.
    pub_p = pub[~pub.level.isin(["ict", "other_province"])].copy()
    pub_p["base_var"] = pub_p.variable.str.replace(r"__.*$", "", regex=True)
    pub_p["district_key"] = np.where(pub_p.level == "tehsil", pub_p.district, None)
    pub_p["division_key"] = np.where(pub_p.level.isin(["tehsil", "district"]), pub_p.division, None)
    # Facilities only in 8.2 that we don't extract (post office etc.) are dropped from the comparison.
    pub_p = pub_p[pub_p.base_var.isin(set(ex.variable)) | pub_p.variable.str.startswith("rp_mouzas__")]
    pub_p.loc[pub_p.variable.str.startswith("rp_mouzas__"), "base_var"] = "rp_mouzas"
    pub_p = pub_p[~pub_p.variable.str.contains("postoffice|conciliatory|police")]
    # Table 1.1 extra columns (qanungo/patwar circles) have no Excel counterpart.
    pub_p = pub_p[~pub_p.variable.isin(["qanungo_circles", "patwar_circles"])]

    key = ["level", "unit", "district_key"]
    exk = ex.copy()
    exk.loc[exk.level != "tehsil", "district_key"] = None
    pub_p["district_key"] = pub_p["district_key"].where(pub_p.level == "tehsil", None)
    for f in (exk, pub_p):
        f["district_key"] = f["district_key"].fillna("")
    cmp_ = pub_p.merge(exk.rename(columns={"variable": "base_var"}), on=key + ["base_var"], how="left",
                       suffixes=("_pub", ""))
    cmp_["is_avg"] = cmp_.base_var.str.startswith("avg_")
    cmp_["diff"] = np.where(cmp_.is_avg, cmp_.excel.round(0) - cmp_.published, cmp_.excel - cmp_.published)
    cmp_["match"] = np.where(cmp_.is_avg, cmp_["diff"].abs() <= 1, cmp_["diff"] == 0)
    # Fully urban units print a blank rural-populated cell in Table 1.1; accept only if the Excel count is 0.
    cmp_["blank_in_pdf"] = cmp_.published.isna()
    cmp_.loc[cmp_.blank_in_pdf, "match"] = cmp_.loc[cmp_.blank_in_pdf, "excel"].eq(0)
    # Averages are blank in Excel when no mouza lacks the facility; published prints 0 or '-' there.
    cmp_.loc[cmp_.is_avg & cmp_.excel.isna(), "match"] = cmp_.loc[cmp_.is_avg & cmp_.excel.isna(), "published"].eq(0)
    unit_cols = ["level", "unit", "district_key"]
    ex_units = exk[unit_cols].drop_duplicates()
    # Units present in the Excel but missing from a given published table (checked table by table).
    missing_in_pdf = []
    for t, g in pub_p.groupby("table"):
        got = g[unit_cols].drop_duplicates().assign(_p=1)
        miss = ex_units.merge(got, how="left").query("_p.isna()")
        if t != "1.1":  # tables 6.3-8.2 cover rural populated mouzas only; fully urban units are not printed
            rp0 = exk[(exk.variable == "rp_mouzas") & (exk.excel == 0)][unit_cols].assign(_rp0=1)
            miss = miss.merge(rp0, how="left").query("_rp0.isna()")
        missing_in_pdf += [(t, *r) for r in miss[unit_cols].itertuples(index=False)]
    unmatched_units = (pub_p[["table"] + unit_cols].drop_duplicates()
                       .merge(ex_units, how="left", indicator=True).query("_merge == 'left_only'").drop(columns="_merge"))
    excel_units = set(map(tuple, exk[["level", "unit", "district_key"]].drop_duplicates().values))
    pub_units = set(map(tuple, pub_p[["level", "unit", "district_key"]].drop_duplicates().values))
    excel_only = sorted(excel_units - pub_units)

    # ---------------- long output
    long = cmp_.rename(columns={"base_var": "variable_std"})[
        ["table", "level", "division_key", "district_key", "unit", "tehsil_uid", "variable", "variable_std", "excel",
         "published", "diff", "match"]]
    long["vintage"] = VINTAGE
    OUT_LONG.parent.mkdir(parents=True, exist_ok=True)
    long.to_csv(OUT_LONG, index=False)

    # Avg columns are only for checking; not carried into the analysis file.
    teh_out = teh.drop(columns=avg_cols)
    teh_out.to_csv(OUT_WIDE, index=False)

    # ---------------- mandatory checks
    lines = [f"# Validation: Mouza Census 2020 tehsil extraction", "",
             f"Written by `scripts/04_extract_mouza.py` on {dt.date.today().isoformat()}. Vintage: {VINTAGE}.", "",
             "**Source used:** Excel mouza-level records from the RAR (aggregated by PBS district + tehsil codes). "
             "The RAR contains no pre-built tables. Published PDF tables were parsed only to validate.", ""]
    lines += ["## Scope", "",
              f"- Punjab mouza records: {len(p):,}; ICT records excluded: {n_ict:,} (ICT is a separate province in the Excel).",
              f"- Tehsils (unique district code + tehsil code): {len(teh)}; of which Cholistan: {int(teh.is_cholistan.sum())}; "
              f"tehsils with 0 rural populated mouzas: {int((teh.rp_mouzas == 0).sum())}.", ""]

    def row(name, got, exp):
        ok = "PASS" if got == exp else "**FAIL**"
        return f"| {name} | {got:,} | {exp:,} | {got - exp:+,} | {ok} |"

    lines += ["## Check 1: Punjab totals vs published figures supplied", "",
              "| Variable | Excel | Expected | Diff | Result |", "|---|---|---|---|---|"]
    for v, e in EXPECTED_PUNJAB.items():
        lines.append(row(v, int(prov[v].iloc[0]), e))
    o = prov.iloc[0]
    lines += ["", f"Note on `n_others`: the **detailed** Table 8.1 Punjab row (report p. 479) prints Others = "
              f"{int(pub[(pub.table=='8.1')&(pub.level=='province')&(pub.variable=='n_others')].published.iloc[0]):,}. "
              f"The summary Table 8.1 on report p. 54 prints 9,418. NGO + RSP + Govt + Others = "
              f"{int(o.n_ngo):,} + {int(o.n_rsp):,} + {int(o.n_govt):,} + {int(o.n_others):,} = "
              f"{int(o.n_ngo + o.n_rsp + o.n_govt + o.n_others):,}. Those are counts of mouza-mentions, not mouzas (a mouza can "
              f"report several), so 9,418 is not a mouza count. `n_others` is kept as the detailed-table 'Others' column. "
              f"**Needs Ahmed's decision** on which 'others' definition to use.", ""]

    bwn = dist[dist.district == "BAHAWALNAGAR DISTRICT"].rp_mouzas.iloc[0]
    lines += ["## Check 2: Bahawalnagar district", "",
              "| Variable | Excel | Expected | Diff | Result |", "|---|---|---|---|---|",
              row("rp_mouzas (Bahawalnagar)", int(bwn), EXPECTED_BAHAWALNAGAR_RP), ""]

    # Check 3: tehsil sums vs published district rows; and published tehsils vs published districts.
    c3 = cmp_[(cmp_.level == "district") & ~cmp_.is_avg]
    pub_t = pub_p[(pub_p.level == "tehsil") & ~pub_p.base_var.str.startswith("avg_")]
    pub_tsum = pub_t.groupby(["table", "district", "variable"]).published.sum().rename("pub_tehsil_sum")
    pub_d = pub_p[(pub_p.level == "district")].set_index(["table", "unit", "variable"]).published
    pub_d.index.names = ["table", "district", "variable"]
    internal = pd.concat([pub_tsum, pub_d.rename("pub_district")], axis=1, join="inner")
    internal = internal[internal.pub_tehsil_sum != internal.pub_district]
    lines += ["## Check 3: tehsils sum to district totals", "",
              f"- (a) Sum of Excel tehsil values vs **published** district rows: {int(c3.match.sum())} of {len(c3)} "
              f"district×variable cells match; {int((~c3.match).sum())} mismatches.",
              f"- (b) Internal consistency of the report: sum of published tehsil rows vs published district rows: "
              f"{len(internal)} mismatching cells.", ""]
    if (~c3.match).any():
        lines += ["Mismatches (a):", "", "| Table | District | Variable | Excel tehsil sum | Published | Diff |", "|---|---|---|---|---|---|"]
        lines += [f"| {r.table} | {r.unit} | {r.variable} | {r.excel:.0f} | {r.published} | {r['diff']:+.0f} |"
                  for _, r in c3[~c3.match].iterrows()]
        lines.append("")
    if len(internal):
        unreadable = {(t, dk) for t, lv, u, dk in missing_in_pdf}
        why = lambda i, r: ("tehsil row(s) unreadable in PDF text layer, so the published tehsil sum is incomplete"
                            if (i[0], i[1]) in unreadable else
                            "district cell printed blank (fully urban district)" if pd.isna(r.pub_district) else
                            "**unexplained**")
        lines += ["Mismatches (b):", "", "| Table | District | Variable | Published tehsil sum | Published district | Reason |",
                  "|---|---|---|---|---|---|"]
        lines += [f"| {i[0]} | {i[1]} | {i[2]} | {r.pub_tehsil_sum:.0f} | {r.pub_district} | {why(i, r)} |"
                  for i, r in internal.iterrows()]
        lines.append("")

    oob = {c: int(((teh[c] < 0) | (teh[c] > 1)).sum()) for c in share_cols}
    nan_ = {c: int(teh[c].isna().sum()) for c in share_cols}
    lines += ["## Check 4: shares within [0, 1]", "",
              f"- Shares outside [0, 1]: {sum(oob.values())} ({'PASS' if sum(oob.values()) == 0 else '**FAIL**'}).",
              f"- Undefined shares (tehsil has 0 rural populated mouzas): {max(nan_.values())} tehsils; shares left blank.", ""]

    # Check 5: every published row
    nonavg, avg = cmp_[~cmp_.is_avg & cmp_.excel.notna()], cmp_[cmp_.is_avg]
    lines += ["## Check 5: every published row (all levels), Excel vs PDF", "",
              "| Table | Cells compared | Exact matches | Mismatches |", "|---|---|---|---|"]
    for t, g in nonavg.groupby("table"):
        lines.append(f"| {t} | {len(g)} | {int(g.match.sum())} | {int((~g.match).sum())} |")
    lines += ["", f"Cells printed blank in the PDF (rural-populated column of fully urban units in Table 1.1) and "
              f"equal to 0 in the Excel: {int((cmp_.blank_in_pdf & cmp_.match).sum())}; blank in PDF but non-zero in "
              f"Excel: {int((cmp_.blank_in_pdf & ~cmp_.match).sum())}."]
    lines += ["", f"Average-distance columns (published as rounded integers; Excel mean over mouzas *without* the "
              f"facility, rounded; tolerance ±1 km): {int(avg.match.sum())} of {len(avg)} cells within tolerance. "
              f"Averages are **not** included in mouza_tehsil.csv.", ""]
    mm_ = nonavg[~nonavg.match]
    if len(mm_):
        lines += ["Count mismatches:", "", "| Table | Level | District | Unit | Variable | Excel | Published | Diff |",
                  "|---|---|---|---|---|---|---|---|"]
        lines += [f"| {r.table} | {r.level} | {r.district_key} | {r.unit} | {r.variable} | {r.excel:.0f} | {r.published} | {r['diff']:+.0f} |"
                  for _, r in mm_.iterrows()]
        lines.append("")
    if missing_in_pdf:
        lines += ["Excel units with no parsed row in a published table (row unreadable in the PDF text layer; "
                  "these cells were NOT validated against the PDF). Units with 0 rural populated mouzas (Lahore "
                  "district's 5 tehsils, Bahawalpur City) are correctly absent from Tables 6.3-8.2 and not listed:", ""]
        lines += [f"- Table {t}: {lv}, {dk or '-'} / {u}" for t, lv, u, dk in missing_in_pdf]
        lines.append("")
    if len(unmatched_units) or excel_only:
        lines += ["Unit names that did not match exactly between PDF and Excel (no fuzzy matching applied):", ""]
        lines += [f"- in PDF only: table {r.table}, {r.level}, {r.district_key or '-'} / {r.unit}" for _, r in unmatched_units.iterrows()]
        lines += [f"- in Excel only: {lv}, {dk or '-'} / {u}" for lv, u, dk in excel_only]
        lines.append("")
    lines += ["## Data anomalies found in the mouza records (reported, not corrected)", ""]
    lines += [f"- {a}" for a in anomalies] or ["- none"]
    lines += ["", "## PDF parsing problems", ""] + ([f"- {x}" for x in parse_problems] or ["- none"])
    VAL_MD.write_text("\n".join(lines) + "\n")

    print(f"tehsils: {len(teh)}  -> {OUT_WIDE.relative_to(ROOT)}")
    print(f"long rows: {len(long)} -> {OUT_LONG.relative_to(ROOT)}")
    print(f"check5 mismatches: {len(mm_)}  unmatched pdf units: {len(unmatched_units)}  excel-only units: {len(excel_only)}")
    print(f"parse problems: {len(parse_problems)}  anomalies: {len(anomalies)}  units missing from a PDF table: {len(missing_in_pdf)}")
    print(f"validation -> {VAL_MD.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
