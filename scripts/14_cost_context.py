"""14_cost_context.py: COST as CONTEXT (no maps). Formal agricultural lending rates vs published arhti cost estimates (D039).

    .venv/bin/python -I scripts/14_cost_context.py

- outputs/tables/sbp_agri_lending_rates.csv: SBP Monthly Statistical Bulletin Table 3.33, every period, institution and loan type,
  read from the September 2026 edition and checked against the June 2024 edition for every overlapping, non-provisional period.
- docs/price_ladder.csv: dated rows on one rate axis (percent per annum). docs/price_ladder_notes.md: items NOT on the rate axis.
- outputs/figures/figP1_price_ladder (PNG + PDF), two panels.
Values supplied by Ahmed are marked source_type = "supplied by Ahmed" and carry their own verification note.
"""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402
import pypdfium2 as pdfium  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
T = ROOT / "outputs" / "tables"
RAW = ROOT / "data" / "raw" / "sbp_bulletin"
EDITIONS = {  # edition: (file, URL)
    "September 2026": ("MSB_September_2026.pdf", "https://www.sbp.org.pk/assets/documents/bulletin/MSB_September_2026.pdf"),
    "June 2024": ("MSB-Jun-24.pdf", "https://archive.sbp.org.pk/reports/stat_reviews/Bulletin/2024/Jun/MSB-Jun-24.pdf"),
}
INST = [("Zarai Taraqiati Bank Ltd. (ZTBL)", "production"), ("Zarai Taraqiati Bank Ltd. (ZTBL)", "development"),
        ("Punjab Provincial Cooperative Bank (PPCB)", "production"), ("Punjab Provincial Cooperative Bank (PPCB)", "development"),
        ("Commercial banks (5 big banks + 14 DPBs)", "production"), ("Commercial banks (5 big banks + 14 DPBs)", "development")]
DEFINITION = "simple average of June quarter end each year (table note); percent per annum"

_spec = importlib.util.spec_from_file_location("figs", ROOT / "scripts" / "09_figures.py")
figs = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(figs)


def table_333(edition: str) -> pd.DataFrame:
    fname, url = EDITIONS[edition]
    pdf = pdfium.PdfDocument(RAW / fname)
    for i in range(len(pdf)):
        t = pdf[i].get_textpage().get_text_range()
        if re.search(r"3\.33 Average Rates? of Return on Advances of Specialized", t) and "June quarter end" in t:
            break                                      # the table page (the contents page lists the title too)
    else:
        sys.exit(f"Table 3.33 not found in {fname}")
    assert "simple average of June quarter end" in t
    flat = " ".join(t.split())
    rows = []
    for m in re.finditer(r"(\d{4}-\d{2})\s*(P?)\s+(.*?)(?=\d{4}-\d{2}|Note:|Source:|\d\. Commercial|$)", flat):
        nums = [float(x) for x in re.findall(r"\d+\.\d+", m.group(3))]       # footnote markers are plain integers: skipped
        assert len(nums) == 6, (edition, m.group(1), nums)
        for (inst, lt), v in zip(INST, nums):
            rows.append(dict(period=m.group(1), provisional=bool(m.group(2)), institution=inst, loan_type=lt, rate_pct=v,
                             edition=edition, table="3.33", page_pdf=i + 1, source_url=url))
    return pd.DataFrame(rows)


def rates() -> pd.DataFrame:
    new, old = table_333("September 2026"), table_333("June 2024")
    k = ["period", "institution", "loan_type"]
    both = new.merge(old[~old.provisional], on=k, suffixes=("", "_jun24"))
    bad = both[(both.rate_pct - both.rate_pct_jun24).abs() > 1e-9]
    assert not len(bad), bad
    new["checked_against_june_2024_edition"] = new.set_index(k).index.isin(both.set_index(k).index)
    new["table_title"] = ("Average Rate of Return on Advances of Specialized Agricultural Finance Institutions and Agriculture "
                          "Lending of Commercial Banks")
    new["definition"] = DEFINITION
    new["vintage"] = "SBP Monthly Statistical Bulletin, September 2026 edition (source: Agriculture Credit & Financial Inclusion Department)"
    return new, len(both)


