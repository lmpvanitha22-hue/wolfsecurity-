"""
generate_pdf.py
Produces Phishing_URL_Detector_Code.pdf — all 4 source files in one document.
  Cover Page
  1. Project Overview
  2. phishing_detector.py  (Python — full)
  3. templates/index.html  (HTML — full)
  4. static/style.css      (CSS  — full)
  5. static/app.js         (JS   — full)
  6. How To Run
"""

import warnings, os, textwrap
warnings.filterwarnings("ignore")

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, HRFlowable, Preformatted, KeepTogether
)

# ── Page geometry ─────────────────────────────────────────────
W, H     = A4
LM = RM  = 2 * cm
TM = BM  = 2.2 * cm
IW       = W - LM - RM          # inner (usable) width

OUT = r"d:\safi\Phishing_URL_Detector_Code.pdf"

# ── Palette ───────────────────────────────────────────────────
NAVY    = colors.HexColor("#0f172a")
DARK    = colors.HexColor("#1e293b")
DARK2   = colors.HexColor("#253348")
BORDER  = colors.HexColor("#334155")
BLUE    = colors.HexColor("#3b82f6")
PURPLE  = colors.HexColor("#7c3aed")
GREEN   = colors.HexColor("#10b981")
ORANGE  = colors.HexColor("#f59e0b")
RED     = colors.HexColor("#ef4444")
MUTED   = colors.HexColor("#94a3b8")
LIGHT   = colors.HexColor("#e2e8f0")
LIGHTER = colors.HexColor("#f8fafc")
TEXT    = colors.HexColor("#1e293b")
WHITE   = colors.white

# ── Styles ────────────────────────────────────────────────────
def S(name, **kw):
    return ParagraphStyle(name, **kw)

COVER_TITLE = S("CT", fontName="Helvetica-Bold", fontSize=32, leading=40,
                textColor=WHITE, alignment=TA_CENTER)
COVER_SUB   = S("CS", fontName="Helvetica",      fontSize=14, leading=20,
                textColor=LIGHT, alignment=TA_CENTER)
COVER_META  = S("CM", fontName="Helvetica",      fontSize=10, leading=15,
                textColor=MUTED, alignment=TA_CENTER)

SEC_HEAD    = S("SH", fontName="Helvetica-Bold", fontSize=11, leading=15,
                textColor=WHITE)
FILE_NAME   = S("FN", fontName="Helvetica-Bold", fontSize=10, leading=14,
                textColor=WHITE)
FILE_LANG   = S("FL", fontName="Helvetica",      fontSize=9,  leading=14,
                textColor=MUTED, alignment=1)

H2          = S("H2", fontName="Helvetica-Bold", fontSize=12, leading=17,
                textColor=BLUE, spaceBefore=10, spaceAfter=4)
BODY        = S("BD", fontName="Helvetica",      fontSize=9.5, leading=14,
                textColor=TEXT, spaceAfter=5, alignment=TA_JUSTIFY)
TBL_HDR     = S("TH", fontName="Helvetica-Bold", fontSize=9,  leading=13,
                textColor=NAVY)
TBL_VAL     = S("TV", fontName="Helvetica",      fontSize=9,  leading=13,
                textColor=TEXT)

CODE        = S("CD", fontName="Courier",         fontSize=7,  leading=10.5,
                textColor=TEXT, backColor=LIGHTER,
                leftIndent=5, rightIndent=5,
                spaceBefore=1, spaceAfter=1)

# ── Helpers ───────────────────────────────────────────────────
CPL = 108   # characters per line in code blocks

def section_banner(num, title, color=NAVY):
    """Full-width coloured section header."""
    t = Table([[Paragraph(f"  {num}.  {title}", SEC_HEAD)]], colWidths=[IW])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), color),
        ("TOPPADDING",    (0,0),(-1,-1), 9),
        ("BOTTOMPADDING", (0,0),(-1,-1), 9),
        ("LEFTPADDING",   (0,0),(-1,-1), 8),
    ]))
    return t

