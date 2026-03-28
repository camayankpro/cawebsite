#!/usr/bin/env python3
"""
generate_industry.py — TaxAMC Industry-Specific Page Generator
Generates one page per industry: article-industry-{slug}.html

Usage:
  python generate_industry.py
  python generate_industry.py --output . --industries industries.json
"""

import os, json, argparse
from datetime import date
from jinja2 import Environment, FileSystemLoader, select_autoescape
import urllib.parse

BASE_URL = "https://taxamc.com"


def load_industries(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"  ✓ Loaded {len(data)} industries")
    return data


def build_env(template_dir):
    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(["html"]),
    )
    env.filters["urlencode"] = lambda s: urllib.parse.quote_plus(str(s))
    return env


def generate_pages(industries, env, output_dir):
    generated = []
    today = date.today().isoformat()
    tmpl = env.get_template("industry.html")

    for ind in industries:
        slug = ind["slug"]
        try:
            html = tmpl.render(**ind)
            fname = f"article-industry-{slug}.html"
            path  = os.path.join(output_dir, fname)
            with open(path, "w", encoding="utf-8") as f:
                f.write(html)
            generated.append({
                "url":      f"{BASE_URL}/{fname}",
                "priority": "0.7",
                "lastmod":  today,
                "label":    ind["name"],
            })
            print(f"  ✓ {fname}")
        except Exception as e:
            print(f"  ✗ {ind['name']}: {e}")

    return generated


def generate_sitemap(generated, output_dir):
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
    path = os.path.join(output_dir, "sitemap-industry.xml")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"\n  ✓ sitemap-industry.xml — {len(generated)} URLs")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output",     default=".")
    parser.add_argument("--industries", default="./industries.json")
    parser.add_argument("--templates",  default="./templates")
    args = parser.parse_args()

    industries = load_industries(args.industries)
    env = build_env(args.templates)
    os.makedirs(args.output, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"  TaxAMC Industry Page Generator")
    print(f"  Industries : {len(industries)}")
    print(f"  Output dir : {os.path.abspath(args.output)}")
    print(f"{'='*60}")

    generated = generate_pages(industries, env, args.output)
    generate_sitemap(generated, args.output)

    print(f"\n{'='*60}")
    print(f"  ✅ Complete! {len(generated)} industry pages generated.")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
