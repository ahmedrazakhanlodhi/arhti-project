"""Data-contract tests for the app and the written deliverables (run: .venv/bin/python -I -m pytest tests -q).

- Every key number equals its source value (file, row, column in outputs/tables/key_numbers.csv).
- Every number written in the narrative, paper draft and slide text is a key number (or a fixed definition).
- Numbers displayed in the app equal their sources; map classes reproduce the paper's class counts.
- Forbidden fields and phrases never appear; nothing mouza-level is shipped.
"""

from __future__ import annotations

import hashlib
import html
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pyogrio
import pytest
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "app"
DATA = APP / "data"
GPKG = ROOT / "outputs" / "arhti_project.gpkg"
sys.path.insert(0, str(APP))
from lib import data as appdata  # noqa: E402

KN = pd.read_csv(ROOT / "outputs" / "tables" / "key_numbers.csv")
CODE = sorted((APP / "views").glob("*.py")) + sorted((APP / "lib").glob("*.py")) + [APP / "app.py"]
CONTENT = sorted((APP / "content").glob("*.md"))
WRITING = [ROOT / "docs" / f for f in ["paper_draft.md", "slide_text.md", "paper_outline.md", "key_numbers.md"]] + [APP / "content" / "narrative.md"]
PUBLIC_DOCS = WRITING + [ROOT / "README.md", ROOT / "docs" / "methods_appendix.md", ROOT / "docs" / "variable_dictionary.md",
                         ROOT / "docs" / "decisions.md", ROOT / "docs" / "project_rules.md", ROOT / "docs" / "deploy.md",
                         ROOT / "docs" / "human_checklist.md"]
PAGES = ["1_overview", "2_access", "3_allocation", "4_reporting", "5_cost", "6_profiles", "7_methods"]


def run_page(page: str, **state) -> AppTest:
    at = AppTest.from_file(str(APP / "app.py"), default_timeout=120)
    at.session_state["present"] = False
    for k, v in state.items():
        at.session_state[k] = v
    at.run()                                   # AppTest needs one run before switch_page takes effect
    if page != PAGES[0]:
        at.switch_page(f"views/{page}.py")
        at.run()
    assert not at.exception, [e.value for e in at.exception]
    return at


def text(at: AppTest) -> str:
    parts = [m.value for m in at.markdown] + [c.value for c in at.caption] + [t.value for t in at.title]
    parts += [str(m.value) for m in at.metric] + [s.value for s in at.subheader] + [i.value for i in at.info] + [w.value for w in at.warning]
    return html.unescape("\n".join(parts))


# ------------------------------------------------------------------ key numbers equal their sources
def source_value(r):
    if r.source.startswith("outputs/arhti_project.gpkg"):
        d = pyogrio.read_dataframe(GPKG, layer=r.source.split("layer ")[-1], read_geometry=False)
    else:
        d = pd.read_csv(ROOT / r.source)
    row = r.row
    m = re.search(r"\((\w+) over \d+ rows\)$", row)
    agg = m.group(1) if m else None
    row = re.sub(r"\s*\(\w+ over \d+ rows\)$", "", row)
    cmp = re.search(r"; obs_exp_ratio ([<>]) 1 \(count\)$", row)
    row = re.sub(r"; obs_exp_ratio [<>] 1 \(count\)$", "", row)
    if row != "all rows":
        for cond in re.split(r"; (?=\w+ = )", row):          # values may themselves contain "; "
            k, v = cond.split(" = ", 1)
            d = d[d[k].astype(str) == v]
    if cmp:
        return int((d.obs_exp_ratio > 1).sum() if cmp.group(1) == ">" else (d.obs_exp_ratio < 1).sum())
    if agg:
        return getattr(d[r.column], agg)()
    if r.id == "flagged_names":
        return ", ".join(sorted(d[r.column]))
    assert len(d) == 1, (r.id, len(d))
    return d[r.column].iloc[0]


def test_key_numbers_equal_sources():
    for r in KN.itertuples():
        v = source_value(r)
        try:
            assert abs(float(v) - float(r.value)) < 1e-9 * max(1, abs(float(v))), r.id
        except (TypeError, ValueError):
            assert str(v) == str(r.value), r.id


def test_key_numbers_doc_matches_csv():
    md = (ROOT / "docs" / "key_numbers.md").read_text()
    for r in KN.itertuples():
        assert f"`{r.id}`" in md and f"**{r.display}**" in md, r.id


