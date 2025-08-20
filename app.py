# app.py

import re
from typing import Set, Dict
import difflib

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Optional imports
try:
    import pdfplumber
except Exception:
    pdfplumber = None

try:
    import docx
except Exception:
    docx = None

from fpdf import FPDF
from logic.career_matcher import load_careers, match_careers

# ---------------------------
# Helpers
# ---------------------------

def extract_text_from_pdf(file) -> str:
    if pdfplumber is None:
        raise ImportError("pdfplumber is not installed. Install it with pip install pdfplumber.")
    text_parts = []
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text_parts.append(page.extract_text() or "")
    return "\n".join(text_parts)

def extract_text_from_docx(file) -> str:
    if docx is None:
        raise ImportError("python-docx is not installed. Install it with pip install python-docx.")
    document = docx.Document(file)
    return "\n".join([p.text for p in document.paragraphs])

def extract_resume_text(uploaded_file) -> str:
    if uploaded_file is None:
        return ""
    name = uploaded_file.name.lower()
    if name.endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file)
    elif name.endswith(".docx"):
        return extract_text_from_docx(uploaded_file)
    elif name.endswith(".txt"):
        return uploaded_file.read().decode("utf-8", errors="ignore")
    else:
        raise ValueError("Unsupported file type. Please upload a PDF, DOCX, or TXT.")

# ---------------------------
# Skill extraction
# ---------------------------

def get_skill_vocab(df: pd.DataFrame) -> Set[str]:
    skills = set()
    if "Key_Skills" not in df.columns:
        return skills
    for cell in df["Key_Skills"].dropna():
        for s in str(cell).split(","):
            skills.add(s.strip().lower())
    return skills

def detect_resume_skills(text: str, skill_vocab: Set[str]) -> Set[str]:
    text_lower = text.lower()
    detected = set()
    for skill in skill_vocab:
        if skill in text_lower:
            detected.add(skill)
        else:
            matches = difflib.get_close_matches(skill, text_lower.split(), n=1, cutoff=0.85)
            if matches:
                detected.add(skill)
    return detected

def score_career(skill_hits: Set[str], career_skill_cell: str) -> float:
    if not isinstance(career_skill_cell, str) or not career_skill_cell.strip():
        return 0.0
    career_skills = {s.strip().lower() for s in career_skill_cell.split(",") if s.strip()}
    if not career_skills:
        return 0.0
    overlap = len(skill_hits.intersection(career_skills))
    return overlap / len(career_skills)

# ---------------------------
# UI helpers
# ---------------------------

def pill(text: str):
    st.markdown(
        f"""
        <span style="
            display:inline-block;
            padding:6px 10px;
            border-radius:999px;
            background:#3b82f6;
            color:white;
            font-size:0.85rem;
            margin:4px 6px 0 0;
            border:1px solid #2563eb;">
            {text}
        </span>
        """,
        unsafe_allow_html=True,
    )

def card(career_row: Dict, score: float):
    st.markdown(
        """
        <div style="
            border:1px solid #e5e7eb;
            border-radius:16px;
            padding:16px;
            background:#ffffff;
            box-shadow: 0 1px 2px rgba(0,0,0,0.04);
            margin-bottom: 1rem;">
        """,
        unsafe_allow_html=True,
    )
    st.subheader(career_row.get("Career", "Unknown"))

    if "Description" in career_row and career_row["Description"]:
        st.write(f"_{career_row['Description']}_")

    cols = st.columns(3)
    cols[0].write(f"**Education:** {career_row.get('Education_Level', '-')}")
    cols[1].write(f"**Work Style:** {career_row.get('Work_Style', '-')}")
    cols[2].write(f"**Personality:** {career_row.get('Personality', '-')}")

    st.write("**Key Skills**")
    for s in str(career_row.get("Key_Skills", "")).split(","):
        if s.strip():
            pill(s.strip())

    st.write("**Subjects**")
    for s in str(career_row.get("Subjects", "")).split(","):
        if s.strip():
            pill(s.strip())

    st.write("**Match Score**")
    st.progress(min(max(score, 0.0), 1.0))

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------
# PDF generation
# ---------------------------

def generate_pdf(user_name, detected_skills, filters, top_careers):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, f"{user_name} — Career Recommendations", ln=True, align="C")
    pdf.ln(10)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(59, 130, 246)
    pdf.cell(0, 8, "Detected Skills:", ln=True)
    pdf.set_text_color(0,0,0)
    pdf.multi_cell(0, 8, ", ".join(detected_skills) if detected_skills else "None")
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(59, 130, 246)
    pdf.cell(0, 8, "Filters Applied:", ln=True)
    pdf.set_text_color(0,0,0)
    filters_text = ", ".join([f"{k}: {v}" for k, v in filters.items()]) if filters else "None"
    pdf.multi_cell(0, 8, filters_text)
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(59, 130, 246)
    pdf.cell(0, 8, "Top Recommended Careers:", ln=True)
    pdf.set_text_color(0,0,0)
    
    for career in top_careers:
        pdf.cell(0, 6, f"- {career['Career']} (Match: {career['Score']*100:.1f}%)", ln=True)
        pdf.multi_cell(0, 6, f"  Skills: {career.get('Key_Skills', '-')}")
        pdf.multi_cell(0, 6, f"  Subjects: {career.get('Subjects', '-')}")
        pdf.multi_cell(0, 6, f"  Description: {career.get('Description', '-')}")
        pdf.ln(3)
    
    return pdf

# ---------------------------
# Highlight skills in resume
# ---------------------------

