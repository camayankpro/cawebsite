"""
TaxAMC Page Test Suite
======================
Two modes:

  LOCAL  — validates generated HTML files on disk (run before pushing)
  LIVE   — checks live URLs on taxamc.com return 200 and have correct content

Usage:
  python test_pages.py                        # local test on current directory
  python test_pages.py --dir ./               # local test, specify folder
  python test_pages.py --live                 # test live URLs from sitemap
  python test_pages.py --live --sample 50     # test random 50 live URLs
  python test_pages.py --live --url https://taxamc.com/article-gst-registration-mumbai.html
"""

import os, re, sys, json, time, random, argparse, urllib.request, urllib.error
from pathlib import Path

# ── ANSI colours ─────────────────────────────────────────────────────────────
G = "\033[92m"; R = "\033[91m"; Y = "\033[93m"; B = "\033[94m"; X = "\033[0m"
OK  = f"{G}✓{X}"
ERR = f"{R}✗{X}"
WRN = f"{Y}⚠{X}"

# ── What every valid article page must contain ────────────────────────────────
REQUIRED_PATTERNS = [
    (r"<title>.+</title>",                          "Has <title> tag"),
    (r'<meta name="description" content=".{50,}"',  "Meta description ≥50 chars"),
    (r'<link rel="canonical"',                      "Has canonical URL"),
    (r'wa\.me/919045222870',                        "Has WhatsApp CTA link"),
    (r'application/ld\+json',                       "Has JSON-LD schema"),
    (r'FAQPage',                                    "Has FAQPage schema"),
    (r'<h1[^>]*>.+</h1>',                           "Has H1 tag"),
    (r'<h2[^>]*>.+</h2>',                           "Has at least one H2"),
    (r'common\.css',                                "Links common.css"),
    (r'common\.js',                                 "Loads common.js"),
]

FORBIDDEN_PATTERNS = [
    (r'\{\{[^}]+\}\}',   "Unrendered Jinja {{ }} variable"),
    (r'\{%[^%]+%\}',     "Unrendered Jinja {% %} tag"),
    (r'<title>\s*</title>', "Empty <title> tag"),
    (r'undefined',       "Literal 'undefined' in output"),
]

# ── LOCAL TEST ────────────────────────────────────────────────────────────────

def check_file(filepath):
    """Run all checks on a single HTML file. Returns (errors, warnings)."""
    errors = []
    warnings = []

    try:
        with open(filepath, encoding="utf-8") as f:
            html = f.read()
    except Exception as e:
        return [f"Cannot read file: {e}"], []

    size_kb = len(html) / 1024

    # Size check
    if size_kb < 10:
        errors.append(f"Suspiciously small: {size_kb:.1f} KB (expected >10 KB)")
    elif size_kb > 300:
        warnings.append(f"Very large: {size_kb:.1f} KB")

    # Required patterns
    for pattern, label in REQUIRED_PATTERNS:
        if not re.search(pattern, html, re.IGNORECASE | re.DOTALL):
            errors.append(f"MISSING: {label}")

    # Forbidden patterns
    for pattern, label in FORBIDDEN_PATTERNS:
        match = re.search(pattern, html)
        if match:
            errors.append(f"FOUND: {label}  →  '{match.group()[:60]}'")

    # City name check — extract expected city from filename
    fn = Path(filepath).stem  # e.g. article-gst-registration-mumbai
    parts = fn.split("-")
    if parts:
        city_slug = parts[-1]  # last part is city slug
        # Convert slug back to rough city name for check
        city_name = city_slug.replace("-", " ").title()
        if city_slug not in html.lower():
            warnings.append(f"City slug '{city_slug}' not found in page content")

    # WhatsApp city parameter check
    if "919045222870" in html and city_slug not in html.lower().replace(" ", "-"):
        pass  # ok if already checked above

    # H2 count — should have at least 5
    h2_count = len(re.findall(r'<h2[^>]*>', html))
    if h2_count < 5:
        warnings.append(f"Only {h2_count} H2 sections (expected ≥5)")

    # CTA count — WhatsApp link appearances
    cta_count = html.count("wa.me/919045222870")
    if cta_count < 3:
        warnings.append(f"Only {cta_count} WhatsApp CTAs (expected ≥3)")

    return errors, warnings


