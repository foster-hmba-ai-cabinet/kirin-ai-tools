#!/usr/bin/env python3
"""
build.py — regenerate the website and the README from tools.yaml.

`tools.yaml` is the single source of truth. This script:
  1. Injects the tool data (as JSON) into index.html  -> the live website.
  2. Renders the Markdown tables in README.md          -> the repo's docs page.

Everything outside the injected regions is hand-written and left untouched.

Usage:
    pip install pyyaml      # one time
    python scripts/build.py
"""

import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("Missing dependency. Run:  pip install pyyaml")

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "tools.yaml"
INDEX = ROOT / "index.html"
README = ROOT / "README.md"
TOOLS_JSON = ROOT / "tools.json"

R_START, R_END = "<!-- TOOLS:START -->", "<!-- TOOLS:END -->"
COST_BADGE = {
    "Free": "🟢 Free",
    "Freemium": "🟡 Freemium",
    "Paid": "🔴 Paid",
    "Free for students": "🎓 Free for students",
    "Institutional": "🏛️ Institutional",
}


CONTEXTS = {"education", "professional", "personal"}


def validate(catalog: dict) -> None:
    cat_ids = {c["id"] for c in catalog["categories"]}
    req = {"name", "url", "category", "what", "best_for", "pricing",
           "cost_tier", "difficulty", "contexts", "added"}
    for t in catalog["tools"]:
        missing = req - t.keys()
        if missing:
            sys.exit(f"Tool '{t.get('name','?')}' missing fields: {missing}")
        if t["category"] not in cat_ids:
            sys.exit(f"Tool '{t['name']}' has unknown category '{t['category']}'")
        if not str(t["url"]).startswith("http"):
            sys.exit(f"Tool '{t['name']}' url must start with http")
        bad_ctx = set(t["contexts"]) - CONTEXTS
        if bad_ctx:
            sys.exit(f"Tool '{t['name']}' has invalid contexts {bad_ctx}; "
                     f"allowed: {CONTEXTS}")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(t["added"])):
            sys.exit(f"Tool '{t['name']}' 'added' must be YYYY-MM-DD, "
                     f"got '{t['added']}'")


def build_site(catalog: dict) -> None:
    payload = {
        "meta": catalog.get("meta", {}),
        "categories": catalog["categories"],
        "tools": catalog["tools"],
    }
    # Machine-readable export for KIRIN ingestion + the n8n monthly digest.
    TOOLS_JSON.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    blob = json.dumps(payload, ensure_ascii=False)
    html = INDEX.read_text(encoding="utf-8")
    pattern = re.compile(
        r'(<script id="tools-data" type="application/json">).*?(</script>)',
        re.DOTALL,
    )
    if not pattern.search(html):
        sys.exit('Could not find <script id="tools-data"> block in index.html')
    new = pattern.sub(lambda m: m.group(1) + blob + m.group(2), html, count=1)
    INDEX.write_text(new, encoding="utf-8")


def esc(text: str) -> str:
    return (text or "").strip().replace("|", "\\|")


def build_readme(catalog: dict) -> None:
    cats = sorted(catalog["categories"], key=lambda c: c["order"])
    by_cat = {}
    for t in catalog["tools"]:
        by_cat.setdefault(t["category"], []).append(t)

    lines = [
        f"_Tool count: **{len(catalog['tools'])}** across **{len(cats)}** "
        f"categories. Pricing accurate as of "
        f"**{catalog['meta']['pricing_as_of']}** — always verify on the "
        "provider's page._",
        "",
    ]
    for c in cats:
        lines += [f"### {c['title']}", "", c["blurb"].strip(), ""]
        rows = by_cat.get(c["id"], [])
        if not rows:
            lines += ["_No tools listed yet — contributions welcome._", ""]
            continue
        lines += ["| Tool | What it does | Best for | Cost | Level |",
                  "|------|--------------|----------|------|-------|"]
        for t in rows:
            best = esc(t["best_for"])
            if t.get("notes"):
                best += f" <br>_⚠ {esc(t['notes'])}_"
            badge = COST_BADGE.get(t["cost_tier"], esc(t["cost_tier"]))
            lines.append(
                f"| **[{esc(t['name'])}]({t['url']})** | {esc(t['what'])} "
                f"| {best} | {badge}<br><sub>{esc(t['pricing'])}</sub> "
                f"| {esc(t['difficulty'])} |"
            )
        lines.append("")

    block = "\n".join(lines).rstrip() + "\n"
    text = README.read_text(encoding="utf-8")
    if R_START not in text or R_END not in text:
        sys.exit(f"Markers {R_START} / {R_END} not found in README.md")
    pre, post = text.split(R_START)[0], text.split(R_END)[1]
    README.write_text(f"{pre}{R_START}\n\n{block}\n{R_END}{post}", encoding="utf-8")


def main() -> None:
    catalog = yaml.safe_load(CATALOG.read_text(encoding="utf-8"))
    validate(catalog)
    build_site(catalog)
    build_readme(catalog)
    print(f"Built: index.html + README.md + tools.json "
          f"({len(catalog['tools'])} tools, {len(catalog['categories'])} categories).")


if __name__ == "__main__":
    main()
