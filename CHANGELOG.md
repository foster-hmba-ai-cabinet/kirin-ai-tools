# Changelog

All notable changes to the KIRIN AI Tools Repository are documented here: pricing
corrections, tool renames, copy changes, and tooling. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/). The guide isn't versioned,
so entries are grouped by date, newest first.

Every change to `tools.yaml` gets an entry here, new tools included. (The site's
**Changelog** section separately lists new tools automatically from each tool's
`added` date.)

## 2026-10-31

### Added
- **Purple (UW):** UW's own generative AI assistant, free for UW students, faculty and staff, and available to students since 2026-07-15. It runs in a University-managed environment, data entered isn't used to train public models, and inactive chats are deleted after 180 days. Use is limited to university-related purposes, and the license is tied to your NetID. Listed first under General-Purpose Assistants. Suggested by a classmate.
- **Granola:** AI meeting notes on desktop and mobile. Free Basic plan with 30 days of meeting history (Slack is its only integration); Business $14/user/mo; Enterprise $35/user/mo. Listed under Meetings & Note-Taking. Suggested by a classmate.

### Changed
- **Near-zero-cost stack** (README and site hero): now leads with Purple as the default for anything school-related, since it's free, UW-run, and keeps coursework inside UW's environment rather than a consumer free tier. Gemini Notebook stays as the free reading tool. The consumer free tiers (ChatGPT, Claude, Gemini) are now for use outside university work, because Purple is limited to university-related purposes. The Gemini AI Pro and GitHub Copilot Student offers remain the next step.
- **Granola:** the note now says recording others requires their consent, so tell participants before you record. This matches Fireflies.ai's note and Ground Rule 5 on recording people.
- **Start here, step 1** (README and site): the daily driver is now **Purple (UW)** for university work, with the free tier of ChatGPT, Claude, or Gemini for anything outside it. The README's step previously suggested only ChatGPT, Claude, or Gemini, which contradicted the near-zero-cost stack copy that now leads with Purple; the site's step named no tool and now matches. Steps 2 and 3 are unchanged.
- **Granola:** the note now says the free tier limits access to the last 30 days of meetings rather than deleting older ones, and paid plans unlock older data. It also flags a classmate's report that signup required a Microsoft 365 account rather than a personal Gmail (the app asks for calendar access). That's a reported experience; Granola's pricing page doesn't state the restriction. Pricing and `last_verified` are unchanged.

## 2026-10-19

### Fixed
- **Governance guide link without JavaScript:** the site's link to [AI Governance: Where to Start](docs/ai-governance.md) was rendered only by the page script, so visitors without JavaScript never saw it. `build.py` now also writes a static link into the Ground Rules section of `index.html`, from the Governance category's `guide` in `tools.yaml`, and fails if the placeholder is missing. The script-rendered link under the Governance category is unchanged.
- **Dashes in `stale.py` output:** the `--markdown` heading and the `--help` description used em dashes, which ended up in pasted issues and PRs. Both now use a colon. `build.py`'s dash check now also runs `stale.py` (Markdown, table, and `--help`, listing every tool) and fails on any em or en dash in its output, or if `stale.py` itself fails.

### Added
- **AI Governance: Where to Start** ([`docs/ai-governance.md`](docs/ai-governance.md)): a reference page for students asked to help write or evaluate AI policy at work, covering ISO/IEC 42001, ISO/IEC 27090, ISO/IEC 27001/27002, and the NIST AI RMF, with guidance on choosing between them and a note on cost. Linked from the README and the site's Governance category. These are standards, not tools, so they are not entries in `tools.yaml`.
- Optional `guide` field on categories in `tools.yaml` (`label` + `path`), rendered as a link under the category on the site and in the README. `build.py` fails if the path doesn't exist.

## 2026-10-05

