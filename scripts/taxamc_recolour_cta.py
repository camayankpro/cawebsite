#!/usr/bin/env python3
"""
taxamc_recolour_cta.py
======================
Recolours the existing blue call-to-action boxes on every article page to the
TaxAMC black / white / red theme. Only colours change. Wording is never touched.

For each article-*.html file:
  1. Uses the matching .bak file as the source if one exists (the original page),
     otherwise uses the page itself.
  2. Replaces blue / orange colour codes with theme variables (var(--...)).
  3. Checks that the visible text is IDENTICAL before and after. If not, the page
     is skipped and reported.
  4. Writes the recoloured page. The .bak files are never modified.

USAGE (run inside the folder that contains the article-*.html files):
  python taxamc_recolour_cta.py --dry-run     # preview only, nothing is changed
  python taxamc_recolour_cta.py               # apply

Requires Python 3 only (no extra packages).
"""

import glob
import html
import os
import re
import sys

FILE_PATTERN = "article-*.html"

# Colour replacements. Order matters: longer / more specific values first.
COLOUR_MAP = [
    ("linear-gradient(135deg,#283593 0%,#3949AB 100%)",
     "linear-gradient(135deg,var(--primary-dark) 0%,var(--primary) 100%)"),
    ("linear-gradient(135deg, #283593 0%, #3949AB 100%)",
     "linear-gradient(135deg, var(--primary-dark) 0%, var(--primary) 100%)"),
    ("rgba(57,73,171,.18)", "rgba(var(--primary-rgb),.18)"),
    ("rgba(57, 73, 171, 0.18)", "rgba(var(--primary-rgb), 0.18)"),
    ("rgba(255,152,0,.10)", "rgba(var(--accent-rgb),.12)"),
    ("rgba(255,152,0,.28)", "rgba(var(--accent-rgb),.28)"),
    ("#FFD180", "var(--accent)"),
    ("#FF9800", "var(--accent-dark)"),
    ("#3949AB", "var(--primary)"),
    ("#283593", "var(--primary-dark)"),
    ("#25D366", "var(--wa-green)"),
]

# Anything still matching these after recolouring means the page needs a manual look.
OLD_COLOUR_RE = re.compile(
    r"#(?:3949AB|283593|FF9800|FFD180|25D366)|rgba\(255,\s?152|rgba\(57,\s?73", re.I)


def visible_text(markup):
    """Text a visitor reads: tags removed, entities decoded, whitespace normalised."""
    no_tags = re.sub(r"<[^>]+>", " ", markup)
    return re.sub(r"\s+", " ", html.unescape(no_tags)).strip()


def recolour(markup):
    for old, new in COLOUR_MAP:
        markup = markup.replace(old, new)
    return markup


def process(path, dry_run):
    bak = path + ".bak"
    if os.path.exists(bak):
        with open(bak, encoding="utf-8", errors="ignore") as f:
            source = f.read()
        source_name = os.path.basename(bak)
    else:
        with open(path, encoding="utf-8", errors="ignore") as f:
            source = f.read()
        source_name = os.path.basename(path)

    result = recolour(source)

    if visible_text(result) != visible_text(source):
        return "SKIPPED (text would change)", source_name

    remaining = OLD_COLOUR_RE.findall(result)
    status = "OK"
    if remaining:
        status = "OK, but old colours remain: %s" % sorted(set(remaining))

    if not dry_run:
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(result)

    return status, source_name


def main():
    dry_run = "--dry-run" in sys.argv
    files = sorted(glob.glob(FILE_PATTERN))

    if not files:
        print("No files matching %s found. Run this inside the article folder." % FILE_PATTERN)
        return

    print("%s %d article pages\n" % ("DRY RUN - nothing will change:" if dry_run else "Recolouring", len(files)))

    counts = {"ok": 0, "skipped": 0, "warn": 0}
    for path in files:
        status, source_name = process(path, dry_run)
        if status.startswith("SKIPPED"):
            counts["skipped"] += 1
        elif "remain" in status:
            counts["warn"] += 1
        else:
            counts["ok"] += 1
        print("  [%s] %s  (source: %s)" % (status, os.path.basename(path), source_name))

    print("\nDone. OK: %d | Skipped: %d | Needs a look: %d" %
          (counts["ok"], counts["skipped"], counts["warn"]))
    if dry_run:
        print("Run again without --dry-run to apply the changes.")


if __name__ == "__main__":
    main()