def file_banner(fname, lang, color=DARK):
    """File name + language tag bar."""
    t = Table([[Paragraph(f"  📄  {fname}", FILE_NAME),
                Paragraph(lang, FILE_LANG)]],
              colWidths=[IW*0.70, IW*0.30])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), color),
        ("TOPPADDING",    (0,0),(-1,-1), 6),
        ("BOTTOMPADDING", (0,0),(-1,-1), 6),
        ("LEFTPADDING",   (0,0),(-1,-1), 6),
        ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
    ]))
    return t

def sub_banner(title, color=DARK2):
    """Sub-section label inside a file."""
    t = Table([[Paragraph(f"  ▸  {title}", S("SB",
               fontName="Helvetica-Bold", fontSize=9, leading=13,
               textColor=LIGHT))]],
              colWidths=[IW])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), color),
        ("TOPPADDING",    (0,0),(-1,-1), 5),
        ("BOTTOMPADDING", (0,0),(-1,-1), 5),
        ("LEFTPADDING",   (0,0),(-1,-1), 10),
    ]))
    return t

def code_block(text):
    lines, out = text.splitlines(), []
    for ln in lines:
        if len(ln) <= CPL:
            out.append(ln)
        else:
            wrapped = textwrap.wrap(ln, CPL, subsequent_indent="    ",
                                    break_long_words=True, break_on_hyphens=False)
            out.extend(wrapped)
    return Preformatted("\n".join(out), CODE)

def info_table(rows, col_w=None):
    cw = col_w or [IW*0.30, IW*0.70]
    cells = []
    for i, (k, v) in enumerate(rows):
        cells.append([Paragraph(k, TBL_HDR), Paragraph(v, TBL_VAL)])
    t = Table(cells, colWidths=cw)
    t.setStyle(TableStyle([
        ("ROWBACKGROUNDS", (0,0),(-1,-1), [LIGHTER, WHITE]),
        ("GRID",           (0,0),(-1,-1), 0.4, MUTED),
        ("TOPPADDING",     (0,0),(-1,-1), 4),
        ("BOTTOMPADDING",  (0,0),(-1,-1), 4),
        ("LEFTPADDING",    (0,0),(-1,-1), 7),
    ]))
    return t

def sp(h=0.2):
    return Spacer(1, h*cm)

# ── Read source files ─────────────────────────────────────────
BASE = r"d:\safi"
def rd(p): return open(p, encoding="utf-8").read()

SRC = {
    "py":   rd(rf"{BASE}\phishing_detector.py"),
    "html": rd(rf"{BASE}\templates\index.html"),
    "css":  rd(rf"{BASE}\static\style.css"),
    "js":   rd(rf"{BASE}\static\app.js"),
}

# Split source at stable markers so section labels stay aligned as files change.
def chunks(src, sections):
    lines = src.splitlines()
    starts = [0]
    for _, marker in sections[1:]:
        starts.append(next(i for i, line in enumerate(lines) if marker in line))
    return [
        (label, "\n".join(lines[start:starts[index + 1] if index + 1 < len(starts) else len(lines)]))
        for index, ((label, _), start) in enumerate(zip(sections, starts))
    ]

py_lines   = SRC["py"].splitlines()
html_lines = SRC["html"].splitlines()
css_lines  = SRC["css"].splitlines()
js_lines   = SRC["js"].splitlines()

PY_CHUNKS = [
    ("Imports and project setup", None),
    ("1 — Blacklist configuration", "1. Blacklist setup"),
    ("2 — Feature extraction", "2. Feature extraction"),
    ("3 — Training data, models, and cross-validation", "3. Training data & model fitting"),
    ("4 — Prediction and explanation helpers", "4. Prediction helpers"),
    ("5 — Prediction pipeline and startup checks", "5. Main prediction function"),
    ("6 — Flask routes, batch prediction, and metrics", "6. Flask app"),
]

HTML_CHUNKS = [
    ("Document head and navigation", None),
    ("Hero", '<section class="hero">'),
    ("Awareness section", '<section id="features"'),
    ("Detection workflow", '<section id="workflow"'),
    ("Analyzer input", '<section id="analyzer"'),
    ("Batch results table", '<div id="batchPanel"'),
    ("Single-URL result details", '<div id="resultPanel"'),
    ("Model metrics and footer", '<section class="metrics-section"'),
]