### Added
- `build.py` fails if the generated `index.html` or `README.md` contains an em dash or en dash, printing the file, line, and nearby text for each.
- `scripts/check_assets.py`, run by `build.py`: the build now fails if `index.html` references a local file (src, href, srcset, CSS url(), or a logo-map entry) that is missing on disk or ignored by git. `python scripts/check_assets.py --self-test` proves the check.

### Changed
- **README and build output:** replaced the remaining em dashes in `build.py` (including the two strings it writes into the README) and in the README's hand-written sections with commas or periods.
- **Catalog copy:** replaced the em dashes in tool and category text with commas or periods (and a hyphen in Claude's Max price range). Three entries gained a connecting word ("with" or "for"); no facts, prices, or dates changed.

## 2026-10-04

### Added
- **Claude for Financial Services:** Anthropic's free, open-source finance agents and skills (DCF, LBO, three-statement models). The base skills work on any Claude plan; the full agents need institutional data access such as FactSet or S&P Capital IQ.

## 2026-09-30

Covers [#1](https://github.com/foster-hmba-ai-cabinet/kirin-ai-tools/pull/1),
[#2](https://github.com/foster-hmba-ai-cabinet/kirin-ai-tools/pull/2),
[#3](https://github.com/foster-hmba-ai-cabinet/kirin-ai-tools/pull/3) and
[#4](https://github.com/foster-hmba-ai-cabinet/kirin-ai-tools/pull/4).

### Added
- `last_verified` date per tool, surfaced on each card and in the README ([#1](https://github.com/foster-hmba-ai-cabinet/kirin-ai-tools/pull/1)).
- `scripts/stale.py` to list tools overdue for a pricing check ([#1](https://github.com/foster-hmba-ai-cabinet/kirin-ai-tools/pull/1)).
- Static fallbacks so tool count, category count, and pricing date render without JavaScript ([#1](https://github.com/foster-hmba-ai-cabinet/kirin-ai-tools/pull/1)).

### Changed
- **Notion AI:** AI is bundled into paid plans, not sold as a separate add-on ([#2](https://github.com/foster-hmba-ai-cabinet/kirin-ai-tools/pull/2)).
- **Tableau:** the free student offer is now Tableau Desktop Public Edition: non-commercial only, and it publishes to Tableau Public ([#2](https://github.com/foster-hmba-ai-cabinet/kirin-ai-tools/pull/2)).
- **Perplexity:** the $4.99/mo Education Pro rate no longer exists; cost tier corrected from "Free for students" to "Freemium" ([#2](https://github.com/foster-hmba-ai-cabinet/kirin-ai-tools/pull/2)).
- **NotebookLM renamed to Gemini Notebook**, with a new URL ([#4](https://github.com/foster-hmba-ai-cabinet/kirin-ai-tools/pull/4)).
- Refreshed pricing for ChatGPT, Claude, Gemini, GitHub Copilot, Midjourney, Notion AI, Perplexity, and Tableau ([#2](https://github.com/foster-hmba-ai-cabinet/kirin-ai-tools/pull/2)).
- Rewrote the near-zero-cost stack copy: removed the unsourced "~90% of MBA needs" claim and the Perplexity reference ([#3](https://github.com/foster-hmba-ai-cabinet/kirin-ai-tools/pull/3)).

### Removed
- Unsourced ".gov / .mil free Pro year" claim from Perplexity's note ([#2](https://github.com/foster-hmba-ai-cabinet/kirin-ai-tools/pull/2)).
- Outdated google.com/students reference from Gemini's note ([#2](https://github.com/foster-hmba-ai-cabinet/kirin-ai-tools/pull/2)).

### Fixed
- The CONTRIBUTING example used an unquoted date, which broke the build ([#1](https://github.com/foster-hmba-ai-cabinet/kirin-ai-tools/pull/1)).
- README commit steps omitted `tools.json` ([#1](https://github.com/foster-hmba-ai-cabinet/kirin-ai-tools/pull/1)).
- Committed `__pycache__` files, now gitignored ([#1](https://github.com/foster-hmba-ai-cabinet/kirin-ai-tools/pull/1)).
