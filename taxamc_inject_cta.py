"""
taxamc_inject_cta.py
=====================
Injects two CTA blocks into every article-*.html file,
precisely matched to the taxamc.com article HTML structure.

  TOP CTA    -> after the first </p> inside <div class="content">
  BOTTOM CTA -> just before the existing <div class="cta"> block
               (or just before </body> if no .cta block found)

CTA text is dynamically built from each file's <title> tag:
  "Need help with [page title]? Contact TaxAMC CA - serving clients across India."

USAGE:
  1. Copy this script into the ROOT folder of your website
     (same folder containing all your article-*.html files)
  2. Open terminal in VS Code  (Ctrl + `)

  DRY RUN first - preview only, no files changed:
      python taxamc_inject_cta.py --dry-run

  Then apply for real:
      python taxamc_inject_cta.py

SAFE TO RUN:
  - Creates a .bak backup of every file before touching it
  - Skips files that already have the CTA (safe to re-run)
  - Prints a clear log of every file processed
"""

import os
import re
import glob
import shutil
import sys

# ─────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────
WHATSAPP_NUMBER = "919045222870"
PHONE_NUMBER    = "+919045222870"
FILE_PATTERN    = "article-*.html"
MARKER          = "taxamc-cta-injected"   # prevents double-injection
# ─────────────────────────────────────────────────────────


def extract_title(content):
    """Pull readable text from the <title> tag, strip site name suffix."""
    match = re.search(r"<title[^>]*>(.*?)</title>", content, re.IGNORECASE | re.DOTALL)
    if not match:
        return "this service"
    title = match.group(1).strip()
    # Remove everything from the first | or — onwards (site name, tagline etc.)
    title = re.split(r"\s*[|—]\s*", title)[0].strip()
    # Decode common HTML entities
    title = title.replace("&amp;", "&").replace("&#39;", "'").replace("&quot;", '"')
    return title if title else "this service"


def build_ctas(title):
    """Return (top_cta_html, bottom_cta_html) personalised to the page title."""

    wa_msg_top    = "Hello%21+I+need+help+with+" + "+".join(title.split()) + ".+I+found+TaxAMC+online."
    wa_msg_bottom = "Hello%21+I+read+your+article+on+TaxAMC+and+need+assistance."

    # All styles are inline so they never clash with common.css
    BLOCK = (
        "background:linear-gradient(135deg,#283593 0%,#3949AB 100%);"
        "border-radius:12px;padding:22px 26px;margin:32px 0;color:#fff;"
        "font-family:'Poppins',sans-serif;display:flex;align-items:center;"
        "gap:18px;flex-wrap:wrap;box-shadow:0 8px 28px rgba(57,73,171,.18);"
        "position:relative;overflow:hidden;"
    )
    CIRCLE = (
        "position:absolute;top:-36px;right:-36px;width:120px;height:120px;"
        "background:rgba(255,152,0,.10);border-radius:50%;pointer-events:none;"
    )
    CONTENT = "flex:1;min-width:180px;"
    LABEL   = (
        "font-size:.68rem;font-weight:700;letter-spacing:.10em;"
        "text-transform:uppercase;color:#FFD180;margin:0 0 4px;"
        "font-family:'Poppins',sans-serif;"
    )
    HEAD = (
        "font-size:.98rem;font-weight:700;color:#fff;margin:0 0 5px;"
        "line-height:1.3;font-family:'Poppins',sans-serif;"
    )
    SUB = (
        "font-size:.78rem;color:rgba(255,255,255,.82);margin:0;"
        "line-height:1.5;font-family:'Poppins',sans-serif;"
    )
    BTNS = "display:flex;gap:10px;flex-wrap:wrap;flex-shrink:0;"
    BTN_WA = (
        "display:inline-flex;align-items:center;gap:7px;"
        "background:#25D366;color:#fff !important;font-family:'Poppins',sans-serif;"
        "font-size:.82rem;font-weight:700;padding:10px 18px;border-radius:8px;"
        "text-decoration:none !important;white-space:nowrap;"
        "box-shadow:0 4px 12px rgba(37,211,102,.28);"
    )
    BTN_CALL = (
        "display:inline-flex;align-items:center;gap:7px;"
        "background:#FF9800;color:#fff !important;font-family:'Poppins',sans-serif;"
        "font-size:.82rem;font-weight:700;padding:10px 18px;border-radius:8px;"
        "text-decoration:none !important;white-space:nowrap;"
        "box-shadow:0 4px 12px rgba(255,152,0,.28);"
    )
    WA_SVG = (
        '<svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
        '<path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15'
        '-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475'
        '-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52'
        '.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207'
        '-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372'
        '-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 '
        '5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118'
        '.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413'
        '-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214'
        '-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 '
        '9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994'
        'c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0'
        'C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654'
        'a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893'
        'a11.821 11.821 0 00-3.48-8.413z"/></svg>'
    )

    top_cta = f"""
<!-- {MARKER} -->
<div style="{BLOCK}">
  <div style="{CIRCLE}"></div>
  <div style="{CONTENT}">
    <p style="{LABEL}">Free Consultation Available</p>
    <h3 style="{HEAD}">Need help with {title}?</h3>
    <p style="{SUB}">Contact TaxAMC CA &mdash; serving clients across India. Quick response guaranteed.</p>
  </div>
  <div style="{BTNS}">
    <a href="https://wa.me/{WHATSAPP_NUMBER}?text={wa_msg_top}" target="_blank" rel="noopener" style="{BTN_WA}">
      {WA_SVG}&nbsp;WhatsApp Us
    </a>
    <a href="tel:{PHONE_NUMBER}" style="{BTN_CALL}">&#128222;&nbsp;Call Now</a>
  </div>
</div>
"""

    bottom_cta = f"""
<div style="{BLOCK}">
  <div style="{CIRCLE}"></div>
  <div style="{CONTENT}">
    <p style="{LABEL}">Agarwal Mayank &amp; Company</p>
    <h3 style="{HEAD}">Ready to get started? We&rsquo;ll handle everything.</h3>
    <p style="{SUB}">Expert CA services &mdash; GST, ITR, Audit, Trademark &amp; more.<br>Based in Hapur, UP &bull; Available online across India.</p>
  </div>
  <div style="{BTNS}">
    <a href="https://wa.me/{WHATSAPP_NUMBER}?text={wa_msg_bottom}" target="_blank" rel="noopener" style="{BTN_WA}">
      {WA_SVG}&nbsp;WhatsApp Us
    </a>
    <a href="tel:{PHONE_NUMBER}" style="{BTN_CALL}">&#128222;&nbsp;Call Now</a>
  </div>
</div>
"""
    return top_cta, bottom_cta


