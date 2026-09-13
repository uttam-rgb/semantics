---
metric: revenue
aliases: [total revenue, revenue generated, sales, expected revenue, revenue by agent]
status: confirmed
owner: TBD
confirmed_by: Uttam (derived from production Metabase SQL; adjudicated 2026-09-12 against Lane_Metric_Definitions_v1.xlsx and confirmed correct as-is, with DP PAID added)
confirmed_date: 2026-09-12
last_verified: 2026-09-12
source: analytics.cratio_leads_analytics
grain: one row per lead; revenue is attributed to the lead's conversion event, not to a payment transaction
time_field: call_date (NOT lead_date — see gotcha)
dimensions: [lead_owner]
---

## Definition

Revenue is **not** computed from `payment` or `enrollment` at all — it's the `expected_revenue` field on the lead itself, summed only for leads that have converted (`lead_stage IN ('CLOSED WON', '50% PAYMENT DONE', 'DP PAID')`). This supersedes an earlier (incorrect) version of this doc that explored `payment.amount`/`payment.total_amount`/`enrollment.amount`/`daily_report_snapshots.revenue_booked` as candidates — none of those are what's actually used in production.

**Adjudicated 2026-09-12** against `Lane_Metric_Definitions_v1.xlsx` (the Analytics team's own semantic spec), which claimed `daily_report_snapshots.revenue_booked` was the authoritative source instead — reviewed side by side and confirmed **this doc's original source (`cratio_leads_analytics.expected_revenue`) is correct**, not the spreadsheet's. Also added `'DP PAID'` (9 rows, ₹54,200 total) as a third converted stage, per the spreadsheet's "Lead Rules" tab — this doc previously only had `CLOSED WON`/`50% PAYMENT DONE`.

## Formula

```
SUM(CASE WHEN lead_stage IN ('CLOSED WON', '50% PAYMENT DONE', 'DP PAID')
         THEN NULLIF(expected_revenue, '')::float
         ELSE 0 END)
```
filtered to leads whose **`call_date`** falls in the reporting window (not `lead_date` — see gotcha below), optionally grouped by `lead_owner`.

## Verified SQL

```sql
-- Revenue Generated, by lead owner and period (source: SQL_Logic/lead_assigned.sql)
select
    lead_owner,
    date(date_trunc({{frequency}}, call_date::date)) as call_frequency,
    sum(case when lead_stage in ('50% PAYMENT DONE', 'CLOSED WON', 'DP PAID')
             then expected_revenue::float else 0 end) as total_revenue_generated
from analytics.cratio_leads_analytics
where call_date::date between {{start_date}} and {{end_date}}
[[and {{lead_owner}}]]
group by 1, 2
order by 1, 2
```

Verified 2026-09-12, last 30 days, all owners: **₹4,340,450** (including `DP PAID`; was ₹4,286,250 without it).

```sql
-- Same-day vs follow-up split (raw amounts)
select
    date(date_trunc({{frequency}}, call_date::date)) as call_frequency,
    sum(case when lead_stage in ('50% PAYMENT DONE', 'CLOSED WON', 'DP PAID') then expected_revenue::float else 0 end) as total_revenue_generated,
    sum(case when lead_stage in ('50% PAYMENT DONE', 'CLOSED WON', 'DP PAID') and lead_date = call_date then expected_revenue::float else 0 end) as same_day_revenue_generated,
    sum(case when lead_stage in ('50% PAYMENT DONE', 'CLOSED WON', 'DP PAID') and lead_date != call_date then expected_revenue::float else 0 end) as followup_revenue_generated
from analytics.cratio_leads_analytics
where call_date::date between {{start_date}} and {{end_date}}
[[and {{lead_owner}}]]
group by 1
order by 1
```

```sql
-- Same-Day Revenue Mix % / Follow-up Revenue Mix % (source: lead_assigned.sql)
-- i.e. of the revenue we generated, what share came from same-day vs follow-up conversions
select
    date(date_trunc({{frequency}}, call_date::date)) as call_frequency,
    sum(case when lead_stage in ('50% PAYMENT DONE', 'CLOSED WON', 'DP PAID') and lead_date = call_date then expected_revenue::float else 0 end) * 1.00
      / nullif(sum(case when lead_stage in ('50% PAYMENT DONE', 'CLOSED WON', 'DP PAID') then expected_revenue::float else 0 end), 0) as "same_day_revenue_pct",
    sum(case when lead_stage in ('50% PAYMENT DONE', 'CLOSED WON', 'DP PAID') and lead_date != call_date then expected_revenue::float else 0 end) * 1.00
      / nullif(sum(case when lead_stage in ('50% PAYMENT DONE', 'CLOSED WON', 'DP PAID') then expected_revenue::float else 0 end), 0) as "followup_revenue_pct"
from analytics.cratio_leads_analytics
where call_date::date between {{start_date}} and {{end_date}}
[[and {{lead_owner}}]]
group by 1
order by 1
```

**Same-Day Revenue Mix % / Follow-up Revenue Mix %** — of the revenue attributed in a period, what share came from leads that converted the same day they were generated vs. after follow-up. Same "Mix %" pattern as `conversion_rate.md`'s Same-Day/Follow-up Conversion Mix % — denominator is total converted revenue, not total revenue-eligible leads.

## Gotchas

- **Filtered by `call_date`, not `lead_date`.** A lead generated last month that converts today contributes its full `expected_revenue` to *today's* revenue, not to the month it was generated. Don't assume "revenue for period X" means "revenue from leads created in period X."
- **`expected_revenue` is `text`**, cast with `NULLIF(expected_revenue, '')::float` — a raw `::float` cast on an empty string errors, hence the `NULLIF`.
- **This is the lead-attributed revenue figure, not a cash-collected figure.** It doesn't reconcile with `payment`/`enrollment` sums (verified during earlier exploration — see `tables/analytics/cratio_leads_analytics.md` history) because it's a different concept: revenue attached to a lead the moment it reaches a converted stage, not the actual payment transactions recorded against that learner's account. If a report ever needs "cash actually collected," that's a **different, still-undefined metric** — don't substitute this one for that question.
- **Same-day vs follow-up split compares `lead_date = call_date` directly (no explicit `::date` cast on both sides in this specific query)** — since both are `text` columns, confirm their formats always align before trusting this exact comparison; the sibling query in `conversion.sql` casts both sides `::date` explicitly, which is safer.

## Owner

TBD

**Last verified:** 2026-09-12
