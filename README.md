# SEEK Scraper

**Get job listings from SEEK Australia (seek.com.au) and SEEK New Zealand (seek.co.nz) as JSON or CSV: title, employer, salary range, location, classification, work type, full description, applicant count and published contact details.**

![Output](https://img.shields.io/badge/output-JSON%20%7C%20CSV%20%7C%20Excel-green?style=flat-square)
![Country](https://img.shields.io/badge/country-Australia%20%7C%20New%20Zealand-blue?style=flat-square)
![License](https://img.shields.io/badge/examples-MIT-lightgrey?style=flat-square)

SEEK is the main job board in Australia and New Zealand. It has no public job-search API for third parties, so recruiters,
labour-market researchers and job seekers who want the data in a spreadsheet usually copy it by hand.

This repo shows how to pull that data with the
**[SEEK Jobs Scraper on Apify](https://apify.com/abotapi/seek-scraper?utm_source=github&utm_medium=seek-scraper&utm_campaign=showcase)**,
a hosted scraper you can run from the web UI or call from code.

## Table of Contents

- [What you can get](#what-you-can-get)
- [Quick start](#quick-start)
- [Examples](#examples)
- [Input options](#input-options)
- [Sample output](#sample-output)
- [Use cases](#use-cases)
- [FAQ](#faq)

## What you can get

| Group | Fields |
| --- | --- |
| **Job** | ID, URL, apply link, title, teaser, bullet points, classification and subclassification, work type (full time, part time, contract, casual), work arrangement (on-site, hybrid, remote), listing date, expiry date, repost flag |
| **Salary** | salary text as shown, parsed `salaryMin` / `salaryMax`, currency, period (annual, monthly, hourly) |
| **Location** | display label, suburb, state, postcode, country, SEO location hierarchy |
| **Full description** (default on) | HTML, plain text or Markdown, description sections, employer screening questions, applicant count and volume, published phone numbers and emails |
| **Employer** | company name and profile URL, industry, size, website, rating and review count, perks, awards, logo, advertiser ID |

## Quick start

**No code:** open the [scraper page](https://apify.com/abotapi/seek-scraper?utm_source=github&utm_medium=seek-scraper&utm_campaign=showcase),
type keywords (`data analyst`, `registered nurse`) and a location (`Sydney`, `All Melbourne VIC`, `Auckland`), click **Start**,
and download JSON, CSV or Excel. You can also paste any SEEK search, company or job URL.

**From code:** get a free [Apify API token](https://console.apify.com/settings/integrations?utm_source=github&utm_medium=seek-scraper&utm_campaign=showcase), then:

```bash
git clone https://github.com/abotapi/seek-scraper && cd seek-scraper
export APIFY_TOKEN=<your token>
```

## Examples

### Python: keyword + location search, saved to CSV

[`examples/python/main.py`](examples/python/main.py) gets jobs from the last 7 days with full descriptions and reports how many ads show a salary.

```bash
pip install "apify-client>=3"
python examples/python/main.py "data analyst" Sydney
python examples/python/main.py "registered nurse" Auckland NZ
```

```text
Saved 20 jobs to seek_jobs.csv
9 of 20 ads show a salary
- Data Analyst | Harbourline Analytics | Parramatta, Sydney NSW | $95,000 - $110,000 + super
- Registered Nurse - Aged Care | Wattle Grove Care | Geelong, Geelong & Western VIC | $45 - $52 per hour + penalty rates
- Warehouse Team Leader | Kauri Bay Logistics | East Tamaki, Auckland | salary not shown
```

(Printed values above are mock.)

### Node.js: several roles in several cities in one run

[`examples/node/index.mjs`](examples/node/index.mjs) searches three nursing roles across three Victorian cities, merges and de-duplicates the results, and counts them by work type.

```bash
cd examples/node && npm install && node index.mjs
```

### cURL: compact JSON for an AI agent or spreadsheet

[`examples/curl.sh`](examples/curl.sh) uses the `run-sync-get-dataset-items` endpoint, which starts the run, waits, and returns the items. `compact` plus a capped Markdown description keeps each row small:

```bash
./examples/curl.sh > auckland-software.json
```

## Input options

| Option | What it does |
| --- | --- |
| `mode` | `search` (use the fields below), `url` (paste SEEK search, company or job links into `urls`) or `auto` |
| `region` | `AU` (seek.com.au) or `NZ` (seek.co.nz) |
| `keywords` / `keywordsList` | Job title or keywords; the list runs one extra search per entry and merges the results |
| `location` / `locationsList` / `radius` | Suburb, city, state or postcode as plain text (`Parramatta NSW 2150`, `All-Australia`), extra locations, and a 1-100 km radius |
| `companyName` | Only jobs from one employer (exact name) |
| `classification` / `subclassification` | SEEK's job categories, e.g. Healthcare & Medical › Nursing - Aged Care |
| `workType` / `workArrangement` | Full time, part time, contract, casual; on-site, hybrid, remote |
| `salaryType` / `salaryMin` / `salaryMax` | Salary range per year, month or hour |
| `daterange` / `fromDate` / `toDate` / `maxAgeMinutes` | Only recent jobs: last 1, 3, 7, 14 or 31 days, a date window, or the last N minutes |
| `includeKeywords` / `excludeKeywords` | Keep or drop jobs that mention certain words |
| `minApplicants` / `maxApplicants` / `requireContact` | Find low-competition roles, or only ads that publish a phone number or email |
| `includeFullDescription` / `descriptionFormat` / `compact` | Full details on or off; HTML, text or Markdown; a smaller core-fields row |
| `maxItems` / `maxTimeSec` | One result cap and one time cap shared by all searches |
| `incrementalMode` | For scheduled runs: label each job NEW, UPDATED, UNCHANGED, REAPPEARED or EXPIRED and output only the changes |

See the [scraper page](https://apify.com/abotapi/seek-scraper?utm_source=github&utm_medium=seek-scraper&utm_campaign=showcase) for the full list.

## Sample output

Mock data with the same fields and types as real output (the employers, jobs and numbers are made up):
[`sample-output/sample.json`](sample-output/sample.json) · [`sample-output/sample.csv`](sample-output/sample.csv)

```json
{
  "id": "90000001",
  "url": "https://www.seek.com.au/job/90000001",
  "title": "Data Analyst",
  "companyName": "Harbourline Analytics",
  "locationLabel": "Parramatta, Sydney NSW",
  "locationState": "NSW",
  "locationPostcode": "2150",
  "classificationInfo": {
    "classification": "Technology & Data (mock category)",
    "subClassification": "Database Development & Administration"
  },
  "workTypes": ["Full time"],
  "workArrangementLabels": ["Hybrid"],
  "salaryLabel": "$95,000 - $110,000 + super",
  "salaryMin": 95000,
  "salaryMax": 110000,
  "salaryPeriod": "annual",
  "salaryCurrency": "AUD",
  "bulletPoints": ["SQL and Python every day", "Hybrid: 3 days in office", "Mentored by a senior analyst"],
  "numApplicants": 24,
  "emails": ["careers@harbourline.example.com"],
  "listingDate": "2026-01-14T22:10:00.000Z",
  "companyIndustry": "Professional Services",
  "companyRating": 4.2
}
```

## Use cases

- **Recruiters and agencies:** a daily feed of new roles in your niche and territory, with employer and contact details
- **Salary benchmarking:** advertised salary ranges by role, classification, city and work type
- **Labour-market research:** hiring volume by industry and region over time (schedule it with `incrementalMode`)
- **Job seekers:** find recent, low-competition roles with `maxApplicants` and get them in one spreadsheet
- **Sales and BD teams:** see which companies are hiring for which roles, a common buying signal
- **AI agents:** `compact` rows with Markdown descriptions fit well in an LLM context

## FAQ

**How much does it cost?** You pay per result on Apify, and new accounts get free monthly credit. Full job details cost a little more than search-page rows. See the scraper page for current pricing.

**Why are salary fields empty for some jobs?** Many SEEK ads don't show a salary. When they do, `salaryLabel` has the text as written and `salaryMin` / `salaryMax` / `salaryPeriod` the parsed numbers.

**Can I get only new jobs every day?** Yes. Schedule the scraper in Apify and turn on `incrementalMode`; each run then outputs only new or changed jobs.

**Does it cover New Zealand?** Yes. Set `region` to `NZ`, or paste seek.co.nz links.

**Is scraping SEEK allowed?** The scraper collects publicly visible job ads. Contact details are only those an employer published in the ad. Check SEEK's terms and privacy law (Australian Privacy Act, NZ Privacy Act 2020) for your use case, especially before any outreach.

## Related

- [Job listings data for Australia and New Zealand](https://github.com/abotapi/web-scraping-guides/tree/main/job-listings-australia): a guide to official labour-market sources, job-board APIs and DIY options
- [Awesome Web Scrapers](https://github.com/abotapi/abotapi): a curated list of ready-to-run scrapers, including other job boards
- [web-scrapers](https://github.com/abotapi/web-scrapers): code examples and mock samples for every scraper in that list

---

<sub>The scraper is maintained by [abotapi](https://abotapi.com/?utm_source=github&utm_medium=seek-scraper&utm_campaign=showcase). Examples in this repo are MIT licensed. Not affiliated with SEEK.</sub>
