import pandas as pd
import re
from collections import Counter
from datetime import datetime

# 1. Define the "Tech Dictionary"
# This is what we are looking for in the text.
TECH_KEYWORDS = [
    "python", "java", "javascript", "typescript", "react", "angular", "vue",
    "aws", "azure", "gcp", "docker", "kubernetes", "linux",
    "sql", "postgresql", "mysql", "mongodb", "redis",
    "django", "flask", "fastapi", "spring boot", "node.js",
    "machine learning", "ai", "pytorch", "tensorflow", "pandas", "numpy",
    "git", "ci/cd", "jenkins", "terraform", "agile", "scrum"
]

def extract_skills(description):
    """
    Scans a text description and returns a list of found keywords.
    Uses regex \b to ensure we match 'Go' but not 'Good'.
    """
    if not isinstance(description, str):
        return []
    
    found_skills = []
    # Normalize text to lowercase
    text = description.lower()
    
    for skill in TECH_KEYWORDS:
        # Regex: \b matches word boundaries (start/end of word)
        # re.escape ensures special chars like C++ or Node.js don't break regex
        pattern = r'\b' + re.escape(skill) + r'\b'
        
        if re.search(pattern, text):
            found_skills.append(skill)
            
    return found_skills

def main():
    print("⚙️ Starting Data Processor...")
    
    # 2. Load Raw Data
    try:
        df = pd.read_csv("data/raw/jobs_raw.csv")
        print(f"   -> Loaded {len(df)} raw jobs.")
    except FileNotFoundError:
        print("❌ Error: data/raw/jobs_raw.csv not found. Run scraper.py first!")
        return

    # 3. Apply Extraction Logic
    print("   -> Extracting skills from descriptions...")
    df['skills_found'] = df['description'].apply(extract_skills)
    
    # 4. Create a "Skills Count" Metadata Table
    # Flatten the list of lists into one big list of all found skills
    all_skills = [skill for sublist in df['skills_found'] for skill in sublist]
    skill_counts = Counter(all_skills)
    
    # Convert to DataFrame for easier saving/viewing
    df_trends = pd.DataFrame(skill_counts.items(), columns=['skill', 'count'])
    df_trends = df_trends.sort_values(by='count', ascending=False)
    
    # 5. Save Processed Data
    # Save the enriched job list (with the new 'skills_found' column)
    df.to_csv("data/processed/jobs_enriched.csv", index=False)
    
    # Save the trends summary (for our dashboard later)
    timestamp = datetime.now().strftime("%Y-%m-%d")
    df_trends['date'] = timestamp
    df_trends.to_csv(f"data/processed/skills_trend_{timestamp}.csv", index=False)
    
    print(f"✅ Success! Enriched data saved to data/processed/")
    print("\n📊 Top 5 Skills Found:")
    print(df_trends.head(5))

if __name__ == "__main__":
    main()