CSS_CHUNKS = [
    ("Reset and CSS variables", None),
    ("Navigation", ".topbar {"),
    ("Hero and content sections", ".hero {"),
    ("Analyzer controls", ".analyzer-card {"),
    ("Batch and model-metric tables", ".batch-panel,"),
    ("Single-URL result panel", ".result-panel {"),
    ("Model and reason cards", ".models-grid {"),
    ("Footer", ".site-footer {"),
    ("Responsive breakpoints", "@media (max-width: 900px) {"),
]

JS_CHUNKS = [
    ("Risk and DOM helper functions", None),
    ("URL analysis request", "async function analyzeUrl()"),
    ("Batch result rendering", "function renderBatchResults(data)"),
    ("Model metrics loading", "async function loadModelMetrics()"),
    ("Single-result rendering and events", "function renderResult(data)"),
]

# ── Page header/footer callback ───────────────────────────────
def on_page(canvas, doc):
    canvas.saveState()
    # Top bar
    canvas.setFillColor(NAVY)
    canvas.rect(LM, H - TM + 0.1*cm, IW, 0.55*cm, fill=1, stroke=0)
    canvas.setFont("Helvetica-Bold", 7.5)
    canvas.setFillColor(WHITE)
    canvas.drawString(LM + 0.3*cm, H - TM + 0.24*cm,
                      "Phishing URL Detector — Complete Source Code")
    canvas.drawRightString(LM + IW - 0.3*cm, H - TM + 0.24*cm,
                           f"Page {doc.page}")
    # Bottom rule
    canvas.setStrokeColor(BORDER)
    canvas.setLineWidth(0.4)
    canvas.line(LM, BM - 0.1*cm, LM + IW, BM - 0.1*cm)
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(MUTED)
    canvas.drawCentredString(W/2, BM - 0.35*cm,
        "For educational & research use only  ·  Phishing URL Detector")
    canvas.restoreState()

# ── Build story ───────────────────────────────────────────────
doc = SimpleDocTemplate(OUT, pagesize=A4,
      leftMargin=LM, rightMargin=RM, topMargin=TM, bottomMargin=BM,
      title="Phishing URL Detector — Complete Source Code",
      author="Phishing Detector Project",
      subject="Dual ML phishing detection system — full source")

story = []

# ═══════════════════════════════════════════════════════════════
# COVER
# ═══════════════════════════════════════════════════════════════
cover = Table([
    [sp(0.6)],
    [Paragraph("🛡️", S("ico", fontName="Helvetica", fontSize=64,
                         alignment=TA_CENTER, textColor=WHITE))],
    [sp(0.3)],
    [Paragraph("Phishing URL Detector", COVER_TITLE)],
    [sp(0.15)],
    [Paragraph("Complete Source Code Documentation", COVER_SUB)],
    [sp(0.4)],
    [HRFlowable(width=IW*0.45, color=BLUE, thickness=2)],
    [sp(0.35)],
    [Paragraph("Dual Machine-Learning Engine  ·  Flask Web Application", COVER_SUB)],
    [Paragraph("Logistic Regression  +  Random Forest  ·  Real-time Risk Analysis", COVER_SUB)],
    [sp(0.35)],
    [Paragraph("Batch URL analysis  ·  LR / RF metrics  ·  Per-model detection reasons", COVER_SUB)],
    [sp(0.6)],
    [Paragraph("Python 3  ·  HTML5  ·  CSS3  ·  JavaScript  ·  scikit-learn  ·  Flask",
               COVER_META)],
    [sp(0.15)],
    [Paragraph("For educational &amp; research use only", COVER_META)],
    [sp(0.6)],
], colWidths=[IW])
cover.setStyle(TableStyle([
    ("BACKGROUND",    (0,0),(-1,-1), NAVY),
    ("ALIGN",         (0,0),(-1,-1), "CENTER"),
    ("TOPPADDING",    (0,0),(-1,-1), 2),
    ("BOTTOMPADDING", (0,0),(-1,-1), 2),
    ("ROUNDEDCORNERS",[6]),
]))
story += [sp(1.2), cover, PageBreak()]