# ------------------------------------------------------------------ every number in the writing is a key number
ALLOWED = {  # fixed definitions, dates and labels that are not results
    "2020", "2022", "2023", "2024", "2026", "2013", "2019", "2012", "2018", "FY2023", "12.5", "50", "1,000", "10,000", "0.05", "0.01",
    "3", "5", "9", "1", "2", "4", "6", "7", "8", "11", "30", "3,000", "3,500", "24", "25", "A", "B", "S1", "S2", "S3", "S4", "S5", "S6",
    "10", "18", "400", "0.5", "k", "38520", "95"}   # 95 = "95% CI"


def numbers_in(s: str) -> set[str]:
    s = re.sub(r"`[^`]*`", "", s)                                   # IDs and file names
    s = re.sub(r"\[[^\]]*\]", "", s)                                 # bracketed key-number IDs and placeholders
    s = re.sub(r"\b(?:Figure|Figures|Fig|Section|Sections|Slide|slides|Table|A\d+)\s*[A-Z]?\d+(?:\.\d+)?(?:[–-]\d+)?", "", s)
    s = re.sub(r"\b(?:FY)?\d{4}-\d{2}\b", "", s)                    # fiscal years such as FY2012-13
    s = re.sub(r"\d+\.\d+\s+(?=[A-Z])", "", s)                       # outline numbering "4.1 Where"
    s = re.sub(r"^#+ .*$", "", s, flags=re.M)                        # headings
    return set(re.findall(r"\d+(?:,\d{3})*(?:\.\d+)?", s))


def test_writing_uses_only_key_numbers():
    allowed = set(ALLOWED)
    for d in KN.display.astype(str):
        allowed |= set(re.findall(r"\d+(?:,\d{3})*(?:\.\d+)?", d))
    for p in [ROOT / "docs" / "paper_draft.md", ROOT / "docs" / "slide_text.md", APP / "content" / "narrative.md"]:
        extra = sorted(n for n in numbers_in(p.read_text()) if n not in allowed and n.rstrip(".") not in allowed)
        assert not extra, (p.name, extra)


# ------------------------------------------------------------------ app numbers equal sources
def test_overview_cards_show_key_numbers():
    t = text(run_page("1_overview"))
    k = KN.set_index("id").display
    for kid in ["mh_or", "mh_lo", "mh_hi", "bd_p", "n_districts_q2", "lahore_total_branches_10k", "lahore_rural_branches_10k",
                "rate_comm_prod_2023", "lit_igc_rates"]:
        assert k[kid] in t, kid
    assert f"{k['reach_min']}–{k['reach_max']}" in t
    assert "Descriptive results. Sources differ in date and geographic unit." in t


def test_pages_show_their_numbers_and_note():
    k = KN.set_index("id").display
    want = {"2_access": ["arhti_pooled", "rp_mouzas", "moran_arhti_queen", "permutations", "seed", "mh_or", "mh_lo", "mh_hi", "bd_p",
                         "tehsils_ratio_above1", "tehsils_ratio_below1", "rho_cropland", "bv_queen", "moran_arhti_knn", "moran_arhti_B"],
            "3_allocation": ["reach_median", "moran_reach", "top_crop_wheat", "rho_tenant"],
            "4_reporting": ["five_credit_share_tot", "five_credit_share_abv", "five_area_share", "five_farm_share", "isb_credit_share_tot",
                            "lahore_total_branches_10k", "lahore_rural_branches_10k"],
            "5_cost": ["kissan_terms"]}
    for page, ids in want.items():
        t = text(run_page(page))
        assert "Descriptive results. Sources differ in date and geographic unit." in t and "Data vintage · " in t, page
        for kid in ids:
            assert k[kid] in t, (page, kid)
    t = text(run_page("2_access", acc_view="Clusters (LISA)"))
    assert k["bh_cutoff_queen"] in t
    assert "attribution under verification" in text(run_page("4_reporting"))


def test_profile_page_matches_scorecard():
    sc = pd.read_csv(ROOT / "outputs" / "tables" / "district_scorecard.csv")
    for nm in ["Lahore", "Jhelum", "Bahawalnagar"]:
        r = sc[sc.adm2_name == nm].iloc[0]
        t = text(run_page("6_profiles", prof_district=nm))
        assert r.profile_type in t and f"{100 * r.small_farm_reach / 100:,.1f}" in t, nm
        assert f"{r.lq_amount_abv:.2f}" in t and "attribution under verification" in t, nm


