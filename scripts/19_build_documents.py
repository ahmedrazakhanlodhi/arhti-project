"""19_build_documents.py: build the paper (.docx) and the presentation (.pptx) from docs/paper_draft.md and docs/slide_text.md.

    .venv/bin/python -I scripts/19_build_documents.py      (after 16_qgis_layouts.py and 17_key_numbers.py)

Text comes only from the two Markdown files (numbers in them are traced in docs/key_numbers.md); figures from outputs/figures/
(QGIS Print Layout exports *_qgis.png for Figures 2-6). Writes outputs/paper/arhti_paper.docx and outputs/slides/arhti_slides.pptx.
Paper: US Letter, 1-inch margins, Times New Roman 11 pt, 1.15 line spacing; main text first, then references, then figures
(main, then appendix), so the text length can be checked against the course limit (4-8 pages, at most 12 excluding figures).
"""

from __future__ import annotations

import re
from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor
from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor as PRGB
from pptx.util import Emu
from pptx.util import Inches as PIn
from pptx.util import Pt as PPt

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "outputs" / "figures"
OUT_P, OUT_S = ROOT / "outputs" / "paper", ROOT / "outputs" / "slides"
INK, MUTED, ACCENT = RGBColor(0x1F, 0x1F, 0x1F), RGBColor(0x5C, 0x5B, 0x57), RGBColor(0x1C, 0x5C, 0xAB)

MAIN_FIGS = [
    ("fig1_study_area_coverage.png", "Figure 1. Study area and matching of census units to boundaries (tehsils and districts)."),
    ("fig2_arhti_share_tehsil_qgis.png", "Figure 2. Reported arhti credit availability by tehsil (QGIS Print Layout)."),
    ("fig3_bivariate_arhti_commercial_qgis.png", "Figure 3. Arhti and commercial-bank credit availability together (bivariate map)."),
    ("fig4_lisa_arhti_tehsil_qgis.png", "Figure 4. LISA clusters of arhti credit availability, with FDR survivors outlined."),
    ("fig5_small_farm_reach_qgis.png", "Figure 5. Small-farm reach of formal credit by district."),
    ("fig6_dasymetric_farms_borrowers_qgis.png", "Figure 6. Dasymetric dots of small farms and proportional circles of small-farm borrower records."),
    ("figA1_holding_class_shares.png", "Figure A1. Shares of farms, operated area, borrower records and disbursement by holding class (Punjab)."),
    ("figR1_lq_maps.png", "Figure R1. Location quotients of recorded lending relative to cultivated area, by holding class."),
    ("figP1_price_ladder.png", "Figure P1. Formal lending rates and published arhti cost estimates (context)."),
]
APPX_FIGS = [
    ("figS1_classification_comparison.png", "Figure S1. Quantile vs natural-breaks classification for each choropleth."),
    ("figS2_lisa_arhti_district.png", "Figure S2. District-level LISA (MAUP scale comparison)."),
    ("figS3_literature_locations.png", "Figure S3. Locations of published studies (context only; approximate town centres)."),
    ("figS4_mouza_cooccurrence.png", "Figure S4. Village-level co-reporting of arhti and commercial-bank credit by tehsil (exploratory)."),
    ("figS5_small_farm_reach_classifications.png", "Figure S5. Small-farm reach with availability- and presence-based classes."),
    ("figS6_concentration_curve.png", "Figure S6. Concentration curve of borrower records over small farms."),
    ("figS7_moran_scatterplot.png", "Figure S7. Moran scatterplot of arhti_share (Queen weights)."),
    ("figS8_gistar_arhti_tehsil.png", "Figure S8. Getis-Ord Gi* hot and cold spots of arhti credit availability."),
    ("figS9_trend_surface.png", "Figure S9. Second-order trend surface and residuals (exploratory)."),
    ("figS10_kmeans_typology.png", "Figure S10. Exploratory k-means typology of districts."),
    ("figS11_tissot_indicatrix.png", "Figure S11. Tissot indicatrix: previous vs current analysis CRS."),
    ("figS12_classification_histograms.png", "Figure S12. Histogram of arhti_share with three 5-class schemes and their GADF."),
    ("figR2_city_shares.png", "Figure R2. Five city districts: shares of lending, farmland, farms and branches."),
]