# ═══════════════════════════════════════════════════════════════
# SECTION 1 — PROJECT OVERVIEW
# ═══════════════════════════════════════════════════════════════
story += [section_banner("1", "Project Overview"), sp(0.3)]

story += [Paragraph("About This Project", H2),
Paragraph(
    "A full-stack phishing URL detection system built with Python and Flask. "
    "Two independent ML models (Logistic Regression and Random Forest) analyse "
    "each URL separately — producing their own risk score, verdict, and explanation. "
    "Users can submit one URL or a batch of up to 1,000 URLs. Results are combined into "
    "overall verdicts in the responsive web UI. The system also compares both models "
    "using 5-fold stratified cross-validation on its 20 synthetic sample URLs.",
    BODY), sp(0.2)]

story += [Paragraph("Tech Stack", H2),
info_table([
    ("Language",      "Python 3.13"),
    ("Web Framework", "Flask 3.x"),
    ("ML Models",     "Logistic Regression + Random Forest (scikit-learn)"),
    ("Data",          "pandas, numpy — 20 training samples, 6 features"),
    ("Frontend",      "HTML5, CSS3 (dark theme), Vanilla JavaScript (ES2020)"),
    ("Blacklist",     "blacklist.json — auto-generated on startup"),
]), sp(0.25)]

story += [Paragraph("File Structure", H2),
info_table([
    ("phishing_detector.py",  "Flask server, ML training, full prediction pipeline"),
    ("templates/index.html",  "Full page UI: hero, awareness tips, workflow, analyzer"),
    ("static/style.css",      "Dark-theme stylesheet for all UI components"),
    ("static/app.js",         "Frontend: fetch calls, per-model result rendering"),
    ("blacklist.json",        "Known-bad domains (auto-created at startup)"),
], col_w=[IW*0.38, IW*0.62]), sp(0.25)]

story += [Paragraph("Detection Workflow", H2),
info_table([
    ("Step 1 — URL Input",          "User enters any URL, domain, or IP link"),
    ("Step 2 — Normalize",          "Strip whitespace, prepend https:// if missing"),
    ("Step 3 — Blacklist Check",    "Domain checked against known-bad list → instant PHISHING if matched"),
    ("Step 4 — Feature Extraction", "url_length, domain_length, qty_dot, qty_hyphen, is_ip, has_at"),
    ("Step 5a — Logistic Regression","LR probability + LR verdict + LR-specific reasons"),
    ("Step 5b — Random Forest",     "RF probability + RF verdict + RF-specific reasons"),
    ("Step 6 — Aggregate",          "Combined score = average of LR and RF probabilities"),
    ("Step 7 — Verdict",            "< 35% = SAFE   |   35–70% = SUSPICIOUS   |   > 70% = PHISHING"),
], col_w=[IW*0.35, IW*0.65]), sp(0.25)]

story += [Paragraph("API Response Fields", H2),
info_table([
    ("status",      "Overall verdict: SAFE / SUSPICIOUS / PHISHING"),
    ("risk_score",  "Combined averaged risk percentage"),
    ("lr_prob",     "Logistic Regression risk %"),
    ("lr_status",   "LR individual verdict"),
    ("lr_reasons",  "List of LR-specific reasons (feature weight explanations)"),
    ("rf_prob",     "Random Forest risk %"),
    ("rf_status",   "RF individual verdict"),
    ("rf_reasons",  "List of RF-specific reasons (ensemble voting explanations)"),
    ("reasons",     "Shared structural detection insights"),
    ("count / results", "Batch response fields: the number of URLs and one prediction per URL"),
    ("/metrics", "5-fold cross-validation Accuracy, Precision, Recall, and F1-Score for both models"),
]), PageBreak()]

# ═══════════════════════════════════════════════════════════════
# SECTION 2 — phishing_detector.py
# ═══════════════════════════════════════════════════════════════
story += [section_banner("2", "phishing_detector.py  —  Python Backend", NAVY), sp(0.2),
          file_banner("phishing_detector.py", "Python 3  ·  Flask  ·  scikit-learn"), sp(0.15)]