def inject_file(filepath, dry_run=False):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Skip if already injected
    if MARKER in content:
        print(f"  [SKIP]     {os.path.basename(filepath)}  — already injected")
        return False

    title = extract_title(content)
    top_cta, bottom_cta = build_ctas(title)

    if dry_run:
        print(f"  [DRY RUN]  {os.path.basename(filepath)}")
        print(f"             Title: \"{title}\"")
        return True

    modified = content

    # ── TOP CTA: after first </p> inside <div class="content"> ──
    content_div = modified.find('<div class="content">')
    search_from = content_div if content_div != -1 else modified.lower().find("<body")
    first_p_end = modified.find("</p>", search_from if search_from != -1 else 0)

    if first_p_end != -1:
        pos = first_p_end + len("</p>")
        modified = modified[:pos] + top_cta + modified[pos:]
    else:
        # Fallback: right after opening <body> tag
        body_pos = modified.lower().find("<body")
        body_end = modified.find(">", body_pos) + 1 if body_pos != -1 else 0
        modified = modified[:body_end] + top_cta + modified[body_end:]

    # ── BOTTOM CTA: just before existing <div class="cta"> ──
    cta_div = modified.find('<div class="cta">')
    if cta_div != -1:
        modified = modified[:cta_div] + bottom_cta + "\n" + modified[cta_div:]
    else:
        # Fallback: just before </body>
        body_close = modified.lower().rfind("</body>")
        if body_close != -1:
            modified = modified[:body_close] + bottom_cta + "\n" + modified[body_close:]
        else:
            modified += "\n" + bottom_cta

    # Backup original then write
    shutil.copy2(filepath, filepath + ".bak")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(modified)

    print(f"  [DONE]     {os.path.basename(filepath)}")
    print(f"             Title: \"{title}\"")
    return True


def main():
    dry_run = "--dry-run" in sys.argv

    if dry_run:
        print("\n🔍 DRY RUN — no files will be changed. Just a preview.\n")
    else:
        print("\n🚀 TaxAMC CTA Injector — starting...\n")

    files = sorted(glob.glob(FILE_PATTERN))

    if not files:
        print(f"⚠️  No files found matching pattern: {FILE_PATTERN}")
        print("   Make sure this script is in the SAME FOLDER as your article files.")
        print("   e.g. if articles are in a subfolder, change FILE_PATTERN at the top.")
        return

    print(f"📂 Found {len(files)} article files\n")

    done = skipped = 0
    for fp in files:
        if inject_file(fp, dry_run=dry_run):
            done += 1
        else:
            skipped += 1

    print(f"\n{'─' * 60}")
    if dry_run:
        print(f"✅ Dry run complete.")
        print(f"   {done} files would be updated  |  {skipped} already have CTA (would skip)")
        print(f"\n   Happy with the preview? Run without --dry-run to apply.\n")
    else:
        print(f"✅ Done!   {done} files updated  |  {skipped} skipped (already had CTA)")
        print(f"💾 Originals backed up as .bak files next to each article.")
        print(f"\n👉 Next steps:")
        print(f"   1. Open 2-3 articles in your browser and check the CTA looks correct")
        print(f"   2. git add . && git commit -m 'Add CTA blocks to all articles'")
        print(f"   3. git push  — to go live on GitHub Pages\n")


if __name__ == "__main__":
    main()
