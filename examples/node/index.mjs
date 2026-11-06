// Several roles in several cities in one run: newest jobs from the last 3 days, merged and de-duplicated.
// npm install && APIFY_TOKEN=<your token> node index.mjs
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

const run = await client.actor('abotapi/seek-scraper').call({
    mode: 'search',
    region: 'AU',
    keywords: 'registered nurse',
    keywordsList: ['enrolled nurse', 'midwife'],    // one extra search per entry, same filters
    location: 'Melbourne VIC',
    locationsList: ['Geelong VIC', 'Ballarat VIC'], // every keyword is searched in every location
    daterange: 3,
    includeFullDescription: false,                  // search-page fields only: faster and cheaper
    maxItems: 100,                                  // one cap shared by all searches, filled in order: keep it high enough to reach later cities
}, { log: null }); // don't stream the run log to your console

const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(`${items.length} jobs`);
const byWorkType = {};
for (const it of items) for (const wt of it.workTypes ?? []) byWorkType[wt] = (byWorkType[wt] ?? 0) + 1;
console.table(byWorkType); // full time vs part time vs casual: useful for rostered roles like nursing
for (const it of items.slice(0, 5)) {
    console.log(`${it.title.slice(0, 50)} | ${it.companyName} | ${it.locationLabel} | ${it.salaryLabel ?? 'salary not shown'}`);
}