for label, chunk in chunks(SRC["py"], PY_CHUNKS):
    story += [KeepTogether([sub_banner(label), code_block(chunk), sp(0.1)])]

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════
# SECTION 3 — index.html
# ═══════════════════════════════════════════════════════════════
story += [section_banner("3", "templates/index.html  —  HTML Frontend", BLUE), sp(0.2),
          file_banner("templates/index.html", "HTML5"), sp(0.15)]

for label, chunk in chunks(SRC["html"], HTML_CHUNKS):
    story += [KeepTogether([sub_banner(label), code_block(chunk), sp(0.1)])]

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════
# SECTION 4 — style.css
# ═══════════════════════════════════════════════════════════════
story += [section_banner("4", "static/style.css  —  CSS Stylesheet", PURPLE), sp(0.2),
          file_banner("static/style.css", "CSS3"), sp(0.15)]

for label, chunk in chunks(SRC["css"], CSS_CHUNKS):
    story += [KeepTogether([sub_banner(label), code_block(chunk), sp(0.1)])]

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════
# SECTION 5 — app.js
# ═══════════════════════════════════════════════════════════════
story += [section_banner("5", "static/app.js  —  JavaScript Frontend Logic", GREEN), sp(0.2),
          file_banner("static/app.js", "JavaScript ES2020"), sp(0.15)]

for label, chunk in chunks(SRC["js"], JS_CHUNKS):
    story += [KeepTogether([sub_banner(label), code_block(chunk), sp(0.1)])]

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════
# SECTION 6 — HOW TO RUN
# ═══════════════════════════════════════════════════════════════
story += [section_banner("6", "How to Run the Application", GREEN), sp(0.3)]

story += [Paragraph("Prerequisites", H2),
info_table([
    ("Python",      "3.10 or later  (tested on 3.13)"),
    ("Install",     "pip install flask scikit-learn pandas numpy"),
], col_w=[IW*0.20, IW*0.80]), sp(0.25)]

story += [Paragraph("Start the server", H2),
code_block("# From the d:\\safi directory:\npython phishing_detector.py"),
sp(0.2)]

story += [Paragraph("Open in browser", H2),
Paragraph("Navigate to <b>http://127.0.0.1:5000</b> — the app trains both ML models, "
          "runs a self-test, then serves the full web UI.", BODY), sp(0.25)]

story += [Paragraph("cURL API example", H2),
code_block(
    'curl -X POST http://127.0.0.1:5000/predict \\\n'
    '     -H "Content-Type: application/json" \\\n'
    '     -d \'{"url": "http://login-secure-paypal-verification.com"}\''
), sp(0.2)]

story += [Paragraph("Analyze a URL batch", H2),
code_block(
    'curl -X POST http://127.0.0.1:5000/predict \\\n'
    '     -H "Content-Type: application/json" \\\n'
    '     -d \'{"urls": ["http://suspicious-site.com", "https://www.example.com"]}\''
), sp(0.2)]

story += [Paragraph("Compare model evaluation metrics", H2),
code_block("curl http://127.0.0.1:5000/metrics"),
Paragraph("The metrics use phishing as the positive class and the project's 20 synthetic "
          "URLs. They illustrate the demo only and should not be treated as production "
          "performance estimates.", BODY), sp(0.2)]

story += [Paragraph("Sample JSON response", H2),
code_block("""{
  "status":      "PHISHING",
  "risk_score":  100.0,
  "lr_prob":     100.0,
  "lr_status":   "PHISHING",
  "lr_reasons":  [
    "LR heavily weighted the 3 hyphens — strong positive coefficient for phishing.",
    "URL length (50 chars) pushed the LR score up — longer URLs correlate with obfuscation."
  ],
  "rf_prob":     100.0,
  "rf_status":   "PHISHING",
  "rf_reasons":  [
    "RF trees found 3 hyphens AND long URL together — strong phishing interaction pattern.",
    "Near-unanimous agreement across the ensemble."
  ],
  "reasons":     [
    "Multiple hyphens in the domain — common trick to mimic legitimate brands.",
    "Abnormally long URL (50 characters) — often used to hide the real destination."
  ]
}""")]

# ── Build ─────────────────────────────────────────────────────
doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print(f"PDF created: {OUT}")
