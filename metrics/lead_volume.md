---
metric: lead_volume
aliases: [leads generated, leads taken, number of leads, lead count]
status: confirmed
owner: TBD
confirmed_by: Uttam (derived directly from production Metabase SQL, SQL_Logic/lead_assigned.sql and leaderdashboard_summary.sql)
confirmed_date: 2026-09-12
last_verified: 2026-09-12
source: analytics.cratio_leads_analytics
grain: one row per lead
time_field: lead_date
dimensions: [lead_owner]
---

## Definition

"Number of leads" is a plain **`COUNT(*)`** (or `COUNT(mobile_number)`, equivalent here since it's NOT NULL in practice) over `analytics.cratio_leads_analytics`, filtered by **`lead_date`** — not `COUNT(DISTINCT mobile_number)`. This supersedes an earlier version of this doc that treated the `count(*)` vs `count(distinct mobile_number)` choice as unresolved — production reporting uses raw row count.

## Formula

```
COUNT(*)  -- (or COUNT(mobile_number), equivalent)
```
filtered to leads whose `lead_date` falls in the reporting window, optionally grouped by `lead_owner`.

## Verified SQL

```sql
-- Leads Generated, by lead owner and period (source: SQL_Logic/lead_assigned.sql)
select
    lead_owner,
    date(date_trunc({{frequency}}, lead_date::date)),
    count(*) as total_leads_generated
from analytics.cratio_leads_analytics
where lead_date::date between {{start_date}} and {{end_date}}
[[and {{lead_owner}}]]
group by 1, 2
order by 1, 2
```

Verified 2026-09-12, last 30 days, all owners: **10,027 leads**.

## Gotchas

- **Filtered by `lead_date`** (when the lead was created), not `call_date` (when it was worked/called) — different from the `revenue`/`conversion_rate` metrics, which filter by `call_date`. Mixing these up will misattribute a lead-generation count to the wrong period, or compare a lead-generation cohort against a conversion cohort that doesn't correspond to the same leads (see `conversion_rate.md`).
- Raw row count includes whatever duplicate/re-entered leads exist in the table (see `tables/analytics/cratio_leads_analytics.md` — ~5,000-row gap between total rows and distinct `mobile_number`). Production reporting does not deduplicate; don't second-guess this by switching to `COUNT(DISTINCT mobile_number)` unless explicitly asked to.
- No filtering of placeholder/test values (`lead_source = '--Select--'`, etc.) happens in this query — "leads generated" includes everything, unfiltered.

## Owner

TBD

**Last verified:** 2026-09-12
