import pandas as pd

# Load files
jobs_df = pd.read_excel("dropbox_jobs.xlsx")
keywords_df = pd.read_excel("department_keywords.xlsx")  # updated file

# Build keyword → department mapping
mapping = []
for _, row in keywords_df.iterrows():
    dept = row["department"]
    keywords = str(row["keywords"]).split("|")
    for kw in keywords:
        kw = kw.strip().lower()
        if kw:
            mapping.append((kw, dept))

# Function to assign department
def assign_department(row):
    if pd.notna(row['department']) and row['department']:
        return row['department']
    
    title = str(row['job_title']).lower()
    for kw, dept in mapping:
        if kw in title:
            return dept
    return None

# Apply enrichment
jobs_df['department'] = jobs_df.apply(assign_department, axis=1)

# Save updated file
jobs_df.to_excel("dropbox_jobs_enriched.xlsx", index=False)

print("✅ Enriched departments saved to dropbox_jobs_enriched.xlsx")
