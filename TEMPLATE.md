# New Tool Proposal Template

Copy the block below into `tools.yaml` under `tools:` and fill it in. Then run
`python scripts/build.py` to render it into the README.

```yaml
  - name: # Tool name as it's officially branded
    url: # https:// canonical homepage
    category: # one of: general research writing data design slides audio meetings automation coding career governance
    what: # ONE sentence: what it actually does. No marketing copy.
    best_for: # ONE phrase: the specific MBA workflow / who it's for.
    pricing: # e.g. "Free; Pro $20/mo" — check the provider's page TODAY.
    cost_tier: # Free | Freemium | Paid | Free for students | Institutional
    difficulty: # Beginner | Intermediate | Advanced
    contexts: # list, any of [education, professional, personal] — e.g. [education, professional]
    added: # today's date, YYYY-MM-DD — powers the NEW badge + changelog
    notes: # OPTIONAL: a caveat, privacy flag, or student-deal tip. Renders as ⚠.
```

## Quick checklist before you submit
- [ ] Does it beat something already listed at a real task? If not, skip it.
- [ ] Is `what` honest and one sentence?
- [ ] Did you verify `pricing` on the provider's own page today?
- [ ] Are `cost_tier` and `difficulty` realistic (not optimistic)?
- [ ] If it handles student data, did you add a privacy note?
- [ ] Did you set `contexts` (who it's for) and `added` (today's date)?
