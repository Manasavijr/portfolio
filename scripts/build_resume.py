#!/usr/bin/env python3
"""Generate the résumé PDF in the classic serif one-page format.

Run from repo root: python3 scripts/build_resume.py
Writes: public/manasa_vijayaraghavan_resume.pdf  and scripts/resume_b64.txt
"""
import base64
import re
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, ListFlowable,
    ListItem, HRFlowable, Table, TableStyle,
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER

INK = HexColor("#111111")
RULE = HexColor("#000000")

def md(text):
    # Escape only bare ampersands, leaving HTML entities (&mdash; &rarr; &amp; ...) intact.
    text = re.sub(r"&(?!(amp|lt|gt|quot|mdash|ndash|rarr|middot|nbsp);)", "&amp;", text)
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)

S = {
    "name": ParagraphStyle("name", fontName="Times-Bold", fontSize=19,
                           textColor=INK, leading=22, alignment=TA_CENTER, spaceAfter=3),
    "contact": ParagraphStyle("contact", fontName="Times-Roman", fontSize=9.5,
                              textColor=INK, leading=12, alignment=TA_CENTER),
    "section": ParagraphStyle("section", fontName="Times-Bold", fontSize=10.5,
                              textColor=INK, leading=12, spaceBefore=7, spaceAfter=0,
                              tracking=0.5),
    "sumbody": ParagraphStyle("sumbody", fontName="Times-Roman", fontSize=9.3,
                              textColor=INK, leading=12),
    "left": ParagraphStyle("left", fontName="Times-Roman", fontSize=9.5,
                           textColor=INK, leading=12),
    "right": ParagraphStyle("right", fontName="Times-Italic", fontSize=9.3,
                            textColor=INK, leading=12, alignment=2),
    "bullet": ParagraphStyle("bullet", fontName="Times-Roman", fontSize=9.1,
                             textColor=INK, leading=11.4),
    "skillcat": ParagraphStyle("skillcat", fontName="Times-Bold", fontSize=9.3,
                               textColor=INK, leading=11.6),
    "skill": ParagraphStyle("skill", fontName="Times-Roman", fontSize=9.3,
                            textColor=INK, leading=11.6),
}

def section(title, story):
    story.append(Paragraph(title.upper(), S["section"]))
    story.append(HRFlowable(width="100%", thickness=0.9, color=RULE,
                            spaceBefore=1.5, spaceAfter=3.5))

def two_col(left, right, ls, rs, w):
    t = Table([[Paragraph(left, ls), Paragraph(right, rs)]], colWidths=w)
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0.5),
    ]))
    return t

def bullets(items, story):
    lst = [ListItem(Paragraph(md(b), S["bullet"]), leftIndent=11, value="•")
           for b in items]
    story.append(ListFlowable(lst, bulletType="bullet", start="•", leftIndent=11,
                              bulletColor=black, bulletFontSize=6.5, spaceBefore=1.5))

# ---------------- Content ----------------
NAME = "Manasa Vijayaraghavan"
CONTACT = ("Los Angeles, CA&nbsp; |&nbsp; manasavijayaraghavan@gmail.com&nbsp; |&nbsp; "
           "(213) 791-7623&nbsp; |&nbsp; LinkedIn&nbsp; |&nbsp; GitHub&nbsp; |&nbsp; Portfolio")

SUMMARY = ("M.S. Applied Data Science at USC &middot; Built agentic AI for BFSI at Wipro and "
           "production ML at Ford Motor Company and iNextLabs &middot; Hands-on in LLMs, RAG, "
           "Agentic AI, multimodal ML, and MLOps at scale &middot; Patent filed &middot; "
           "Published author &middot; Open to Fall 2026 internships and full-time from 2027 "
           "across the USA.")

EDUCATION = [
    ("University of Southern California", "M.S. Applied Data Science", "Los Angeles, CA", "May 2027"),
    ("SRM Institute of Science and Technology", "B.Tech. Computer Science Engineering", "Chennai, India", "Jun 2025"),
]

SKILLS = [
    ("Languages", "Python, SQL, R, JavaScript, Bash, Git/GitHub"),
    ("AI &amp; GenAI", "LLMs, Agentic AI, RAG, Prompt Engineering, Fine-tuning (LoRA/QLoRA), Multimodal AI, NLP, Computer Vision"),
    ("ML Frameworks", "PyTorch, TensorFlow, Scikit-learn, XGBoost, HuggingFace, LangChain, LangGraph, OpenCV, FastAPI"),
    ("Data Engineering", "PySpark, PostgreSQL, FAISS, pgvector, ETL Pipelines, Feature Engineering, EDA"),
    ("MLOps &amp; Cloud", "MLflow, Docker, CI/CD, GCP (Vertex AI), AWS, Azure AI, Automated Retraining"),
    ("Certifications", "AWS Data Analytics &middot; IBM Data Scientist &middot; Microsoft Azure ML &middot; Google Prompt Design (Vertex AI)"),
]

