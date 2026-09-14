#!/usr/bin/env python3
"""
Build script for the Cyberia IT Solutions website.

What it does:
  Reads business details (name, phone, email, address, stats, etc.) from
  site_config.json, and fills in the {{TOKEN}} placeholders found in every
  templates/*.html file, writing the finished, ready-to-publish pages into
  docs/. style.css is copied alongside them unchanged.

Why templates/ + docs/ are separate:
  templates/*.html is your source content — edit headings, paragraphs,
  service lists, etc. directly in those files (in VS Code or any editor).
  Just don't touch the {{TOKEN}} markers, since those get replaced automatically.
  site_config.json is your one place to update contact details and stats.
  docs/ is generated output — never edit it by hand, since re-running this
  script overwrites it completely. It's named "docs" (not "build") on purpose:
  GitHub Pages can serve a site straight out of a folder with that exact name,
  with no extra setup — see README.md.

Usage:
    python3 build_site.py            # render templates -> docs/
    python3 build_site.py --check    # just report missing/unused tokens, write nothing
"""
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TEMPLATES_DIR = ROOT / "templates"
BUILD_DIR = ROOT / "docs"
CONFIG_PATH = ROOT / "site_config.json"
CSS_FILE = ROOT / "style.css"
IMAGES_DIR = ROOT / "images"

TOKEN_RE = re.compile(r"\{\{([A-Z0-9_]+)\}\}")


def load_config():
    if not CONFIG_PATH.exists():
        sys.exit(f"Missing {CONFIG_PATH.name} next to this script.")
    with open(CONFIG_PATH, encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            sys.exit(f"{CONFIG_PATH.name} is not valid JSON: {e}")


def render(text, config, filename, warnings):
    def repl(match):
        key = match.group(1)
        if key not in config:
            warnings.append(f"{filename}: no value set for {{{{{key}}}}}")
            return match.group(0)
        return str(config[key])
    return TOKEN_RE.sub(repl, text)


def main():
    check_only = "--check" in sys.argv
    config = load_config()

    if not TEMPLATES_DIR.exists():
        sys.exit("Missing templates/ folder next to this script.")

    html_files = sorted(TEMPLATES_DIR.glob("*.html"))
    if not html_files:
        sys.exit("No .html files found in templates/.")

    warnings = []
    used_keys = set()
    rendered = {}

    for path in html_files:
        text = path.read_text(encoding="utf-8")
        used_keys.update(m.group(1) for m in TOKEN_RE.finditer(text))
        rendered[path.name] = render(text, config, path.name, warnings)

    unused_keys = sorted(set(config.keys()) - used_keys)
    if unused_keys:
        print("Note: unused config keys (not referenced by any template):", ", ".join(unused_keys))

    if warnings:
        print("Missing config values:")
        for w in warnings:
            print("  -", w)

    if check_only:
        print("All good — run without --check to build." if not warnings else "Fix the missing values above, then build.")
        return

    BUILD_DIR.mkdir(exist_ok=True)
    for name, text in rendered.items():
        (BUILD_DIR / name).write_text(text, encoding="utf-8")

    if CSS_FILE.exists():
        shutil.copy(CSS_FILE, BUILD_DIR / CSS_FILE.name)
    else:
        print(f"Warning: {CSS_FILE.name} not found — pages in {BUILD_DIR.name}/ will be unstyled.")

    if IMAGES_DIR.exists():
        dest = BUILD_DIR / "images"
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(IMAGES_DIR, dest)
    else:
        print(f"Note: no images/ folder found — pages will show the placeholder image boxes until you add one.")

    print(f"Built {len(rendered)} page(s) into {BUILD_DIR}/")
    if warnings:
        print("(built anyway — fix the missing values above and re-run to clean them up)")


if __name__ == "__main__":
    main()