def test_cost_points_equal_rate_table():
    rt = pd.read_csv(ROOT / "outputs" / "tables" / "sbp_agri_lending_rates.csv")
    pl = pd.read_csv(ROOT / "docs" / "price_ladder.csv")
    sbp = pl[pl.source_type == "outputs/tables/sbp_agri_lending_rates.csv"]
    for r in sbp.itertuples():
        per = re.search(r"FY(\d{4}-\d{2})", r.date).group(1)
        inst, lt = r.item.rsplit(", ", 1)
        v = rt[(rt.period == per) & (rt.institution == inst) & (rt.loan_type == lt.replace(" loans", ""))].rate_pct.iloc[0]
        assert v == r.rate_low == r.rate_high
    assert not pl["item"].str.contains("PMN|180", regex=True).any()          # PMN/MEDA stays off the rate axis
    assert (pd.read_csv(DATA / "price_ladder.csv").shape == pl.shape)


def test_map_classes_reproduce_paper_counts():
    t = appdata.props("tehsils"); d = appdata.props("districts")
    for var, fig, vals in [("arhti_share", "Fig 2", t.loc[t.rp_mouzas > 0, "arhti_share"]), ("small_farm_reach", "Fig 5", d.small_farm_reach)]:
        c = appdata.classes(var, fig)
        k = appdata.class_index(vals, c["bins"])
        assert [int((k == i).sum()) for i in range(5)] == c["counts"], var


def test_bivariate_counts_and_cutpoints_match_figure_3():
    t = appdata.props("tehsils")
    fn = pd.read_csv(ROOT / "outputs" / "tables" / "figure_numbers.csv")
    for ra in (1, 2, 3):
        for rc in (1, 2, 3):
            n = fn[(fn.figure == "Fig 3") & (fn["item"] == f"Tehsils in cell arhti tertile {ra} × commercial tertile {rc}")].value.iloc[0]
            assert int((t.bivariate_class == f"A{ra}-C{rc}").sum()) == int(n)


def test_web_layers_equal_gpkg_and_manifest():
    man = json.loads((DATA / "manifest.json").read_text())
    for r in man["layers"] + man["tables"]:
        assert hashlib.sha256((DATA / r["file"]).read_bytes()).hexdigest() == r["sha256"], r["file"]
    for r in man["layers"]:
        assert r["bytes"] < 3 * 1024 * 1024
        src = pyogrio.read_dataframe(GPKG, layer=r["source"].split("layer ")[-1], read_geometry=False)[r["fields"]]
        web = pd.DataFrame([f["properties"] for f in json.loads((DATA / r["file"]).read_text())["features"]])[r["fields"]]
        assert len(src) == len(web) == r["features"]
        for c in r["fields"]:
            a, b = src[c], web[c]
            if pd.api.types.is_numeric_dtype(a) and not pd.api.types.is_bool_dtype(a):
                assert np.allclose(a.astype(float), b.astype(float), rtol=1e-6, equal_nan=True), (r["file"], c)
            else:
                assert (a.astype(str).where(a.notna(), "nan") == b.astype(str).where(b.notna(), "nan")).all(), (r["file"], c)


# ------------------------------------------------------------------ forbidden fields and phrases
DISTRICT_AMOUNT = r"credit_share_|lq_amount_|credit_per_cultivated_acre|_amount_mn|head_amount_share|five_credit_share|isb_credit_share"


def test_amounts_only_on_reporting_geography():
    """District disbursement amounts are mapped only on the reporting-geography page (D039); the district-profile page shows the
    scorecard's labelled values in a table, and its map is a plain locator."""
    for f in list(DATA.glob("*.csv")) + list(DATA.glob("*.geojson")):
        cols = (pd.read_csv(f, nrows=0).columns if f.suffix == ".csv" else json.loads(f.read_text())["features"][0]["properties"].keys())
        assert not [c for c in cols if re.search(r"avg_loan", c)], f.name
        if f.name not in {"reporting_geography.csv", "district_scorecard.csv", "holding_class_shares.csv"}:
            assert not [c for c in cols if re.search(r"amount|credit_share|lq_", c)], f.name
    hits = sorted(p.name for p in CODE if re.search(DISTRICT_AMOUNT, p.read_text()))
    assert hits == ["4_reporting.py", "6_profiles.py"], hits
    prof = (APP / "views" / "6_profiles.py").read_text()
    call = prof[prof.index("maps.layer("):].split(")", 1)[0]
    assert not re.search(DISTRICT_AMOUNT, call)                           # locator map is not coloured by amounts
    for p in CODE:
        assert not re.search(r"avg_loan_|sub_amount_mn|abv_amount_share", p.read_text()), p.name


