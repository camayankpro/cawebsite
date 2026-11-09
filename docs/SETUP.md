# TaxAMC SSG — Setup Guide

This guide covers everything you need to go from a fresh GitHub repo to 1,776 live pages on taxamc.com.

---

## What's in this ZIP

```
generate.py                          ← The page generator (run this)
cities.json                          ← 74 cities, pre-filled (fallback if no Sheet)
cities-google-sheet-template.csv     ← Import this into Google Sheets to manage cities
SETUP.md                             ← This file
.github/
  workflows/
    generate.yml                     ← GitHub Actions workflow (runs automatically)
templates/
  gst-registration.html              ← 24 service templates
  company-registration.html
  itr-filing.html
  ... (21 more)
```

---

## Step 1 — Upload to GitHub

Upload the contents of this ZIP to your GitHub repo (`taxamc/taxamc.github.io` or whichever repo powers taxamc.com on GitHub Pages).

The folder structure must be exactly:
```
your-repo/
├── generate.py
├── cities.json
├── cities-google-sheet-template.csv
├── templates/
│   ├── gst-registration.html
│   └── ... (all 24 templates)
└── .github/
    └── workflows/
        └── generate.yml
```

Once pushed, GitHub Actions will automatically run and generate all 1,776 pages.

---

## Step 2 — Google Sheet Setup (Optional but Recommended)

The Google Sheet lets you add/edit/remove cities without touching any code files. It is the primary data source. `cities.json` is only used as a fallback if the Sheet fails.

### 2a — Import the CSV into Google Sheets

