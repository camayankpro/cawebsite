# TaxAMC — City Pages Generator
## Complete Setup Guide (No coding knowledge needed)

---

## What This Does

Automatically generates city-specific SEO pages for:
- **GST Registration in [City]** — one page per city
- **Company Registration in [City]** — one page per city

Currently set up for **74 pan-India cities = 148 pages total**.
Runs automatically. You never touch code.

---

## Files in This Package

```
your-repo/
├── generate.py                          ← Generator engine (never edit)
├── cities.json                          ← City data backup (auto-used if Sheet fails)
├── google-sheet-template.csv            ← Import this into Google Sheets to start
├── templates/
│   ├── gst-registration.html            ← GST page design
│   └── company-registration.html        ← Company page design
└── .github/
    └── workflows/
        └── generate.yml                 ← Automation brain (never edit)
```

---

## PART A — INITIAL SETUP (Do Once)

### Step 1 — Upload All Files to GitHub

1. Go to **github.com** → open your `cawebsite` repo
2. For each file below, click **"Add file" → "Create new file"**
3. Type the path in the filename box and paste the file content

| Type this as the filename | Upload this file |
|---|---|
| `generate.py` | generate.py |
| `cities.json` | cities.json |
| `google-sheet-template.csv` | google-sheet-template.csv |
| `templates/gst-registration.html` | gst-registration.html |
| `templates/company-registration.html` | company-registration.html |
| `.github/workflows/generate.yml` | generate.yml |

> Typing the `/` in the filename box automatically creates the folder.

---

### Step 2 — Set Up Your Google Sheet (Recommended)

This lets you manage cities from a spreadsheet — no GitHub editing needed.

**2a — Import the template into Google Sheets**
1. Go to **sheets.google.com** → click **"+"** (Blank spreadsheet)
2. Click **File → Import → Upload** → upload `google-sheet-template.csv`
3. Select "Replace spreadsheet" → click Import

You now have a sheet with the correct column headers and 3 sample cities.

**2b — Add all 74 cities**
Copy the city data from `cities.json` into the sheet.
Each city = one row. For columns with multiple values (local_areas, key_industries, nearby_cities), separate items with a `|` pipe character.

Example for the `local_areas` column:
```
Whitefield|Electronic City|Koramangala|Indiranagar
```

**2c — Publish the sheet as CSV**
1. Click **File → Share → Publish to web**
2. Under "Link" dropdown — select your sheet name (e.g. "Sheet1")
3. Under the second dropdown — select **"Comma-separated values (.csv)"**
4. Click **Publish** → click **OK**
5. **Copy the URL shown** — it looks like:
   `https://docs.google.com/spreadsheets/d/e/XXXXX/pub?gid=0&single=true&output=csv`

**2d — Save the URL as a GitHub Secret**
1. Go to your GitHub repo → **Settings** tab
2. Click **Secrets and variables** → **Actions**
3. Click **"New repository secret"**
4. Name: `SHEET_CSV_URL`
5. Value: paste the Google Sheet CSV URL from step 2c
6. Click **"Add secret"**

✅ Done! The generator now reads from your Google Sheet automatically.

---

### Step 3 — Submit Sitemaps to Google

1. Go to **search.google.com/search-console**
2. Click **"Sitemaps"** in the left menu
3. Enter `sitemap-cities.xml` → click **Submit**

---

### Step 4 — Set Up Bing Webmaster Tools (Covers Yahoo + DuckDuckGo)

> **Important:** Yahoo and DuckDuckGo do NOT have their own search index.
> Both use Bing's index. Submitting to Bing = appearing on Yahoo + DuckDuckGo automatically. No separate submission needed for them.

1. Go to **bing.com/webmasters** → sign in (free Microsoft account)
2. Click **"Add a site"** → enter `https://taxamc.com` → click Add
3. Verify ownership:
   - Choose **"HTML Meta Tag"** option
   - Copy the meta tag shown
   - Paste it inside the `<head>` section of your `index.html`
   - Commit the change → come back and click Verify
4. Once verified → click **"Sitemaps"** in the left menu
5. Enter `sitemap-cities.xml` → click **Submit**

