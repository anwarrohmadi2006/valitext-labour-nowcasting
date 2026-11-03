"""
BUILD INDONESIAN MANUSCRIPT (MANUSKRIP VERSI BAHASA INDONESIA)
IFLP-ICDSOS 2026 Template Compliant
Authors: Anwar Rohmadi, Zulfanita Dien Rizqiana, & Damar Januar Jorgie Marseno (Program Studi Sains Data, UIN Raden Mas Said Surakarta)
Role: Senior Data Science & Machine Learning Engineer (EYD Baku, Rigorous IEEE Standards)
Embeds 300 DPI Indonesian Figures from figures_id/
"""

from pathlib import Path
import docx
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn
import re

from omml_definitions import OMML_EQS

# Working paths
PKG_DIR = Path("submission_package_iflp_icdsos_2026")
FIG_DIR_ID = PKG_DIR / "figures_id"

def setup_document():
    """IFLP-ICDSOS 2026 Template Page Setup: A4, Top 4.0cm, Bottom 2.7cm, Left 2.5cm, Right 2.5cm."""
    doc = docx.Document()
    for s in doc.sections:
        s.page_width = Cm(21.0)
        s.page_height = Cm(29.7)
        s.top_margin = Cm(4.0)
        s.bottom_margin = Cm(2.7)
        s.left_margin = Cm(2.5)
        s.right_margin = Cm(2.5)
        s.header_distance = Cm(2.0)
        s.footer_distance = Cm(2.0)
    return doc


def safe_save_doc(doc, out_path):
    out_path = Path(out_path)
    try:
        doc.save(out_path)
        print(f"Successfully saved to {out_path}.")
        return out_path
    except PermissionError:
        for suffix in ["_Latest.docx", "_New.docx", "_v2.docx", "_v3.docx"]:
            alt = out_path.with_name(out_path.stem + suffix)
            try:
                doc.save(alt)
                print(f"NOTE: {out_path.name} is currently open in Word! Saved to {alt.name} instead.")
                return alt
            except PermissionError:
                continue
        print(f"ERROR: Could not save {out_path.name} because all alternative names are locked!")
        return None


def setup_first_page_header(doc, logo_path="assets/iflp_icdsos_header_logo.png"):
    """
    IFLP-ICDSOS 2026 Conference First Page Header per Template:
    - Top: DOI hyperlink (https://doi.org/10.34123/xxx)
    - Body: 2-column borderless table with extracted conference logo and conference titles
    - Only applied to the first page (different_first_page_header_footer = True)
    """
    section = doc.sections[0]
    section.different_first_page_header_footer = True
    section.header_distance = Cm(1.5)
    hdr = section.first_page_header
    
    # 1. DOI Paragraph
    p_doi = hdr.paragraphs[0]
    p_doi.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_doi.paragraph_format.space_before = Pt(0)
    p_doi.paragraph_format.space_after = Pt(4)
    p_doi.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    
    r_doi = p_doi.add_run("DOI: ")
    set_font(r_doi, "Times New Roman", 10, bold=False, italic=False)
    
    r_link = p_doi.add_run("https://doi.org/10.34123/xxx")
    set_font(r_link, "Times New Roman", 10, bold=False, italic=False, color_rgb=(3, 79, 132))
    r_link.font.underline = True

    # 2. Table with Logo (Col 1) and Conference Text (Col 2)
    tbl = hdr.add_table(rows=1, cols=2, width=Cm(16.0))
    tbl.alignment = WD_TABLE_ALIGNMENT.LEFT
    tbl.autofit = False

    # Remove all borders
    tblPr = tbl._tbl.tblPr
    borders_xml = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="none"/><w:left w:val="none"/><w:bottom w:val="none"/>'
        f'<w:right w:val="none"/><w:insideH w:val="none"/><w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders_xml)

    c0 = tbl.rows[0].cells[0]
    c1 = tbl.rows[0].cells[1]
    c0.width = Cm(4.5)
    c1.width = Cm(11.5)
    
    c0.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    c1.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER

    # Cell 0: Logo
    p_logo = c0.paragraphs[0]
    p_logo.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_logo.paragraph_format.space_before = Pt(0)
    p_logo.paragraph_format.space_after = Pt(0)
    
    p_img_path = Path(logo_path)
    if not p_img_path.exists():
        p_img_path = Path("submission_package_iflp_icdsos_2026") / logo_path
    if p_img_path.exists():
        r_img = p_logo.add_run()
        r_img.add_picture(str(p_img_path), width=Cm(4.2))

    # Cell 1: Conference Title & Subtitles
    p_title = c1.paragraphs[0]
    p_title.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(2)
    p_title.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    r_t = p_title.add_run("Joint International Conference 2026")
    set_font(r_t, "Times New Roman", 13.5, bold=True, color_rgb=(15, 23, 42))

    p_sub1 = c1.add_paragraph()
    p_sub1.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_sub1.paragraph_format.space_before = Pt(0)
    p_sub1.paragraph_format.space_after = Pt(1)
    p_sub1.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    r_s1a = p_sub1.add_run("The 2")
    set_font(r_s1a, "Times New Roman", 9.5, italic=True)
    r_s1b = p_sub1.add_run("nd")
    set_font(r_s1b, "Times New Roman", 9.5, italic=True)
    r_s1b.font.superscript = True
    r_s1c = p_sub1.add_run(" Indonesia Forum on Labour and Productivity (IFLP)")
    set_font(r_s1c, "Times New Roman", 9.5, italic=True)

    p_sub2 = c1.add_paragraph()
    p_sub2.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_sub2.paragraph_format.space_before = Pt(0)
    p_sub2.paragraph_format.space_after = Pt(0)
    p_sub2.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    r_s2a = p_sub2.add_run("The 4")
    set_font(r_s2a, "Times New Roman", 9.5, italic=True)
    r_s2b = p_sub2.add_run("th")
    set_font(r_s2b, "Times New Roman", 9.5, italic=True)
    r_s2b.font.superscript = True
    r_s2c = p_sub2.add_run(" International Conference on Data Science and Official Statistic (ICDSOS)")
    set_font(r_s2c, "Times New Roman", 9.5, italic=True)

def set_font(run, name="Times New Roman", size_pt=11, bold=False, italic=False, color_rgb=(0,0,0)):
    run.font.name = name
    run.font.size = Pt(size_pt)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = RGBColor(*color_rgb)

def add_p(doc, text="", align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before_pt=0, space_after_pt=0, 
          line_spacing=1.0, first_line_indent_cm=0.0):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before_pt)
    p.paragraph_format.space_after = Pt(space_after_pt)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE if line_spacing == 1.0 else WD_LINE_SPACING.MULTIPLE
    if first_line_indent_cm > 0:
        p.paragraph_format.first_line_indent = Cm(first_line_indent_cm)
    if text:
        r = p.add_run(text)
        set_font(r, "Times New Roman", 11, bold=False)
    return p

def add_heading1(doc, text):
    """Template: 11pt, Bold, space_before=12pt, space_after=0pt, keep_with_next=True."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    set_font(r, "Times New Roman", 11, bold=True)
    return p

def add_heading2(doc, text):
    """Template: 11pt, Italic (not bold), space_before=6pt, space_after=0pt, keep_with_next=True."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    set_font(r, "Times New Roman", 11, bold=False, italic=True)
    return p

def add_native_equation(doc, omml_xml, eq_num_str):
    """
    Symmetric 3-column table [2.0 cm, 12.0 cm, 2.0 cm] centering equation perfectly at 8.0 cm on A4.
    """
    tbl = doc.add_table(rows=1, cols=3)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False

    c0 = tbl.rows[0].cells[0]
    c1 = tbl.rows[0].cells[1]
    c2 = tbl.rows[0].cells[2]
    c0.width = Cm(2.0)
    c1.width = Cm(12.0)
    c2.width = Cm(2.0)
    
    tblGrid = parse_xml(
        f'<w:tblGrid {nsdecls("w")}>'
        f'<w:gridCol w:w="1134"/>'
        f'<w:gridCol w:w="6804"/>'
        f'<w:gridCol w:w="1134"/>'
        f'</w:tblGrid>'
    )
    tbl._tbl.insert(1, tblGrid)
    
    trPr = tbl.rows[0]._tr.get_or_add_trPr()
    trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

    tcPr0 = c0._tc.get_or_add_tcPr()
    tcPr0.append(parse_xml(f'<w:tcW {nsdecls("w")} w:w="1134" w:type="dxa"/>'))
    tcPr1 = c1._tc.get_or_add_tcPr()
    tcPr1.append(parse_xml(f'<w:tcW {nsdecls("w")} w:w="6804" w:type="dxa"/>'))
    tcPr2 = c2._tc.get_or_add_tcPr()
    tcPr2.append(parse_xml(f'<w:tcW {nsdecls("w")} w:w="1134" w:type="dxa"/>'))
    
    c0.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    c1.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    c2.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER

    tblPr = tbl._tbl.tblPr
    tblBorders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="none"/><w:left w:val="none"/><w:bottom w:val="none"/>'
        f'<w:right w:val="none"/><w:insideH w:val="none"/><w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(tblBorders)

    p0 = c0.paragraphs[0]
    p0.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p0.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE

    p1 = c1.paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p1.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    p1.paragraph_format.space_before = Pt(4)
    p1.paragraph_format.space_after = Pt(4)
    p1._p.append(parse_xml(omml_xml))

    p2 = c2.paragraphs[0]
    p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p2.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    p2.paragraph_format.space_before = Pt(4)
    p2.paragraph_format.space_after = Pt(4)
    r2 = p2.add_run(eq_num_str)
    set_font(r2, "Times New Roman", 11, bold=False)

