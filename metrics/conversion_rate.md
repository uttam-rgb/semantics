---
metric: conversion_rate
aliases: [conversion rate, l2c, lead to conversion, close rate, win rate, conversions by agent]
status: confirmed
owner: TBD
confirmed_by: Uttam (derived from production Metabase SQL; adjudicated 2026-09-12 against Lane_Metric_Definitions_v1.xlsx and confirmed correct as-is, with DP PAID added to the converted-stage set)
confirmed_date: 2026-09-12
last_verified: 2026-09-12
source: analytics.cratio_leads_analytics
grain: one row per lead
time_field: "call_date for conversion counts; lead_date for the leads-taken denominator in the overall L2C rate — these are different cohorts, see gotcha"
dimensions: [lead_owner]
---

## Definition

"Converted" = `lead_stage IN ('CLOSED WON', '50% PAYMENT DONE', 'DP PAID')`.

**Adjudicated 2026-09-12** against `Lane_Metric_Definitions_v1.xlsx`: production SQL only checked `CLOSED WON`/`50% PAYMENT DONE`; the spreadsheet's "Lead Rules" tab also maps **`DP PAID`** (Down Payment Paid — 9 rows, ₹54,200 total `expected_revenue`) to "Converted." Added here. Note the spreadsheet has a **second, different** lead-stage mapping ("Business Rules → Status Bucket," used for a different set of cards — Source Wise Summary / Agent Wise Lead Status) where `50% PAYMENT DONE` isn't listed at all and would fall into that mapping's default "Live" bucket. That second mapping is for a different metric family (Live/Hot/Dead Lead counts, not yet built — see `future_work.md`) — don't let it override this "converted" definition.

There are **five distinct, correctly-named metrics** in production that all relate to conversion, easily confused with each other because the source reports used inconsistent names for them. Renamed here for clarity; original query-comment names noted so you can match them back to Metabase.

| Clear name | Formula | Was called (in SQL) |
|---|---|---|
| **Total Conversions** | `COUNT(mobile_number)` where converted, by `call_date` | `total_leads_converted` / `lead_conversion` |
| **Lead-to-Conversion Rate (L2C%)** | `SUM(conversions) / SUM(leads_taken)` — leads_taken by `lead_date`, conversions by `call_date` (different cohorts, see gotcha) | `l2c_conversion%` |
| **Same-Day Conversion Mix %** — *of the leads we converted, what share converted the same day they came in* | `COUNT(converted AND call_date=lead_date) / COUNT(all converted)` | `same_day_converted %` (`conversion.sql`) |
| **Follow-up Conversion Mix %** — complement of the above | `COUNT(converted AND call_date≠lead_date) / COUNT(all converted)` | `followup_converted %` (`conversion.sql`) |
| **Same-Day Lead Conversion Rate (D0 L2C%)** — *of everyone we called this period, what share converted same-day* | `COUNT(converted AND call_date=lead_date) / COUNT(all leads called)` | `d0_conversion%` (`leaderdashboard_summary.sql`) — **formula was buggy in the source file, fixed here, see gotcha** |
| **Follow-up Lead Conversion Rate** | `COUNT(converted AND call_date≠lead_date) / COUNT(all leads called)` | `followup_conversion%` (`leaderdashboard_summary.sql`) |
| **Full-Payment Conversions** | `COUNT(mobile_number)` where `lead_stage = 'CLOSED WON'` only, by `call_date` | `full_payment_leads` (`leaderdashboard_summary.sql`) |
| **Partial-Payment Conversions** | `COUNT(mobile_number)` where `lead_stage = '50% PAYMENT DONE'` only, by `call_date` | `50%_payment_leads` (`leaderdashboard_summary.sql`) |

The "Mix %" pair and the "Lead Conversion Rate" pair look similar but answer different questions: **Mix %** describes the composition of wins you already have; **Lead Conversion Rate** describes your hit rate against everyone you called. Don't use them interchangeably.

**Total Conversions = Full-Payment Conversions + Partial-Payment Conversions + `DP PAID` conversions.** The full/partial breakdown query only ever checked `CLOSED WON`/`50% PAYMENT DONE` — `DP PAID` (9 rows) isn't assigned to either bucket. Not yet confirmed whether "Down Payment Paid" should count as full, partial, or its own third bucket — low volume, but flag rather than guess if a report needs the full/partial split to add up exactly to Total Conversions.

## Verified SQL

```sql
-- Total Conversions + Same-Day / Follow-up Conversion Mix % (source: conversion.sql)
select
    date(date_trunc({{frequency}}, call_date::date)) as call_frequency,
    count(case when lead_stage in ('50% PAYMENT DONE', 'CLOSED WON', 'DP PAID') then mobile_number end) as total_leads_converted,
    count(case when lead_stage in ('50% PAYMENT DONE', 'CLOSED WON', 'DP PAID') and call_date = lead_date then mobile_number end) as same_day_converted,
    count(case when lead_stage in ('50% PAYMENT DONE', 'CLOSED WON', 'DP PAID') and call_date != lead_date then mobile_number end) as followup_converted
from analytics.cratio_leads_analytics
where call_date::date between {{start_date}} and {{end_date}}
[[and {{lead_owner}}]]
group by 1
order by 1;

-- then divide same_day_converted / total_leads_converted for "Same-Day Conversion Mix %"
-- and followup_converted / total_leads_converted for "Follow-up Conversion Mix %"
```