**Optional — Get Bing API Key for automatic submission:**
1. In Bing Webmaster Tools → **Settings** → **API access**
2. Click **"Generate API key"** → copy the key
3. Go to GitHub → your repo → **Settings → Secrets → Actions**
4. Add new secret: Name `BING_API_KEY` → paste the key
5. Now every time the generator runs, it also submits to Bing API automatically

---

## PART B — DAILY USE (Ongoing)

### How to Add a New City

**Option 1 — Via Google Sheet (easiest)**
1. Open your Google Sheet
2. Add a new row with the city data
3. For `local_areas`, `key_industries`, `nearby_cities` — use `|` to separate values
4. Go to your GitHub repo → **Actions** tab → click **"TaxAMC — Generate City Pages"**
5. Click **"Run workflow"** → click the green **"Run workflow"** button
6. Wait 2–3 minutes → new city pages are live ✅

**Option 2 — Via cities.json in GitHub**
1. Open `cities.json` in your GitHub repo → click the pencil (Edit) icon
2. Add a new city block at the end (before the last `]`):
```json
,
{
  "city": "Agartala",
  "state": "Tripura",
  "state_code": "IN-TR",
  "slug": "agartala",
  "commissionerate": "CGST Commissionerate, Guwahati",
  "zone": "Guwahati Zone",
  "local_areas": ["Battala Market", "Sadar", "Industrial Area"],
  "key_industries": ["Bamboo products", "Rubber", "Government services"],
  "intro_note": "Tripura's capital city.",
  "nearby_cities": ["Guwahati", "Silchar"],
  "company_note": "Agartala falls under ROC Assam, Guwahati.",
  "gst_note": "Special category state GST threshold of Rs. 10 lakh applies."
}
```
3. Click **"Commit changes"** → pages generate automatically ✅

---

### What Runs Automatically Without Any Action From You

| What | When |
|---|---|
| All 148 pages regenerate | 1st of every month at 9 AM |
| Google is pinged | After every regeneration |
| Bing is pinged (covers Yahoo + DuckDuckGo) | After every regeneration |
| Sitemap date refreshes | After every regeneration |

---

### When to Manually Click "Run Workflow"

Only in these situations:
- You added new cities to your Google Sheet
- You edited a template and want to rebuild all pages
- You want to regenerate immediately without waiting for the 1st of the month

---

## PART C — SEARCH ENGINE COVERAGE EXPLAINED

| Search Engine | Has Own Index? | How Covered |
|---|---|---|
| Google | ✅ Yes | Sitemap submitted + pinged after every run |
| Bing | ✅ Yes | Sitemap submitted + pinged after every run |
| Yahoo | ❌ No (uses Bing) | Covered automatically via Bing |
| DuckDuckGo | ❌ No (uses Bing) | Covered automatically via Bing |
| Ecosia | ❌ No (uses Bing) | Covered automatically via Bing |

**Summary:** Submit to Google + Bing once → appear on all 5 search engines.

---

## PART D — ADDING MORE SERVICES LATER

To add ITR Filing, Trademark, MSME pages for all cities:

1. Create a new template: `templates/itr-filing.html`
   (Copy the GST template and change the content)
2. Open `generate.py` → find the `SERVICES` section at the top → add:
```python
"itr": {
    "template":    "itr-filing.html",
    "slug_prefix": "article-itr-filing",
    "label":       "ITR Filing",
    "priority":    "0.8",
},
```
3. Commit → 74 new ITR pages generate automatically

---

## PART E — TROUBLESHOOTING

**Red cross in Actions tab?**
Click on it → read the error → share a screenshot for help.

**Google Sheet not loading?**
Check the sheet is published (File → Share → Publish to web).
The generator automatically falls back to cities.json if the sheet fails.

**Pages generated but not on Google?**
Normal — Google takes 2–6 weeks to index new pages.
Check Search Console → Coverage → to see indexing status.

**Wrong data on a page?**
Fix it in your Google Sheet or cities.json → run workflow → pages update.

---

*TaxAMC Generator — Agarwal Mayank & Company*
