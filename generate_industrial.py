#!/usr/bin/env python3
"""
generate_industrial.py — TaxAMC Industrial Area Page Generator
Generates:
  1. One combined CA services page per industrial area (article-ca-{slug}.html)
  2. Four service-specific pages per area:
     - article-gst-{slug}.html       (GST Registration & Returns)
     - article-msme-{slug}.html      (MSME Registration)
     - article-itr-business-{slug}.html  (ITR for Business Owners)
     - article-tds-{slug}.html       (TDS for Contractors)

Usage:
  python generate_industrial.py
  python generate_industrial.py --output .
  python generate_industrial.py --areas industrial_areas.json
"""

import os, json, sys, argparse
from datetime import date
from jinja2 import Environment, FileSystemLoader, select_autoescape
import urllib.parse

BASE_URL        = "https://taxamc.com"
WHATSAPP_NUMBER = "919045222870"

# The 4 service-specific templates to generate per area
SERVICE_PAGES = [
    {
        "key":          "gst",
        "template":     "gst-registration.html",
        "slug_prefix":  "article-gst-registration",
        "label":        "GST Registration & Returns",
        "priority":     "0.8",
    },
    {
        "key":          "msme",
        "template":     "msme-registration.html",
        "slug_prefix":  "article-msme-registration",
        "label":        "MSME Registration",
        "priority":     "0.7",
    },
    {
        "key":          "itr-business-owners",
        "template":     "itr-business-owners.html",
        "slug_prefix":  "article-itr-business-owners",
        "label":        "ITR for Business Owners",
        "priority":     "0.7",
    },
    {
        "key":          "tds-contractors",
        "template":     "tds-contractors.html",
        "slug_prefix":  "article-tds-contractors",
        "label":        "TDS for Contractors",
        "priority":     "0.7",
    },
]


def load_areas(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        areas = json.load(f)
    print(f"  ✓ Loaded {len(areas)} industrial areas")
    return areas


def build_env(template_dir):
    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(["html"]),
    )
    env.filters["urlencode"] = lambda s: urllib.parse.quote_plus(str(s))
    return env


def make_context(area):
    """Build Jinja2 context from an industrial area dict."""
    industries = area.get("key_industries", [])
    nearby    = area.get("nearby_areas", [])
    return {
        "name":             area["name"],
        "slug":             area["slug"],
        "city":             area["city"],
        "district":         area.get("district", area["city"]),
        "state":            area["state"],
        "state_code":       area.get("state_code", "IN"),
        "key_industries":   industries,
        "nearby_areas":     nearby,
        "intro_note":       area.get("intro_note", f"{area['name']} is an important industrial area in {area['city']}, {area['state']}."),
        "gst_note":         area.get("gst_note", f"Businesses in {area['name']} deal with regular inter-state and intra-state transactions requiring timely GST compliance."),
        "company_note":     area.get("company_note", f"Many businesses in {area['name']} operate as proprietorships or partnerships and can benefit from converting to Pvt Ltd for better credibility and access to funding."),
        "local_areas":      nearby if nearby else [area["city"]],
        "nearby_cities":    nearby,
        "whatsapp_number":  WHATSAPP_NUMBER,
        "commissionerate":  area.get("commissionerate", ""),
        "zone":             area.get("zone", ""),
    }


def generate_pages(areas, env, output_dir):
    generated = []
    today = date.today().isoformat()

    for area in areas:
        ctx = make_context(area)
        slug = area["slug"]

        # ── 1. Combined CA services page ──────────────────────────────
        try:
            tmpl = env.get_template("industrial-area.html")
            html = tmpl.render(**ctx)
            fname = f"article-ca-{slug}.html"
            path  = os.path.join(output_dir, fname)
            with open(path, "w", encoding="utf-8") as f:
                f.write(html)
            generated.append({
                "url":      f"{BASE_URL}/{fname}",
                "priority": "0.8",
                "lastmod":  today,
                "label":    f"CA Services — {area['name']}",
            })
        except Exception as e:
            print(f"  ✗ Combined page for {area['name']}: {e}")

        # ── 2. Four service-specific pages ────────────────────────────
        for svc in SERVICE_PAGES:
            try:
                tmpl  = env.get_template(svc["template"])
                html  = tmpl.render(**ctx)
                fname = f"{svc['slug_prefix']}-{slug}.html"
                path  = os.path.join(output_dir, fname)
                with open(path, "w", encoding="utf-8") as f:
                    f.write(html)
                generated.append({
                    "url":      f"{BASE_URL}/{fname}",
                    "priority": svc["priority"],
                    "lastmod":  today,
                    "label":    f"{svc['label']} — {area['name']}",
                })
            except Exception as e:
                print(f"  ✗ {svc['label']} page for {area['name']}: {e}")

    return generated


def generate_sitemap(generated, output_dir):
    today = date.today().isoformat()
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for p in generated:
        lines.append(f"""  <url>
    <loc>{p['url']}</loc>
    <lastmod>{p['lastmod']}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>{p['priority']}</priority>
  </url>""")
    lines.append("</urlset>")

    path = os.path.join(output_dir, "sitemap-industrial.xml")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  ✓ sitemap-industrial.xml written — {len(generated)} URLs")


def write_report(generated, output_dir):
    path = os.path.join(output_dir, "_industrial_pages.csv")
    with open(path, "w", encoding="utf-8") as f:
        f.write("url,priority,label\n")
        for p in generated:
            f.write(f"{p['url']},{p['priority']},{p['label']}\n")
    print(f"  ✓ Report written: _industrial_pages.csv")


def main():
    parser = argparse.ArgumentParser(description="TaxAMC Industrial Area Page Generator")
    parser.add_argument("--output",    default=".",               help="Output directory")
    parser.add_argument("--areas",     default="./industrial_areas.json", help="Industrial areas JSON")
    parser.add_argument("--templates", default="./templates",     help="Templates directory")
    args = parser.parse_args()

    areas = load_areas(args.areas)
    env   = build_env(args.templates)
    os.makedirs(args.output, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"  TaxAMC Industrial Area Page Generator")
    print(f"  Areas      : {len(areas)}")
    print(f"  Pages/area : 5 (1 combined + 4 service pages)")
    print(f"  Total pages: {len(areas) * 5}")
    print(f"  Output dir : {os.path.abspath(args.output)}")
    print(f"{'='*60}")

    generated = generate_pages(areas, env, args.output)
    generate_sitemap(generated, args.output)
    write_report(generated, args.output)

    print(f"\n{'='*60}")
    print(f"  ✅ Complete! {len(generated)} pages generated.")
    print(f"     {len(areas)} combined pages  (article-ca-*.html)")
    print(f"     {len(areas) * 4} service pages   (gst/msme/itr/tds per area)")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
