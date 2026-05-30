# Monthly "What's New" Digest — n8n + SES

The retention engine: once a month, email the cohort the tools added since the last digest. It reuses what you already run (n8n at `n8n.kirinai.app`, SES) and reads the same `tools.json` the site is built from — so there's no second source of truth to maintain.

## How it works

```
Schedule (monthly)  →  HTTP GET tools.json  →  Code (filter + format)  →  IF newCount>0  →  SES Send Email
```

The digest reads `added` dates straight from the catalog. If nothing was added that month, the IF node short-circuits and no email goes out — no noise, no "sorry, nothing new" filler.

## Dependencies

1. **`tools.json` must be committed and pushed.** `scripts/build.py` generates it; make sure it's in the repo (the commit step in `CONTRIBUTING.md` includes it).
2. **The raw URL** — adjust org/branch to match where you host:
   `https://raw.githubusercontent.com/foster-hmba-ai-cabinet/kirin-ai-tools/main/tools.json`
3. **SES is still in sandbox** (per your setup). Until production access lands, the digest can only send to *verified* addresses — fine for testing against yourself. Point it at the cohort distribution list once the sandbox lift goes through.

## Node-by-node

**1. Schedule Trigger**
- Rule: Cron → `0 13 1 * *` (the 1st of each month, 13:00 UTC = 06:00 MT, matching your Morning Brief cadence). Covers the month that just ended.

**2. HTTP Request**
- Method `GET`, URL = the raw `tools.json` URL above.
- Response Format: **JSON**. (Output lands at `$json`, with `$json.tools` being the array.)

**3. Code** (language: JavaScript) — paste the script below. It outputs one item with `newCount`, `subject`, `html`, and `monthLabel`.

**4. IF**
- Condition (Number): `{{ $json.newCount }}` **is greater than** `0`. True branch → SES.

**5. AWS SES → Send Email** (true branch)
- From: your verified sender (`tylerfutch1997@gmail.com` while in sandbox).
- To: yourself for testing; the cohort list after the sandbox lift.
- Subject: `={{ $json.subject }}`
- HTML body: `={{ $json.html }}`

## Code node script

```javascript
// Reads tools.json from the HTTP node; emits a digest for the PREVIOUS calendar month.
const data = $input.first().json;
const tools = Array.isArray(data.tools) ? data.tools : [];
const cats = Object.fromEntries((data.categories || []).map(c => [c.id, c.title]));

// Target = the month that just ended (run fires on the 1st).
const now = new Date();
const target = new Date(now.getFullYear(), now.getMonth() - 1, 1);
const ym = `${target.getFullYear()}-${String(target.getMonth() + 1).padStart(2, '0')}`;
const monthLabel = target.toLocaleString('en-US', { month: 'long', year: 'numeric' });

const fresh = tools
  .filter(t => (t.added || '').slice(0, 7) === ym)
  .sort((a, b) => a.name.localeCompare(b.name));

// Group by category for a tidy email.
const groups = {};
for (const t of fresh) (groups[t.category] = groups[t.category] || []).push(t);

const esc = s => String(s || '').replace(/[&<>]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]));

const sections = Object.entries(groups).map(([cid, items]) => {
  const rows = items.map(t => `
    <li style="margin:0 0 12px">
      <a href="${esc(t.url)}" style="color:#4b2e83;font-weight:600;text-decoration:none">${esc(t.name)}</a>
      &nbsp;<span style="color:#8a6d1f;font-size:12px">[${esc(t.cost_tier)} · ${esc(t.difficulty)}]</span><br>
      <span style="color:#333;font-size:14px">${esc(t.what)}</span>
    </li>`).join('');
  return `<h3 style="font-family:Georgia,serif;color:#1f1b16;margin:20px 0 8px">${esc(cats[cid] || cid)}</h3>
          <ul style="padding-left:18px;margin:0">${rows}</ul>`;
}).join('');

const siteUrl = 'https://foster-hmba-ai-cabinet.github.io/kirin-ai-tools/'; // adjust to your live URL

const html = `
  <div style="font-family:Arial,Helvetica,sans-serif;max-width:620px;margin:0 auto;color:#1f1b16">
    <div style="border-top:5px solid #4b2e83;padding-top:16px">
      <p style="font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:#8a6d1f;margin:0">Foster HMBA · AI Cabinet</p>
      <h2 style="font-family:Georgia,serif;margin:6px 0 2px">New AI tools — ${monthLabel}</h2>
      <p style="color:#5c5346;font-size:14px;margin:0 0 8px">
        ${fresh.length} tool${fresh.length === 1 ? '' : 's'} added to the Field Guide this month.
      </p>
    </div>
    ${sections}
    <p style="margin:24px 0 8px">
      <a href="${siteUrl}" style="background:#4b2e83;color:#fff;padding:10px 18px;border-radius:8px;text-decoration:none;font-size:14px">Browse the full guide →</a>
    </p>
    <p style="color:#8a8275;font-size:12px;border-top:1px solid #ddd;padding-top:10px;margin-top:18px">
      Maintained by the Foster HMBA AI Cabinet. Reply with tools you'd like added.
    </p>
  </div>`;

return [{
  json: {
    newCount: fresh.length,
    monthLabel,
    subject: `New AI tools for the cohort — ${monthLabel} (${fresh.length})`,
    html,
  },
}];
```

## Testing before you trust the schedule

- **Force a hit:** temporarily change `ym` to a month you know has additions (e.g. `'2026-05'`) and run the workflow manually — you should get the 3 May tools rendered.
- **Confirm the empty case:** point `ym` at a month with no additions and check the IF node blocks the send.
- Once both pass, revert `ym` to the dynamic value and activate the schedule.

## Optional upgrades (later)

- Swap the HTTP source for the **KIRIN RDS** if you'd rather the catalog live in `tyler_ai` than in the repo — but the repo-as-source keeps the site and digest in lockstep, which is the cleaner handoff story.
- Surface the same `tools.json` as a **KIRIN knowledge-base module** so KIRIN can answer "what's the best tool for X?" from the cabinet's curated list rather than the open web.