def ladder(r: pd.DataFrame) -> pd.DataFrame:
    lit = pd.read_csv(ROOT / "docs" / "literature_evidence.csv", dtype=str, keep_default_na=False)
    igc = lit[lit.study.str.contains("Who is the Arthi")].iloc[0]
    rows = []
    for crop, v in re.findall(r"(\w+) ([\d.]+)%", igc.value):
        rows.append(dict(date="2012 (interviews); published 2013", era="~2012-13", panel="a", item=f"Arhti implicit annualized cost: {crop}",
                         institution="arhti (commission agent)", rate_low=float(v), rate_high=float(v), on_rate_axis=True,
                         basis=igc.basis, sample=igc["sample"], source=f"{igc.study} ({igc.year}), Table 11, PDF p. {igc.page}",
                         source_type="docs/literature_evidence.csv", url=igc.url,
                         note="Purposive small sample; rate by crop, not by location; CONTEXT only"))
    rows.append(dict(date="2012 (interviews); published 2013", era="~2012-13", panel="a", item="Bank rates reported by interviewed farmers",
                     institution="banks (farmer-reported)", rate_low=9.0, rate_high=18.0, on_rate_axis=True, basis="farmer-reported",
                     sample=igc["sample"], source=f"{igc.study} ({igc.year})", source_type="supplied by Ahmed", url=igc.url,
                     note="Supplied by Ahmed 2026-11-01; not yet in docs/literature_evidence.csv; page to be recorded (checklist P3)"))
    for period, era, panel in [("2012-13", "~2012-13", "a"), ("2023-24", "FY2023-24", "b")]:
        for x in r[r.period == period].itertuples():
            rows.append(dict(date=f"FY{period} (June quarter end)", era=era, panel=panel, item=f"{x.institution}, {x.loan_type} loans",
                             institution=x.institution, rate_low=x.rate_pct, rate_high=x.rate_pct, on_rate_axis=True, basis=DEFINITION,
                             sample="institutional average", source=f"SBP Monthly Statistical Bulletin, {x.edition}, Table 3.33, PDF p. {x.page_pdf}",
                             source_type="outputs/tables/sbp_agri_lending_rates.csv", url=x.source_url, note="Institutional average, not a matched contract"))
    rows.append(dict(date="registration opened 2024-06-01; cards operational 2024-10-15", era="after FY2023-24", panel="b",
                     item="Punjab CM Kissan Card (interest-free)", institution="Government of Punjab / Bank of Punjab", rate_low=0.0, rate_high=0.0,
                     on_rate_axis=True, basis="0% markup to the borrower", sample="holdings up to 12.5 acres",
                     source="Punjab Portal, CM Kissan Card Scheme; CM Special Monitoring Unit, Kissan Card",
                     source_type="official web pages + dates supplied by Ahmed",
                     url="https://punjab.gov.pk/cm-kissan-card-scheme; https://smu.punjab.gov.pk/kissan-card",
                     note=("Eligibility: 1 to 12.5 acres; loan limit Rs 30,000 per acre capped at Rs 150,000 per season (i.e. sized on 5 acres) "
                           "per the Punjab Portal. Registration opened 1 Jun 2024 (SMU page); cards operational 15 Oct 2024 (supplied by Ahmed). "
                           "Both after the FY2023-24 SBP data period except the last month of registration.")))
    d = pd.DataFrame(rows)
    d.insert(0, "row", range(1, len(d) + 1))
    return d


NOTES = """# Price ladder: items NOT on the rate axis

Companion to `docs/price_ladder.csv` (written by `scripts/14_cost_context.py`).

- **PMN/MEDA 2019, "Warehouse Receipt Financing":** focus-group statements of an arhti markup of about 180% (PDF pp. 19, 23).
  Not an annualized rate: it varies with the farmer's urgency to sell, and the sample is non-representative (400-farmer survey in
  10 Punjab districts plus 4 FGDs, 2018). Kept off the rate axis so it is not read as comparable to the rates there.
- **Kissan Card loan size:** eligibility runs to 12.5 acres, but the per-season limit (Rs 30,000 per acre, capped at Rs 150,000)
  is reached at 5 acres, so holdings between 5 and 12.5 acres receive the same maximum (Punjab Portal, CM Kissan Card Scheme).
  Later phases (2026) report higher limits on third-party sites only; not used.
- **Not matched contracts:** arhti costs are implicit annualized estimates from a purposive 2012 sample (by crop); SBP rates are
  simple averages at June quarter end by institution. The comparison shows orders of magnitude, not like-for-like prices.
"""


