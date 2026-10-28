"""Checks the site before it is published. Exits 1 on any problem."""
import glob
import os
import re
import sys

ROOT = "site"
LANGS = {"es": ["trozo", "trabajo", "trabajador", "vigilante"],
         "pt-br": ["trabalho", "trabalhador", "vigia "]}
errors = []

for path in glob.glob(f"{ROOT}/**/*.html", recursive=True):
    text = open(path, encoding="utf-8").read()
    rel = os.path.relpath(path, ROOT)
    lang = rel.split(os.sep)[0] if rel.split(os.sep)[0] in LANGS else None
    for tag in re.findall(r"<(?:a|link|script|img)\b[^>]*>", text):
        m = re.search(r'(?:href|src)="([^"]+)"', tag)
        if not m or m.group(1).startswith(("http", "#", "mailto:")):
            continue
        target = m.group(1).split("#")[0]
        resolved = os.path.normpath(os.path.join(os.path.dirname(path), target))
        if not os.path.exists(resolved):
            errors.append(f"{rel}: broken link {target}")
            continue
        # a page in es/ or pt-br/ must link to pages of its own language,
        # except the language switcher and shared assets
        if lang and resolved.endswith(".html") and "hreflang" not in tag:
            if not os.path.relpath(resolved, ROOT).startswith(lang + os.sep):
                errors.append(f"{rel}: link {target} leaves the {lang} pages")
    if lang:
        low = text.lower()
        for word in LANGS[lang]:
            if word in low:
                errors.append(f"{rel}: banned term '{word}'")

# the install commands must be identical in every home page and deck
INSTALL = "git clone https://github.com/rdorta27/knowman"
for path in glob.glob(f"{ROOT}/**/index.html", recursive=True) + glob.glob(f"{ROOT}/**/deck.html", recursive=True):
    if INSTALL not in open(path, encoding="utf-8").read():
        errors.append(f"{path}: install command missing or changed")

# the eval figure must match on every home page and deck
for path in glob.glob(f"{ROOT}/**/index.html", recursive=True) + glob.glob(f"{ROOT}/**/deck.html", recursive=True):
    if "25/25" not in open(path, encoding="utf-8").read():
        errors.append(f"{path}: eval figure 25/25 missing or changed")

# every absolute site URL in the head metadata must point at a file in site/
SITE = "https://rdorta27.github.io/knowman-site/"
for path in glob.glob(f"{ROOT}/**/*.html", recursive=True):
    for url in re.findall(r'(?:content|href)="' + re.escape(SITE) + r'([^"#]*)"', open(path, encoding="utf-8").read()):
        if not os.path.exists(os.path.join(ROOT, url or "index.html")):
            errors.append(f"{path}: {SITE}{url} has no file in {ROOT}/")

print("\n".join(errors) or "site ok")
sys.exit(1 if errors else 0)
