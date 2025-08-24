'''from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Configure Selenium
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Step 1: Go to RemoteOK jobs page
driver.get("https://remoteok.com/")
WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tr.job")))

# Step 2: Scroll to load more jobs (optional)
for _ in range(3):
    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
    time.sleep(2)

# Step 3: Scrape job data
titles, companies, locations, tags, dates = [], [], [], [], []
job_cards = driver.find_elements(By.CSS_SELECTOR, "tr.job")

for card in job_cards:
    try:
        title = card.find_element(By.CSS_SELECTOR, "h2").text
    except:
        title = ""
    try:
        company = card.find_element(By.CSS_SELECTOR, "h3").text
    except:
        company = ""
    try:
        location = card.find_element(By.CSS_SELECTOR, ".location").text
    except:
        location = ""
    try:
        skill_tags = [t.text for t in card.find_elements(By.CSS_SELECTOR, ".tags .tag")]
        tags_str = ", ".join(skill_tags)
    except:
        tags_str = ""
    try:
        date_posted = card.find_element(By.CSS_SELECTOR, "time").get_attribute("datetime")
    except:
        date_posted = ""

    titles.append(title)
    companies.append(company)
    locations.append(location)
    tags.append(tags_str)
    dates.append(date_posted)

# Step 4: Save to CSV
df = pd.DataFrame({
    "Job Title": titles,
    "Company": companies,
    "Location": locations,
    "Tags": tags,
    "Date Posted": dates
})
df.to_csv("remoteok_jobs.csv", index=False)

print(f"Scraping completed. {len(df)} jobs saved to remoteok_jobs.csv")
driver.quit()'''

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time


# ----------------- Department Mapping Loader -----------------
def load_keyword_mapping(filepath):
    """Load department-keyword mapping from the tab-delimited file."""
    df = pd.read_csv(filepath, sep="\t")  # file is tab-delimited
    mapping = []
    for _, row in df.iterrows():
        dept = row["department"]
        keywords = str(row["keywords"]).split("|")
        for kw in keywords:
            kw = kw.strip().lower()
            if kw:
                mapping.append((kw, dept))
    return mapping

def assign_departments(df, keyword_file):
    """Assign department to each job row based on job title & tags."""
    keyword_map = load_keyword_mapping(keyword_file)

    def match_department(title, tags):
        text = (str(title) + " " + str(tags)).lower()
        for kw, dept in keyword_map:
            if kw in text:
                return dept
        return None

    df["Department"] = df.apply(
        lambda row: match_department(row["Job Title"], row["Tags"]), axis=1
    )
    return df
# --------------------------------------------------------------

# Configure Selenium
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Step 1: Go to RemoteOK jobs page
driver.get("https://remoteok.com/")
WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tr.job")))

# Step 2: Scroll to load more jobs (optional)
for _ in range(3):
    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
    time.sleep(2)

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Keep scrolling until no new jobs appear
prev_count = 0
while True:
    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
    time.sleep(3)  # wait for new jobs to load
    job_cards = driver.find_elements(By.CSS_SELECTOR, "tr.job")
    if len(job_cards) == prev_count:  # no new jobs
        break
    prev_count = len(job_cards)

print(f"Total jobs loaded: {len(job_cards)}")


# Step 3: Scrape job data
titles, companies, locations, tags, dates = [], [], [], [], []
job_cards = driver.find_elements(By.CSS_SELECTOR, "tr.job")

for card in job_cards:
    try:
        title = card.find_element(By.CSS_SELECTOR, "h2").text
    except:
        title = ""
    try:
        company = card.find_element(By.CSS_SELECTOR, "h3").text
    except:
        company = ""
    try:
        location = card.find_element(By.CSS_SELECTOR, ".location").text
    except:
        location = ""
    try:
        skill_tags = [t.text for t in card.find_elements(By.CSS_SELECTOR, ".tags .tag")]
        tags_str = ", ".join(skill_tags)
    except:
        tags_str = ""
    try:
        date_posted = card.find_element(By.CSS_SELECTOR, "time").get_attribute("datetime")
    except:
        date_posted = ""

    titles.append(title)
    companies.append(company)
    locations.append(location)
    tags.append(tags_str)
    dates.append(date_posted)

# Step 4: Save to CSV with Department
df = pd.DataFrame({
    "Job Title": titles,
    "Company": companies,
    "Location": locations,
    "Tags": tags,
    "Date Posted": dates
})

# 🔑 Enrich with departments
df = assign_departments(df, "department_keywords.xls")

df.to_csv("remoteok_jobs_output.csv", index=False)

print(f"Scraping completed. {len(df)} jobs saved to remoteok_jobs.csv")

driver.quit()
