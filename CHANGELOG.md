# Changelog

All notable changes to the KIRIN AI Tools Repository are documented here: pricing
corrections, tool renames, copy changes, and tooling. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/). The guide isn't versioned,
so entries are grouped by date, newest first.

Every change to `tools.yaml` gets an entry here, new tools included. (The site's
**📜 Changelog** section separately lists new tools automatically from each tool's
`added` date.)

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
