# Sample output

**Mock data.** These records have the same fields and types as real scraper output, but every value is made up: the employers, jobs, salaries, phone numbers, emails, IDs and URLs are fictional. They show the structure only.

- `sample.json`: jobs with full details (`includeFullDescription: true`, the default), two from SEEK Australia and one from SEEK New Zealand
- `sample.csv`: the flat (non-nested) fields of the same records

With `compact: true` each row keeps only the core fields (id, links, title, company, location, classification, work type, salary, dates, applicants, contacts, teaser, bullet points, description).
