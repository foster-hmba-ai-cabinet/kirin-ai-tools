# Contributing & Handoff Guide

This repo is a living reference. It only stays useful if it's maintained — and in Sept 2026 it becomes **Cohort 10's** responsibility. This guide is written to make that handoff painless.

---

## How it's structured

| File | Role |
|------|------|
| `tools.yaml` | **Single source of truth.** All tools and categories live here. |
| `README.md` | Human-readable front door. Tables are **generated** from `tools.yaml`. |
| `index.html` | The **website** — generated from `tools.yaml` (data injected). |
| `scripts/build.py` | Generator: rebuilds the site **and** README tables from `tools.yaml`. |
| `TEMPLATE.md` | Copy-paste template for proposing a new tool. |

**Golden rule:** never hand-edit the tables in `README.md`. Edit `tools.yaml`, then run the script.

---

## Adding or editing a tool

1. Open `tools.yaml`.
2. Add an entry under `tools:` using this schema (copy from `TEMPLATE.md`):

   ```yaml
   - name: Tool Name
     url: https://example.com           # canonical homepage, https
     category: research                 # must match a category id below
     what: One sentence — what it does.
     best_for: One phrase — who/what it's for.
     pricing: "Free; Pro $20/mo"        # point-in-time; verify on provider page
     cost_tier: Freemium                # Free | Freemium | Paid | Free for students | Institutional
     difficulty: Beginner               # Beginner | Intermediate | Advanced
     contexts: [education, professional]# any of: education, professional, personal
     added: 2026-06-15                  # today's date (YYYY-MM-DD)
     notes: Optional caveat (renders as a ⚠ line).
   ```

3. Regenerate and commit:

   ```bash
   pip install pyyaml
   python scripts/build.py
   git add tools.yaml index.html README.md tools.json
   git commit -m "tools: add Tool Name"
   git push
   ```

### Valid category ids
`general` · `research` · `writing` · `data` · `design` · `slides` · `audio` · `meetings` · `automation` · `coding` · `career` · `governance`

To add a category, append it under `categories:` with a unique `id`, a `title` (include an emoji), an `order` number, and a `blurb`.

---

## Quality bar (keep it curated, not exhaustive)

A tool earns a spot only if it **clearly serves an MBA-student workflow**. Before adding, check:

- [ ] It does something a tool already listed doesn't do better.
- [ ] `what` is one honest sentence — no marketing copy.
- [ ] `pricing` was checked on the provider's own page today.
- [ ] `cost_tier` and `difficulty` are accurate, not optimistic.
- [ ] If it touches student data, the `notes` field flags the privacy consideration.
- [ ] `contexts` reflects where it's actually useful (education / professional / personal).
- [ ] `added` is today's date — this is what drives the NEW badge and changelog.

Curated beats comprehensive. A focused list of ~30–40 great tools is more useful to a new student than 150 entries. Prune aggressively.

---

## Maintenance cadence

| When | Task |
|------|------|
| **Each term** | Spot-check that links resolve and nothing major was discontinued. |
| **Quarterly** | Pricing refresh — AI pricing shifts fast. Update `pricing` strings and bump `meta.pricing_as_of` in `tools.yaml`. |
| **Each major model launch** | Sanity-check the General-Purpose Assistants section. |
| **Annually (Sept onboarding)** | Ownership handoff to the incoming cohort (below). |

---

## Handoff checklist (current cohort → next)

- [ ] Transfer or confirm GitHub repo ownership / maintainer access for incoming leads.
- [ ] Update `meta.maintainers` and `meta.handoff_to` in `tools.yaml`.
- [ ] Walk the new owners through one full add-a-tool → regenerate → commit cycle live.
- [ ] Run a quarterly-style pricing refresh together as the first shared task.
- [ ] Update the maintainer names in `README.md`.

---

## Reviewing before publishing

Before the first cohort-wide share, a second Cabinet member reviews for accuracy and tone. Open a pull request rather than committing straight to `main` so changes are visible and reversible.

---

## License

Content: **CC BY 4.0**. Keep attribution to the Foster HMBA AI Cabinet on forks.