def fig_p1(d: pd.DataFrame):
    fig, axes = plt.subplots(1, 2, figsize=(13, 6.2), gridspec_kw=dict(width_ratios=[1.15, 1]))
    col = {"arhti (commission agent)": figs.ORANGE5[2], "banks (farmer-reported)": "#8a8984"}
    for ax, panel, title in [(axes[0], "a", "(a) About 2012-13: published arhti cost estimates vs SBP agricultural rates"),
                             (axes[1], "b", "(b) FY2023-24: SBP agricultural rates, and the Kissan Card")]:
        g = d[(d.panel == panel) & d.on_rate_axis].reset_index(drop=True)
        ys = list(range(len(g)))[::-1]
        for y, r in zip(ys, g.itertuples()):
            c = col.get(r.institution, figs.CAT["aqua"] if "Kissan" in r.item else figs.BLUE5[3])
            if r.rate_high > r.rate_low:
                ax.plot([r.rate_low, r.rate_high], [y, y], color=c, lw=6, solid_capstyle="round", alpha=0.85)
                ax.text(r.rate_high + 1.5, y, f"{r.rate_low:g}–{r.rate_high:g}%", va="center", fontsize=7.5)
            else:
                ax.scatter([r.rate_low], [y], s=60, color=c, edgecolor="white", linewidth=1.5, zorder=3)
                ax.text(r.rate_low + 1.5, y, f"{r.rate_low:g}%", va="center", fontsize=7.5)
        labels = [r.item + (" (from Oct 2024)" if "Kissan" in r.item else "") for r in g.itertuples()]
        ax.set_yticks(ys, labels, fontsize=7.5)
        ax.set_xlim(-2, 95); ax.set_xlabel("Percent per annum")
        ax.grid(axis="x", color="#eceae5"); ax.set_axisbelow(True)
        for s in ["top", "right"]:
            ax.spines[s].set_visible(False)
        ax.set_title(title, loc="left", fontsize=9)
    fig.suptitle("Figure P1. Formal agricultural lending rates and published estimates of the cost of arhti credit (CONTEXT)",
                 x=0.01, ha="left", fontsize=10.5, fontweight="bold")
    fig.text(0.01, -0.04, "\n".join([
        "Purposive small-sample arhti estimates (implicit annualized cost by crop; IGC 2013, interviews 2012, Table 11) vs institutional averages "
        "(SBP Monthly Statistical Bulletin Table 3.33, simple average at June quarter end); not matched contracts.",
        "Farmer-reported bank rates 9–18% from the same IGC study (supplied by Ahmed). Kissan Card: 0% for holdings up to 12.5 acres; registration "
        "from 1 Jun 2024, cards operational from 15 Oct 2024, after the FY2023-24 data period.",
        "PMN/MEDA 2019 focus-group markup (~180%) is not an annualized rate and is not plotted (docs/price_ladder_notes.md).",
        f"{figs.AUTHOR}. Script: scripts/14_cost_context.py."]), fontsize=6.4, color=figs.MUTED, va="top")
    fig.tight_layout()
    figs.save(fig, "figP1_price_ladder")


def main() -> int:
    r, n_checked = rates()
    r.to_csv(T / "sbp_agri_lending_rates.csv", index=False)
    d = ladder(r)
    d.to_csv(ROOT / "docs" / "price_ladder.csv", index=False)
    (ROOT / "docs" / "price_ladder_notes.md").write_text(NOTES)
    fig_p1(d)
    print(f"Table 3.33: {r.period.nunique()} periods; {n_checked} values checked against the June 2024 edition (all equal)")
    print(r[r.period.isin(["2012-13", "2023-24"])].pivot_table(index="period", columns=["institution", "loan_type"], values="rate_pct").T.to_string())
    return 0


if __name__ == "__main__":
    sys.exit(main())
