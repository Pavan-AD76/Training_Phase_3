import requests
import pandas as pd
import datetime

# Company to scrape
company = "dropbox"

# Headers (helps avoid blocking)
headers = {
    "User-Agent": "HiringHeatmapBot/1.0 (+contact@example.com)"
}

def fetch_greenhouse_jobs(company):
    """Fetch job data from Greenhouse for a company"""
    url = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs"
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f" Error fetching {company}: {e}")
        return pd.DataFrame()

    rows = []
    for job in data.get("jobs", []):
        dept = job["departments"][0]["name"] if job.get("departments") else None
        loc = job["location"]["name"] if job.get("location") else None
        rows.append({
            "company": company,
            "job_id": job.get("id"),
            "job_title": job.get("title"),
            "department": dept,
            "location": loc,
            "url": job.get("absolute_url"),
            "post_date": job.get("updated_at") or job.get("created_at"),
            "scrape_date": datetime.date.today().isoformat()
        })

    return pd.DataFrame(rows)

# Run only for Dropbox
df = fetch_greenhouse_jobs(company)

if not df.empty:
    print(f" {company}: {len(df)} jobs scraped")
    df.to_excel("dropbox_jobs.xlsx", index=False)
    print(" Saved to dropbox_jobs.xlsx")
else:
    print(" No jobs scraped.")
