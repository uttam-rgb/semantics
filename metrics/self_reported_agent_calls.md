---
metric: self_reported_agent_calls
aliases: [calls made - agent, calls made (self-reported)]
status: confirmed
owner: TBD
confirmed_by: "Uttam — Source Tables tab confirms this reads a self-reported figure, deliberately separate from call_activity.md's telephony-verified numbers"
confirmed_date: 2026-09-12
last_verified: 2026-09-12
source: analytics.daily_report_snapshots
grain: one row per (snapshot_date, lead_owner)
time_field: snapshot_date
dimensions: [lead_owner]
---

## Definition

"Calls each agent **reported** making in the period" — a self-reported figure from `daily_report_snapshots.total_calls_made`, **not** derived from `public.exotel_calls`. This is a deliberately separate number from `call_activity.md`'s telephony-verified "Total calls made" — the spreadsheet's own Known Caveat C-01 says these two "will not tie," and confirms `daily_report_snapshots`' calls figure is "self-reported, not telephony-verified."

**Do not merge or reconcile this with `call_activity.md`.** Both are real, named metrics on different dashboard cards (Company/Agent Performance vs. Agent Wise Call Summary) that intentionally read different sources.

## Formula

```
SUM(total_calls_made)
```
from `analytics.daily_report_snapshots`, filtered to `snapshot_date` in range, optionally grouped by `lead_owner`.

## Verified SQL

```sql
select lead_owner,
       date(date_trunc({{frequency}}, snapshot_date)) as frequency,
       sum(total_calls_made) as calls_made_self_reported
from analytics.daily_report_snapshots
where snapshot_date between {{start_date}} and {{end_date}}
[[and lead_owner = {{lead_owner}}]]
group by 1, 2
order by 1, 2
```

Verified 2026-09-12, last 30 days, all owners: **31,423** (self-reported) vs. **40,313** (telephony-verified, `call_activity.md`, same window) — a ~22% gap, consistent with the spreadsheet's own caveat that these don't tie.

## ⚠️ Not buildable: "Call Connected Agent" (self-reported)

The spreadsheet names this as a metric on the same card, but **no supporting column exists**. Checked `daily_report_snapshots`'s live schema (2026-09-12) — it has `total_calls_made`, `calls_made_for_new_leads`, `calls_made_for_old_leads`, but nothing resembling a self-reported "connected calls" count. If this metric is genuinely needed, either it doesn't actually exist in Metabase yet either (worth asking), or it's computed from a different table not yet identified — not guessing a substitute here.

## ⚠️ Not built: "Incoming Calls" / "Missed Calls" / "Missed Calls Not Called Back"

These three rows exist in the spreadsheet's Metric Definitions list with **blank Report/Card and blank Business Definition columns** — not even the source document defines them yet. Not building these; there's no spec to build against, and inventing one would mean documenting a guess as if it were confirmed logic.

## Owner

TBD

**Last verified:** 2026-09-12
