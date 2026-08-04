import pandas as pd
from collections import defaultdict

# -------------------------------------------------------------
# 1. TARGET COMPANIES
# -------------------------------------------------------------
TARGET_COMPANIES = [
    "Google", "Amazon", "Flipkart", "Myntra", "Meesho",
    "Microsoft", "Cisco", "Oracle", "Intuit", "Visa"
]

# -------------------------------------------------------------
# 2. ROLE TO SKILLS MAPPING (13 ROLES)
# -------------------------------------------------------------
ROLE_SKILL_MAPPING = {
    "Software Development Engineer (SDE)": {
        "companies": TARGET_COMPANIES,
        "skills": ["Java", "C++", "Python", "Data Structures", "Algorithms", "System Design", "SQL", "Git"]
    },
    "Frontend Engineer": {
        "companies": TARGET_COMPANIES,
        "skills": ["JavaScript", "TypeScript", "React", "HTML5/CSS3", "Redux", "REST API", "Git"]
    },
    "Backend Engineer": {
        "companies": TARGET_COMPANIES,
        "skills": ["Python", "Java", "Node.js", "C++", "SQL", "MongoDB", "AWS", "Docker", "REST API"]
    },
    "Full Stack Developer": {
        "companies": TARGET_COMPANIES,
        "skills": ["JavaScript", "React", "Node.js", "Python", "Java", "SQL", "MongoDB", "AWS", "Git"]
    },
    "Data Analyst": {
        "companies": TARGET_COMPANIES,
        "skills": ["Python", "SQL", "Pandas", "NumPy", "PowerBI", "Tableau", "Excel"]
    },
    "DevOps Engineer": {
        "companies": TARGET_COMPANIES,
        "skills": ["AWS", "Azure", "GCP", "Docker", "Kubernetes", "CI/CD", "Linux", "Git", "Python"]
    },
    "Product Manager": {
        "companies": TARGET_COMPANIES,
        "skills": ["Product Strategy", "Agile/Scrum", "Data Analytics", "SQL", "Roadmapping", "A/B Testing", "User Research"]
    },
    "UX/UI Designer": {
        "companies": TARGET_COMPANIES,
        "skills": ["Figma", "User Research", "Wireframing", "Prototyping", "UI Design", "Design Systems", "HTML5/CSS3"]
    },
    "Data Scientist": {
        "companies": TARGET_COMPANIES,
        "skills": ["Python", "R", "SQL", "Machine Learning", "Pandas", "NumPy", "Scikit-Learn", "Statistics", "Tableau"]
    },
    "Machine Learning Engineer": {
        "companies": TARGET_COMPANIES,
        "skills": ["Python", "PyTorch", "TensorFlow", "Machine Learning", "Deep Learning", "SQL", "Docker", "Algorithms", "C++"]
    },
    "QA Automation Engineer": {
        "companies": TARGET_COMPANIES,
        "skills": ["Python", "Java", "Selenium", "PyTest", "API Testing", "Postman", "Git", "CI/CD"]
    },
    "Security Engineer": {
        "companies": TARGET_COMPANIES,
        "skills": ["Network Security", "Cryptography", "Python", "Linux", "Penetration Testing", "Cloud Security", "OWASP"]
    },
    "Mobile Engineer": {
        "companies": TARGET_COMPANIES,
        "skills": ["Kotlin", "Swift", "Flutter", "React Native", "Java", "REST API", "Git", "iOS/Android"]
    }
}

# -------------------------------------------------------------
# 3. GENERATE COMPLETE JOB MATRIX & SKILL COUNT
# -------------------------------------------------------------
job_records = []
skill_frequency = defaultdict(int)

for role_name, data in ROLE_SKILL_MAPPING.items():
    companies_list = ", ".join(data["companies"])
    skills_list = ", ".join(data["skills"])
    
    # Append structured job record
    job_records.append({
        "Job Title": role_name,
        "Company Name": companies_list,
        "Required Skills": skills_list
    })
    
    # Count frequency per individual company occurrence (10 per role)
    num_companies = len(data["companies"])
    for skill in data["skills"]:
        skill_frequency[skill] += num_companies

# -------------------------------------------------------------
# 4. EXPORT TO CSV SHEETS
# -------------------------------------------------------------
df_jobs = pd.DataFrame(job_records)
df_jobs.to_csv("product_company_jobs.csv", index=False)

df_skills = pd.DataFrame(list(skill_frequency.items()), columns=["Skill", "Frequency"])
df_skills = df_skills.sort_values(by="Frequency", ascending=False)
df_skills.to_csv("skill_repetition_count.csv", index=False)

# -------------------------------------------------------------
# 5. PRINT SUMMARY REPORT
# -------------------------------------------------------------
print("=========================================================================")
print(f"  SUCCESSFULLY GENERATED MATRIX FOR {len(job_records)} ROLES ACROSS 10 COMPANIES")
print("=========================================================================\n")

print("--- SUMMARY OF ALL INCLUDED ROLES ---")
print(df_jobs[["Job Title", "Required Skills"]].to_string(index=False))

print("\n--- TOP 20 IN-DEMAND SKILLS OVERALL ---")
print(df_skills.head(20).to_string(index=False))

print("\nSaved files in C:\\WebScrapingProject:")
print("1. product_company_jobs.csv")
print("2. skill_repetition_count.csv")