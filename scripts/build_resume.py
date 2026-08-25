#!/usr/bin/env python3
"""Generate the résumé PDF from the site data and emit its base64.

Run from repo root: python3 scripts/build_resume.py
Writes: public/manasa_vijayaraghavan_resume.pdf  and prints base64 to stdout.
"""
import base64
import re
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, ListFlowable,
    ListItem, HRFlowable, Table, TableStyle,
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT

TEAL = HexColor("#0E7C8B")
INK = HexColor("#1A1A1A")
MUTED = HexColor("#555555")
RULE = HexColor("#BFD7DC")

def md(text):
    """Convert **bold** to <b> and escape ampersands for reportlab."""
    text = text.replace("&", "&amp;")
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)

styles = {
    "name": ParagraphStyle("name", fontName="Helvetica-Bold", fontSize=20,
                            textColor=INK, leading=23, spaceAfter=2),
    "title": ParagraphStyle("title", fontName="Helvetica", fontSize=10.5,
                             textColor=TEAL, leading=13, spaceAfter=3),
    "contact": ParagraphStyle("contact", fontName="Helvetica", fontSize=8.5,
                              textColor=MUTED, leading=12),
    "section": ParagraphStyle("section", fontName="Helvetica-Bold", fontSize=10,
                              textColor=TEAL, leading=12, spaceBefore=9,
                              spaceAfter=1, tracking=1),
    "role": ParagraphStyle("role", fontName="Helvetica-Bold", fontSize=10,
                           textColor=INK, leading=12),
    "meta": ParagraphStyle("meta", fontName="Helvetica-Oblique", fontSize=8.5,
                           textColor=MUTED, leading=11, alignment=2),
    "body": ParagraphStyle("body", fontName="Helvetica", fontSize=9,
                           textColor=INK, leading=12.5),
    "bullet": ParagraphStyle("bullet", fontName="Helvetica", fontSize=8.8,
                             textColor=INK, leading=11.8),
    "skillcat": ParagraphStyle("skillcat", fontName="Helvetica-Bold", fontSize=8.8,
                               textColor=INK, leading=12),
    "skill": ParagraphStyle("skill", fontName="Helvetica", fontSize=8.8,
                            textColor=MUTED, leading=12),
}

def section(title, story):
    story.append(Paragraph(title.upper(), styles["section"]))
    story.append(HRFlowable(width="100%", thickness=0.8, color=RULE,
                            spaceBefore=1, spaceAfter=4))

def header_row(left, right, left_style, right_style, widths):
    t = Table([[Paragraph(left, left_style), Paragraph(right, right_style)]],
              colWidths=widths)
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    return t

# ---- Data (mirrors src/ManasaPortfolio.jsx) ----
NAME = "Manasa Vijayaraghavan"
TITLE = "Data Scientist & ML Engineer"
CONTACT = ("manasavijayaraghavan@gmail.com  |  Los Angeles, CA  |  "
           "linkedin.com/in/manasa-vijayaraghavan  |  github.com/Manasavijr")
ABOUT = ("Data Scientist and ML Engineer pursuing an M.S. in Applied Data Science at USC, "
         "with hands-on experience building end-to-end ML pipelines, GenAI workflows, and "
         "production-grade analytics systems. Filed a patent for real-time sign-language "
         "translation AI and delivered measurable impact at Ford Motor Company and iNextLabs. "
         "Open to Data Science, Data Analytics, AI Engineering, ML Engineering, and Data "
         "Engineering roles.")

EXPERIENCE = [
    ("Wipro", "AI Native Intern", "June 2026 – August 2026", [
        "Built **AgenticOS BFSI Skills**, an agentic decision-support library for **Banking, Financial Services & Insurance**, owning two life-insurance skills end to end.",
        "Architected multi-step **LangGraph** agent workflows with a **human-in-the-loop** gate, enforcing **maker-checker approval** on every run.",
        "Engineered deterministic **Python scoring engines** for underwriting tiers and fraud detection, confining the LLM to extraction and narration to eliminate hallucination on key figures.",
        "Implemented real document ingestion (**PDF/XLSX**) and wired skills to data stores over read-only **MCP servers**.",
        "Validated with **golden-case regression suites** and an examiner-traceable audit trail on every run.",
    ]),
    ("Ford Motor Company", "Data Science Intern", "Feb 2025 – May 2025", [
        "Built a **multimodal emotion analysis** system using **Python**, **DeepFace** (facial recognition via OpenCV), **VADER** (text sentiment), and **Vosk** (speech-to-text); fused video, audio, and text modalities into a unified emotion classification, deployed on **GCP** with **Vertex AI**.",
        "Collaborated with a cross-functional corporate AI team applying **NLP**, **computer vision**, and **speech processing** to real-world multimodal data, improving system efficiency by **75%**.",
    ]),
    ("iNextLabs", "Data Science Intern", "Aug 2024 – Oct 2024", [
        "Built **NLP, anomaly detection, and GenAI** solutions using **PyTorch** and **Azure AI**; integrated into production systems, reducing issue resolution time by **40%**.",
        "Designed and deployed **AI analytics pipelines** and dashboards serving **500+ users** across technical and non-technical teams.",
    ]),
]