1. Go to [sheets.google.com](https://sheets.google.com) → **Blank spreadsheet**
2. **File → Import → Upload** → select `cities-google-sheet-template.csv`
3. Import settings: **Replace current sheet**, **Comma** separator → **Import data**
4. You now have all 74 cities pre-filled with correct column headers

### 2b — Column Reference

| Column | Format | Example |
|--------|--------|---------|
| `city` | Plain text | `Bengaluru` |
| `state` | Plain text | `Karnataka` |
| `state_code` | ISO format | `IN-KA` |
| `slug` | Lowercase, hyphens only | `bengaluru` |
| `commissionerate` | Plain text | `CGST Commissionerate, Bengaluru` |
| `zone` | Plain text | `Bengaluru Zone` |
| `local_areas` | **Pipe-separated** | `Whitefield\|Electronic City\|Koramangala\|Indiranagar` |
| `key_industries` | **Pipe-separated** | `IT and software\|Aerospace\|Biotech` |
| `intro_note` | 1–2 sentences about the city | `India's Silicon Valley and...` |
| `nearby_cities` | **Pipe-separated** | `Mysuru\|Tumkur\|Hassan\|Mandya` |
| `company_note` | 1 sentence about company registration in the city | `Bengaluru leads...` |
| `gst_note` | 1 sentence about GST in the city | `Bengaluru's IT sector...` |

> **Important:** For `local_areas`, `key_industries`, and `nearby_cities` — separate multiple values with a **pipe character `|`**, not a comma. Commas break the CSV format.

### 2c — Add a New City

1. Scroll to the bottom of the Sheet
2. Add a new row with all 12 columns filled in
3. Go to GitHub → Actions → **Run workflow** → it will pick up the new city

### 2d — Publish the Sheet as CSV

1. **File → Share → Publish to web**
2. Under "Link", select your sheet tab name (e.g., `Sheet1`)
3. Under format, select **Comma-separated values (.csv)**
4. Click **Publish** → copy the URL (looks like `https://docs.google.com/spreadsheets/d/...`)

### 2e — Save as GitHub Secret

1. Go to your GitHub repo → **Settings → Secrets and variables → Actions**
2. Click **New repository secret**
3. Name: `SHEET_CSV_URL`
4. Value: paste the Google Sheet CSV URL
5. Click **Add secret**

That's it. Every time the workflow runs it fetches fresh data from your Sheet.

---

## Step 3 — Gemini AI Intros (Optional)

The generator can call Google Gemini (free tier) to write a **unique, city-specific intro paragraph** for every page — instead of reusing the same `intro_note` from your Sheet for all 24 services of a given city.

Without AI: every service page for Mumbai uses the same `intro_note` from your Sheet.  
With AI: the GST page for Mumbai gets a tailored GST intro, the ITR page gets a tailored ITR intro, etc. Better for SEO and user experience.

### 3a — Get a Free Gemini API Key

1. Go to [aistudio.google.com](https://aistudio.google.com)
2. Sign in with your Google account
3. Click **Get API key → Create API key**
4. Copy the key (starts with `AIza...`)

The free tier is generous — 15 requests/minute, 1,500 requests/day. For 74 cities × 24 services = 1,776 pages, you may hit the daily limit. The generator handles this gracefully: if Gemini fails for a page, it falls back to the `intro_note` from your Sheet automatically.

### 3b — Save as GitHub Secret

1. Go to your GitHub repo → **Settings → Secrets and variables → Actions**
2. Click **New repository secret**
3. Name: `GEMINI_API_KEY`
4. Value: paste your Gemini API key
5. Click **Add secret**

### 3c — Enable AI Intros in the Workflow

When triggering the workflow manually:
- Go to **Actions → TaxAMC — Generate City Pages → Run workflow**
- Set **"Use AI for unique city intros?"** to `true`
- Click **Run workflow**

For scheduled runs (1st of every month), AI is off by default to save API quota. Enable it manually after any major content update.

---

## Step 4 — GitHub Secrets Summary

Go to: **Your repo → Settings → Secrets and variables → Actions → New repository secret**

| Secret Name | Required? | Value |
|-------------|-----------|-------|
| `SHEET_CSV_URL` | Optional (recommended) | Google Sheet published CSV URL |
| `GEMINI_API_KEY` | Optional | Gemini API key from aistudio.google.com |
| `BING_API_KEY` | Optional | Bing Webmaster API key (covers Yahoo + DuckDuckGo) |

`GITHUB_TOKEN` is automatically available — you don't need to create it.

---

## Step 5 — Running the Generator

### Automatic (recommended)
The workflow runs automatically when you push changes to:
- `cities.json`
- `templates/*.html`
- `generate.py`

It also runs on the **1st of every month at 9:00 AM IST** to keep sitemap dates fresh.

### Manual — All 24 services, all 74 cities
Go to **Actions → TaxAMC — Generate City Pages → Run workflow → Run workflow**  
Leave the services field blank — generates all 1,776 pages.

### Manual — Specific services only
In the workflow dispatch form, enter a comma-separated list:
```
gst,itr,capital-gains
```

### Local (on your computer)
```bash
pip install jinja2
python generate.py                          # all 24 services, cities.json
python generate.py --services gst,itr       # specific services
python generate.py --sheet "YOUR_URL"       # use Google Sheet
python generate.py --ai                     # enable Gemini intros (needs GEMINI_API_KEY env var)
```

---

## What Gets Generated

| Metric | Count |
|--------|-------|
| Services | 24 |
| Cities | 74 |
| Total pages | **1,776** |
| Sitemap | `sitemap-cities.xml` |
| Page report | `_generated_pages.csv` |

Pages are named: `article-{service-slug}-{city-slug}.html`  
Example: `article-gst-registration-mumbai.html`

---

## Adding a New Service Template

1. Create `templates/your-template.html` (follow existing template structure)
2. Add an entry to the `SERVICES` dict in `generate.py`:
   ```python
   "your-key": {
       "template":    "your-template.html",
       "slug_prefix": "article-your-service",
       "label":       "Your Service Label",
       "priority":    "0.7",
   },
   ```
3. Add `"your-key"` to the `ALL_SERVICES` string in `generate.py`
4. Push to GitHub — the workflow runs automatically

---

## Troubleshooting

**Pages not committed after workflow runs**  
Check the Actions log. The `git add article-*.html` step covers all 24 services. If no HTML was generated, the generator likely errored — check the "Generate city pages" step logs.

**Google Sheet not loading**  
Make sure the Sheet is published (File → Publish to web) and the URL in `SHEET_CSV_URL` secret is the CSV URL (not the regular Sheet URL). The generator falls back to `cities.json` automatically if the Sheet fails.

**Gemini API quota exceeded**  
The generator automatically falls back to the `intro_note` field from your Sheet. No pages are skipped — they just use the static intro. Run with `--ai` again the next day for remaining cities.

**`--services` argument error**  
Make sure you're using the latest `generate.py` from this ZIP. The fix for the shell quoting bug is in `nargs="+"` — any older version will fail with space-separated service names.