def highlight_skills(resume_text, hits):
    highlighted = resume_text
    for skill in hits:
        highlighted = re.sub(
            rf"(?i)\b{re.escape(skill)}\b",
            lambda m: f"<mark>{m.group(0)}</mark>",
            highlighted
        )
    return highlighted

# ---------------------------
# Missing skills suggestion
# ---------------------------

def missing_skills(top_careers, hits):
    suggestions = {}
    for career in top_careers:
        required = {s.strip().lower() for s in str(career.get("Key_Skills","")).split(",")}
        missing = required - hits
        if missing:
            suggestions[career['Career']] = missing
    return suggestions

# ---------------------------
# App
# ---------------------------

st.set_page_config(page_title="AI Career Guide", page_icon="🎯", layout="wide")

with st.sidebar:
    st.title("🎯 AI Career Guide")
    st.caption("Upload your resume and get personalized career matches.")

    st.subheader("Filters")
    education = st.selectbox(
        "Education Level (optional)",
        options=["", "Diploma", "Bachelor's", "Master's", "PhD", "MBBS"],
        index=0,
    )
    work_style = st.multiselect(
        "Work Style (optional)",
        options=["Remote", "Team", "Solo", "Field", "Classroom", "Hospital", "Office"],
    )
    personality = st.multiselect(
        "Personality (optional)",
        options=["Analytical", "Creative", "Leader", "Practical", "Empathetic", "Detail-Oriented", "Patient", "Innovative"],
    )

    top_n = st.slider("How many top careers to show", 1, 10, 5)
    show_chart = st.checkbox("Show bar chart", value=True)

st.title("💼 AI Career Guide — Resume Based")
st.write(
    "Upload a **PDF**, **DOCX**, or **TXT** resume. We’ll detect skills, filter by your preferences, "
    "and rank careers by skill overlap."
)

df = load_careers("data/careers.csv")
uploaded = st.file_uploader("Upload your resume", type=["pdf", "docx", "txt"])

if uploaded is not None:
    try:
        resume_text = extract_resume_text(uploaded)
    except Exception as e:
        st.error(f"Could not read the file: {e}")
        st.stop()

    if not resume_text.strip():
        st.warning("The uploaded file appears empty. Please check your resume and try again.")
        st.stop()

    # ----------------------
    # Skill detection
    # ----------------------
    skill_vocab = get_skill_vocab(df)
    hits = detect_resume_skills(resume_text, skill_vocab)

    st.markdown("### 🔎 Detected Skills")
    if hits:
        for s in sorted(hits):
            pill(s)
    else:
        st.info("No skills detected from the dataset. Check your resume formatting or add skills to careers.csv.")

    # ----------------------
    # Resume preview with highlighted skills
    # ----------------------
    st.markdown("### 📝 Resume Preview with Detected Skills")
    st.markdown(highlight_skills(resume_text, hits), unsafe_allow_html=True)

    # ----------------------
    # Filters
    # ----------------------
    user_input = {}
    if education:
        user_input["education"] = education
    if work_style:
        user_input["work_style"] = "|".join(work_style)
    if personality:
        user_input["personality"] = "|".join(personality)

    filtered = match_careers(user_input, df)

    scores = []
    for idx, row in filtered.iterrows():
        score = score_career(hits, row.get("Key_Skills", ""))
        scores.append((idx, score))

    scores.sort(key=lambda tup: (tup[1], str(filtered.loc[tup[0], "Career"]).lower()), reverse=True)

    top_rows = scores[:top_n]

    if not top_rows:
        st.warning("No careers matched your filters.")
    else:
        if show_chart:
            fig, ax = plt.subplots()
            labels = [filtered.loc[i, "Career"] for i, _ in top_rows]
            values = [round(s * 100, 2) for _, s in top_rows]
            bars = ax.bar(labels, values)

            ax.set_ylabel("Match Score (%)")
            ax.set_title("Top Career Matches")
            ax.set_ylim(0, 100)
            plt.xticks(rotation=20, ha="right")

            for bar, val in zip(bars, values):
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + 1,
                    f"{val:.1f}%",
                    ha="center",
                    va="bottom",
                    fontsize=9,
                )

            st.pyplot(fig, clear_figure=True)

        st.markdown("### 🧭 Recommended Careers")
        top_career_list = []
        for i, s in top_rows:
            row = filtered.loc[i].to_dict()
            card(row, s)
            row["Score"] = s
            top_career_list.append(row)

        # ----------------------
        # Missing skills suggestion
        # ----------------------
        suggestions = missing_skills(top_career_list, hits)
        if suggestions:
            st.markdown("### ⚡ Suggested Skills to Learn")
            for career, skills in suggestions.items():
                st.write(f"**{career}**: {', '.join(skills)}")

        # ----------------------
        # PDF download button
        # ----------------------
        if st.button("Download PDF Report"):
            pdf = generate_pdf("Resume Analysis", sorted(hits), user_input, top_career_list)
            pdf_output = pdf.output(dest='S').encode('latin1')
            st.download_button(
                label="Download PDF",
                data=pdf_output,
                file_name="career_report.pdf",
                mime="application/pdf"
            )

else:
    st.info("Upload a resume to begin. You can also set filters from the left sidebar.")
    st.markdown(
        """
        **Tips**
        - Use a PDF or DOCX with clear sections like *Skills*, *Projects*, and *Education*.
        - The app looks for skills listed in your dataset's **Key_Skills** column.
        - Add more roles and skills in `data/careers.csv` to improve matching.
        """
    )