EXPERIENCE = [
    ("Wipro", "AI Native Intern", "June 2026 &ndash; August 2026", [
        "Built **AgenticOS BFSI Skills**, an agentic decision-support library for **Banking, Financial Services & Insurance**, owning two life-insurance skills end to end.",
        "Architected multi-step **LangGraph** agent workflows with a **human-in-the-loop** maker-checker gate, and deterministic **Python scoring engines** for underwriting tiers and fraud detection &mdash; confining the LLM to extraction and narration to eliminate hallucination on key figures.",
        "Implemented real document ingestion (**PDF/XLSX**) over read-only **MCP servers**; validated with **golden-case regression suites** and an examiner-traceable audit trail on every run.",
    ]),
    ("Ford Motor Company", "Data Science Intern", "Feb 2025 &ndash; May 2025", [
        "Built a **multimodal emotion analysis** system (**Python, DeepFace/OpenCV, VADER, Vosk**) fusing video, audio, and text into a unified classifier deployed on **GCP Vertex AI** &mdash; improving system efficiency by **75%**.",
        "Collaborated with a cross-functional corporate AI team applying **NLP, computer vision, and speech processing** to real-world multimodal data.",
    ]),
    ("iNextLabs", "Data Science Intern", "Aug 2024 &ndash; Oct 2024", [
        "Built **NLP, anomaly detection, and GenAI** solutions (**PyTorch, Azure AI**) integrated into production, reducing issue resolution time by **40%**.",
        "Designed and deployed **AI analytics pipelines** and dashboards serving **500+ users** across technical and non-technical teams.",
    ]),
]

PROJECTS = [
    ("SignMate AI &mdash; Patent Filed", "Python, PyTorch, OpenCV, CNNs",
     "Real-time Indian Sign Language &rarr; text translation; **patent filed with IP India** and published."),
    ("Finance Analytics &amp; NL&rarr;SQL Intelligence", "PostgreSQL, pgvector, LangChain, FastAPI",
     "ETL and forecasting with **plain-English SQL** over a pgvector backend, letting non-technical users query financial data."),
    ("Large-Scale Customer Churn Prediction", "PySpark, XGBoost, SHAP, K-Means",
     "**92.6% AUC** on 1M+ rows with behavioral segmentation and SHAP explainability on a Plotly dashboard."),
]

PUBLICATIONS = [
    ("AIVerify: An Enhancement of AI Security", "Medium",
     "LLM safety, red teaming, and responsible AI &mdash; IMDA Singapore Project Moonshot."),
    ("Building a Predictive Model for Cancer Detection", "Medium",
     "Random Forest vs. Linear Regression for high-stakes healthcare ML classification."),
]


def build():
    story = []
    W = LETTER[0] - 1.0 * inch  # frame content width

    story.append(Paragraph(NAME, S["name"]))
    story.append(Paragraph(CONTACT, S["contact"]))
    story.append(HRFlowable(width="100%", thickness=1.0, color=RULE,
                            spaceBefore=5, spaceAfter=1))

    section("Summary", story)
    story.append(Paragraph(SUMMARY, S["sumbody"]))

    section("Education", story)
    for school, degree, loc, period in EDUCATION:
        story.append(two_col(f"<b>{school}</b>", loc, S["left"], S["right"],
                             [W * 0.68, W * 0.32]))
        story.append(two_col(degree, period, S["left"], S["right"],
                             [W * 0.68, W * 0.32]))
        story.append(Spacer(1, 2.5))

    section("Technical Skills", story)
    rows = [[Paragraph(cat, S["skillcat"]), Paragraph(items, S["skill"])]
            for cat, items in SKILLS]
    t = Table(rows, colWidths=[W * 0.20, W * 0.80])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 1),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
    ]))
    story.append(t)

    section("Experience", story)
    for i, (company, role, period, bl) in enumerate(EXPERIENCE):
        if i > 0:
            story.append(Spacer(1, 3.5))
        story.append(two_col(f"<b>{company}</b> &mdash; <i>{role}</i>", period,
                             S["left"], S["right"], [W * 0.74, W * 0.26]))
        bullets(bl, story)

    section("Projects", story)
    for i, (title, stack, desc) in enumerate(PROJECTS):
        if i > 0:
            story.append(Spacer(1, 2))
        story.append(Paragraph(f"<b>{title}</b>&nbsp; <i>/ {stack}</i>", S["left"]))
        bullets([desc], story)

    section("Publications &amp; Writing", story)
    for i, (title, outlet, desc) in enumerate(PUBLICATIONS):
        if i > 0:
            story.append(Spacer(1, 2))
        story.append(two_col(f"<b>{title}</b>", outlet, S["left"], S["right"],
                             [W * 0.78, W * 0.22]))
        story.append(Paragraph(desc, S["bullet"]))

    doc = BaseDocTemplate(
        "public/manasa_vijayaraghavan_resume.pdf", pagesize=LETTER,
        leftMargin=0.5 * inch, rightMargin=0.5 * inch,
        topMargin=0.5 * inch, bottomMargin=0.4 * inch,
        title="Manasa Vijayaraghavan — Résumé", author=NAME,
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, W, LETTER[1] - 0.9 * inch, id="main")
    doc.addPageTemplates([PageTemplate(id="main", frames=[frame])])
    doc.build(story)

    data = open("public/manasa_vijayaraghavan_resume.pdf", "rb").read()
    b64 = base64.b64encode(data).decode()
    open("scripts/resume_b64.txt", "w").write(b64)
    pages = data.count(b"/Type /Page") - data.count(b"/Type /Pages")
    print(f"PDF written: {len(data)} bytes, pages={pages}, base64 len={len(b64)}")


if __name__ == "__main__":
    build()