```sql
-- Full-Payment vs Partial-Payment Conversions, plus raw d0/followup counts (source: leaderdashboard_summary.sql)
select
    coalesce(lead_owner, 'Unknown') as lead_owner,
    date(date_trunc({{frequency}}, call_date::date)) as frequency,
    count(case when lead_stage in ('CLOSED WON', '50% PAYMENT DONE', 'DP PAID') then mobile_number end) as lead_conversion,
    count(case when call_date::date = lead_date::date
               and lead_stage in ('CLOSED WON', '50% PAYMENT DONE', 'DP PAID') then mobile_number end) as d0_lead_conversion,
    count(case when call_date::date != lead_date::date
               and lead_stage in ('CLOSED WON', '50% PAYMENT DONE', 'DP PAID') then mobile_number end) as followup_lead_conversion,
    count(case when lead_stage = 'CLOSED WON' then mobile_number end) as full_payment_leads,
    count(case when lead_stage = '50% PAYMENT DONE' then mobile_number end) as "50%_payment_leads"
from analytics.cratio_leads_analytics
where call_date::date between {{start_date}} and {{end_date}}
[[and {{lead_owner}}]]
group by 1, 2;
```

```sql
-- Same-Day Lead Conversion Rate (D0 L2C%) — CORRECTED formula (see gotcha)
-- and Follow-up Lead Conversion Rate, both denominated over all leads called
select
    coalesce(lead_owner, 'Unknown') as lead_owner,
    date(date_trunc({{frequency}}, call_date::date)) as frequency,
    count(mobile_number) as total_customers_called,
    count(case when call_date::date = lead_date::date
               and lead_stage in ('CLOSED WON', '50% PAYMENT DONE', 'DP PAID') then mobile_number end) * 1.00
      / nullif(count(mobile_number), 0) as "d0_conversion_pct_FIXED",
    count(case when call_date::date != lead_date::date
               and lead_stage in ('CLOSED WON', '50% PAYMENT DONE', 'DP PAID') then mobile_number end) * 1.00
      / nullif(count(mobile_number), 0) as "followup_conversion_pct"
from analytics.cratio_leads_analytics
where call_date::date between {{start_date}} and {{end_date}}
[[and {{lead_owner}}]]
group by 1, 2
```

```sql
-- Overall Lead-to-Conversion Rate (L2C%) — ratio of sums, NOT average of per-row rates
with leads_taken as (
    select count(mobile_number) as n
    from analytics.cratio_leads_analytics
    where lead_date::date between {{start_date}} and {{end_date}}
),
conversions as (
    select count(case when lead_stage in ('CLOSED WON','50% PAYMENT DONE') then mobile_number end) as n
    from analytics.cratio_leads_analytics
    where call_date::date between {{start_date}} and {{end_date}}
)
select conversions.n * 1.00 / nullif(leads_taken.n, 0) as l2c_pct
from leads_taken, conversions;
```

Verified 2026-09-12, last 30 days: leads_taken = 10,027, conversions = 588 (including `DP PAID`; was 579 without it), **L2C% = 5.86%** (was 5.77%).

## Gotchas

1. **The overall L2C% numerator and denominator are different cohorts.** `leads_taken` is windowed by `lead_date`; `conversions` is windowed by `call_date`. A lead generated on day 1 that converts on day 20 counts in "leads_taken" for the period containing day 1, and in "conversions" for the period containing day 20 — if your reporting window only spans one of those, the two numbers aren't describing the same set of people. This is how production computes it (confirmed, not a bug) — just don't over-interpret L2C% as "of the leads generated this period, X% converted this period."

2. **`d0_conversion%` had a real bug in the source production SQL** (`leaderdashboard_summary.sql`): its numerator didn't actually filter `call_date = lead_date` — it reused the unfiltered `lead_conversion` count, making it silently identical to *(all conversions / all leads called)* rather than *(same-day conversions / all leads called)*. The corrected version is what's in the "Verified SQL" section above (column aliased `d0_conversion_pct_FIXED` to make the correction obvious). **If this is still live in Metabase, it should be fixed there too.**

3. **Never average a per-row/per-owner rate to get an overall rate** — always recompute as `SUM(numerator)/SUM(denominator)` over the full set, per the ratio-of-sums pattern shown above. **This isn't hypothetical — it's a confirmed bug already present in production**: `leaderdashboard_summary.sql`'s final "Summary Overall" query computes `l2c_conversion%` correctly (`SUM(lead_conversion) * 1.00 / SUM(leads_taken)`), but right next to it, in the same query, computes `d0_conversion%` and `followup_conversion%` as `AVG("d0_conversion%")` / `AVG("followup_conversion%")` — averaging the already-computed per-owner-period percentage columns instead of re-deriving from summed counts. Same query, two different (and inconsistent) aggregation methods. The corrected version:
   ```sql
   -- replaces avg("d0_conversion%") / avg("followup_conversion%") in the Summary Overall query
   sum(d0_lead_conversion) * 1.00 / nullif(sum(leads_taken), 0) as "d0_conversion_pct_FIXED",
   sum(followup_lead_conversion) * 1.00 / nullif(sum(leads_taken), 0) as "followup_conversion_pct_FIXED"
   ```
   **If this "Summary Overall" report is live in Metabase, it should be fixed there too** — same class of issue as the earlier `d0_conversion%` bug, but this one hides in the rollup step rather than the row-level formula.

## Owner

TBD

**Last verified:** 2026-09-12
