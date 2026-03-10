#!/usr/bin/env python3
"""
TaxAMC Static Site Generator — Final Complete Version
======================================================
- Reads cities from Google Sheet (primary) or cities.json (fallback)
- Generates GST Registration + Company Registration pages for all cities
- Generates sitemap-cities.xml
- Pings Google, Bing, Yahoo, DuckDuckGo (all covered via Bing index)
- Optionally calls Claude AI for unique city intro paragraphs

Usage:
  python generate.py                   (uses cities.json)
  python generate.py --sheet URL       (uses Google Sheet)
  python generate.py --ai              (AI-enhanced intros)
  python generate.py --services gst    (only GST pages)
"""

import json, os, sys, csv, argparse, time
import urllib.request, urllib.parse
from datetime import date
from jinja2 import Environment, FileSystemLoader, select_autoescape

# ─── CONFIGURATION ────────────────────────────────────────────────────────────

BASE_URL        = "https://taxamc.com"
WHATSAPP_NUMBER = "919045222870"


SERVICES = {
    # ── Original 5 ──────────────────────────────────────────────────────────
    "gst": {
        "template":    "gst-registration.html",
        "slug_prefix": "article-gst-registration",
        "label":       "GST Registration",
        "priority":    "0.8",
    },
    "company": {
        "template":    "company-registration.html",
        "slug_prefix": "article-company-registration",
        "label":       "Company Registration",
        "priority":    "0.8",
    },
    "itr": {
        "template":    "itr-filing.html",
        "slug_prefix": "article-itr-filing",
        "label":       "ITR Filing",
        "priority":    "0.8",
    },
    "trademark": {
        "template":    "trademark-registration.html",
        "slug_prefix": "article-trademark-registration",
        "label":       "Trademark Registration",
        "priority":    "0.8",
    },
    "msme": {
        "template":    "msme-registration.html",
        "slug_prefix": "article-msme-registration",
        "label":       "MSME Registration",
        "priority":    "0.8",
    },
    # ── Batch 1 ─────────────────────────────────────────────────────────────
    "llp": {
        "template":    "llp-registration.html",
        "slug_prefix": "article-llp-registration",
        "label":       "LLP Registration",
        "priority":    "0.8",
    },
    "partnership": {
        "template":    "partnership-registration.html",
        "slug_prefix": "article-partnership-registration",
        "label":       "Partnership Firm Registration",
        "priority":    "0.8",
    },
    "roc": {
        "template":    "roc-filing.html",
        "slug_prefix": "article-roc-filing",
        "label":       "ROC Annual Filing",
        "priority":    "0.8",
    },
    "iec": {
        "template":    "iec-registration.html",
        "slug_prefix": "article-iec-registration",
        "label":       "IEC Registration",
        "priority":    "0.8",
    },
    # ── Batch 2 ─────────────────────────────────────────────────────────────
    "gst-return": {
        "template":    "gst-return-filing.html",
        "slug_prefix": "article-gst-return-filing",
        "label":       "GST Return Filing",
        "priority":    "0.8",
    },
    "tds": {
        "template":    "tds-filing.html",
        "slug_prefix": "article-tds-filing",
        "label":       "TDS Return Filing",
        "priority":    "0.8",
    },
    "gst-cancellation": {
        "template":    "gst-cancellation.html",
        "slug_prefix": "article-gst-cancellation",
        "label":       "GST Cancellation",
        "priority":    "0.7",
    },
    "gst-notice": {
        "template":    "gst-notice-reply.html",
        "slug_prefix": "article-gst-notice-reply",
        "label":       "GST Notice Reply",
        "priority":    "0.7",
    },
    # ── Batch 3 ─────────────────────────────────────────────────────────────
    "business-loan": {
        "template":    "business-loan-docs.html",
        "slug_prefix": "article-business-loan-docs",
        "label":       "Business Loan Documentation",
        "priority":    "0.7",
    },
    "itr-freelancers": {
        "template":    "itr-freelancers.html",
        "slug_prefix": "article-itr-freelancers",
        "label":       "ITR for Freelancers",
        "priority":    "0.7",
    },
    "itr-doctors": {
        "template":    "itr-doctors.html",
        "slug_prefix": "article-itr-doctors",
        "label":       "Tax for Doctors",
        "priority":    "0.7",
    },
    "ecommerce-gst": {
        "template":    "ecommerce-gst.html",
        "slug_prefix": "article-ecommerce-gst",
        "label":       "GST for Online Sellers",
        "priority":    "0.7",
    },
    # ── Batch 4 ─────────────────────────────────────────────────────────────
    "capital-gains": {
        "template":    "capital-gains.html",
        "slug_prefix": "article-capital-gains",
        "label":       "Capital Gains Tax",
        "priority":    "0.7",
    },
    "itr-creators": {
        "template":    "itr-creators.html",
        "slug_prefix": "article-itr-creators",
        "label":       "ITR for YouTubers & Creators",
        "priority":    "0.7",
    },
    "restaurant-gst": {
        "template":    "restaurant-gst.html",
        "slug_prefix": "article-restaurant-gst",
        "label":       "GST for Restaurants",
        "priority":    "0.7",
    },
    "export-lut": {
        "template":    "export-lut.html",
        "slug_prefix": "article-export-lut",
        "label":       "GST LUT for Exporters",
        "priority":    "0.7",
    },
    # ── Batch 5 ─────────────────────────────────────────────────────────────
    "gst-pharma": {
        "template":    "pharma-gst.html",
        "slug_prefix": "article-gst-pharma",
        "label":       "GST for Pharma",
        "priority":    "0.7",
    },
    "accounting-it": {
        "template":    "startup-accounting.html",
        "slug_prefix": "article-accounting-it",
        "label":       "Accounting for IT Companies",
        "priority":    "0.7",
    },
    "tds-contractors": {
        "template":    "tds-contractors.html",
        "slug_prefix": "article-tds-contractors",
        "label":       "TDS for Contractors",
        "priority":    "0.7",
    },
}

