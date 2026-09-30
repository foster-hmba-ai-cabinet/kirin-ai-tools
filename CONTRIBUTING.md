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
| `scripts/stale.py` | Lists tools whose pricing hasn't been re-verified in 90 days (quarterly refresh). |
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
     added: "2026-06-15"                # today's date (YYYY-MM-DD, quoted)
     last_verified: "2026-06-15"        # date pricing was checked on the provider's page (quoted)
     notes: Optional caveat (renders as a ⚠ line).
   ```

   > **Quote your dates.** Write `added: "2026-06-15"`, not `added: 2026-06-15`. Unquoted, YAML reads the value as a date object instead of a string, which older versions of `build.py` couldn't serialize to JSON (the build crashed with `TypeError: Object of type date is not JSON serializable`). The build now normalizes them, but quoted dates are the convention and keep `tools.yaml` unambiguous.
   >
   > **`added` vs `last_verified`:** `added` is when the tool entered the catalog and never changes. `last_verified` is when someone last checked its pricing / free-tier claim on the provider's page — bump it on every re-check, even if nothing changed. It must be on or after `added`, and it's shown on each tool card (amber once it's more than 90 days old).

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
- [ ] `last_verified` is the date you checked the pricing (usually the same as `added` for a new tool).

Curated beats comprehensive. A focused list of ~30–40 great tools is more useful to a new student than 150 entries. Prune aggressively.

---

## Maintenance cadence

| When | Task |
|------|------|
| **Each term** | Spot-check that links resolve and nothing major was discontinued. |
| **Quarterly** | Pricing refresh — AI pricing shifts fast. See below. |
| **Each major model launch** | Sanity-check the General-Purpose Assistants section. |
| **Annually (Sept onboarding)** | Ownership handoff to the incoming cohort (below). |

### Quarterly pricing refresh

```bash
python scripts/stale.py              # tools not verified in the last 90 days
python scripts/stale.py --markdown   # same list as a checklist — paste into the refresh PR
```

For each tool listed: open its provider page, update `pricing` (and `cost_tier` if it moved), set `last_verified` to the date you checked, then run `python scripts/build.py` and open a PR. `stale.py` exits non-zero while anything is stale, so the refresh is done when it prints `0 of N tools`.

`meta.pricing_as_of` is the older, catalog-wide pricing date. Keep bumping it after a full refresh until it's retired (see the comment in `tools.yaml`).

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
