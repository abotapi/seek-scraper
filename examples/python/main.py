"""Search SEEK (Australia or New Zealand) for jobs and save them, with salary and full description, to CSV.

pip install "apify-client>=3"
APIFY_TOKEN=<your token> python main.py "data analyst" Sydney
APIFY_TOKEN=<your token> python main.py "registered nurse" Auckland NZ
"""
import csv
import os
import sys

from apify_client import ApifyClient

keywords = sys.argv[1] if len(sys.argv) > 1 else "data analyst"
location = sys.argv[2] if len(sys.argv) > 2 else "Sydney"
region = sys.argv[3] if len(sys.argv) > 3 else "AU"   # AU = seek.com.au, NZ = seek.co.nz
client = ApifyClient(os.environ["APIFY_TOKEN"])

run = client.actor("abotapi/seek-scraper").call(run_input={
    "mode": "search",
    "region": region,
    "keywords": keywords,
    "location": location,           # a suburb, city, state or postcode, e.g. "Parramatta NSW 2150"
    "daterange": 7,                 # listed in the last 7 days (SEEK accepts 1, 3, 7, 14 or 31)
    "sortmode": "ListedDate",       # newest first; or KeywordRelevance
    "includeFullDescription": True, # full text, bullet points, applicant numbers, contact details, employer profile
    "descriptionFormat": "text",    # plain text only keeps the CSV readable
    "maxItems": 20,
}, logger=None)  # logger=None: don't stream the run log to your console

items = list(client.dataset(run.default_dataset_id).iterate_items())
fields = ["title", "companyName", "locationLabel", "workTypes", "salaryLabel", "salaryMin", "salaryMax",
          "salaryPeriod", "listingDate", "numApplicants", "url"]
with open("seek_jobs.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
    writer.writeheader()
    for it in items:
        writer.writerow({**it, "workTypes": ", ".join(it.get("workTypes") or [])})

print(f"Saved {len(items)} jobs to seek_jobs.csv")
with_salary = [it for it in items if it.get("salaryLabel")]
print(f"{len(with_salary)} of {len(items)} ads show a salary")
for it in items[:5]:
    print(f"- {it['title'][:50]} | {it.get('companyName')} | {it.get('locationLabel')} | {it.get('salaryLabel') or 'salary not shown'}")