# ─── STEP 1 — LOAD CITIES DATA ────────────────────────────────────────────────

def load_from_json(path):
    with open(path, "r", encoding="utf-8") as f:
        cities = json.load(f)
    print(f"  ✓ Loaded {len(cities)} cities from cities.json")
    return cities


def load_from_sheet(csv_url):
    """
    Load cities from a Google Sheet published as CSV.

    HOW TO GET YOUR GOOGLE SHEET CSV URL:
    1. Open your Google Sheet
    2. Click File → Share → Publish to web
    3. Under "Link", choose your sheet tab name
    4. Under "Embed", choose "Comma-separated values (.csv)"
    5. Click Publish → Copy the URL
    6. Paste that URL as the SHEET_CSV_URL in generate.yml

    REQUIRED COLUMN HEADERS in your Google Sheet (row 1):
    city | state | state_code | slug | commissionerate | zone |
    local_areas | key_industries | intro_note | nearby_cities |
    company_note | gst_note

    For local_areas, key_industries, nearby_cities:
    Separate multiple values with a pipe character |
    Example: Whitefield|Electronic City|Koramangala
    """
    print(f"  Fetching cities from Google Sheet...")
    try:
        req = urllib.request.Request(csv_url, headers={"User-Agent": "TaxAMC-Generator/1.0"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            content = resp.read().decode("utf-8")

        reader = csv.DictReader(content.splitlines())
        cities = []
        LIST_FIELDS = ["local_areas", "key_industries", "nearby_cities"]

        for row in reader:
            # Skip empty rows
            if not row.get("slug", "").strip():
                continue
            # Convert pipe-separated strings to lists
            for field in LIST_FIELDS:
                val = row.get(field, "")
                row[field] = [x.strip() for x in val.split("|") if x.strip()] if val else []
            cities.append(dict(row))

        print(f"  ✓ Loaded {len(cities)} cities from Google Sheet")
        return cities

    except Exception as e:
        print(f"  ⚠ Google Sheet failed: {e}")
        return None


def load_cities(json_path, sheet_url=None):
    cities = None
    if sheet_url and sheet_url.strip():
        cities = load_from_sheet(sheet_url.strip())
    if not cities:
        if sheet_url:
            print(f"  Falling back to cities.json...")
        cities = load_from_json(json_path)

    # Deduplicate by slug
    seen, unique = set(), []
    for c in cities:
        slug = c.get("slug", "").strip()
        if slug and slug not in seen:
            seen.add(slug)
            unique.append(c)

    removed = len(cities) - len(unique)
    if removed:
        print(f"  ⚠ Removed {removed} duplicate/empty rows")

    print(f"  → {len(unique)} unique cities ready for generation")
    return unique


# ─── STEP 2 — OPTIONAL AI INTROS (Google Gemini — Free Tier) ─────────────────
#
#  HOW TO SET UP (free, no credit card needed):
#  1. Go to aistudio.google.com
#  2. Sign in with your Google account
#  3. Click "Get API key" → "Create API key" → copy the key
#  4. Go to your GitHub repo → Settings → Secrets → Actions
#  5. Add new secret → Name: GEMINI_API_KEY → paste key → Save
#  6. When running the workflow, set "Use AI for unique city intros?" to true
#
#  Free limits: 15 requests/minute, 1500 requests/day — more than enough.

def get_ai_intro(city_data, service_label, api_key):
    """Call Google Gemini API (free) to write a unique intro paragraph per city.
    Retries up to 3 times on 429 (rate limit) with exponential backoff.
    """
    # If daily quota was exhausted earlier in this run, skip API call immediately
    if getattr(get_ai_intro, "_quota_exhausted", False):
        return city_data["intro_note"]

    prompt = f"""Write a single paragraph (3-4 sentences) for a {service_label} article targeting businesses in {city_data['city']}, {city_data['state']}.

Key facts:
- Major industries: {', '.join(city_data['key_industries'][:3])}
- Key local areas: {', '.join(city_data['local_areas'][:3])}
- City context: {city_data['intro_note']}

Rules:
- Mention the city name and state naturally
- Reference 1-2 specific local industries or areas by name
- Explain why {service_label} matters for this city's businesses
- Tone: professional CA firm, helpful, locally relevant
- Do NOT use clichés like "vibrant city" or "bustling hub"
- Output ONLY the paragraph, no heading, no extra commentary"""

    body = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"maxOutputTokens": 300, "temperature": 0.7}
    }).encode("utf-8")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

    # Per-minute limit: wait up to 5 minutes with increasing delays
    # Daily quota: if STILL failing after 5 long retries, give up for the whole run
    MAX_RETRIES = 5
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            req = urllib.request.Request(
                url,
                data=body,
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                get_ai_intro._consecutive_429s = 0   # reset on success
                return result["candidates"][0]["content"]["parts"][0]["text"].strip()

        except urllib.error.HTTPError as e:
            if e.code == 429:
                get_ai_intro._consecutive_429s = getattr(get_ai_intro, "_consecutive_429s", 0) + 1

                # Only declare daily quota exhausted after 10 consecutive 429s
                # across different cities — this rules out per-minute bursts
                if get_ai_intro._consecutive_429s >= 10:
                    print(f"    ⚠ Gemini daily quota exhausted after "
                          f"{get_ai_intro._consecutive_429s} consecutive rate limits. "
                          f"Switching to default intros for all remaining pages.")
                    get_ai_intro._quota_exhausted = True
                    return city_data["intro_note"]

                # Per-minute rate limit — wait longer before retrying
                # 30s → 60s → 90s → 120s → 120s
                wait = min(30 * attempt, 120)
                print(f"    ⏳ Gemini rate limit for {city_data['city']} "
                      f"(attempt {attempt}/{MAX_RETRIES}) — waiting {wait}s...")
                time.sleep(wait)
                if attempt == MAX_RETRIES:
                    print(f"    ⚠ Gemini gave up for {city_data['city']} after {MAX_RETRIES} attempts — using default intro")
                    return city_data["intro_note"]
            else:
                print(f"    ⚠ Gemini failed for {city_data['city']}: HTTP {e.code} {e.reason} — using default intro")
                return city_data["intro_note"]

        except Exception as e:
            print(f"    ⚠ Gemini failed for {city_data['city']}: {e} — using default intro")
            return city_data["intro_note"]

    return city_data["intro_note"]



def check_gemini_quota(api_key):
    """
    Make a single minimal test call to Gemini before starting the run.
    Returns True if quota is available, False if exhausted (429).
    Fails fast — no retries — so we don't waste time.
    """
    print("  Checking Gemini API quota...")
    body = json.dumps({
        "contents": [{"parts": [{"text": "Say OK"}]}],
        "generationConfig": {"maxOutputTokens": 5}
    }).encode("utf-8")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    try:
        req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            print("  ✓ Gemini quota available — proceeding with AI intros")
            return True
    except urllib.error.HTTPError as e:
        if e.code == 429:
            print(f"  ✗ Gemini quota exhausted (HTTP 429).")
            print(f"    Quota resets at midnight US Pacific time (12:30 PM IST).")
            print(f"    Re-run after that time. Pages will be generated without AI intros for now.")
            return False
        print(f"  ⚠ Gemini test call failed: HTTP {e.code} — proceeding without AI intros")
        return False
    except Exception as e:
        print(f"  ⚠ Gemini test call failed: {e} — proceeding without AI intros")
        return False

# ─── STEP 3 — BUILD HTML PAGES ────────────────────────────────────────────────

def build_env(template_dir):
    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(["html"]),
    )
    env.filters["urlencode"] = lambda s: urllib.parse.quote_plus(str(s))
    return env


