
import streamlit as st
import pandas as pd
import re
from pypdf import PdfReader
import docx

# Set Page Title and Layout
st.set_page_config(page_title="Tech Job Market & Skill Gap Analyzer", layout="wide")

st.title("📊 Tech Job Market & Skill Gap Analyzer")
st.markdown("Analyze demand metrics across top product companies and evaluate your resume against targeted job descriptions.")

# --- FILE PARSING FUNCTIONS ---
def extract_text_from_pdf(pdf_file):
    try:
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + " "
        return text
    except Exception as e:
        st.error(f"Error reading PDF file: {e}")
        return ""

def extract_text_from_docx(docx_file):
    try:
        doc = docx.Document(docx_file)
        full_text = [para.text for para in doc.paragraphs]
        return "\n".join(full_text)
    except Exception as e:
        st.error(f"Error reading Word document: {e}")
        return ""

def extract_text_from_txt(txt_file):
    try:
        return txt_file.read().decode("utf-8")
    except Exception as e:
        st.error(f"Error reading Text file: {e}")
        return ""

def process_file(uploaded_file):
    if uploaded_file is None:
        return ""
    file_type = uploaded_file.name.split('.')[-1].lower()
    if file_type == 'pdf':
        return extract_text_from_pdf(uploaded_file)
    elif file_type in ['docx', 'doc']:
        return extract_text_from_docx(uploaded_file)
    elif file_type == 'txt':
        return extract_text_from_txt(uploaded_file)
    else:
        st.error("Unsupported file format! Please upload PDF, DOCX, or TXT files.")
        return ""

# Load Datasets
@st.cache_data
def load_data():
    try:
        jobs_df = pd.read_csv("product_company_jobs.csv")
        skills_df = pd.read_csv("skill_repetition_count.csv")
        return jobs_df, skills_df
    except FileNotFoundError:
        st.error("CSV files not found! Ensure 'product_company_jobs.csv' and 'skill_repetition_count.csv' are in the directory.")
        return None, None

jobs_df, skills_df = load_data()

