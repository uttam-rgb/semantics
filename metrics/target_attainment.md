---
metric: target_attainment
aliases: [target vs actual, target achievement, expected revenue target]
status: confirmed
owner: TBD
confirmed_by: Uttam (derived directly from production Metabase SQL, SQL_Logic/leaderdashboard_summary.sql)
confirmed_date: 2026-09-12
last_verified: 2026-09-12
source: analytics.lead_owner_target
grain: one row per (lead_owner, target_date)
time_field: target_date
dimensions: [lead_owner]
---

## Definition

Compares each lead owner's revenue **target** (`analytics.lead_owner_target.target`) against their actual `revenue` metric (see `revenue.md`) for the same period. **Resolves `open_questions.md` item 17**: `lead_owner_target.target` is a **revenue target**, not a conversion-count or lead-count target — confirmed by production SQL aliasing `sum(target)` directly as `expected_revenue` and comparing it against `total_revenue` (the revenue metric) in the same report.

## Formula

```
target_data:  SUM(target) grouped by (lead_owner, date_trunc(frequency, target_date))
actual:       revenue metric (see revenue.md), same grouping
```

## Verified SQL

```sql
with target_data as (
    select lead_owner,
           date(date_trunc({{frequency}}, target_date)) as frequency,
           sum(target) as expected_revenue
    from analytics.lead_owner_target
    where target_date between {{start_date}} and {{end_date}}
    group by 1, 2
)
select * from target_data;
-- join to the `revenue` metric's actual total_revenue on (lead_owner, frequency) via LEFT JOIN
-- to compare target ("expected_revenue" here) against actual (see revenue.md)
```

## Gotchas

- `lead_owner_target` has **no enforced PK/unique constraint** (see `tables/analytics/lead_owner_target.md`) — verify there's genuinely one row per (lead_owner, target_date) before trusting a 1:1 join; a duplicate row would silently inflate the target sum.
- The field is literally named `expected_revenue` in this query's output (reusing the same alias as the `revenue` metric's target-vs-actual naming convention in the source dashboard) — don't confuse this with `cratio_leads_analytics.expected_revenue`, a different column on a different table that happens to share a name.

## Owner

TBD

**Last verified:** 2026-09-12
