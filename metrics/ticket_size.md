---
metric: ticket_size
aliases: [ticket size, average revenue per conversion, avg deal size, ticket size by agent]
status: confirmed
owner: TBD
confirmed_by: Uttam (derived live from cratio_leads_analytics per revenue.md/conversion_rate.md, deliberately not read from daily_report_snapshots.avg_revenue_per_conversion — same table-choice precedent as those two metrics)
confirmed_date: 2026-09-12
last_verified: 2026-09-12
source: analytics.cratio_leads_analytics
grain: derived — revenue and conversion count, both by call_date
time_field: call_date
dimensions: [lead_owner]
---

## Definition

Average revenue per conversion for a period: **`revenue.md`'s revenue ÷ `conversion_rate.md`'s Total Conversions**, over the same window and (optionally) the same `lead_owner`.

**Note on source table**: `analytics.daily_report_snapshots` has a precomputed `avg_revenue_per_conversion` column that could serve this same purpose. Deliberately **not** using it — same reasoning already applied to `revenue`/`conversion_rate`: the live `cratio_leads_analytics`-derived figure is the one confirmed correct in this project, and computing Ticket Size from the same source keeps it consistent with those two metrics rather than mixing sources.

## Formula

```
SUM(expected_revenue WHERE converted) / COUNT(mobile_number WHERE converted)
```
both sides filtered to `call_date` in the reporting window, using the same converted-stage set as `revenue.md`/`conversion_rate.md`: `lead_stage IN ('CLOSED WON', '50% PAYMENT DONE', 'DP PAID')`.

## Verified SQL

```sql
-- Ticket Size (Achieved) — overall or by lead_owner
select
    lead_owner,
    sum(case when lead_stage in ('CLOSED WON','50% PAYMENT DONE','DP PAID')
             then nullif(expected_revenue,'')::float else 0 end) as revenue,
    count(case when lead_stage in ('CLOSED WON','50% PAYMENT DONE','DP PAID') then mobile_number end) as conversions,
    sum(case when lead_stage in ('CLOSED WON','50% PAYMENT DONE','DP PAID')
             then nullif(expected_revenue,'')::float else 0 end)
      / nullif(count(case when lead_stage in ('CLOSED WON','50% PAYMENT DONE','DP PAID') then mobile_number end), 0) as ticket_size
from analytics.cratio_leads_analytics
where call_date::date between {{start_date}} and {{end_date}}
[[and {{lead_owner}}]]
group by 1
order by conversions desc
```

Verified 2026-09-12, last 30 days: revenue = ₹4,340,450, conversions = 588, **Ticket Size = ₹7,382** (company-wide). Top agents by volume ranged ₹6,533–₹7,800 in the same window — a fairly tight band, no single outlier skewing the average.

## Gotchas

- Never average a per-owner ticket size across owners to get the company figure — recompute as `SUM(revenue)/SUM(conversions)` over the full set, same ratio-of-sums rule as `conversion_rate.md`.
- Inherits every gotcha from `revenue.md` and `conversion_rate.md` (the `expected_revenue` text-cast, the `call_date` windowing, the `DP PAID` sub-bucket ambiguity) since it's built directly from both.
- Zero-conversion periods/owners produce a divide-by-zero — guard with `NULLIF` as shown, and treat a NULL result as "no conversions," not "ticket size of zero."

## Owner

TBD

**Last verified:** 2026-09-12
