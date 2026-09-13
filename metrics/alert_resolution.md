---
metric: alert_resolution
aliases: [resolution rate, alert resolution %, touch rate]
status: confirmed
owner: TBD
confirmed_by: Uttam (derived directly from production Metabase SQL, SQL_Logic/alert.sql)
confirmed_date: 2026-09-12
last_verified: 2026-09-12
source: analytics.alert_resolution_log
grain: one row per (check_date, alert_date, alert_type, lead_owner)
time_field: check_date
dimensions: [lead_owner, alert_type]
---

## Definition

Of the leads alerted on a given day, what fraction had moved to a different stage by the next morning's check. See [`tables/analytics/alert_resolution_log.md`](../tables/analytics/alert_resolution_log.md) for the table itself.

## Formula

```
resolution_pct = 100 * SUM(moved) / SUM(total_alerted)
```
with a traffic-light status:
- **Green**: resolution_pct ≥ 70
- **Yellow**: resolution_pct ≥ 40
- **Red**: resolution_pct < 40

## Verified SQL

```sql
-- ARR: Owner Summary (source: alert.sql)
select
    lead_owner,
    sum(total_alerted) as total_alerted,
    sum(called)        as called,
    sum(moved)          as moved,
    sum(total_alerted) - sum(moved) as not_moved,
    round(100.0 * sum(moved) / nullif(sum(total_alerted), 0), 1) as resolution_pct,
    case
        when round(100.0 * sum(moved) / nullif(sum(total_alerted), 0), 1) >= 70 then 'Green'
        when round(100.0 * sum(moved) / nullif(sum(total_alerted), 0), 1) >= 40 then 'Yellow'
        else 'Red'
    end as status
from analytics.alert_resolution_log
where check_date - interval '1 day' = {{resolution_date}}::date
[[and {{lead_owner}}]]
group by 1
order by total_alerted desc;
```

Note the date logic: `check_date - interval '1 day' = {{resolution_date}}::date` means "the check that happened the day *after* `{{resolution_date}}`" — i.e., `{{resolution_date}}` is the `alert_date` you actually care about, and the query finds its next-morning check.

## ⚠️ "Touch Rate %" is not actually computed anywhere in the source SQL

The production file has a query block titled **"ARR: Detail by Alert Type — Touch Rate % (Called / Alerted)"**, but its body is byte-for-byte identical to the "Total Called" query right above it — it selects `called as total_called` with no division by `total_alerted` at all. **There is no working "touch rate %" query in the file as given.** If a report is currently labeled "Touch Rate %" in Metabase, it is very likely just showing raw `total_called`, not a percentage. The correct formula, if this metric is wanted, would be:

```sql
-- Proposed fix — not yet verified against production, needs sign-off
select
    lead_owner, alert_type,
    called * 1.00 / nullif(total_alerted, 0) as touch_rate_pct
from analytics.alert_resolution_log
where check_date - interval '1 day' = {{resolution_date}}::date
[[and {{lead_owner}}]];
```

**Flag this to whoever owns the alert dashboard before treating any existing "Touch Rate %" number as real.**

## Owner

TBD

**Last verified:** 2026-09-12
