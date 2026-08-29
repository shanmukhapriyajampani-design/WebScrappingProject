import streamlit as st
import pandas as pd
import re

# Set Page Title and Layout
st.set_page_config(page_title="Tech Job Market & Skill Gap Analyzer", layout="wide")

st.title("📊 Tech Job Market & Skill Gap Analyzer")
st.markdown("Analyze demand metrics across top product companies and evaluate your resume against targeted job descriptions.")

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
    st.caption("Paste your current skills and target job description below to check your fit score and missing keywords.")
    
    col_input1, col_input2 = st.columns(2)
    
    with col_input1:
        user_skills_raw = st.text_area(
            "Your Current Skills / Resume Summary:", 
            placeholder="e.g. Python, SQL, Git, Pandas, Data Structures",
            height=180
        )
        
    with col_input2:
        jd_text_raw = st.text_area(
            "Target Job Description (JD):", 
            placeholder="Paste raw text from a LinkedIn, Amazon, or Google job posting here...",
            height=180
        )
        
    if st.button("🚀 Analyze Job Match", type="primary"):
        if not user_skills_raw or not jd_text_raw:
            st.warning("Please fill in both text areas to generate an analysis.")
        else:
            # Complete tech keyword list for pattern extraction
            all_known_skills = list(skills_df["Skill"].dropna().unique()) + [
                "JavaScript", "TypeScript", "React", "HTML5/CSS3", "Redux", "REST API",
                "Node.js", "MongoDB", "AWS", "Docker", "Kubernetes", "CI/CD", "Linux",
                "Selenium", "PyTest", "Postman", "Figma", "Machine Learning", "Deep Learning",
                "PyTorch", "TensorFlow", "Scikit-Learn", "Statistics", "PowerBI", "Tableau",
                "Swift", "Kotlin", "Flutter", "React Native", "Cryptography", "Network Security"
            ]
            all_known_skills = list(set(all_known_skills))
            
            # Extract skills using Regex boundary matching
            user_found = set([s for s in all_known_skills if re.search(r'\b' + re.escape(s) + r'\b', user_skills_raw, re.IGNORECASE)])
            jd_found = set([s for s in all_known_skills if re.search(r'\b' + re.escape(s) + r'\b', jd_text_raw, re.IGNORECASE)])
            
            if not jd_found:
                st.info("No standard technical keywords recognized in the JD text. Try adding standard technical terms.")
            else:
                matched = user_found.intersection(jd_found)
                missing = jd_found - user_found
                score = int((len(matched) / len(jd_found)) * 100)
                
                # Display Results
                res_col1, res_col2 = st.columns([1, 2])
                
                with res_col1:
                    st.metric("Overall Match Score", f"{score}%")
                    if score >= 75:
                        st.success("Strong Match! Your profile aligns well with this role.")
                    elif score >= 50:
                        st.warning("Moderate Match. Address missing key skills before applying.")
                    else:
                        st.error("Low Match. Learning the missing keywords will boost your eligibility.")
                        
                with res_col2:
                    st.write("### Skill Breakdown")
                    st.write(f"✅ **Matched Skills ({len(matched)}):** " + (", ".join([f"`{s}`" for s in matched]) if matched else "None"))
                    st.write(f"❌ **Missing Keywords to Learn ({len(missing)}):** " + (", ".join([f"`{s}`" for s in missing]) if missing else "None"))
                    
                st.subheader("💡 Recommended Next Steps")
                if missing:
                    st.write(f"1. Complete a mini-project that incorporates high-priority missing skills: **{', '.join(list(missing)[:3])}**.")
                    st.write("2. Update your resume bullet points to include these keywords explicitly for ATS optimization.")
                    st.write("3. Re-scan your resume text against this job description to verify an improved fit score.")
                else:
                    st.write("Your technical profile covers all key requirements extracted from this job description!")