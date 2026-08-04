import requests
from bs4 import BeautifulSoup
import pandas as pd

# Step 1: Fetch the web page HTML
url = "https://realpython.github.io/fake-jobs/"
print("Downloading job board page...")
response = requests.get(url)

if response.status_code == 200:
    print("Successfully connected!")
else:
    print(f"Failed to connect. Status code: {response.status_code}")

# Step 2: Parse HTML content with BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")
job_cards = soup.find_all("div", class_="card-content")

# Step 3: Define skills to track and count frequency
target_skills = [
    "Python", "C++", "Java", "JavaScript", "React", 
    "AWS", "SQL", "Docker", "Git", "Linux", "REST"
]

skill_counts = {skill: 0 for skill in target_skills}
extracted_jobs = []

for card in job_cards:
    title_element = card.find("h2", class_="title")
    company_element = card.find("h3", class_="company")
    
    title = title_element.text.strip() if title_element else "N/A"
    company = company_element.text.strip() if company_element else "N/A"
    
    full_card_text = card.text
    matched_skills = []
    
    for skill in target_skills:
        if skill.lower() in full_card_text.lower():
            skill_counts[skill] += 1
            matched_skills.append(skill)
            
    extracted_jobs.append({
        "Title": title,
        "Company": company,
        "Matched Skills": ", ".join(matched_skills)
    })

# Step 4: Generate and display the Top 10 Report
df_skills = pd.DataFrame(list(skill_counts.items()), columns=["Skill", "Demand_Count"])
df_top10 = df_skills.sort_values(by="Demand_Count", ascending=False).head(10)

print("\n==========================================")
print("     TOP 10 IN-DEMAND SKILLS REPORT       ")
print("==========================================")
print(df_top10.to_string(index=False))

# Step 5: Save results to CSV files
df_top10.to_csv("top_10_skills.csv", index=False)
df_jobs = pd.DataFrame(extracted_jobs)
df_jobs.to_csv("all_scraped_jobs.csv", index=False)

print("\nSuccess! Saved 'top_10_skills.csv' and 'all_scraped_jobs.csv' in C:\\WebScrapingProject.")