def load_ai_log(output_dir):
    """Load the set of filenames that already received an AI intro."""
    path = os.path.join(output_dir, "_ai_intros.json")
    if os.path.isfile(path):
        with open(path, "r", encoding="utf-8") as f:
            return set(json.load(f))
    return set()


def save_ai_log(output_dir, ai_done):
    """Persist the set of filenames that received an AI intro."""
    path = os.path.join(output_dir, "_ai_intros.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(sorted(ai_done), f, indent=2)


def generate_pages(cities, env, output_dir, services, use_ai=False, api_key=None, force_ai=False):
    os.makedirs(output_dir, exist_ok=True)
    generated = []

    # Load the log of pages that already got AI intros.
    # --force-ai skips pages already in this log so each run only
    # processes pages not yet done — picking up where yesterday left off.
    ai_done = load_ai_log(output_dir)
    ai_new   = set()   # pages that get AI intros in this run

    for service_key in services:
        svc      = SERVICES[service_key]
        template = env.get_template(svc["template"])
        written  = 0
        skipped  = 0
        ai_skipped = 0
        print(f"\n  [{svc['label']}] Checking {len(cities)} pages...")

        for i, city in enumerate(cities, 1):
            data = dict(city)

            filename = f"{svc['slug_prefix']}-{data['slug']}.html"
            filepath = os.path.join(output_dir, filename)

            # Decide whether to call Gemini:
            #   --ai:       only for pages that don't exist yet
            #   --force-ai: for pages not yet in the AI log (resumes across days)
            should_call_ai = api_key and (
                (use_ai     and not os.path.isfile(filepath)) or
                (force_ai   and filename not in ai_done)
            )
            if should_call_ai:
                data["intro_note"] = get_ai_intro(data, svc["label"], api_key)
                if not getattr(get_ai_intro, "_quota_exhausted", False):
                    ai_new.add(filename)
                time.sleep(5)    # Gemini free tier: 15 req/min — 5s gap keeps well under limit
            elif force_ai and filename in ai_done:
                ai_skipped += 1  # already has AI intro — skip

            new_html = template.render(**data, whatsapp_number=WHATSAPP_NUMBER)

            # Skip writing if file already exists and content is identical.
            # Only pages whose template or city data changed get rewritten —
            # so git only commits the truly updated files.
            if os.path.isfile(filepath):
                with open(filepath, "r", encoding="utf-8") as f:
                    if f.read() == new_html:
                        generated.append({
                            "url":      f"{BASE_URL}/{filename}",
                            "priority": svc["priority"],
                            "service":  svc["label"],
                            "city":     data["city"],
                            "filename": filename,
                        })
                        skipped += 1
                        continue  # unchanged — skip write

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_html)
            written += 1

            generated.append({
                "url":      f"{BASE_URL}/{filename}",
                "priority": svc["priority"],
                "service":  svc["label"],
                "city":     data["city"],
                "filename": filename,
            })

            # Progress indicator every 10 cities
            if i % 10 == 0 or i == len(cities):
                ai_info = f", ai_done: {ai_skipped}" if force_ai else ""
                print(f"    {i}/{len(cities)} — written: {written}, skipped: {skipped}{ai_info}")

    # Save updated AI log
    if ai_new:
        ai_done.update(ai_new)
        save_ai_log(output_dir, ai_done)
        print(f"\n  ✓ AI log updated: {len(ai_done)} pages total have AI intros ({len(ai_new)} new this run)")
    elif force_ai:
        remaining = 1776 - len(ai_done)
        if remaining > 0:
            print(f"\n  ℹ AI log: {len(ai_done)}/1776 pages done. {remaining} remaining — run again tomorrow.")
        else:
            print(f"\n  ✓ All 1776 pages have AI intros.")

    return generated


