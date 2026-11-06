#!/usr/bin/env bash
# Newest software jobs in Auckland (SEEK New Zealand) as compact JSON, in one HTTP call (waits for the run to finish).
# APIFY_TOKEN=<your token> ./curl.sh > auckland-software.json
curl -s -X POST \
  "https://api.apify.com/v2/acts/abotapi~seek-scraper/run-sync-get-dataset-items?token=${APIFY_TOKEN}" \
  -H 'Content-Type: application/json' \
  -d '{
    "mode": "search",
    "region": "NZ",
    "keywords": "software engineer",
    "location": "Auckland",
    "sortmode": "ListedDate",
    "compact": true,
    "descriptionFormat": "markdown",
    "descriptionMaxLength": 1500,
    "maxItems": 20
  }'