# ------------------------------------------------------------------------------------------ Markdown subset
def blocks(md: str):
    """Yield (kind, payload): title, h1, h2, para, table(rows), bullets([(level, text)])."""
    lines = md.splitlines()
    i = 0
    while i < len(lines):
        ln = lines[i]
        if not ln.strip():
            i += 1; continue
        if ln.startswith("# "):
            yield "title", ln[2:].strip(); i += 1
        elif ln.startswith("## "):
            yield "h1", ln[3:].strip(); i += 1
        elif ln.startswith("### "):
            yield "h2", ln[4:].strip(); i += 1
        elif ln.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
                    rows.append(cells)
                i += 1
            yield "table", rows
        elif re.match(r"\s*- ", ln):
            items = []
            while i < len(lines) and (re.match(r"\s*- ", lines[i]) or (items and re.match(r"\s+\S", lines[i]))):
                m = re.match(r"(\s*)- (.*)", lines[i])
                if m:
                    items.append([len(m.group(1)) // 2, m.group(2).strip()])
                else:
                    items[-1][1] += " " + lines[i].strip()
                i += 1
            yield "bullets", items
        else:
            buf = []
            while i < len(lines) and lines[i].strip() and not re.match(r"(#|\||\s*- )", lines[i]):
                buf.append(lines[i].strip()); i += 1
            yield "para", " ".join(buf)


TOKEN = re.compile(r"(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)")


def runs(par, text, size=None, color=None):
    for part in TOKEN.split(text):
        if not part:
            continue
        if part.startswith("**"):
            r = par.add_run(part[2:-2]); r.bold = True
        elif part.startswith("*"):
            r = par.add_run(part[1:-1]); r.italic = True
        elif part.startswith("`"):
            r = par.add_run(part[1:-1]); r.font.name = "Courier New"
        else:
            r = par.add_run(part)
        if size:
            r.font.size = Pt(size)
        if color:
            r.font.color.rgb = color


def page_number_footer(section, text):
    p = section.footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(f"{text}   ·   "); r.font.size = Pt(8.5); r.font.color.rgb = MUTED
    r = p.add_run()
    for tag, txt in [("begin", None), (None, "PAGE"), ("end", None)]:
        if tag:
            el = OxmlElement("w:fldChar"); el.set(qn("w:fldCharType"), tag); r._r.append(el)
        else:
            el = OxmlElement("w:instrText"); el.set(qn("xml:space"), "preserve"); el.text = txt; r._r.append(el)
    r.font.size = Pt(8.5)


def figure(doc, name, caption, max_w=6.5, max_h=8.3):
    path = FIG / name
    if not path.exists():
        raise SystemExit(f"missing figure {name}")
    w, h = Image.open(path).size
    width = min(max_w, max_h * w / h)
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.keep_with_next = True
    p.add_run().add_picture(str(path), width=Inches(width))
    c = doc.add_paragraph(); c.alignment = WD_ALIGN_PARAGRAPH.CENTER
    runs(c, caption, 9, MUTED)
    c.paragraph_format.space_after = Pt(4)


def csv_table(doc, title, df, note):
    p = doc.add_paragraph(); runs(p, f"**{title}**", 10)
    p.paragraph_format.keep_with_next = True
    t = doc.add_table(rows=len(df) + 1, cols=len(df.columns)); t.style = "Table Grid"; t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for ci, c in enumerate(df.columns):
        cell = t.cell(0, ci); cell.text = ""; runs(cell.paragraphs[0], f"**{c}**", 8)
        sh = OxmlElement("w:shd"); sh.set(qn("w:val"), "clear"); sh.set(qn("w:fill"), "ECE4D3"); cell._tc.get_or_add_tcPr().append(sh)
    for ri, row in enumerate(df.itertuples(index=False), 1):
        for ci, v in enumerate(row):
            cell = t.cell(ri, ci); cell.text = ""
            runs(cell.paragraphs[0], v if isinstance(v, str) else ("" if v != v else (f"{v:,.0f}" if float(v).is_integer() and abs(v) >= 100 else f"{v:.3f}")), 8)
    for row in t.rows:
        for cell in row.cells:
            cell.paragraphs[0].paragraph_format.space_after = Pt(0); cell.paragraphs[0].paragraph_format.line_spacing = 1.0
    n = doc.add_paragraph(); runs(n, note, 8.5, MUTED); n.paragraph_format.space_after = Pt(10)


def appendix_tables(doc):
    import pandas as pd
    T = ROOT / "outputs" / "tables"
    h = pd.read_csv(T / "course_h1_by_source.csv")
    h = h[["source", "mouza_share_reporting", "spearman_rho", "spearman_p_bh", "bivariate_moran_I", "bivariate_moran_p", "mh_or",
           "mh_ci95_low", "mh_ci95_high", "mh_strata", "breslow_day_p"]]
    h.columns = ["Formal source", "Mouzas reporting", "Spearman ρ", "BH p", "Bivariate I", "Pseudo p", "MH odds ratio", "CI low", "CI high",
                 "Strata", "Breslow–Day p"]
    csv_table(doc, "Table B1. Arhti credit availability against each formal source", h,
              "Mouza Census 2020 (Jan–Mar 2020); availability reports, not borrowing. Spearman: same tehsil (n = 137). Bivariate Moran: arhti in a "
              "tehsil vs the source in its Queen neighbours (row-standardised; 999 permutations, seed 20261031; one-sided pseudo p). Odds ratio: "
              "Mantel–Haenszel across mouzas within tehsils; tehsils whose 2×2 table has an empty row or column are uninformative and dropped. "
              "Exploratory.")
    c = pd.read_csv(T / "course_h1_by_source.csv")
    c = c[c.source.isin(["commercial", "any formal"])][["source", "n_both_sources", "n_arhti_only", "n_other_only", "n_neither", "mouzas_in_dropped_strata"]]
    c.columns = ["Formal source", "Both reported", "Arhti only", "Formal only", "Neither", "In dropped strata"]
    csv_table(doc, "Table B2. Mouzas by reported credit sources (pooled over informative tehsil strata)", c,
              "Counts of rural populated mouzas, Mouza Census 2020. 'Any formal' = commercial bank, ZTBL, cooperative bank or microfinance bank.")
    m = pd.read_csv(T / "course_market_model.csv")[["model", "label", "coef_per_sd", "se", "p", "fit"]]
    m.columns = ["Model", "Predictor (standardised)", "Coefficient per SD", "SE", "p", "Fit"]
    csv_table(doc, "Table B3. Exploratory model of arhti credit availability (tehsils, n = 137)", m,
              "OLS with HC3 standard errors; binomial GLM on mouza counts with quasi-binomial standard errors (dispersion = Pearson χ²/df); spatial "
              "error model (ML, Queen). Associations, not effects. Data: Mouza Census 2020; ESA WorldCover 2021; MAP travel time 2015.")
    import geopandas as gpd
    q = gpd.read_file(ROOT / "outputs" / "arhti_project.gpkg", layer="q2_districts_credit_allocation")
    q = q[q.flagged == 1][["adm2_name", "flag_reasons"]]
    q.columns = ["District", "Reason flagged"]
    csv_table(doc, "Table B4. Districts flagged by the SBP data-quality screen", q,
              "Screen: F1 = a class's average loan (disbursement ÷ borrower records) above 5× or below 0.2× the Punjab median for that class; "
              "F2 = above-economic loans over 75% of the district's farm-sector disbursement. Flagged districts are marked, not dropped. "
              "SBP FY2023-24, district as reported by SBP (attribution under verification).")
    r = pd.read_csv(T / "models_arhti.csv")
    r = r[(r.level == "tehsil")][["model", "term", "coef", "se", "p"]]
    r.columns = ["Model", "Term", "Coefficient", "SE", "p"]
    csv_table(doc, "Table B5. Prespecified regressions of arhti_share (tehsils, n = 137)", r,
              "OLS (HC3), spatial error and spatial lag models, Queen weights; unstandardised coefficients. Exploratory; no model is chosen on significance.")


def build_paper():
    md = (ROOT / "docs" / "paper_draft.md").read_text()
    main, refs = md.split("## References", 1)
    refs, appx = refs.split("## Appendix (list)", 1)
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Inches(8.5), Inches(11)
    for side in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
        setattr(sec, side, Inches(1))
    st = doc.styles["Normal"]
    st.font.name = "Times New Roman"; st.font.size = Pt(11)
    st.element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    st.paragraph_format.line_spacing = 1.15; st.paragraph_format.space_after = Pt(6)
    for nm, size, before in [("Heading 1", 13, 12), ("Heading 2", 11.5, 8)]:
        h = doc.styles[nm]; h.font.name = "Times New Roman"; h.font.size = Pt(size); h.font.bold = True
        h.font.color.rgb = INK; h.paragraph_format.space_before = Pt(before); h.paragraph_format.space_after = Pt(4)
        h.paragraph_format.keep_with_next = True
        h.element.rPr.rFonts.set(qn("w:ascii"), "Times New Roman"); h.element.rPr.rFonts.set(qn("w:hAnsi"), "Times New Roman")
    page_number_footer(sec, "Lodhi and Akram, PPHA 38520")

    first_para = True
    for kind, x in blocks(main):
        if kind == "title":
            p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(x); r.bold = True; r.font.size = Pt(15)
        elif kind == "h1":
            doc.add_heading(x, level=1)
        elif kind == "h2":
            doc.add_heading(x, level=2)
        elif kind == "para":
            p = doc.add_paragraph()
            if first_para:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER; runs(p, x, 11, MUTED); first_para = False
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY; runs(p, x)
        elif kind == "bullets":
            for lvl, t in x:
                p = doc.add_paragraph(style="List Bullet" if lvl == 0 else "List Bullet 2"); runs(p, t)
                p.paragraph_format.space_after = Pt(2)
        elif kind == "table":
            t = doc.add_table(rows=len(x), cols=len(x[0])); t.style = "Table Grid"; t.alignment = WD_TABLE_ALIGNMENT.CENTER
            for ri, row in enumerate(x):
                for ci, cell in enumerate(row):
                    c = t.cell(ri, ci); c.text = ""
                    runs(c.paragraphs[0], cell, 8.5)
                    c.paragraphs[0].paragraph_format.space_after = Pt(0)
                    c.paragraphs[0].paragraph_format.line_spacing = 1.0
                    if ri == 0:
                        for r in c.paragraphs[0].runs:
                            r.bold = True
                        sh = OxmlElement("w:shd"); sh.set(qn("w:val"), "clear"); sh.set(qn("w:fill"), "ECE4D3")
                        c._tc.get_or_add_tcPr().append(sh)
            doc.add_paragraph().paragraph_format.space_after = Pt(2)
    doc.add_heading("References", level=1)
    for kind, x in blocks(refs):
        if kind == "para":
            p = doc.add_paragraph(); runs(p, x, 10)
            p.paragraph_format.left_indent = Inches(0.3); p.paragraph_format.first_line_indent = Inches(-0.3)
            p.paragraph_format.space_after = Pt(3); p.paragraph_format.line_spacing = 1.0
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
    doc.add_heading("Figures", level=1)
    for n, c in MAIN_FIGS:
        figure(doc, n, c)
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
    doc.add_heading("Appendix", level=1)
    for kind, x in blocks(appx):
        if kind == "bullets":
            for lvl, t in x:
                p = doc.add_paragraph(style="List Bullet"); runs(p, t, 10)
    appendix_tables(doc)
    for n, c in APPX_FIGS:
        figure(doc, n, c)
    OUT_P.mkdir(parents=True, exist_ok=True)
    path = OUT_P / "arhti_paper.docx"
    doc.core_properties.author = "Ahmed Raza Khan Lodhi; Hasnain Akram"
    doc.core_properties.title = "Where the Bank Ends and the Arhti Begins"
    doc.save(path)
    words = sum(len(TOKEN.sub(lambda m: m.group(0).strip("*`"), x).split()) for k, x in blocks(main) if k == "para")
    words += sum(len(t.split()) for k, x in blocks(main) if k == "bullets" for _, t in x)
    print(f"paper: {path.relative_to(ROOT)} ({words:,} words of main text excluding tables)")


# ------------------------------------------------------------------------------------------ slides
def parse_slides(md):
    slides = []
    parts = re.split(r"^## Slide \d+\. ", md, flags=re.M)[1:]
    for p in parts:
        lines = p.strip().splitlines()
        s = dict(title=lines[0].strip(), headline="", bullets=[], figures=[], notes="")
        for ln in lines[1:]:
            if ln.startswith("Headline:"):
                s["headline"] = ln.split(":", 1)[1].strip()
            elif ln.startswith("- "):
                s["bullets"].append(ln[2:].strip())
            elif ln.startswith("Figures:"):
                s["figures"] = [f.strip() for f in ln.split(":", 1)[1].split(",") if f.strip()]
            elif ln.startswith("Notes:"):
                s["notes"] = ln.split(":", 1)[1].strip()
        slides.append(s)
    return slides


def add_text(slide, x, y, w, h, text, size, bold=False, color=(0x1F, 0x1F, 0x1F), font="Helvetica Neue"):
    tb = slide.shapes.add_textbox(PIn(x), PIn(y), PIn(w), PIn(h))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]
    for part in TOKEN.split(text):
        if not part:
            continue
        r = p.add_run(); r.text = part.strip("*`") if part.startswith(("*", "`")) else part
        r.font.size = PPt(size); r.font.bold = bold or part.startswith("**"); r.font.name = font
        r.font.color.rgb = PRGB(*color)
    return tb


def fit_picture(slide, path, x, y, w, h):
    iw, ih = Image.open(path).size
    scale = min(w / iw, h / ih)
    pw, ph = iw * scale, ih * scale
    slide.shapes.add_picture(str(path), PIn(x + (w - pw) / 2), PIn(y + (h - ph) / 2), PIn(pw), PIn(ph))


def bullet(p, char="•", indent_emu=228600):
    """Real PowerPoint bullet (a:buChar) with a hanging indent, instead of a typed glyph."""
    from pptx.oxml.ns import qn as pqn
    pPr = p._p.get_or_add_pPr()
    pPr.set("marL", str(indent_emu)); pPr.set("indent", str(-indent_emu))
    for tag in ("a:buNone", "a:buChar", "a:buAutoNum"):
        for el in pPr.findall(pqn(tag)):
            pPr.remove(el)
    bu = pPr.makeelement(pqn("a:buChar"), {"char": char})
    pPr.append(bu)


def build_slides():
    slides = parse_slides((ROOT / "docs" / "slide_text.md").read_text())
    prs = Presentation()
    prs.slide_width, prs.slide_height = PIn(13.333), PIn(7.5)
    blank = prs.slide_layouts[6]
    for i, s in enumerate(slides, 1):
        sl = prs.slides.add_slide(blank)
        bg = sl.background.fill; bg.solid(); bg.fore_color.rgb = PRGB(0xFB, 0xF8, 0xF2)
        band = sl.shapes.add_shape(1, 0, 0, prs.slide_width, PIn(0.12)); band.fill.solid()
        band.fill.fore_color.rgb = PRGB(0x1C, 0x5C, 0xAB); band.line.fill.background()
        figs = [FIG / f for f in s["figures"]]
        for f in figs:
            if not f.exists():
                raise SystemExit(f"slide {i}: missing figure {f.name}")
        if i == 1:
            add_text(sl, 0.7, 1.6, 6.6, 1.6, s["title"], 36, True)
            add_text(sl, 0.7, 3.25, 6.4, 1.2, s["headline"], 18, False, (0x1C, 0x5C, 0xAB))
            for k, b in enumerate(s["bullets"]):
                add_text(sl, 0.7, 4.7 + 0.5 * k, 6.4, 0.5, b, 15, k == 0, (0x5C, 0x5B, 0x57))
            if figs:
                fit_picture(sl, figs[0], 7.6, 0.35, 5.4, 6.9)
        else:
            add_text(sl, 0.5, 0.3, 12.3, 0.7, s["title"], 26, True)
            add_text(sl, 0.5, 0.95, 12.3, 0.6, s["headline"], 17, False, (0x1C, 0x5C, 0xAB))
            text_w = 12.3 if not figs else (5.2 if len(figs) == 1 else 4.3)
            tb = sl.shapes.add_textbox(PIn(0.5), PIn(1.75), PIn(text_w), PIn(5.2))
            tf = tb.text_frame; tf.word_wrap = True
            for k, b in enumerate(s["bullets"]):
                p = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
                bullet(p)
                r = p.add_run(); r.text = TOKEN.sub(lambda m: m.group(0).strip("*`"), b)
                r.font.size = PPt(17 if not figs else 15); r.font.name = "Helvetica Neue"; r.font.color.rgb = PRGB(0x1F, 0x1F, 0x1F)
                p.space_after = PPt(10)
            if len(figs) == 1:
                fit_picture(sl, figs[0], 5.9, 1.55, 7.1, 5.55)
            elif len(figs) == 2:
                fit_picture(sl, figs[0], 4.95, 1.55, 4.1, 5.55)
                fit_picture(sl, figs[1], 9.05, 1.55, 4.1, 5.55)
        add_text(sl, 0.5, 7.08, 9, 0.3, "Lodhi and Akram · PPHA 38520 · University of Chicago · Descriptive, not causal", 9, False, (0x5C, 0x5B, 0x57))
        add_text(sl, 12.3, 7.08, 0.6, 0.3, str(i), 9, False, (0x5C, 0x5B, 0x57))
        if s["notes"]:
            sl.notes_slide.notes_text_frame.text = s["notes"]
    OUT_S.mkdir(parents=True, exist_ok=True)
    path = OUT_S / "arhti_slides.pptx"
    prs.core_properties.author = "Ahmed Raza Khan Lodhi; Hasnain Akram"
    prs.save(path)
    print(f"slides: {path.relative_to(ROOT)} ({len(slides)} slides)")


def main() -> int:
    build_paper()
    build_slides()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
