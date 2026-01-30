import streamlit as st
import pandas as pd

from logic.career_matcher import load_careers
from app import (
    extract_resume_text,
    get_skill_vocab,
    detect_resume_skills,
    pill
)

st.set_page_config(
    page_title="Resume Improver",
    page_icon="🛠",
    layout="wide"
)

st.title("🛠 Resume Improvement & Job Fit")
st.write("Upload your resume and paste a job description to see what to improve.")
df = load_careers("data/careers.csv")
skill_vocab = get_skill_vocab(df)

uploaded = st.file_uploader(
    "Upload your Resume",
    type=["pdf", "docx", "txt"]
)

job_description = st.text_area(
    "Paste Job Description",
    height=220,
    placeholder="Paste the job description here..."
)
if uploaded and job_description:

    resume_text = extract_resume_text(uploaded)

    resume_skills = detect_resume_skills(resume_text, skill_vocab)

    jd_skills = {
        skill for skill in skill_vocab
        if skill in job_description.lower()
    }
    matched_skills = resume_skills & jd_skills
    missing_skills = jd_skills - resume_skills
    st.markdown("## ✅ Matching Skills")

    if matched_skills:
        for skill in sorted(matched_skills):
            pill(skill)
    else:
        st.warning("No matching skills found.")
    st.markdown("## ❌ Missing Skills (You should learn)")

    if missing_skills:
        for skill in sorted(missing_skills):
            pill(skill)
    else:
        st.success("Great! Your resume matches most job requirements.")
        st.markdown("## 🎓 What You Should Learn")

    for skill in sorted(missing_skills):
        st.write(f"- Learn **{skill}** with hands-on projects and practice.")
        st.write(f"- Learn **{skill}** with hands-on projects and practice.")
        st.write(f"- Learn **{skill}** with hands-on projects and practice.")
        st.markdown("## ✍️ Resume Improvement Tips")

    st.write("""
    - Add **projects** using the missing skills  
    - Use **exact keywords** from the job description  
    - Add a **Skills section** if missing  
    - Mention tools, frameworks, and technologies clearly  
    - Quantify results (e.g., *improved accuracy by 20%*)
    """)
else:
    st.info("Please upload your resume and paste a job description to see improvement suggestions.")
