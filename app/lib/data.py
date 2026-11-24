"""Loading layer for the app. Everything on screen is read from app/data/ (copied from outputs/ by
scripts/16_export_web.py), from docs/, or from app/content/. Nothing is estimated here."""

from __future__ import annotations

import json
import re
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "app" / "data"
CONTENT = ROOT / "app" / "content"
DOCS = ROOT / "docs"
PLACEHOLDER = "AHMED: write this"


def _mtime(p: Path) -> float:
    return p.stat().st_mtime


@st.cache_data(show_spinner=False)
def _geo(name: str, mtime: float) -> dict:
    return json.loads((DATA / f"{name}.geojson").read_text())


def geo(name: str) -> dict:
    return _geo(name, _mtime(DATA / f"{name}.geojson"))


def props(name: str) -> pd.DataFrame:
    return pd.DataFrame([f["properties"] for f in geo(name)["features"]])


@st.cache_data(show_spinner=False)
def _table(name: str, mtime: float) -> pd.DataFrame:
    return pd.read_csv(DATA / name)


def table(name: str) -> pd.DataFrame:
    name = name if name.endswith(".csv") else f"{name}.csv"
    return _table(name, _mtime(DATA / name)).copy()


def text(name: str) -> str:
    return (DATA / name).read_text()


def manifest() -> dict:
    return json.loads((DATA / "manifest.json").read_text())


def kn(kid: str) -> str:
    """A key number as displayed (outputs/tables/key_numbers.csv, written by scripts/15_key_numbers.py)."""
    k = table("key_numbers").set_index("id")
    return str(k.loc[kid, "display"])


def kn_row(kid: str) -> pd.Series:
    return table("key_numbers").set_index("id").loc[kid]


# ------------------------------------------------------------------ class breaks (paper rule; values from outputs)
def classes(variable: str, figure: str) -> dict:
    c = table("classification_comparison")
    r = c[(c.figure == figure) & (c.variable.str.startswith(variable + " (")) & (c.chosen)]
    if len(r) != 1:
        return {}
    r = r.iloc[0]
    return dict(scheme=r.scheme, bins=[float(b) for b in r.bins_exact.split(";")], counts=[int(x) for x in r["counts"].split(";")],
                n=int(r.n), figure=r.figure)


def class_index(values: pd.Series, bins: list[float]) -> pd.Series:
    """Same assignment as mapclassify's find_bin (upper bounds, right-closed); -1 = no value."""
    v = pd.to_numeric(values, errors="coerce")
    k = np.digitize(v.fillna(-np.inf), bins, right=True).clip(0, len(bins) - 1)
    return pd.Series(np.where(v.notna(), k, -1), index=values.index)


def fig_number(item: str) -> float:
    f = table("figure_numbers")
    return float(f[f["item"] == item].value.iloc[0])


# ------------------------------------------------------------------ text
def md_sections(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    text = re.sub(r"<!--.*?-->", "", path.read_text(), flags=re.S)
    out, cur = {}, None
    for line in text.splitlines():
        m = re.match(r"^##\s+(.*)$", line)
        if m:
            cur = m.group(1).strip(); out[cur] = []
        elif cur is not None:
            out[cur].append(line)
    return {k: "\n".join(v).strip() for k, v in out.items()}


def narrative(section: str) -> str | None:
    """Interpretation text from app/content/narrative.md (read live); None when missing or still a placeholder."""
    body = md_sections(CONTENT / "narrative.md").get(section)
    if not body or PLACEHOLDER in body:
        return None
    return body


def content(name: str, section: str) -> str | None:
    return md_sections(CONTENT / name).get(section)


def checklist() -> pd.DataFrame:
    """docs/human_checklist.md table, read live."""
    rows = [l for l in (DOCS / "human_checklist.md").read_text().splitlines() if l.startswith("|")]
    head = [h.strip() for h in rows[0].strip("|").split("|")]
    body = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows[2:]]
    df = pd.DataFrame([b + [""] * (len(head) - len(b)) for b in body], columns=head)
    s = df[head[-1]].str.strip()
    df["status"] = np.select([s.eq(""), s.str.startswith("✓"), s.str.startswith("✗")], ["pending", "verified", "does not match"], "note")
    return df


def sources() -> pd.DataFrame:
    """Sources table from docs/data_inventory.md."""
    lines = (DOCS / "data_inventory.md").read_text().splitlines()
    i = next(j for j, l in enumerate(lines) if l.startswith("|") and "Dataset" in l)
    rows = []
    for l in lines[i:]:
        if not l.startswith("|"):
            break
        rows.append([c.strip() for c in l.strip().strip("|").split("|")])
    df = pd.DataFrame(rows[2:], columns=rows[0])
    for c in df.columns:
        df[c] = df[c].str.replace(r"[*`]", "", regex=True)
    df["URL"] = df.URL.map(lambda s: (re.findall(r"https?://[^\s)]+", s) or [""])[-1].rstrip(".,"))
    return df