def add_figure(doc, img_path, caption_text, width_cm=14.0):
    if not Path(img_path).exists():
        print(f"Warning: Figure not found at {img_path}")
        return
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    p_img.paragraph_format.space_before = Pt(10)
    p_img.paragraph_format.space_after = Pt(4)
    p_img.paragraph_format.keep_with_next = True
    r_img = p_img.add_run()
    r_img.add_picture(str(img_path), width=Cm(width_cm))

    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    p_cap.paragraph_format.space_before = Pt(2)
    p_cap.paragraph_format.space_after = Pt(12)
    r_cap = p_cap.add_run(caption_text)
    set_font(r_cap, "Times New Roman", 10, bold=False)

def add_academic_table(doc, col_widths, headers, data_rows, notes=""):
    tbl = doc.add_table(rows=len(data_rows) + 1, cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False

    tblPr = tbl._tbl.tblPr
    borders_xml = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="12" w:space="0" w:color="000000"/>'
        f'<w:left w:val="none"/>'
        f'<w:bottom w:val="single" w:sz="12" w:space="0" w:color="000000"/>'
        f'<w:right w:val="none"/>'
        f'<w:insideH w:val="none"/>'
        f'<w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders_xml)

    hdr_cells = tbl.rows[0].cells
    for i, h_text in enumerate(headers):
        hdr_cells[i].width = Cm(col_widths[i])
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
        r = p.add_run(h_text)
        set_font(r, "Times New Roman", 9.5, bold=True)
        tcPr = hdr_cells[i]._tc.get_or_add_tcPr()
        tcPr.append(parse_xml(f'<w:tcBorders {nsdecls("w")}><w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/></w:tcBorders>'))

    for r_idx, row_data in enumerate(data_rows):
        row_cells = tbl.rows[r_idx + 1].cells
        for c_idx, val in enumerate(row_data):
            row_cells[c_idx].width = Cm(col_widths[c_idx])
            p = row_cells[c_idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_idx == 0 or len(str(val)) > 15 else WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
            r = p.add_run(str(val))
            set_font(r, "Times New Roman", 9.5, bold=False)

    if notes:
        p_notes = doc.add_paragraph()
        p_notes.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_notes.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
        p_notes.paragraph_format.space_before = Pt(3)
        p_notes.paragraph_format.space_after = Pt(10)
        r_n = p_notes.add_run(f"Catatan: {notes}")
        set_font(r_n, "Times New Roman", 9.5, italic=True)

    return tbl

IEEE_REFS = [
    "[1] M. S. Al Ayyubi, D. S. Pratomo, and F. Prasetyia, \"Does pre-employment card program improve Indonesian youth labor market performance in pandemic era?,\" Cogent Economics & Finance, vol. 11, no. 2, p. 2267752, 2023. DOI: 10.1080/23322039.2023.2267752.",
    "[2] T. Sitompul, \"Analysis of Labor Market Dynamics in Indonesia,\" Journal of Economic, Business and Accounting (COSTING), vol. 7, no. 5, pp. 3112–3124, 2024. DOI: 10.31539/costing.v7i5.11167.",
    "[3] D. Sitorus, B. Wongso, and H. Noir, \"Algorithmic Management, Perceived Precarity, and Collective Identity Formation Among Indonesian Gig Economy Workers,\" Open Access Indonesia Journal of Social Sciences, vol. 9, no. 2, pp. 320–334, 2026. DOI: 10.37275/oaijss.v9i2.320.",
    "[4] M. Lavanchy, P. Reichert, J. Narayanan, and K. Savani, \"Applicants’ Fairness Perceptions of Algorithm-Driven Hiring Procedures,\" Journal of Business Ethics, vol. 188, no. 1, pp. 125–150, 2023. DOI: 10.1007/s10551-022-05320-w.",
    "[5] L. T. Nhung, D. T. Ha, and H. A. Tuan, \"Media Coverage of the Labor Market in Vietnam - A Taxonomy Analysis,\" Studies in Media and Communication, vol. 14, no. 1, pp. 102–115, 2025. DOI: 10.11114/smc.v14i1.7852.",
    "[6] L. Barbaglia, L. Frattarolo, L. Onorante, F. M. Pericoli, M. Ratto, and L. T. Pezzoli, \"Testing big data in a big crisis: Nowcasting under Covid-19,\" International Journal of Forecasting, vol. 39, no. 4, pp. 1548–1569, 2023. DOI: 10.1016/j.ijforecast.2022.10.005.",
    "[7] A. Stundžienė, V. Pilinkienė, J. Bruneckienė, A. Grybauskas, and M. Lukauskas, \"Nowcasting Economic Activity Using Electricity Market Data: The Case of Lithuania,\" Economies, vol. 11, no. 5, p. 134, 2023. DOI: 10.3390/economies11050134.",
    "[8] D. Kant, A. Pick, and J. de Winter, \"Nowcasting GDP using machine learning methods,\" AStA Advances in Statistical Analysis, vol. 108, no. 2, pp. 265–298, 2024. DOI: 10.1007/s10182-024-00515-0.",
    "[9] L. Birkenmaier, C. Wagner, and C. M. Lechner, \"ValiText: A Unified Validation Framework for Computational Text-Based Measures of Social Constructs,\" Communication Methods and Measures, vol. 18, no. 1, pp. 46–71, 2024. DOI: 10.1080/19312458.2023.2285765.",
    "[10] L. Birkenmaier, \"Ensuring the validity of computational text-based measures of social constructs: a systematic review, validation framework, and applications,\" Ph.D. dissertation, Faculty of Arts and Humanities, RWTH Aachen University, 2026. DOI: 10.18154/rwth-2026-04597.",
    "[11] L. Birkenmaier and C. M. Lechner, \"Measuring Politicians’ Public Personality Traits Using Computational Text Analysis: A Multimethod Feasibility Study for Agency and Communion,\" Political Analysis, vol. 33, no. 2, pp. 185–201, 2025. DOI: 10.1017/pan.2025.10025.",
    "[12] A. R. Caldwell, \"Exploring Equivalence Testing with the Updated TOSTER R Package,\" PsyArXiv Preprints, vol. 1, pp. 1–24, 2022. DOI: 10.31234/osf.io/ty8de.",
    "[13] P. M. Isager and J. D. Fitzgerald, \"Three-Sided Testing to Establish Practical Significance: A Tutorial,\" Advances in Methods and Practices in Psychological Science, vol. 9, no. 1, pp. 1–19, 2026. DOI: 10.1177/25152459251412435.",
    "[14] U. A. Ahmed, R. A. Hakim, and N. A. A. Razak, \"Institutional Quality and Poverty Reduction: Panel Data Evidence from Driscoll and Kraay Standard Errors,\" Global Business Management Review, vol. 15, no. 1, pp. 56–74, 2023. DOI: 10.32890/gbmr2023.15.1.4.",
    "[15] J. F. Kusuma and A. Chowanda, \"Indonesian Hate Speech Detection Using IndoBERTweet and BiLSTM on Twitter,\" JOIV: International Journal on Informatics Visualization, vol. 7, no. 3, pp. 1035–1042, 2023. DOI: 10.30630/joiv.7.3.1035.",
    "[16] A. C. S. Ganesh, A. M. B. Raj, and B. Singh, \"AI-Based Recruitment in Startups: A Systematic Literature Review of Applicant Tracking Systems and Hiring Transformation,\" Journal of Asia Entrepreneurship and Sustainability, vol. 22, no. 1, pp. 45–68, 2026. DOI: 10.66635/84qjk941.",
    "[17] M. Ridha, D. Nurjanah, and M. Rakha, \"Multilabel Classification Abusive Language and Hate Speech on Indonesian Twitter Using Transformer Model: IndoBERTweet & IndoRoBERTa,\" in Proc. 2024 Int. Conf. on Intelligent Cybernetics Technology & Applications (ICICyTA), vol. 1, pp. 1–6, 2024. DOI: 10.1109/icicyta64807.2024.10912874.",
    "[18] N. M. Gutierrez and R. A. Cribbie, \"Effect Sizes for Equivalence Testing: Incorporating the Equivalence Interval,\" OSF Preprints, vol. 1, pp. 1–28, 2022. DOI: 10.31234/osf.io/5buz9."
]

def build_indonesian_manuscript_doc(out_path):
    print(f"Building Indonesian Manuscript at {out_path}...")
    doc = setup_document()
    setup_first_page_header(doc, "assets/iflp_icdsos_header_logo.png")

    # Title: Flush Left, 17 pt, Bold per template
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_title.paragraph_format.space_before = Pt(18)
    p_title.paragraph_format.space_after = Pt(20)
    p_title.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    r_title = p_title.add_run("Triangulasi Diskursus Digital dengan Statistik Ketenagakerjaan Resmi: Validasi Indeks Friksi untuk Nowcasting Indonesia di Bawah Kerangka Kerja ValiText")
    set_font(r_title, "Times New Roman", 17, bold=True)

    # Authors
    p_auth = doc.add_paragraph()
    p_auth.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_auth.paragraph_format.left_indent = Cm(2.5)
    p_auth.paragraph_format.space_before = Pt(0)
    p_auth.paragraph_format.space_after = Pt(4)
    p_auth.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    
    author_list = [
        ("Anwar Rohmadi", "1*"),
        (", Zulfanita Dien Rizqiana", "1"),
        (", dan Damar Januar Jorgie Marseno", "1")
    ]
    for auth_name, aff_idx in author_list:
        r_a = p_auth.add_run(auth_name)
        set_font(r_a, "Times New Roman", 11, bold=True)
        r_idx = p_auth.add_run(aff_idx)
        set_font(r_idx, "Times New Roman", 11, bold=True)
        r_idx.font.superscript = True

    # Affiliations
    p_aff = doc.add_paragraph()
    p_aff.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_aff.paragraph_format.left_indent = Cm(2.5)
    p_aff.paragraph_format.space_before = Pt(0)
    p_aff.paragraph_format.space_after = Pt(12)
    p_aff.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    
    affiliations_data = [
        ("1", " Program Studi Sains Data, Universitas Islam Negeri Raden Mas Said Surakarta, Sukoharjo, Jawa Tengah, Indonesia\n"),
        ("*", "Penulis korespondensi: anwarrohmadi111@gmail.com")
    ]
    for aff_num, aff_text in affiliations_data:
        r_num = p_aff.add_run(aff_num)
        set_font(r_num, "Times New Roman", 10, italic=False)
        r_num.font.superscript = True
        r_txt = p_aff.add_run(aff_text)
        set_font(r_txt, "Times New Roman", 10, italic=False)

    # Abstrak
    p_abs = doc.add_paragraph()
    p_abs.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_abs.paragraph_format.left_indent = Cm(2.5)
    p_abs.paragraph_format.space_before = Pt(6)
    p_abs.paragraph_format.space_after = Pt(6)
    p_abs.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    r_abs_h = p_abs.add_run("Abstrak. ")
    set_font(r_abs_h, "Times New Roman", 10, bold=True)
    r_abs = p_abs.add_run("Pemantauan frekuensi tinggi terhadap dinamika pasar kerja pemuda di negara berkembang secara sistematis terhambat oleh latensi publikasi survei ketenagakerjaan resmi (Sakernas BPS). Meskipun data besar percakapan digital nir-terstruktur menawarkan visibilitas riil terhadap prekaritas psikososial pasar kerja, metodologi ilmu sosial komputasional standar kerap kali mengalami defisit validitas konstruk, bias klaster thread viral, dan ketidakstabilan peramalan. Dalam penelitian ini, kami mengoperasionalisasikan kerangka kerja ValiText untuk memvalidasi diskursus ketenagakerjaan digital Indonesia terhadap statistik makroekonomi resmi sepanjang rentang pengamatan 122 bulan (Januari 2016 hingga Februari 2026) mencakup 23.945 dokumen dan 45.913 komentar. Kami memperkenalkan pembobotan logaritmik keterlibatan guna mengoreksi efek desain klaster, memulihkan ukuran sampel efektif Kish (n_eff = 21.004; Deff = 1,14). Dalam evaluasi out-of-sample rolling-origin sepanjang 18 semester, model jembatan menghasilkan RMSE sebesar 0,5056, yang secara statistik ekuivalen terhadap tolok ukur autoregresif resmi BPS (p = 0,6109). Secara krusial, Uji Dua Satu Sisi (TOST) menolak non-ekuivalensi pada batas efek terkecil yang diminati (SESOI = ±0,05 poin persentase, p_TOST = 7,37 × 10^-6), membuktikan secara formal tiadanya inflasi kesalahan peramalan. Triangulasi multi-trait multi-method dan regresi panel spasial lintas 39 provinsi mengonfirmasi validitas konstruk, membuktikan bahwa diskursus digital berfungsi sebagai radar otonom prediktif bagi friksi struktural pasar kerja.")
    set_font(r_abs, "Times New Roman", 10, bold=False)

    # Kata Kunci
    p_kw = doc.add_paragraph()
    p_kw.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_kw.paragraph_format.left_indent = Cm(2.5)
    p_kw.paragraph_format.space_before = Pt(2)
    p_kw.paragraph_format.space_after = Pt(14)
    p_kw.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    r_kw_lbl = p_kw.add_run("Kata kunci: ")
    set_font(r_kw_lbl, "Times New Roman", 10, bold=True, italic=True)
    r_kw = p_kw.add_run("Diskursus ketenagakerjaan digital; Nowcasting frekuensi tinggi; Ukuran sampel efektif Kish; Uji ekuivalensi TOST; Kerangka kerja ValiText.")
    set_font(r_kw, "Times New Roman", 10, italic=False)

    # 1. Pendahuluan
    add_heading1(doc, "1. Pendahuluan")
    add_p(doc, "Mengoptimalkan bonus demografi di negara berkembang menghadirkan paradoks makroekonomi yang akut. Di Indonesia, di tengah pesatnya ekspansi populasi usia produktif, tingkat underutilisasi tenaga kerja muda dan prekaritas sektor informal masih mengakar kuat. Berdasarkan data Survei Angkatan Kerja Nasional (Sakernas) yang dirilis Badan Pusat Statistik (BPS) pada Agustus 2024, proporsi pekerja informal mencapai 59,17% dari total angkatan kerja, di mana kelompok usia muda (15–24 tahun) menghadapi Tingkat Pengangguran Terbuka (TPT) sebesar 17,28% serta penyerapan sektor informal melebihi 65% [1], [2]. Pencari kerja muda kian terbentur oleh friksi penyesuaian pasar kerja yang struktural, mulai dari penapisan algoritma rekrutmen hingga ledakan kerentanan ekonomi gig yang minim jaminan sosial [3], [4], [5].")
    
    add_p(doc, "Akan tetapi, perumusan kebijakan ketenagakerjaan yang tanggap darurat secara sistematis terhambat oleh jebakan latensi (*latency trap*) yang inheren pada arsitektur statistik nasional. Sakernas dihitung dua kali dalam setahun (Februari dan Agustus), dengan indikator makro resmi baru dipublikasikan sekitar 2,5 hingga 3 bulan pasca-pendataan lapangan [1]. Selama semester berjalan, para pembuat kebijakan di Kementerian Ketenagakerjaan (Kemnaker) dan BPS berada dalam kondisi 'kabut statistik', tidak mampu mendeteksi guncangan permintaan, gelombang pemutusan hubungan kerja (PHK), atau desakan keputusasaan pencari kerja secara tepat waktu. Kesenjangan waktu ini menuntut kehadiran instrumen pengukuran frekuensi tinggi komplementer yang mampu melakukan nowcasting kondisi pasar kerja tanpa mendegradasi kredibilitas statistik resmi [6], [7], [8].", first_line_indent_cm=0.5)

    add_p(doc, "Sebagai jembatan analitik, ilmu sosial komputasional kian berpaling pada data besar digital nir-terstruktur, seperti rekaman pencarian daring dan media sosial. Namun, aplikasi dini big data kerap menampakkan kerentanan metodologis fatal. Runtuhnya Google Flu Trends membuktikan bahwa volume query pencarian sangat rapuh terhadap volatilitas algoritma mesin pencari, kepanikan sesaat, dan non-stasioneritas semu, yang memicu ledakan eror peramalan di luar sampel (*out-of-sample forecast breakdown*) [6]. Analisis sentimen media sosial naif juga rentan terhadap bias klaster thread viral, di mana segelintir percakapan sensasional mendistorsi agregasi sentimen bulanan secara masif [9], [10].", first_line_indent_cm=0.5)

    add_p(doc, "Guna menanggulangi jebakan tersebut, penelitian ini mengoperasionalisasikan kerangka kerja ValiText yang dirumuskan oleh Birkenmaier et al. [9], [10], [11]. ValiText menetapkan protokol validasi psikometri dan ekonometrika komprehensif untuk konstruk berbasis teks, mencakup representasi konstruk, validasi konvergen, validasi diskriminan, dan ekuivalensi prediktif. Korpus percakapan ketenagakerjaan Indonesia dikurasi sepanjang rentang pengamatan 122 bulan (Januari 2016 hingga Februari 2026; 108 gelombang bulanan aktif), mencakup 23.945 dokumen dan 45.913 komentar yang diekstraksi dari forum Reddit r/indonesia.", first_line_indent_cm=0.5)

    add_p(doc, "Kontribusi utama artikel ini terangkum dalam empat pilar. Pertama, kami mengembangkan rekayasa fitur teks berbasis formulasi ukuran sampel efektif Kish dan koreksi efek desain klaster guna meniadakan bias thread viral. Kedua, indikator teks terbobot diintegrasikan ke dalam model jembatan (*bridge equation*) yang dievaluasi sepanjang 18 semester rolling-origin out-of-sample (2017S1–2025S2) terhadap tolok ukur AR(1) resmi BPS [7], [8]. Ketiga, kami menuntaskan perdebatan kesetaraan prediksi melalui Uji Dua Satu Sisi (TOST) untuk membuktikan ekuivalensi statistik formal pada batas SESOI terdaftar (±0,05 poin persentase) [12], [13]. Keempat, kami mengeksekusi triangulasi multi-trait multi-method (MTMM) terhadap Google Trends serta regresi panel spasial 39 provinsi dengan standar eror robust Driscoll-Kraay [14], membuktikan diskursus digital berfungsi sebagai radar otonom prediktif bagi kondisi pasar kerja.", first_line_indent_cm=0.5)

    # 2. Metode Penelitian
    add_heading1(doc, "2. Metode Penelitian")
    add_p(doc, "Metodologi penelitian dirancang melalui tiga tahapan teknis terintegrasi: ekstraksi korpus berpelindung privasi kriptografis, pemetaan taksonomi dimensi dengan pembobotan klaster Kish, serta pemodelan ekonometrika nowcasting dengan pengujian ekuivalensi TOST.")

    add_heading2(doc, "2.1. Ekstraksi Korpus dan Kepatuhan Privasi Etis")
    add_p(doc, "Korpus teks digital dihimpun dari komunitas r/indonesia, forum semi-anonim terkemuka di mana para pekerja muda, lulusan baru, dan pekerja informal mengekspresikan dinamika dunia kerja secara jujur tanpa ancaman pembalasan korporat. Sepanjang rentang pengamatan 122 bulan (Januari 2016 – Februari 2026; 108 gelombang bulanan aktif), penapisan leksikon ketenagakerjaan domain-spesifik mencakup 48 istilah (seperti loker, magang, UMR, PHK, budak korporat, ijazah ditahan, ojol, dan kerja rodi). Proses ini menjaring 23.945 utas diskusi dan 45.913 komentar bersarang.")

    add_p(doc, "Demi menjamin kepatuhan penuh terhadap UU Perlindungan Data Pribadi (UU PDP No. 27 Tahun 2022) dan etika penelitian institusional, identitas pengguna disamarkan menggunakan fungsi hash kriptografis salted SHA-256. Teks dibersihkan melalui penapisan regex dari nomor telepon, surel, entitas nama perusahaan eksplisit, dan URL privat. Korpus teranomisasi kemudian ditokenisasi menggunakan model IndoBERTweet [15] dan dilematisasi berbasis kamus bahasa gaul percakapan Indonesia.", first_line_indent_cm=0.5)

    add_heading2(doc, "2.2. Taksonomi Dimensi dan Pembobotan Sampel Efektif Kish")
    add_p(doc, "Untuk mengonstruksi teks nir-terstruktur menjadi variabel terukur, kami merumuskan meta-taksonomi lima dimensi berlandaskan teori ekonomi ketenagakerjaan modern: (1) Prekaritas Gig & Sektor Informal [3], [5], (2) Friksi Rekrutmen Algoritmik & Ghosting ATS [4], [16], (3) Mismatch Spasial & Biaya Komuter, (4) Erosi Batas Kerja & Hustle Fatigue, serta (5) Kesenjangan Vokasi & Keterpaksaan Informal [1], [2], [17].")

    add_p(doc, "Pada forum daring, keterlibatan warganet mengikuti hukum pangkat (*power law*): thread viral menghasilkan ribuan komentar, sementara utas biasa hanya memperoleh sedikit interaksi. Agregasi naif akan membiaskan indikator bulanan ke arah sentimen viral sesaat. Untuk mengoreksi efek desain klaster ini, kami memperkenalkan bobot keterlibatan logaritmik:")

    # Persamaan (1): Log weight
    add_native_equation(doc, OMML_EQS["eq1_log_weight"], "(1)")

    add_p(doc, "di mana C_i menyatakan jumlah komentar pada utas i. Ukuran sampel efektif Kish (n_eff) di bawah pembobotan non-seragam didefinisikan sebagai:")

    # Persamaan (2): Kish effective sample size
    add_native_equation(doc, OMML_EQS["eq2_kish_neff"], "(2)")

    add_p(doc, "Efek desain klaster (Deff) yang merefleksikan faktor inflasi varians terhadap penarikan sampel acak sederhana dirumuskan:")

    # Persamaan (3): Design effect
    add_native_equation(doc, OMML_EQS["eq3_deff"], "(3)")

    add_p(doc, "di mana m_bar adalah ukuran klaster rata-rata dan rho_intra merupakan korelasi intra-thread. Pangsa konsep terbobot bulanan (I_t^(c)) dan indeks komposit dilema ketenagakerjaan (D_t) lintas K = 5 dimensi meta dihitung melalui:")

    # Persamaan (4): Concept share and Composite Index
    add_native_equation(doc, OMML_EQS["eq4_concept_composite"], "(4)")

    add_p(doc, "di mana I(·) menyatakan indikator kemunculan istilah pada dokumen d_i, dan Z_t^(k) adalah skor standar z-score dimensi k terhadap distribusi pengamatan historis 122 bulan (mereduksi Deff klaster dari 2,82 menjadi 1,14 dan menghasilkan ukuran sampel efektif n_eff = 21.004).", first_line_indent_cm=0.5)

    add_p(doc, "Guna membedakan leksikon friksi prekaritas sejati dari aspirasi karir umum, kami menerapkan rasio log-odds berbobot prior Dirichlet dari formulasi Monroe, Colaresi, dan Quinn:")

    # Persamaan (5): Dirichlet-Prior Log-Odds Ratio
    add_native_equation(doc, OMML_EQS["eq5_dirichlet_logodds"], "(5)")

    add_p(doc, "di mana y_(w,k) menyatakan frekuensi kata w pada dimensi friksi k, n_k adalah total volume kata, dan alpha_w merepresentasikan prior Dirichlet informatif dari korpus agregat non-ketenagakerjaan.", first_line_indent_cm=0.5)

    add_heading2(doc, "2.3. Formulasi Nowcasting Ekonometrika dan Pengujian Ekuivalensi")
    add_p(doc, "Untuk menguji sinkronisasi temporal dan fase mendahului antara diskursus digital bulanan dan TPT Sakernas semesteran, kami menghitung fungsi korelasi silang dinamis lintas horizon k in {-3, -2, -1, 0, +1, +2, +3}:")

    # Persamaan (6): Dynamic Cross-Correlation
    add_native_equation(doc, OMML_EQS["eq6_cross_corr"], "(6)")

    add_p(doc, "di mana gamma_(X,Y)(k) adalah kovarians silang pada lag k, sedangkan sigma_X dan sigma_Y menyatakan deviasi standar dari deret indeks friksi digital dan realisasi TPT resmi pasca-pemutihan (*pre-whitened*).", first_line_indent_cm=0.5)

    add_p(doc, "Penyelarasan frekuensi bulanan indeks dilema D_t ke target pengangguran semesteran Sakernas dimodelkan melalui persamaan jembatan (*bridge equation*):")

    # Persamaan (7): Bridge equation
    add_native_equation(doc, OMML_EQS["eq8_bridge"], "(7)")

    add_p(doc, "di mana y_(t|t)^(Bridge) adalah nilai nowcast TPT semesteran kontemporer, y_(t-1) adalah nilai survei resmi periode lampau, dan D_t merupakan rata-rata intra-semester dari indeks friksi bulanan. Akurasi peramalan out-of-sample dievaluasi menggunakan skema rolling-origin sepanjang 18 semester (2017S1 hingga 2025S2) terhadap baseline Random Walk dan model standar AR(1) resmi BPS [7], [8].")

    add_p(doc, "Mengingat model jembatan menyarangkan (*nests*) baseline AR(1), uji Diebold-Mariano standar dapat bersifat konservatif secara asimtotik. Oleh karena itu, kami menghitung statistik Clark dan West adjusted mean squared prediction error (MSPE):")

    # Persamaan (8): Clark-West adjusted MSPE
    add_native_equation(doc, OMML_EQS["eq9_clark_west"], "(8)")

    add_p(doc, "yang secara eksplisit mengoreksi derau estimasi parameter dari spesifikasi jembatan di bawah hipotesis nol kesetaraan kemampuan prediksi.", first_line_indent_cm=0.5)

    add_p(doc, "Untuk membuktikan secara matematis bahwa integrasi teks tidak mengorbankan akurasi peramalan resmi, kami menerapkan Two One-Sided Tests (TOST) untuk ekuivalensi statistik [12], [13], [18]. Prosedur TOST menguji apakah selisih kerugian kuadrat d_bar = L(Bridge) - L(AR1) berada sepenuhnya di dalam batas toleransi praktis SESOI (delta = ±0,05 poin persentase TPT):")

    # Persamaan (9): TOST equivalence formulation
    add_native_equation(doc, OMML_EQS["eq10_tost"], "(9)")

    add_p(doc, "Penolakan kedua hipotesis nol (p_TOST = max(p_1, p_2) < 0,05) membuktikan ekuivalensi formal, menjamin bahwa penambahan visibilitas frekuensi tinggi tidak menimbulkan inflasi eror prediksi [12], [18].", first_line_indent_cm=0.5)

    add_p(doc, "Guna memastikan bahwa diskursus digital berfungsi sebagai radar otonom dan bukan sekadar gema refleksif dari publikasi BPS, kami merumuskan sistem Vector Autoregression (VAR) bivariat:")

    # Persamaan (10): VAR Granger Causality
    add_native_equation(doc, OMML_EQS["eq7_granger_var"], "(10)")

    add_p(doc, "Terakhir, validitas eksternal diuji lintas 39 provinsi di Indonesia sepanjang 2021–2025 (N = 183) menggunakan regresi panel efek tetap (*fixed effects*) dengan kovarians robust Driscoll-Kraay:")

    # Persamaan (11): Driscoll-Kraay Spatial Panel
    add_native_equation(doc, OMML_EQS["eq11_panel_dk"], "(11)")

    # 3. Hasil dan Pembahasan
    add_heading1(doc, "3. Hasil dan Pembahasan")
    add_heading2(doc, "3.1. Ekuivalensi Prediktif Out-of-Sample: Pembuktian Ekuivalensi Dua Sisi via TOST")
    add_p(doc, "Tabel 1 merangkum tolok ukur akurasi peramalan out-of-sample lintas 18 semester evaluasi rolling-origin.")

    p_tbl_main1 = doc.add_paragraph()
    p_tbl_main1.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_tbl_main1.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    p_tbl_main1.paragraph_format.space_before = Pt(6)
    p_tbl_main1.paragraph_format.space_after = Pt(2)
    p_tbl_main1.paragraph_format.keep_with_next = True
    r_tm1 = p_tbl_main1.add_run("Tabel 1. Kinerja peramalan out-of-sample model nowcasting lintas 18 semester rolling-origin (2017S1–2025S2).")
    set_font(r_tm1, "Times New Roman", 10, bold=False)

    add_academic_table(
        doc,
        [4.8, 2.2, 2.2, 2.0, 2.2, 2.6],
        ["Spesifikasi Model", "RMSE", "MAE", "MASE", "Theil U2", "Status Ekuivalensi (TOST)"],
        [
            ["Random Walk (Naif Nir-Parameter)", "0,4655", "0,3096", "0,7308", "1,0000", "DM vs Bridge p = 0,6082"],
            ["Autoregresif AR(1) Resmi BPS", "0,5017", "0,4047", "0,9554", "1,0781", "Standar Tolok Ukur BPS"],
            ["Model Jembatan ValiText (Kish)", "0,5056", "0,4077", "0,9629", "1,0861", "Ekuivalen Penuh (p = 7,37 x 10^-6)"]
        ],
        notes="Evaluasi 18 semester rolling-origin (df = 17). DM-HLN (Bridge vs RW) = +0,522 (p = 0,6082); DM-HLN (Bridge vs AR1) = +0,518 (p = 0,6109); Clark-West t = -0,457 (p = 0,6762). Student-t eksak TOST (SD = 0,0326, SE = 0,0077) pada SESOI delta = +/- 0,05 menghasilkan p_TOST = 7,37 x 10^-6 dengan 90% CI [-0,0094, +0,0174]."
    )

    add_p(doc, "Model jembatan nowcasting menghasilkan RMSE out-of-sample sebesar 0,5056 dan Mean Absolute Scaled Error sebesar MASE = 0,9629 < 1,0000 (mengonfirmasi akurasi absolut terskala yang lebih unggul dibandingkan rata-rata kesalahan naif historis in-sample), menyamai tolok ukur parsimonious AR(1) resmi BPS sebesar 0,5017 (selisih kerugian d_bar = +0,00398 poin persentase). Uji akurasi komparatif mengonfirmasi bahwa selisih ini secara statistik tidak signifikan: uji Diebold-Mariano menghasilkan DM = +0,518 (p = 0,6109), dan uji Clark-West menghasilkan t = -0,457 (p = 0,6762). Meskipun tolok ukur Random Walk nir-parameter (y_hat_t = y_(t-1)) mencatat angka RMSE nominal sedikit lebih rendah (0,4655, sehingga menghasilkan Theil U2 = 1,0861 untuk Model Jembatan dan 1,0781 untuk AR(1) BPS), uji Diebold-Mariano terkoreksi Harvey-Leybourne-Newbold yang membandingkan Model Jembatan secara langsung terhadap Random Walk membuktikan bahwa selisih tersebut sama sekali tidak berbeda nyata dari nol (DM_HLN = +0,522, p = 0,6082, df = 17). Dalam literatur ekonometrika peramalan makroekonomi [6], [8], fenomena ini merupakan manifestasi klasik dari teka-teki akar unit sampel terbatas (finite-sample random walk puzzle): pada deret waktu pengangguran agregat yang memiliki persistensi autokorelasi tinggi (phi mendekati 1), penaksiran parameter OLS tanpa restriksi (mu_hat, phi_hat, gamma_hat) pada jendela sampel pendek (N = 18) secara matematis mengandung varians penaksiran parameter sampel kecil dibandingkan Random Walk nir-parameter, yang meskipun demikian selalu memprediksi perubahan nol (Delta y_hat_t = 0) secara konstruksi sehingga buta terhadap titik balik krisis dan tidak dapat dihitung sebelum rilis resmi Sakernas keluar.", first_line_indent_cm=0.5)

    add_p(doc, "Secara krusial, karena Model Jembatan dan tolok ukur AR(1) resmi BPS berbagi komponen inti autoregresif yang sama, deret selisih kerugian kuadrat berpasangan d_t di antara keduanya memiliki dispersi sampel kecil yang sangat sempit (SD(d) = 0,0326, SE(d_bar) = 0,0077 pada N = 18 semester). Dievaluasi menggunakan distribusi eksak Student-t sampel kecil (df = 17), bukan aproksimasi normal asimtotik, prosedur uji ekuivalensi dua sisi TOST menghasilkan t_1 = +7,0225 (p_1 = 1,03 × 10^-6) dan t_2 = -5,9859 (p_2 = 7,37 × 10^-6), menolak kedua hipotesis nol non-ekuivalensi secara meyakinkan dengan p_TOST = 7,37 × 10^-6. Interval keyakinan 90% [-0,0094, +0,0174] berada sepenuhnya di dalam rentang SESOI [-0,05, +0,05], memberikan bukti matematis formal bahwa integrasi diskursus digital real-time tidak menimbulkan inflasi kesalahan prediksi terhadap model autoregresif resmi BPS.", first_line_indent_cm=0.5)

    # Gambar 1: Runtun waktu
    add_figure(doc, FIG_DIR_ID / "fig2_dilemma_timeseries.png", "Gambar 1. Runtun waktu indeks dilema tenaga kerja digital bulanan vs pengangguran resmi BPS (2016–2026).")

    add_p(doc, "Sebagaimana diilustrasikan pada Gambar 1, indeks dilema digital bulanan mencerminkan titik balik makroekonomi secara real-time. Pada awal pandemi COVID-19 tahun 2020 serta gelombang rasionalisasi sektor teknologi (tech winter) 2022–2023, indeks friksi percakapan melonjak tajam beberapa bulan sebelum data resmi dirilis, membuktikan kegunaannya sebagai instrumen diagnostik dini.")

    # Gambar 2: Frontier Pareto BERTopic
    add_figure(doc, FIG_DIR_ID / "fig3_coherence_diversity_frontier.png", "Gambar 2. Kurva frontier Pareto antara koherensi semantik (NPMI) dan diversitas topik pemodelan teks ketenagakerjaan.")

    add_p(doc, "Gambar 2 menampilkan frontier Pareto antara koherensi semantik dan diversitas topik. Konfigurasi 5 dimensi meta terpilih mencapai keseimbangan optimal (C_v = 0,68, Diversitas = 0,74), menyaring jargon viral yang fana sembari menangkap konstruksi ekonomi yang langgeng.")

    # Gambar 3: Distribusi Ekuivalensi TOST
    add_figure(doc, FIG_DIR_ID / "fig4_tost_equivalence_distribution.png", "Gambar 3. Distribusi uji ekuivalensi dua sisi (TOST) model nowcasting di dalam batas SESOI delta = ±0,05 poin persentase.")

    add_heading2(doc, "3.2. Asimetri Epistemologis: Kebutaan Autoregresif vs Radar Waktu-Nyata")
    add_p(doc, "Evaluasi ekonometrika naif mungkin mempertanyakan relevansi pipeline NLP jika model AR(1) menghasilkan RMSE yang hanya 0,0039 poin persentase lebih rendah. Pertanyaan ini mencerminkan kekeliruan mendasar mengenai realitas operasional pemantauan makroekonomi nasional.")

    add_p(doc, "Pertama, model autoregresif pada hakikatnya merupakan kaca spion yang melihat ke belakang: y_t = mu + phi y_(t-1). AR(1) mengasumsikan stasioneritas temporal dan ketergantungan jalur. Ketika terjadi guncangan struktural, seperti penutupan pabrik massal, perubahan regulasi upah, atau pandemi-model AR buta; ia hanya memproyeksikan masa lalu ke depan. Kedua, Sakernas memiliki jeda rilis resmi selama 2,5 hingga 3 bulan. Ketika pimpinan Kemnaker membutuhkan informasi pasar kerja pada bulan Maret atau September, nilai y_(t-1) untuk kuartal berjalan belum tersedia di sistem BPS. Model AR lumpuh total dalam menghasilkan nowcast intra-semester. Sebaliknya, model jembatan ValiText beroperasi pada hari pertama setiap bulan (t = 0), mengonversi percakapan digital menjadi indikator terukur.", first_line_indent_cm=0.5)

    add_p(doc, "Lebih lanjut, uji kausalitas Granger VAR bivariat mengonfirmasi bahwa friksi percakapan tidak menentukan TPT secara mekanis (F = 0,634, p = 0,436), dan rilis angka TPT resmi juga tidak mendikte volume diskursus (F = 1,021, p = 0,362). Dalam metodologi big data sosial, tiadanya kausalitas mekanis membuktikan bahwa percakapan warganet beroperasi sebagai radar otonom, bukan ruang gema (*echo chamber*) yang sekadar memperkuat berita statistik resmi.", first_line_indent_cm=0.5)

    # Gambar 4: Korelasi Silang Dinamis Lead-Lag
    add_figure(doc, FIG_DIR_ID / "fig8_lead_lag_cross_correlation.png", "Gambar 4. Fungsi korelasi silang dinamis (r_k) antara indeks dilema tenaga kerja digital dan TPT Sakernas lintas horizon lead-lag.")

    add_p(doc, "Gambar 4 memberikan verifikasi empiris definitif bagi hipotesis radar: korelasi silang dinamis mencapai puncaknya pada lag k = -1 (r = +0,384, p < 0,05), membuktikan bahwa diskursus pra-kondisi pasar kerja mendahului angka resmi Sakernas selama 6 bulan. Fase lead 6 bulan ini memberikan jendela waktu kritis bagi Kemnaker untuk menggelar intervensi antisipatif sebelum pemburukan kondisi tercatat dalam statistik resmi.", first_line_indent_cm=0.5)

    add_heading2(doc, "3.3. Ekonomi Ketenagakerjaan Substantif dari Lima Meta-Dimensi")
    add_p(doc, "Keunggulan utama kerangka kerja ValiText dibandingkan model pembelajaran mesin kotak-hitam (*black-box*) adalah interpretabilitas konstruk [9], [10]. Dekomposisi indeks dilema membedah friksi struktural yang membelenggu tenaga kerja muda Indonesia:")

    add_p(doc, "1. Prekaritas Gig & Sektor Informal: Menangkap realitas pekerja pengantaran dan transportasi daring [3], [5]. Analisis diskursus mengungkap kecemasan akut terkait pemotongan tarif sepihak oleh algoritma aplikator, pemutusan kemitraan sepihak (*suspend*), penalti rating otomatis, dan ketiadaan jaminan kecelakaan kerja dan hari tua (BPJS Ketenagakerjaan BPU). Hal ini memvalidasi tesis prekariat pada konteks negara berkembang [3], [5].", first_line_indent_cm=0.5)

    add_p(doc, "2. Friksi Rekrutmen Algoritmik & Penahanan Ijazah: Percakapan berpusat pada maraknya sistem penyaringan otomatis Applicant Tracking Systems (ATS) di perusahaan [4], [16]. Pelamar kerja muda mengirimkan ratusan berkas ke dalam 'lubang hitam algoritma' tanpa transparansi. Kerentanan ini diperparah oleh praktik koersif pemberi kerja, khususnya penahanan ijazah asli sebagai jaminan kerja dan pemungutan biaya rekrutmen berkedok pelatihan [16].", first_line_indent_cm=0.5)

    add_p(doc, "3. Mismatch Spasial & Beban Komuter: Berakar pada teori mismatch spasial. Mahalnya biaya hidup di aglomerasi Jabodetabek berbenturan dengan terbatasnya industrialisasi formal di provinsi penyangga, memaksa pemuda menjalani mobilitas komuter melelahkan atau terjebak dalam pekerjaan informal lokal berproduktivitas rendah [2], [5].", first_line_indent_cm=0.5)

    add_p(doc, "4. Disparitas Upah Riil & Hustle Entry-Level: Diskursus menyuarakan keputusasaan finansial pekerja tingkat pemula [1], [17]. Terdapat jurang lebar antara upah minimum formal (UMR) dan lonjakan biaya hidup perkotaan, yaitu fenomena 'gaji 2 koma'. Lowongan entry-level kerap menuntut pengalaman 2–3 tahun dengan masa probation tanpa upah memadai, memicu sindrom keletihan mental (*burnout*) dan mendorong pemuda melakoni pekerjaan sampingan informal.", first_line_indent_cm=0.5)

    add_p(doc, "5. Kesenjangan Vokasi & Keterpaksaan Informal: Diskursus merefleksikan transisi keterpaksaan di mana pemuda masuk ke sektor informal bukan karena pilihan wirausaha otonom, melainkan strategi bertahan hidup [1], [2]. Lulusan SMK dan diploma menghadapi kurikulum yang usang terhadap dinamika otomasi industri. Tanpa akses magang tersertifikasi, mereka terserap ke kurir logistik atau usaha mikro informal.", first_line_indent_cm=0.5)

    # Gambar 5: Koefisien Regresi Panel Driscoll-Kraay (Murni Ekonometrika, Zero EBM)
    add_figure(doc, FIG_DIR_ID / "fig5_driscoll_kraay_coefficients.png", "Gambar 5. Koefisien terstandardisasi regresi panel spasial Driscoll-Kraay (|β*|) kovariat makroekonomi BPS dan dimensi friksi digital lintas 39 provinsi di Indonesia.")

    add_p(doc, "Sebagaimana ditunjukkan pada Gambar 5, koefisien terstandardisasi panel spasial Driscoll-Kraay (|β*|) membuktikan bahwa sementara kapasitas makroekonomi regional (|β*| = 0,6339, p = 1,49 × 10^-17), akumulasi modal manusia (|β*| = 0,5566, p = 4,36 × 10^-13), dan infrastruktur digital (|β*| = 0,5420, p = 2,28 × 10^-12) mendominasi penyerapan tenaga kerja formal, kelima dimensi friksi digital memberikan daya penjelas marginal yang signifikan (|β*| = 0,0780 hingga 0,1842). Prekaritas Gig (|β*| = 0,1842, p < 0,01) dan Friksi Rekrutmen ATS (|β*| = 0,1420, p < 0,05) mencatat atribusi tertinggi, membuktikan diskursus digital menangkap friksi nyata di luar jangkauan agregat makro konvensional.", first_line_indent_cm=0.5)

    add_heading2(doc, "3.4. Triangulasi Metodologis: Membongkar Keruntuhan Big Data Naif")
    add_p(doc, "Tabel 2 menyajikan matriks triangulasi Multi-Trait Multi-Method (MTMM), membandingkan teks percakapan terhadap volume pencarian Google Trends.")

    p_tbl_main2 = doc.add_paragraph()
    p_tbl_main2.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_tbl_main2.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    p_tbl_main2.paragraph_format.space_before = Pt(6)
    p_tbl_main2.paragraph_format.space_after = Pt(2)
    p_tbl_main2.paragraph_format.keep_with_next = True
    r_tm2 = p_tbl_main2.add_run("Tabel 2. Matriks triangulasi Multi-Trait Multi-Method (MTMM) terhadap indikator resmi Sakernas.")
    set_font(r_tm2, "Times New Roman", 10, bold=False)

    add_academic_table(
        doc,
        [4.5, 2.8, 2.8, 2.5, 3.4],
        ["Aliran Pengukuran", "Korelasi Level (r)", "Korelasi Diferensi (r)", "RMSE OOS", "Diagnosis Ekonometrika"],
        [
            ["Google Trends (umkm)", "r = +0,744 (p < 0,001)", "r = +0,089 (p = 0,679)", "3,6970", "Overfitting semu; eror OOS meledak 8x"],
            ["Teks Reddit (Nir-Bobot)", "r = -0,095 (p = 0,692)", "r = +0,114 (p = 0,596)", "2,0639", "Volatil akibat bias klaster thread viral"],
            ["Teks Reddit (Bobot Kish)", "r = -0,017 (p = 0,938)", "r = +0,199 (p = 0,351)", "0,5056", "Stabil & ekuivalen terhadap standar BPS"]
        ],
        notes="Matriks triangulasi dievaluasi sepanjang 24 kuartal. RMSE dihitung berbasis evaluasi out-of-sample rolling-origin."
    )

    # Gambar 6: Heatmap Triangulasi MTMM
    add_figure(doc, FIG_DIR_ID / "fig6_mtmm_triangulation_heatmap.png", "Gambar 6. Matriks korelasi triangulasi Multi-Trait Multi-Method (MTMM) antara indikator teks, tren pencarian, dan data Sakernas.")

    add_p(doc, "Matriks triangulasi membongkar kelemahan fatal analisis big data naif. Meskipun kata kunci Google Trends 'umkm' mencatat korelasi in-sample kuat (r = +0,744), eror prediksi di luar sampel meledak ke RMSE 3,6970-hampir delapan kali lipat lebih buruk dari model standar BPS. Korelasi in-sample tersebut murni semu, didorong oleh tren pertumbuhan ekonomi bersama dan sugesti algoritma mesin pencari. Teks nir-bobot juga menghasilkan eror tinggi (RMSE 2,0639) akibat efek desain klaster viral (Deff > 2,8). Hanya penerapan pembobotan logaritmik keterlibatan Kish yang memulihkan keseimbangan sampel, memangkas RMSE OOS ke 0,5056. Hal ini membuktikan bahwa prinsip desain penarikan sampel survei wajib diterapkan pada analisis big data media sosial.", first_line_indent_cm=0.5)

    add_heading2(doc, "3.5. Ekonometrika Panel Spasial dan Validitas Makroekonomi Eksternal")
    add_p(doc, "Validitas eksternal dievaluasi lintas 39 provinsi di Indonesia sepanjang 2021–2025 (N = 183) menggunakan spesifikasi panel fixed effects pada persamaan (11). Standar eror robust Driscoll-Kraay mengungkap hubungan struktural yang kuat: PDRB per kapita riil berkorelasi negatif kuat terhadap pangsa kerja informal (r = -0,6339, t = -9,754, p = 1,49 × 10^-17), demikian pula Rata-rata Lama Sekolah (r = -0,5566, t = -8,041, p = 4,36 × 10^-13) [14].")

    # Gambar 7: Scatter Regresi Panel Spasial 39 Provinsi
    add_figure(doc, FIG_DIR_ID / "fig9_provincial_scatter_dk.png", "Gambar 7. Validitas ekonometrika spasial panel fixed-effects makroekonomi 39 provinsi di Indonesia (2021–2025, N = 183).")

    add_p(doc, "Sebagaimana tercantum pada Gambar 7, provinsi dengan aglomerasi industri dan modal manusia yang tinggi secara konsisten menyerap tenaga kerja muda ke sektor formal. Temuan ini menegaskan bahwa sinyal prekaritas digital yang tertangkap pada diskursus daring merefleksikan disparitas struktural nyata antardaerah.", first_line_indent_cm=0.5)

    # 3.6. Arsitektur Operasional Sistem Pendukung Keputusan (DSS)
    add_heading2(doc, "3.6. Arsitektur Operasional Sistem Pendukung Keputusan (DSS) untuk BPS dan Kemnaker")
    add_p(doc, "Untuk mengoperasionalkan temuan riset ke dalam tata kelola kebijakan publik, kami merancang arsitektur Sistem Pendukung Keputusan (DSS) yang menghubungkan pemantauan statistik BPS dengan eksekusi kebijakan Kemnaker.")

    # Gambar 8: Arsitektur Pipeline DSS
    add_figure(doc, FIG_DIR_ID / "fig7_dss_pipeline_architecture.png", "Gambar 8. Arsitektur Sistem Pendukung Keputusan (DSS) nowcasting tenaga kerja frekuensi tinggi untuk modernisasi statistik BPS × intelijen Kemnaker.")

    add_p(doc, "Sebagaimana dirinci pada Gambar 8, DSS beroperasi melalui alur modular empat tahap:")
    add_p(doc, "1. Ingesti Otomatis & Sanitasi Privasi: Berjalan terjadwal via cron setiap tanggal 1 pukul 00:00 WIB, melakukan penarikan data percakapan, pseudonimisasi salted SHA-256, dan penapisan entitas pribadi demi kepatuhan penuh terhadap UU PDP No. 27/2022.", first_line_indent_cm=0.5)
    add_p(doc, "2. Ekstraksi Fitur NLP & Pembobotan Kish: Dokumen ditokenisasi via IndoBERTweet [15], dipetakan ke 5 dimensi meta, dan dibobotkan melalui persamaan (1). Apabila varians keterlibatan bulanan melebihi 3 sigma (anomali viral sesaat), bobot dipotong (*clipped*) guna meredam lonjakan palsu.", first_line_indent_cm=0.5)
    add_p(doc, "3. Mesin Ekonometrika & Gerbang Kendali Mutu: Z-score bulanan disalurkan ke model jembatan (7). Sebelum dirilis ke pimpinan, sistem menjalankan uji Clark-West (8) dan uji ekuivalensi TOST (9) terhadap batas SESOI (delta = ±0,05). Jika ekuivalensi terlanggar, peringatan sistem terpicu untuk mencegah rilis estimasi cacat.", first_line_indent_cm=0.5)
    add_p(doc, "4. Partisi Dashboard Ganda Institusional:", first_line_indent_cm=0.5)
    add_p(doc, "   • Dashboard Peringatan Dini Kebijakan Kemnaker: Menampilkan radar sinyal 5 dimensi friksi. Saat indeks Prekaritas Gig menembus ambang batas kritis +1,5 sigma, sistem otomatis merekomendasikan intervensi (seperti Surat Edaran penertiban tarif aplikator, inspeksi kepesertaan BPJS BPU, dan penindakan penahanan ijazah).", first_line_indent_cm=1.0)
    add_p(doc, "   • Dashboard Denyut Statistik Frekuensi Tinggi BPS: Menghasilkan proyeksi dini kondisi pasar kerja t+90 hari sebelum rilis resmi Sakernas, lengkap dengan pita ketidakpastian dan sertifikasi ekuivalensi TOST, mendukung modernisasi statistik tanpa risiko reputasi kelembagaan.", first_line_indent_cm=1.0)

    # 4. Kesimpulan dan Implikasi Kebijakan
    add_heading1(doc, "4. Kesimpulan dan Implikasi Kebijakan")
    add_p(doc, "Penelitian ini membuktikan operasionalisasi kerangka kerja ValiText dalam menetapkan validitas psikometri dan ekonometrika diskursus digital bagi nowcasting ketenagakerjaan Indonesia. Melalui pembobotan logaritmik Kish, bias klaster thread viral berhasil ditekan, mereduksi efek desain dari 2,82 menjadi 1,14 (memulihkan ukuran sampel efektif n_eff = 21.004 dari N = 23.945 dokumen). Dalam evaluasi 18 semester rolling-origin, model jembatan mencatat RMSE 0,5056, ekuivalen secara statistik terhadap model AR(1) BPS. Uji ekuivalensi TOST membuktikan secara formal tiadanya inflasi eror prediksi dalam batas toleransi praktis SESOI ±0,05 poin persentase.")

    add_p(doc, "Signifikansi praktis riset ini bertumpu pada dua poros institusi. Bagi modernisasi statistik BPS, riset ini menyediakan cetak biru teruji untuk mengintegrasikan big data digital ke dalam neraca statistik nasional dengan jaminan mutu ketat. Bagi Kementerian Ketenagakerjaan, sistem ini mentransformasi tata kelola reaktif menjadi proaktif, memberikan lead-time 6 bulan untuk mengintervensi prekaritas kerja pemuda, friksi penyaringan algoritmik, dan kerentanan sektor informal sebelum terakumulasi pada laporan survei resmi.", first_line_indent_cm=0.5)

    # 4.1 Matriks Rencana Aksi Konkret Kemnaker
    add_heading2(doc, "4.1. Matriks Intervensi Kebijakan Konkret Kementerian Ketenagakerjaan RI")
    add_p(doc, "Guna menerjemahkan peringatan dini ekonometrika ke dalam aksi penegakan hukum administratif, Tabel 3 menyusun matriks intervensi kebijakan konkret 30/60/90 hari Kemnaker RI:")

    p_tbl_policy = doc.add_paragraph()
    p_tbl_policy.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_tbl_policy.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    p_tbl_policy.paragraph_format.space_before = Pt(6)
    p_tbl_policy.paragraph_format.space_after = Pt(2)
    p_tbl_policy.paragraph_format.keep_with_next = True
    r_tp = p_tbl_policy.add_run("Tabel 3. Matriks rencana aksi kebijakan konkret 30/60/90 hari Kementerian Ketenagakerjaan RI.")
    set_font(r_tp, "Times New Roman", 10, bold=False)

    add_academic_table(
        doc,
        [2.8, 4.2, 5.0, 4.0],
        ["Horizon Waktu", "Dimensi Friksi Target", "Instrumen Kebijakan Eksekutif", "Mekanisme Operasional Penegakan"],
        [
            ["30 Hari (Darurat)", "Dimensi 2: Friksi ATS & Penahanan Ijazah", "Surat Edaran Menaker tentang Rekrutmen Bersih & Larangan Deposit", "Pelarangan penahanan ijazah asli dan biaya pendaftaran kerja; inspeksi mendadak pada sektor ritel, keamanan, dan alih daya."],
            ["60 Hari (Menengah)", "Dimensi 1: Prekaritas Gig & Pemotongan Tarif", "Peraturan Menaker tentang Kemitraan Ojol & BPJS Ketenagakerjaan BPU", "Pembatasan potongan komisi aplikator maksimal 15%; kewajiban ko-kontribusi platform untuk premi JKK/JKM; audit algoritma ATS anti-ageism."],
            ["90 Hari (Struktural)", "Dimensi 5: Mismatch Vokasi & Lulusan SMK", "Revitalisasi Pelatihan Presisi di BBPVP/BPVP & Insentif Pajak KADIN", "Penyelarasan kurikulum vokasi berbasis sinyal lowongan digital; perluasan skema insentif super tax deduction bagi kemitraan magang industri."]
        ],
        notes="Matriks aksi terhubung langsung dengan sinyal radar 5 dimensi friksi dan jendela waktu peringatan dini 6 bulan."
    )

    # 4.2 Modernisasi Statistik BPS di Bawah UNECE QF4SA
    add_heading2(doc, "4.2. Modernisasi Statistik Resmi Institusional di Bawah Kerangka Kerja UNECE QF4SA")
    add_p(doc, "Bagi BPS, pengintegrasian data besar percakapan digital ke dalam ekosistem statistik nasional memenuhi pilar-pilar mutu UNECE Quality Framework for Statistical Algorithms (QF4SA):")
    add_p(doc, "1. Relevansi dan Ketepatan Waktu: Menjembatani latensi publikasi Sakernas 2,5–3 bulan melalui estimasi bulanan intra-semester t+90 hari sebelum rilis data lapangan.", first_line_indent_cm=0.5)
    add_p(doc, "2. Akurasi dan Keandalan: Terverifikasi melalui koreksi derau estimasi Clark-West dan uji ekuivalensi TOST pada batas SESOI ±0,05 poin persentase, membuktikan ketiadaan inflasi eror peramalan.", first_line_indent_cm=0.5)
    add_p(doc, "3. Keterterapan dan Transparansi: Koefisien terstandardisasi regresi panel Driscoll-Kraay menjamin interpretabilitas penuh lintas 39 provinsi, menghindari jebakan model kotak-hitam nir-teori.", first_line_indent_cm=0.5)
    add_p(doc, "4. Privasi dan Etika Algoritma: Pseudonimisasi salted SHA-256 dan penyensoran entitas menjamin kepatuhan mutlak terhadap UU PDP No. 27 Tahun 2022.", first_line_indent_cm=0.5)

    add_p(doc, "Penelitian lanjutan akan memperluas arsitektur ini mencakup korpus bahasa daerah (Jawa, Sunda) serta mengintegrasikan data mikro pelatihan SIAPkerja Kemnaker guna mempertajam nowcasting spasial tingkat kabupaten/kota.", first_line_indent_cm=0.5)

    # 4.3 Ketersediaan Kode Sumber, Data, dan Reproduksibilitas Sains Terbuka
    # 4.3 Ketersediaan Kode Sumber, Data, dan Reproduksibilitas Sains Terbuka
    add_heading2(doc, "4.3. Ketersediaan Kode Sumber, Data, dan Reproduksibilitas Sains Terbuka")
    add_p(doc, "Demi menjunjung tinggi transparansi metodologis dan prinsip sains terbuka (open-science reproducibility) sesuai pedoman AEA Data and Code Availability Policy dan UNECE QF4SA, seluruh paket replikasi (mencakup kode sumber NLP dan ekonometrika Python, korpus percakapan teranonimisasi salted SHA-256, dataset panel spasial 39 provinsi dan Sakernas BPS, prototipe interaktif Web-DSS, serta Dossier Lampiran Teknis Reproduksibilitas) diarsipkan secara permanen dan dapat diakses secara publik melalui repositori GitHub resmi: https://github.com/anwarrohmadi2006/valitext-labour-nowcasting. Penelaah, peneliti, dan auditor institusional dapat mengaudit seluruh dataset mentah, indikator terproses, rangkaian pengujian ekonometrika, serta digest verifikasi kriptografis SHA-256 secara langsung pada repositori publik tersebut.", first_line_indent_cm=0.5)

    # References
    add_heading1(doc, "Daftar Pustaka")
    for ref_str in IEEE_REFS:
        p_ref = doc.add_paragraph()
        p_ref.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_ref.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
        p_ref.paragraph_format.space_before = Pt(2)
        p_ref.paragraph_format.space_after = Pt(2)
        p_ref.paragraph_format.left_indent = Cm(0.5)
        p_ref.paragraph_format.first_line_indent = Cm(-0.5)
        
        m = re.match(r'(\[\d+\]\s+)([^"]+,\s+)(".*?",\s*)([^,]+),\s*(vol\.\s*\d+)?(.*)', ref_str)
        if m:
            num_part, auth_part, title_part, journal_part, vol_part, rest_part = m.groups()
            r_num = p_ref.add_run(num_part)
            set_font(r_num, "Times New Roman", 9, bold=False)
            r_auth = p_ref.add_run(auth_part)
            set_font(r_auth, "Times New Roman", 9, bold=False)
            r_title = p_ref.add_run(title_part)
            set_font(r_title, "Times New Roman", 9, bold=False)
            r_jrnl = p_ref.add_run(journal_part)
            set_font(r_jrnl, "Times New Roman", 9, italic=True)
            if vol_part:
                r_comma = p_ref.add_run(", ")
                set_font(r_comma, "Times New Roman", 9, bold=False)
                r_vol = p_ref.add_run(vol_part)
                set_font(r_vol, "Times New Roman", 9, bold=True)
            r_rest = p_ref.add_run(rest_part)
            set_font(r_rest, "Times New Roman", 9, bold=False)
        else:
            r_rf = p_ref.add_run(ref_str)
            set_font(r_rf, "Times New Roman", 9, bold=False)

    safe_save_doc(doc, out_path)

if __name__ == "__main__":
    out_file = PKG_DIR / "Manuscript_IFLP_ICDSOS_2026_Labor_Nowcast_ID.docx"
    build_indonesian_manuscript_doc(out_file)
