---
metric: call_activity
aliases: [calls made, connected calls, meaningful calls, talk time, connect rate, leads dialed, leads spoken to, customers called, customers connected, calls made by agent, agent call summary]
status: confirmed
owner: TBD
confirmed_by: Uttam (derived from production Metabase SQL; adjudicated 2026-09-12 against Lane_Metric_Definitions_v1.xlsx — direction filter and source table (public.exotel_calls) confirmed correct as-is, phone normalization switched to last-10-digits)
confirmed_date: 2026-09-12
last_verified: 2026-09-12
source: "public.exotel_calls, joined to analytics.cratio_leads_analytics"
grain: one row per outbound call
time_field: start_time (date part)
dimensions: [lead_owner, source_bucket]
---

## Definition

Outbound calling activity, joined from the call log to the leads table by phone number. **Not** `analytics.exotel_calls`-vs-`exotel.call_logs` (already resolved in `schema_map.md`) — this is about how the call log joins to leads to attribute calls to a lead owner (or to any other lead-level attribute).

**This is the single source of truth for "which leads were called/connected," however you slice it.** "Customers Called"/"Customers Connected" here and "Leads Dialed"/"Leads Spoken To" (as named in `Lane_Metric_Definitions_v1.xlsx`'s Source Wise Summary card) are **the same metric** — same table, same join, same definition — just grouped by a different dimension: `lead_owner` (who called them) vs. `source_bucket` (where the lead came from, see `source_wise_summary.md` for that mapping). Don't maintain separate formulas for these in different docs; add a `GROUP BY` dimension here instead.

## Join logic (important — non-obvious phone normalization)

```sql
select
    date(start_time) as call_date,
    right(from_number, 10) as lead_owner_number,
    right(to_number, 10)   as customer_number,
    status, direction, duration_seconds, start_time, end_time
from public.exotel_calls
where direction != 'inbound'
```
joined to `analytics.cratio_leads_analytics` on `customer_number = mobile_number`. **Both phone numbers are normalized to their last 10 digits (`RIGHT(number, 10)`)** before joining — neither table's raw phone format matches the other's without this.

**Adjudicated 2026-09-12** against `Lane_Metric_Definitions_v1.xlsx`: production SQL originally used `ltrim(number, '0')` (strip only leading zeros); the spreadsheet's documented attribution rule uses last-10-digits instead. Checked both empirically against real data — `ltrim` matched 16,071 of 16,384 distinct numbers, last-10-digits matched 16,090 — a small (~0.1%) difference in this dataset specifically, because `exotel_calls.to_number` is overwhelmingly a clean 11 characters (leading zero + 10 digits) and `cratio_leads_analytics.mobile_number` is overwhelmingly a clean 10 digits, so there's little `+91`/`91` country-code contamination for the two methods to disagree on today. **Adopted last-10-digits going forward** — strictly more robust (handles a country-code prefix `ltrim` can't), matches the spreadsheet's documented standard, and found slightly more real matches.

**Only outbound calls count** (`direction != 'inbound'`) — inbound calls are excluded from this entire metric family. **Adjudicated 2026-09-12**: the spreadsheet's attribution rule says only `direction = 'outbound-dial'` should count, excluding `outbound-api` (13,095 rows — material, not negligible). Reviewed and **confirmed `!= 'inbound'` (including `outbound-api`) is correct as originally documented here** — kept as-is.

## Formulas

| Metric | Formula |
|---|---|
| Customers called | `COUNT(DISTINCT customer_number)` |
| **Customers connected** (= "Leads Connected(Unique)" per agent, see `agent_lead_status.md`) | `COUNT(DISTINCT customer_number) WHERE status='completed'` |
| Total calls made | `COUNT(*)` |
| Total connected calls | `COUNT(*) WHERE status = 'completed'` |
| **Meaningful calls** | `COUNT(*) WHERE status = 'completed' AND duration_seconds >= 120` — a "meaningful" call requires both connection **and** at least 2 minutes duration |
| Connected calls % | `COUNT(DISTINCT customer_number WHERE status='completed') / COUNT(DISTINCT customer_number)` |
| Total talk time (mins) | `SUM(duration_seconds) / 60.0` |
| Avg talk time | `SUM(duration_seconds)/60.0 / COUNT(*) WHERE status='completed'` — denominator is connected calls only, not all calls |

## Verified SQL

```sql
with merged_call_data as (
    select o.*, a.lead_owner
    from (
        select date(start_time) as call_date,
               right(from_number, 10) as lead_owner_number,
               right(to_number, 10) as customer_number,
               status, direction, duration_seconds, start_time, end_time
        from public.exotel_calls
        where date(start_time) between {{start_date}} and {{end_date}}
          and direction != 'inbound'
    ) o
    left join (select lead_owner, mobile_number from analytics.cratio_leads_analytics) a
        on o.customer_number = a.mobile_number
)
select
    lead_owner,
    date(date_trunc({{frequency}}, call_date)) as frequency,
    count(distinct customer_number) as customers_called,
    count(distinct case when status = 'completed' then customer_number end) as customers_connected,
    count(*) as total_calls_made,
    sum(case when status = 'completed' then 1 else 0 end) as total_connected_calls,
    sum(case when status = 'completed' and duration_seconds >= 120 then 1 else 0 end) as meaningful_calls,
    count(distinct case when status = 'completed' then customer_number end) * 1.00
      / count(distinct customer_number) as "connected_calls_pct",
    sum(duration_seconds/60.0) as total_talk_time_mins,
    sum(duration_seconds/60.0) / nullif(sum(case when status = 'completed' then 1 else 0 end), 0) as avg_talk_time
from merged_call_data
group by 1, 2;
```

```sql
-- Same metric, grouped by source_bucket instead of lead_owner
-- ("Leads Dialed" / "Leads Spoken To" on the Source Wise Summary card — see source_wise_summary.md)
-- Note: counts DISTINCT LEADS here (by mobile_number), not distinct phone numbers or call volume,
-- to match "lead count by source" being lead-row-based in source_wise_summary.md.
with called as (
    select distinct right(to_number, 10) as customer_number
    from public.exotel_calls where direction != 'inbound'
),
connected as (
    select distinct right(to_number, 10) as customer_number
    from public.exotel_calls where direction != 'inbound' and status = 'completed'
)
select
    case
        when lower(c.lead_source) like '%facebook%' or lower(c.lead_source) like '%meta%' or lower(c.lead_source) like '%fb%' then 'Meta'
        when lower(c.lead_source) like '%google%' or lower(c.lead_source) like '%paid search%' or lower(c.lead_source) like '%cpc%' then 'Google Ads'
        when lower(c.lead_source) like '%instagram%' or lower(c.lead_source) like '%ig%' or lower(c.lead_source) like '%whatsapp%' or lower(c.lead_source) like '%direct message%' then 'Instagram DMs'
        else 'Offline Activations'
    end as source_bucket,
    count(distinct case when ca.customer_number is not null then c.mobile_number end) as leads_dialed,
    count(distinct case when co.customer_number is not null then c.mobile_number end) as leads_spoken_to
from analytics.cratio_leads_analytics c
left join called ca on ca.customer_number = c.mobile_number
left join connected co on co.customer_number = c.mobile_number
group by 1
order by leads_dialed desc;
```

Verified 2026-09-12, all-time: Meta 8,624 dialed / 5,971 spoken to; Offline Activations 2,556 / 1,868; Google Ads 2,457 / 1,586; Instagram DMs 682 / 488.

## Gotchas

- **`analytics.cratio_leads_analytics.call_did_status` must never be used as a "was this lead called" signal** — checked it against this table's telephony data and found them almost entirely disjoint (of 10,770 leads marked "dialed" via that CRM field, only 579 also matched a real telephony call). Per Uttam (2026-09-12), that field doesn't populate reliably; this table (`exotel_calls`) is the only source of truth for call activity. See `conventions.md`.
- Phone-number join is by normalized match, not a real foreign key — a small percentage of calls (~1.8% by distinct number, last-10-digits method) won't match any lead and will have `lead_owner = NULL`. Decide whether to exclude or bucket these as "Unknown" before reporting owner-level totals (production SQL uses `coalesce(lead_owner, 'Unknown')` elsewhere for this reason).
- Also confirmed (2026-09-12): the spreadsheet documents building the sales-team roster from `DISTINCT non-blank lead_owner` in `daily_report_snapshots`, and restricting calls to only those owners (excluding shared/admin/founder accounts) before attributing — this doc doesn't currently apply that roster restriction. Worth adding if agent-level totals need to exactly match the spreadsheet's stated methodology, not yet done here.
- "Connected" (`status='completed'`) and "meaningful" (`status='completed' AND duration_seconds >= 120`) are different thresholds — don't conflate a short connected call with a meaningful conversation.
- `avg_talk_time`'s denominator is connected calls, not all calls — a period with many unconnected calls won't drag this average down.
- **Same averaging risk as `conversion_rate.md`'s confirmed bug**: production's "Summary Overall" rollup (`leaderdashboard_summary.sql`) computes an overall `avg_talk_time` as `AVG(avg_talk_time)` across each owner-period's already-computed average, rather than `SUM(total_talk_time_mins) / SUM(total_connected_calls)` over the full set. Lower-stakes than the conversion-rate version (a talk-time average being slightly off is less consequential than a conversion rate being off), but the same fix applies if precision matters: recompute from the raw sums, don't average an average.

## Owner

TBD

**Last verified:** 2026-09-12