BANNED = [r"credit desert", r"\bcaus(e|es|ed|ing)\b", r"\bdriv(e|es|en|ing)\b", r"\bexplain(s|ed|ing)?\b", r"bank presence"]
AI_TERMS = [r"Cl[a]ude", r"Anthr[o]pic", r"\bAI\b", r"AI-", r"\bLLM", r"language model", r"[Gg]enerated by", r"the model\b"]


def test_no_banned_language_in_app_and_writing():
    for p in CODE + CONTENT + WRITING:
        for i, line in enumerate(p.read_text().splitlines(), 1):
            low = line.lower()
            for b in BANNED:
                if re.search(b, low) and "never" not in low:
                    raise AssertionError(f"{p.relative_to(ROOT)}:{i}: {line.strip()}")


def test_no_ai_references_anywhere_public():
    files = CODE + CONTENT + PUBLIC_DOCS + list(DATA.glob("*")) + sorted(p for p in (ROOT / "scripts").glob("*") if p.is_file()) + [ROOT / "run_all.sh"]
    for p in files:
        s = p.read_text(errors="ignore")
        for b in AI_TERMS:
            m = re.search(b, s)
            assert not m, f"{p.relative_to(ROOT)}: {b} -> {s[max(0, m.start() - 40):m.end() + 40]!r}"
    names = [str(p.relative_to(ROOT)) for p in ROOT.rglob("*") if ".venv" not in p.parts and "private" not in p.parts
             and "raw" not in p.parts and not p.name.endswith(".local.md") and re.search(r"cl[a]ude|anthr[o]pic|ai_use|llm", p.name, re.I)]
    assert not names, names


# ------------------------------------------------------------------ nothing mouza-level
@pytest.fixture(scope="module")
def mouza_names() -> set[str]:
    x = ROOT / "data" / "interim" / "mouza_census_2020_excel" / "Mouza Census-2020.xlsx"
    if not x.exists():
        pytest.skip("Mouza Census Excel not present in this checkout")
    codes = pd.read_excel(x, header=None, skiprows=2, nrows=1, dtype=str).iloc[0].tolist()
    d = pd.read_excel(x, header=None, skiprows=3, dtype=str, usecols=[codes.index("prv_desc"), codes.index("vil_desc")])
    d.columns = ["prv", "vil"]
    names = {" ".join(str(v).upper().split()) for v in d[d.prv.fillna("").str.upper().str.contains("PUNJAB")].vil.dropna()}
    places = set()
    for f in DATA.glob("*.geojson"):
        for ft in json.loads(f.read_text())["features"]:
            for k in ("adm1_name", "adm2_name", "adm3_name"):
                if isinstance(ft["properties"].get(k), str):
                    places.add(" ".join(ft["properties"][k].upper().split()))
    generic = {"NONE", "OTHER", "OTHERS", "TRUE", "FALSE", "DATA"}   # ordinary words that are also mouza names
    return {n for n in names if n not in places and n not in generic and len(n) > 3}


def test_no_mouza_names_or_codes(mouza_names):
    for f in list(DATA.glob("*.csv")) + list(DATA.glob("*.geojson")):
        if f.suffix == ".csv":
            df = pd.read_csv(f, dtype=str)
        else:
            df = pd.DataFrame([x["properties"] for x in json.loads(f.read_text())["features"]]).astype(str)
        assert not [c for c in df.columns if re.search(r"vil_|mouza_(name|code|tehsil_uid)|mauza", c, re.I)], f.name
        for v in map(str, df.stack().tolist()):
            assert " ".join(v.upper().split()) not in mouza_names, (f.name, v)
            assert not re.search(r"PB-\d{3}-\d{3}", v), (f.name, v)


# ------------------------------------------------------------------ narrative and checklist
def test_narrative_sections_shown_or_placeholder():
    secs = appdata.md_sections(APP / "content" / "narrative.md")
    want = {"1_overview": ["Central question", "Main conclusion"], "2_access": ["Access"], "3_allocation": ["Allocation"],
            "4_reporting": ["Reporting geography"], "5_cost": ["Cost"], "6_profiles": ["District profiles"], "7_methods": ["Limitations"]}
    for page, names in want.items():
        t = text(run_page(page))
        for n in names:
            assert n in secs, n
            body = appdata.narrative(n)
            assert (body.splitlines()[0][:50] in t) if body else (appdata.PLACEHOLDER in t), (page, n)


def test_verification_status_read_live():
    t = text(run_page("7_methods"))
    hc = appdata.checklist()
    assert str(int((hc.status == "pending").sum())) in t
