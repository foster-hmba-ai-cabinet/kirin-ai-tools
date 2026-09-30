#!/usr/bin/env python3
"""
stale.py — list tools whose pricing hasn't been re-verified recently.

The quarterly pricing refresh in one command. Reads tools.yaml (the same
loader as build.py) and prints every tool whose `last_verified` date is older
than the threshold, oldest first, with its current pricing string and URL.

After re-checking a tool on the provider's page, update `pricing` if needed,
set `last_verified` to today's date, and run `python scripts/build.py`.

Usage:
    python scripts/stale.py                     # older than 90 days, as of today
    python scripts/stale.py --days 30
    python scripts/stale.py --as-of 2026-12-31
    python scripts/stale.py --markdown          # checklist to paste into an issue/PR

Exit code: 0 if nothing is stale, 1 if anything is (usable as a CI check).
"""

import argparse
import datetime as dt
import signal
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build import load_catalog, validate  # noqa: E402

DEFAULT_DAYS = 90  # keep in sync with STALE_DAYS in index.html


def main() -> None:
    if hasattr(signal, "SIGPIPE"):  # exit quietly when piped into head, etc.
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--days", type=int, default=DEFAULT_DAYS,
                    help=f"staleness threshold in days (default {DEFAULT_DAYS})")
    ap.add_argument("--as-of", type=dt.date.fromisoformat, default=dt.date.today(),
                    metavar="YYYY-MM-DD", help="evaluate as of this date (default today)")
    ap.add_argument("--markdown", action="store_true",
                    help="print a Markdown checklist instead of a table")
    args = ap.parse_args()

    catalog = load_catalog()
    validate(catalog)
    titles = {c["id"]: c["title"] for c in catalog["categories"]}

    stale = []
    for t in catalog["tools"]:
        age = (args.as_of - dt.date.fromisoformat(t["last_verified"])).days
        if age > args.days:
            stale.append((age, t))
    stale.sort(key=lambda x: (-x[0], x[1]["name"].lower()))

    total = len(catalog["tools"])
    header = (f"{len(stale)} of {total} tools not verified in the last "
              f"{args.days} days (as of {args.as_of.isoformat()}).")

    if args.markdown:
        print(f"## Pricing refresh — {args.as_of.isoformat()}\n")
        print(f"_{header}_\n")
        print("For each: check the provider's page, update `pricing` if it "
              "changed, set `last_verified` to the check date, then run "
              "`python scripts/build.py`.\n")
        for age, t in stale:
            print(f"- [ ] **[{t['name']}]({t['url']})** · "
                  f"{titles.get(t['category'], t['category'])} · "
                  f"last verified {t['last_verified']} ({age} days)  \n"
                  f"      Current: {t['pricing']}")
    else:
        print(header)
        if stale:
            w = max(len(t["name"]) for _, t in stale)
            print(f"\n{'TOOL':<{w}}  {'VERIFIED':<10}  {'AGE':>5}  PRICING")
            for age, t in stale:
                print(f"{t['name']:<{w}}  {t['last_verified']:<10}  {age:>4}d  "
                      f"{t['pricing']}")

    sys.exit(1 if stale else 0)


if __name__ == "__main__":
    main()
