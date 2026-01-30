---

# 🚀 AI Career Guide

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![License](https://img.shields.io/github/license/Keerthana-Uppanda/AI_Career_Guide)
![Repo Size](https://img.shields.io/github/repo-size/Keerthana-Uppanda/AI_Career_Guide)
![Issues](https://img.shields.io/github/issues/Keerthana-Uppanda/AI_Career_Guide)

**AI Career Guide** is an intelligent, resume-driven career recommendation system that analyzes user skills and provides **personalized career suggestions, learning gaps, and downloadable career reports**.

It is designed to help students and early professionals understand **which careers suit them best and what they need to learn next**.

---

## 🎯 Key Features

✅ **Resume-Based Career Matching**
Upload your resume (PDF / DOCX / TXT) and get career recommendations based on skill overlap.

✅ **Skill Extraction & Analysis**
Automatically detects technical and soft skills from resumes.

✅ **Career Match Scoring**
Ranks careers using skill similarity scores for clear comparison.

✅ **Professional PDF Career Report**
Download a clean, structured PDF including:

* Detected skills
* Applied filters
* Ranked career recommendations

✅ **Modern UI (Streamlit)**
Clean cards, progress bars, and an intuitive interface.

✅ **Extensible Design**
Easily add new careers, skills, or future AI enhancements.

---

## 🧠 How It Works

1. User uploads a resume
2. Skills are extracted using keyword & fuzzy matching
3. Skills are compared against curated career datasets
4. Careers are ranked using match scores
5. Results are displayed visually and exported as a PDF report

---

## 🛠️ Tech Stack

**Frontend & UI**

* Streamlit
* HTML/CSS (via Streamlit components)

**Backend & Logic**

* Python
* Pandas (data handling)
* FPDF (PDF generation)

**Data**

* CSV-based career dataset (easily extendable)

**Tools**

* Git & GitHub

---

## 📁 Project Structure

```
AI_Career_Guide/
│
├── app.py                  # Main Streamlit application
├── logic/
│   └── career_matcher.py   # Career filtering & matching logic
├── data/
│   └── careers.csv         # Career dataset
├── pages/
│   └── Resume_Improver.py  # (Planned / optional feature)
├── assets/                 # Screenshots, logos (optional)
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Keerthana-Uppanda/AI_Career_Guide.git
cd AI_Career_Guide
```

### 2️⃣ Create Virtual Environment (Recommended)

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the App

```bash
streamlit run app.py
```

### 5️⃣ Open in Browser

```
http://localhost:8501
```

---

## 📄 Sample Output

The application generates a **professional PDF report** containing:

* Detected skills
* Applied filters
* Ranked career recommendations
* Match percentages

Perfect for **career planning, self-assessment, and mentorship discussions**.

---

## 🚧 Future Enhancements

* 🔍 Job Description vs Resume Comparison
* 📚 Learning Roadmaps for Missing Skills
* 🤖 NLP / ML-based semantic skill matching
* 🌐 Deployment on Streamlit Cloud
* 🧠 Career trend & demand analysis

---

## 🤝 Contributing

Contributions are welcome!

You can:

* Add new careers & skills
* Improve UI/UX
* Enhance matching logic
* Optimize performance

**Steps:**

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push and open a Pull Request

---

## 👩‍💻 Author

**Uppanda Keerthana**
🎓 B.Tech Computer Science Student

* GitHub: [https://github.com/Keerthana-Uppanda](https://github.com/Keerthana-Uppanda)
* Project Repo: [https://github.com/Keerthana-Uppanda/AI_Career_Guide](https://github.com/Keerthana-Uppanda/AI_Career_Guide)

---