def run_local_tests(directory):
    files = sorted(Path(directory).glob("article-*.html"))
    if not files:
        print(f"{ERR} No article-*.html files found in: {directory}")
        sys.exit(1)

    print(f"\n{B}TaxAMC Local Page Tests{X}")
    print(f"Directory : {os.path.abspath(directory)}")
    print(f"Files     : {len(files)} article pages\n")

    total_errors   = 0
    total_warnings = 0
    failed_files   = []

    for i, fp in enumerate(files, 1):
        errors, warnings = check_file(fp)
        total_errors   += len(errors)
        total_warnings += len(warnings)

        if errors:
            failed_files.append((fp.name, errors, warnings))
            status = ERR
        elif warnings:
            status = WRN
        else:
            status = OK

        # Print failures immediately; suppress clean passes for brevity
        if errors or warnings:
            print(f"  {status} {fp.name}")
            for e in errors:
                print(f"       {R}{e}{X}")
            for w in warnings:
                print(f"       {Y}{w}{X}")

        # Progress every 100 files
        if i % 100 == 0:
            print(f"  ... checked {i}/{len(files)} ...")

    # Summary
    print(f"\n{'='*60}")
    clean = len(files) - len(failed_files)
    print(f"  Total files  : {len(files)}")
    print(f"  {OK} Clean        : {clean}")
    print(f"  {ERR} With errors  : {len(failed_files)}")
    print(f"  {WRN} With warnings: {total_warnings}")
    print(f"  Total errors : {total_errors}")

    if not failed_files:
        print(f"\n{G}All pages passed local validation.{X}\n")
    else:
        print(f"\n{R}Fix the errors above before deploying.{X}\n")

    return len(failed_files) == 0


# ── LIVE TEST ─────────────────────────────────────────────────────────────────

def check_live_url(url, timeout=10):
    """Fetch a live URL and run content checks. Returns (status_code, errors, response_time_ms)."""
    errors = []
    t0 = time.time()
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "TaxAMC-TestBot/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            status = resp.status
            html   = resp.read().decode("utf-8", errors="replace")
            ms     = int((time.time() - t0) * 1000)
    except urllib.error.HTTPError as e:
        return e.code, [f"HTTP {e.code}: {e.reason}"], 0
    except urllib.error.URLError as e:
        return 0, [f"Connection error: {e.reason}"], 0
    except Exception as e:
        return 0, [f"Error: {e}"], 0

    # Content checks on live page
    for pattern, label in REQUIRED_PATTERNS:
        if not re.search(pattern, html, re.IGNORECASE | re.DOTALL):
            errors.append(f"MISSING: {label}")

    for pattern, label in FORBIDDEN_PATTERNS:
        match = re.search(pattern, html)
        if match:
            errors.append(f"FOUND: {label}")

    if ms > 3000:
        errors.append(f"Slow response: {ms}ms (>3s)")

    return status, errors, ms


def load_urls_from_sitemap(sitemap_path):
    """Extract URLs from sitemap-cities.xml."""
    if not os.path.exists(sitemap_path):
        return []
    with open(sitemap_path) as f:
        content = f.read()
    return re.findall(r'<loc>(https://taxamc\.com/article-[^<]+)</loc>', content)


def run_live_tests(urls, sample=None):
    if sample and sample < len(urls):
        urls = random.sample(urls, sample)
        print(f"  (testing random sample of {sample} URLs)")

    print(f"\n{B}TaxAMC Live URL Tests{X}")
    print(f"URLs to test: {len(urls)}\n")

    passed = failed = 0
    slow   = []
    errors_by_url = []

    for i, url in enumerate(urls, 1):
        status, errors, ms = check_live_url(url)

        if status == 200 and not errors:
            passed += 1
            icon = OK
        else:
            failed += 1
            icon = ERR
            errors_by_url.append((url, status, errors, ms))

        # Print every URL result
        speed = f"{ms}ms" if ms else "—"
        if errors:
            print(f"  {icon} [{status}] {speed:>6}  {url}")
            for e in errors:
                print(f"             {R}{e}{X}")
        else:
            # Only print every 10th clean result to avoid wall of text
            if i % 10 == 0:
                print(f"  {OK} [{status}] {speed:>6}  ... ({i}/{len(urls)} checked)")

        time.sleep(0.3)  # polite rate limiting

    print(f"\n{'='*60}")
    print(f"  {OK} Passed : {passed}")
    print(f"  {ERR} Failed : {failed}")

    if failed == 0:
        print(f"\n{G}All live URLs passed.{X}\n")
    else:
        print(f"\n{R}{failed} URLs failed. Fix before submitting sitemap to Google.{X}\n")

    return failed == 0


# ── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="TaxAMC page test suite")
    parser.add_argument("--dir",    default=".",
                        help="Directory containing generated HTML files (default: current dir)")
    parser.add_argument("--live",   action="store_true",
                        help="Test live URLs on taxamc.com instead of local files")
    parser.add_argument("--sample", type=int, default=None,
                        help="For --live: test a random sample of N URLs")
    parser.add_argument("--url",    default=None,
                        help="For --live: test a single specific URL")
    parser.add_argument("--sitemap", default="sitemap-cities.xml",
                        help="Sitemap file to read URLs from (default: sitemap-cities.xml)")
    args = parser.parse_args()

    if args.live:
        if args.url:
            urls = [args.url]
        else:
            urls = load_urls_from_sitemap(args.sitemap)
            if not urls:
                # Fallback: scan local HTML files and build URLs
                files = sorted(Path(args.dir).glob("article-*.html"))
                urls  = [f"https://taxamc.com/{f.name}" for f in files]
            if not urls:
                print(f"{ERR} No URLs found. Run generator first or provide --url.")
                sys.exit(1)
        ok = run_live_tests(urls, sample=args.sample)
    else:
        ok = run_local_tests(args.dir)

    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