PROJECTS = [
    ("SignMate AI", "Patented real-time CNN system translating Indian Sign Language to text (PyTorch, OpenCV). Patent filed with IP India; published on the IP India website."),
    ("Finance Analytics & NL→SQL Intelligence", "ETL pipelines for financial data with forecasting models and a PostgreSQL + pgvector backend; LangChain-powered plain-English SQL lets non-technical users query data directly."),
    ("Production MLOps Platform & LLM Inference", "Full ML lifecycle — MLflow experiment tracking, DistilBERT inference, drift detection, and zero-downtime rollouts on Docker + GCP Cloud Run."),
    ("Large-Scale Customer Churn Prediction", "PySpark pipeline on 1M+ rows — 92.6% AUC, 45 engineered features, K-Means segmentation, and SHAP explainability with a Plotly dashboard."),
    ("Local RAG Pipeline — LangChain, Ollama & FAISS", "Privacy-first retrieval-augmented generation, 100% local with zero API cost; sub-second retrieval over 10K+ document chunks."),
    ("Fraud Detection & Churn Prediction — ML Research", "Automotive ECU fraud detection at 98.7% AUC on a 2% imbalanced rate; PyTorch autoencoder embeddings for churn across 4 benchmarked architectures."),
]

SKILLS = [
    ("Languages", "Python, SQL, Git / GitHub"),
    ("ML / AI", "Machine Learning, NLP, LLMs & RAG, Computer Vision, Prompt Engineering"),
    ("Frameworks", "PyTorch, TensorFlow, Scikit-learn, LangChain, HuggingFace, XGBoost"),
    ("Data Engineering", "ETL Pipelines, PySpark / Spark, Feature Engineering, Data Cleaning & EDA"),
    ("Visualization", "Tableau, Power BI, Matplotlib / Seaborn"),
    ("Cloud", "GCP, Azure ML, AWS, Docker, PostgreSQL"),
]

EDUCATION = [
    ("University of Southern California", "M.S. Applied Data Science", "May 2027", "Los Angeles, CA"),
    ("SRM Institute of Science and Technology", "B.Tech. Computer Science Engineering", "Jun 2025", "Chennai, India"),
]

CERTS = [
    "Patent Filed — SignMate AI (IP India) · Real-time sign-language translation via CNNs",
    "Publication — Project Eye (TechRxiv, peer-reviewed) · Neural ML vision systems",
    "AIVerify: An Enhancement of AI Security (Medium) · IMDA Singapore Project Moonshot",
    "Predictive Model for Cancer Detection (Medium) · Healthcare ML classification",
    "Google Cloud AI (Advanced) · Azure ML Engineer (Microsoft)",
]


def build():
    story = []
    full_width = LETTER[0] - 1.1 * inch  # matches frame width below

    story.append(Paragraph(NAME, styles["name"]))
    story.append(Paragraph(TITLE, styles["title"]))
    story.append(Paragraph(CONTACT, styles["contact"]))
    story.append(HRFlowable(width="100%", thickness=1.1, color=TEAL,
                            spaceBefore=6, spaceAfter=2))

    section("Summary", story)
    story.append(Paragraph(ABOUT, styles["body"]))

    section("Experience", story)
    for i, (company, role, period, bullets) in enumerate(EXPERIENCE):
        if i > 0:
            story.append(Spacer(1, 5))
        story.append(header_row(f"{company} — {role}", period,
                                styles["role"], styles["meta"],
                                [full_width * 0.72, full_width * 0.28]))
        items = [ListItem(Paragraph(md(b), styles["bullet"]), leftIndent=10,
                          value="•") for b in bullets]
        story.append(ListFlowable(items, bulletType="bullet", start="•",
                                  leftIndent=10, bulletColor=TEAL,
                                  bulletFontSize=7, spaceBefore=2))

    section("Projects", story)
    for title, desc in PROJECTS:
        story.append(Paragraph(f"<b>{title}.</b> {md(desc)}", styles["bullet"]))
        story.append(Spacer(1, 2.5))

    section("Skills", story)
    rows = [[Paragraph(cat, styles["skillcat"]), Paragraph(items, styles["skill"])]
            for cat, items in SKILLS]
    t = Table(rows, colWidths=[full_width * 0.22, full_width * 0.78])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 1.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5),
    ]))
    story.append(t)

    section("Education", story)
    for school, degree, period, loc in EDUCATION:
        story.append(header_row(f"<b>{school}</b> — {degree}", f"{period} · {loc}",
                                styles["body"], styles["meta"],
                                [full_width * 0.70, full_width * 0.30]))
        story.append(Spacer(1, 2))

    section("Selected Publications & Certifications", story)
    items = [ListItem(Paragraph(c, styles["bullet"]), leftIndent=10, value="•")
             for c in CERTS]
    story.append(ListFlowable(items, bulletType="bullet", start="•",
                              leftIndent=10, bulletColor=TEAL, bulletFontSize=7))

    doc = BaseDocTemplate(
        "public/manasa_vijayaraghavan_resume.pdf", pagesize=LETTER,
        leftMargin=0.55 * inch, rightMargin=0.55 * inch,
        topMargin=0.5 * inch, bottomMargin=0.45 * inch,
        title="Manasa Vijayaraghavan — Résumé", author=NAME,
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin,
                  LETTER[0] - 1.1 * inch, LETTER[1] - 0.95 * inch, id="main")
    doc.addPageTemplates([PageTemplate(id="main", frames=[frame])])
    doc.build(story)

    with open("public/manasa_vijayaraghavan_resume.pdf", "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    with open("scripts/resume_b64.txt", "w") as f:
        f.write(b64)
    print(f"PDF written. base64 length: {len(b64)}")


if __name__ == "__main__":
    build()