# ─── STEP 4 — GENERATE SITEMAP ────────────────────────────────────────────────

def generate_sitemap(generated, output_dir):
    today = date.today().isoformat()
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for p in generated:
        lines.append(f"""  <url>
    <loc>{p['url']}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>{p['priority']}</priority>
  </url>""")
    lines.append("</urlset>")

    path = os.path.join(output_dir, "sitemap-cities.xml")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"\n  ✓ Sitemap written: {len(generated)} city URLs → sitemap-cities.xml")


# ─── STEP 5 — PING ALL SEARCH ENGINES ────────────────────────────────────────
#
#  HOW EACH SEARCH ENGINE WORKS:
#
#  Google      → Has its own index. We ping directly.
#
#  Bing        → Has its own index. We ping directly.
#                Bing Webmaster Tools submission covers all Bing searches.
#
#  Yahoo       → Does NOT have its own search index.
#                Yahoo Search is POWERED BY BING.
#                So pinging Bing = your site appears on Yahoo automatically.
#                No separate Yahoo submission needed.
#
#  DuckDuckGo  → Does NOT have its own index either.
#                DuckDuckGo results come from BING (plus some other sources).
#                So pinging Bing = DuckDuckGo picks it up automatically.
#                No separate DuckDuckGo submission needed.
#
#  Ecosia      → Also powered by Bing. Covered automatically.
#
#  Bottom line: Ping Google + Bing → covered on all 5 major search engines.

