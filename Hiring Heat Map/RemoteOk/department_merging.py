import pandas as pd

# Load files
jobs_df = pd.read_csv("remoteok_jobs_with_department.csv")
keywords_df = pd.read_excel("department_keywords.xlsx")

# Build keyword → department mapping
mapping = []
for _, row in keywords_df.iterrows():
    dept = row["department"]
    keywords = str(row["keywords"]).split("|")
    for kw in keywords:
        kw = kw.strip().lower()
        if kw:
            mapping.append((kw, dept))

# Function to assign department from tags
def assign_department(row):
    tags = str(row['tags']).lower()
    for kw, dept in mapping:
        if kw in tags:
            return dept
    return row.get("department") if "department" in row and pd.notna(row["department"]) else None

# Apply enrichment
jobs_df['department'] = jobs_df.apply(assign_department, axis=1)

jobs_df['department'] = jobs_df['department'].fillna("Others")
jobs_df['department'] = jobs_df['department'].replace("", "Others")

# Save updated file
jobs_df.to_csv("remoteok_jobs_enriched.csv", index=False)

print("Departments updated based on Tags. Saved to remoteok_jobs_enriched.csv")
