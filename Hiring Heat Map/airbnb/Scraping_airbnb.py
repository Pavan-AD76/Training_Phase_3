'''import requests
import pandas as pd
import datetime

# Greenhouse API endpoint for Airbnb
API_URL = "https://boards-api.greenhouse.io/v1/boards/airbnb/jobs"

# Custom headers to avoid blocking
headers = {
    "User-Agent": "HiringHeatmapBot/0.1 (+youremail@example.com)"
}

def fetch_jobs(url, timeout=10):
    """Fetch job listings from the given Greenhouse API URL."""
    try:
        resp = requests.get(url, headers=headers, timeout=timeout)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def parse_greenhouse_jobs(payload, company_name):
    """Parse the Greenhouse API JSON into a pandas DataFrame."""
    if not payload or "jobs" not in payload:
        return pd.DataFrame()

    jobs_list = payload["jobs"]
    rows = []
    
    for job in jobs_list:
        dept = None
        depts = job.get("departments") or []
        if depts:
            dept = depts[0].get("name")

        loc = None
        location = job.get("location") or {}
        if isinstance(location, dict):
            loc = location.get("name")

        rows.append({
            "company": company_name,
            "job_id": job.get("id"),
            "job_title": job.get("title"),
            "department": dept,
            "location": loc,
            "url": job.get("absolute_url"),
            "post_date": job.get("updated_at") or job.get("created_at"),
            "scrape_date": datetime.date.today().isoformat()
        })
    
    return pd.DataFrame(rows)

# Fetch and parse
payload = fetch_jobs(API_URL)
df = parse_greenhouse_jobs(payload, "Airbnb")

if not df.empty:
    print(f"Scraped {len(df)} jobs from Airbnb")
    print(df.head())
    df.to_csv("airbnb_jobs.csv", index=False)
    print("Saved to airbnb_jobs.csv")
else:
    print("No jobs found.")'''

import requests
import pandas as pd
import datetime

# Greenhouse API endpoint for Airbnb
API_URL = "https://boards-api.greenhouse.io/v1/boards/airbnb/jobs"

# Custom headers to avoid blocking
headers = {
    "User-Agent": "HiringHeatmapBot/0.1 (+youremail@example.com)"
}

def fetch_jobs(url, timeout=10):
    """Fetch job listings from the given Greenhouse API URL."""
    try:
        resp = requests.get(url, headers=headers, timeout=timeout)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def parse_greenhouse_jobs(payload, company_name):
    """Parse the Greenhouse API JSON into a pandas DataFrame."""
    if not payload or "jobs" not in payload:
        return pd.DataFrame()

    jobs_list = payload["jobs"]
    rows = []
    
    for job in jobs_list:
        dept = None
        depts = job.get("departments") or []
        if depts:
            dept = depts[0].get("name")

        loc = None
        location = job.get("location") or {}
        if isinstance(location, dict):
            loc = location.get("name")

        rows.append({
            "company": company_name,
            "job_id": job.get("id"),
            "job_title": job.get("title"),
            "department": dept,   # may be None
            "location": loc,
            "url": job.get("absolute_url"),
            "post_date": job.get("updated_at") or job.get("created_at"),
            "scrape_date": datetime.date.today().isoformat()
        })
    
    return pd.DataFrame(rows)

def load_keyword_mapping(filepath):
    """Load department-keyword mapping from the file."""
    # Read as tab-separated file (not real Excel)
    df = pd.read_csv(filepath, sep="\t")
    
    mapping = []
    for _, row in df.iterrows():
        dept = row["department"]
        keywords = str(row["keywords"]).split("|")
        for kw in keywords:
            kw = kw.strip().lower()
            if kw:
                mapping.append((kw, dept))
    return mapping


def enrich_departments(df, keywords_file):
    """Fill missing department values using keyword mapping file."""
    keyword_map = load_keyword_mapping(keywords_file)
    
    def assign_department(row):
        # Keep department if already present
        if pd.notna(row['department']) and row['department']:
            return row['department']
        
        title = str(row['job_title']).lower()
        for kw, dept in keyword_map:
            if kw in title:
                return dept
        return None
    
    df['department'] = df.apply(assign_department, axis=1)
    return df

# Fetch and parse
payload = fetch_jobs(API_URL)
df = parse_greenhouse_jobs(payload, "Airbnb")

if not df.empty:
    print(f"Scraped {len(df)} jobs from Airbnb")
    
    # Apply enrichment
    df = enrich_departments(df, "department_keywords.xls")
    
    print(df.head())
    df.to_csv("airbnb_jobs.csv", index=False)
    print("Saved to airbnb_jobs.csv")
else:
    print("No jobs found.")