if jobs_df is not None and skills_df is not None:
    # --- DYNAMIC SKILL DICTIONARY BUILDER ---
    # 1. Collect all skills from skill_repetition_count.csv
    base_skills = set(skills_df["Skill"].dropna().str.strip().unique())
    
    # 2. Extract every skill listed in product_company_jobs.csv
    if "Required Skills" in jobs_df.columns:
        for skills_str in jobs_df["Required Skills"].dropna():
            split_skills = [s.strip() for s in str(skills_str).split(",")]
            base_skills.update(split_skills)
            
    # 3. Comprehensive fallback tech keywords
    fallback_tech_keywords = {
        "Python", "Java", "C++", "C#", "JavaScript", "TypeScript", "SQL", "HTML", "CSS", "React",
        "Angular", "Vue.js", "Node.js", "Django", "Flask", "FastAPI", "Spring Boot", ".NET",
        "AWS", "Azure", "GCP", "Docker", "Kubernetes", "CI/CD", "Git", "GitHub", "GitLab",
        "Linux", "Unix", "Bash", "REST API", "GraphQL", "PostgreSQL", "MySQL", "MongoDB",
        "Redis", "Elasticsearch", "Kafka", "Pandas", "NumPy", "Scikit-Learn", "TensorFlow",
        "PyTorch", "Tableau", "PowerBI", "Excel", "Spark", "Hadoop", "Snowflake", "BigQuery",
        "Airflow", "Machine Learning", "Deep Learning", "NLP", "Computer Vision", "Data Structures",
        "Algorithms", "System Design", "Microservices", "Unit Testing", "Selenium", "Postman",
        "Agile", "Scrum", "Jira", "Figma", "DevOps", "Cybersecurity", "Terraform"
    }
    
    # Combine into one complete skill lexicon
    MASTER_SKILL_LIST = sorted(list(base_skills.union(fallback_tech_keywords)), key=len, reverse=True)

    # --- SECTION 1: MARKET TRENDS DASHBOARD ---
    st.header("1. Market-Wide Skill Insights")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Filter Roles")
        selected_role = st.selectbox("Select Target Tech Role:", ["All Roles"] + list(jobs_df["Job Title"].unique()))
        
    with col2:
        st.subheader("Top Demand Skills")
        if selected_role == "All Roles":
            chart_data = skills_df.head(10).set_index("Skill")
            st.bar_chart(chart_data)
        else:
            role_row = jobs_df[jobs_df["Job Title"] == selected_role]
            if not role_row.empty:
                required_skills = [s.strip() for s in role_row["Required Skills"].values[0].split(",")]
                st.write(f"**Required Skills for {selected_role}:**")
                st.write(", ".join([f"`{s}`" for s in required_skills]))
                
    st.divider()

    # --- SECTION 2: LIVE JOB DESCRIPTION & RESUME MATCHER ---
    st.header("2. Live Job Description & Resume Matcher")
    st.caption("Upload your resume (PDF, Word, or Text) or paste your text alongside a target job description to check your fit score.")
    
    col_input1, col_input2 = st.columns(2)
    
    with col_input1:
        st.subheader("Your Profile / Resume")
        input_method = st.radio("Choose Input Method:", ["Upload File (PDF, DOCX, TXT)", "Paste Text Manually"], horizontal=True)
        
        user_skills_raw = ""
        if input_method == "Upload File (PDF, DOCX, TXT)":
            uploaded_file = st.file_uploader("Upload your resume file:", type=["pdf", "docx", "txt"])
            if uploaded_file is not None:
                user_skills_raw = process_file(uploaded_file)
                if user_skills_raw:
                    st.success(f"Successfully read `{uploaded_file.name}`!")
        else:
            user_skills_raw = st.text_area(
                "Your Current Skills / Resume Summary:", 
                placeholder="e.g. Python, SQL, Git, Pandas, Data Structures...",
                height=180
            )
        
    with col_input2:
        st.subheader("Target Job Posting")
        jd_text_raw = st.text_area(
            "Target Job Description (JD):", 
            placeholder="Paste raw text from a LinkedIn, Amazon, or Google job posting here...",
            height=220
        )
        
    if st.button("🚀 Analyze Job Match", type="primary"):
        if not user_skills_raw or not jd_text_raw:
            st.warning("Please provide both your resume/skills and a target job description.")
        else:
            # Extract skills using word-boundary pattern matching
            user_found = set()
            jd_found = set()

            for skill in MASTER_SKILL_LIST:
                pattern = r'\b' + re.escape(skill) + r'\b'
                if re.search(pattern, user_skills_raw, re.IGNORECASE):
                    user_found.add(skill)
                if re.search(pattern, jd_text_raw, re.IGNORECASE):
                    jd_found.add(skill)
            
            if not jd_found:
                st.info("No recognized technical keywords were detected in the target job description.")
            else:
                matched = user_found.intersection(jd_found)
                missing = jd_found - user_found
                score = int((len(matched) / len(jd_found)) * 100)
                
                res_col1, res_col2 = st.columns([1, 2])
                
                with res_col1:
                    st.metric("Overall Match Score", f"{score}%")
                    if score >= 75:
                        st.success("Strong Match! Your profile aligns well with this role.")
                    elif score >= 50:
                        st.warning("Moderate Match. Address missing key skills before applying.")
                    else:
                        st.error("Low Match. Adding key missing keywords will boost your ATS fit.")
                        
                with res_col2:
                    st.write("### Skill Breakdown")
                    st.write(f"✅ **Matched Skills ({len(matched)}):** " + (", ".join([f"`{s}`" for s in sorted(matched)]) if matched else "None"))
                    st.write(f"❌ **Missing Keywords to Learn ({len(missing)}):** " + (", ".join([f"`{s}`" for s in sorted(missing)]) if missing else "None"))
                    
                st.subheader("💡 Recommended Next Steps")
                if missing:
                    st.write(f"1. Build a project incorporating key missing skills: **{', '.join(list(sorted(missing))[:3])}**.")
                    st.write("2. Include missing keywords in your resume bullet points for ATS optimization.")
                    st.write("3. Re-run this check to verify an updated fit score.")
                else:
                    st.write("Your technical profile covers all key requirements extracted from this job description!")