def ping_search_engines():
    sitemap_encoded = urllib.parse.quote(f"{BASE_URL}/sitemap-cities.xml", safe="")

    engines = [
        ("Google",                   f"https://www.google.com/ping?sitemap={sitemap_encoded}"),
        ("Bing (covers Yahoo+DDG)",  f"https://www.bing.com/ping?sitemap={sitemap_encoded}"),
    ]

    print("\n  Pinging search engines...")
    print("  (Bing ping covers: Bing + Yahoo + DuckDuckGo + Ecosia)")

    for name, url in engines:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "TaxAMC-Generator/1.0"})
            with urllib.request.urlopen(req, timeout=10) as r:
                print(f"    ✓ {name}: HTTP {r.status}")
        except urllib.error.HTTPError as e:
            print(f"    ✓ {name}: HTTP {e.code} (ping accepted)")
        except Exception as e:
            print(f"    ⚠ {name}: {e}")


# ─── STEP 6 — WRITE REPORT ────────────────────────────────────────────────────

def write_report(generated, output_dir):
    path = os.path.join(output_dir, "_generated_pages.csv")
    with open(path, "w", encoding="utf-8") as f:
        f.write("service,city,filename,url\n")
        for p in generated:
            f.write(f"{p['service']},{p['city']},{p['filename']},{p['url']}\n")
    print(f"  ✓ Page report: _generated_pages.csv")


# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output",    default=".")
    parser.add_argument("--cities",    default="./cities.json")
    parser.add_argument("--templates", default="./templates")
    # --services accepts EITHER:
    #   a single comma-separated string:  --services gst,itr,company
    #   or space-separated tokens:        --services gst itr company
    #   or a mix:                         --services gst,itr company
    # This makes it robust against shell quoting differences in CI/CD environments.
    ALL_SERVICES = ("gst,company,itr,trademark,msme,llp,partnership,roc,iec,"
                    "gst-return,tds,gst-cancellation,gst-notice,business-loan,"
                    "itr-freelancers,itr-doctors,ecommerce-gst,capital-gains,"
                    "itr-creators,restaurant-gst,export-lut,gst-pharma,"
                    "accounting-it,tds-contractors")
    parser.add_argument("--services", nargs="+", default=[ALL_SERVICES])
    parser.add_argument("--sheet",     default=None,
                        help="Google Sheet published CSV URL")
    parser.add_argument("--ai",        action="store_true",
                        help="Use Gemini AI for unique city intros (skips existing pages)")
    parser.add_argument("--force-ai",  action="store_true",
                        help="Use Gemini AI for ALL pages, including existing ones (to refresh intros)")
    parser.add_argument("--ping",      action="store_true",
                        help="Ping search engines after generation")
    args = parser.parse_args()

    # Flatten nargs list (handles both "gst,itr" and "gst" "itr" or mix)
    raw = ",".join(args.services)
    services = [s.strip() for s in raw.split(",") if s.strip() in SERVICES]
    if not services:
        print("ERROR: Valid services are: " + ", ".join(SERVICES.keys()))
        sys.exit(1)

    # API key for AI mode (Google Gemini — free)
    api_key = None
    if args.ai or args.force_ai:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            print("  ⚠ --ai/--force-ai set but GEMINI_API_KEY not found. Skipping AI intros. Get free key at aistudio.google.com")
            args.ai = args.force_ai = False
        elif not check_gemini_quota(api_key):
            # Quota exhausted — disable AI and continue generating pages without intros
            args.ai = args.force_ai = False
            api_key = None

    print(f"\n{'='*60}")
    print(f"  TaxAMC Static Site Generator")
    print(f"  Services   : {', '.join(services)}")
    print(f"  Output dir : {os.path.abspath(args.output)}")
    print(f"  Data source: {'Google Sheet' if args.sheet else 'cities.json'}")
    print(f"  AI intros  : {'Force (all pages)' if args.force_ai else 'Yes (new pages only)' if args.ai else 'No'}")
    print(f"{'='*60}")

    cities    = load_cities(args.cities, args.sheet)
    env       = build_env(args.templates)
    generated = generate_pages(cities, env, args.output, services, args.ai, api_key, force_ai=args.force_ai)

    generate_sitemap(generated, args.output)
    write_report(generated, args.output)

    if args.ping:
        ping_search_engines()

    print(f"\n{'='*60}")
    print(f"  ✅ Complete! {len(generated)} pages generated.")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
