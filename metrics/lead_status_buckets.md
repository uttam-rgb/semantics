---
metric: lead_status_buckets
aliases: [live leads, hot leads, dead leads, leads in non-serviceable areas, lead pipeline status]
status: draft
owner: TBD
confirmed_by: "Uttam — mapping taken from Lane_Metric_Definitions_v1.xlsx 'Lead Rules' tab; the SQL itself is newly constructed and verified against live data by Claude, not copied from an existing production query (no SQL_Logic file covers this)"
confirmed_date: 2026-09-12
last_verified: 2026-09-12
source: analytics.cratio_leads_analytics
grain: one row per lead
time_field: "lead_date (assumed — not explicitly stated in the spreadsheet; see gotcha)"
dimensions: [lead_owner]
---

## Definition

Buckets every lead into one status using the spreadsheet's "Lead Rules" mapping, then reports counts per bucket. Four of the buckets correspond to named dashboard cards:

| Card name | Status bucket | Business Definition (from spreadsheet) |
|---|---|---|
| Live Leads | `Live` | Leads still in play |
| Hot Leads | `Hot` | Leads close to conversion |
| Dead Leads | `Lost` *(inferred — see gotcha)* | Leads closed lost |
| Leads in Non-Serviceable Areas | `Future Prospect` *(inferred — see gotcha)* | Demand Lane could not serve for geography or supply reasons |

Two more buckets exist in the mapping but aren't named as their own dashboard card here: `Cold` (leads gone quiet — not responding, paused) and `Converted` (already covered by `conversion_rate.md` — this doc's `Converted` bucket should agree with that metric's definition, though note the mapping list here is the exact same 3 stages, `CLOSED WON`/`50% PAYMENT DONE`/`DP PAID`).

## ⚠️ Coverage gap: 28 of 49 real lead_stage values aren't in this mapping

Verified 2026-09-12 against all 82,053 rows in `cratio_leads_analytics`: the spreadsheet's "Lead Rules" tab explicitly covers 21 distinct `lead_stage` values; **28 more distinct values exist in real data with no defined bucket** (4,433 rows, 5.4% of all leads). Unlike the separate "Business Rules → Status Bucket" mapping (used for a different metric family), "Lead Rules" has no documented default. **Decision (2026-09-12): bucket all unmapped values as `'Unmapped'` explicitly**, rather than guessing a default or silently dropping them — keeps the gap visible instead of quietly inflating another bucket.

Some unmapped values are likely near-duplicates of mapped ones (e.g. `'No Car'`/`'No car'` vs. the mapped `'2 W geared - we cannot teach'`; `'2 W non geared - we cannot teach'` is a different string than the mapped `'2 W geared - we cannot teach'`). Others look like they may not belong to this funnel at all — `'Instructor Onboarded'`, `'They will get to us - Instructor only'`, `'Send instructor details'`, `'Assessment booked'` read like **instructor-recruitment** stages, not customer sales stages, sharing the same `lead_stage` field. And `'Full Refund'`/`'Partial Refund'`/`'50% Payment - Refund done - Closed'` look like **post-conversion refund/cancellation** states. None of this is guessed into the mapping — flagged for the business owner to extend the "Lead Rules" tab, not resolved here.

## Verified SQL

```sql
select
    lead_owner,
    case lead_stage
        when 'CALL BACK' then 'Live'
        when 'CLOSED LOST' then 'Lost'
        when '50% PAYMENT DONE' then 'Converted'
        when 'OUT OF BANGALORE' then 'Lost'
        when 'Area not servisable' then 'Future Prospect'
        when 'Hot Lead- Close to conversion' then 'Hot'
        when 'SEND COURSE DETAILS' then 'Hot'
        when 'Agreed to pay' then 'Hot'
        when 'Old Leads clean up' then 'Live'
        when 'CLOSED WON' then 'Converted'
        when 'Demo Class' then 'Hot'
        when 'Ready to pay unable to serve' then 'Future Prospect'
        when '2 W geared - we cannot teach' then 'Lost'
        when 'DP PAID' then 'Converted'
        when 'NEW' then 'Live'
        when 'RNR' then 'Live'
        when 'RNR_2' then 'Live'
        when 'RNR_3' then 'Live'
        when 'RNR_4' then 'Live'
        when '4 Calls not responding' then 'Cold'
        when 'Paused Lead' then 'Cold'
        else 'Unmapped'
    end as status_bucket,
    count(*) as lead_count
from analytics.cratio_leads_analytics
where lead_date::date between {{start_date}} and {{end_date}}
[[and {{lead_owner}}]]
group by 1, 2
order by 1, lead_count desc
```

All-time distribution, verified 2026-09-12 (no date filter applied, full table):

| status_bucket | lead_count |
|---|---|
| Lost | 60,553 |
| Converted | 4,996 |
| **Unmapped** | **4,433** |
| Future Prospect | 4,415 |
| Cold | 3,709 |
| Live | 2,947 |
| Hot | 1,000 |

Note `Lost` dominates at ~74% of all-time leads — consistent with a long-running lead funnel where most historical leads eventually go cold/disqualified; don't be alarmed by this ratio on its own, but also don't use it as a "conversion rate" proxy (that's `conversion_rate.md`, which is period-windowed and denominated differently).

## Gotchas

- **`Dead Leads` → `Lost` and `Leads in Non-Serviceable Areas` → `Future Prospect` are inferred mappings**, not explicitly stated 1:1 in the spreadsheet (it only gives prose descriptions: "leads closed lost," "could not serve for geography or supply reasons"). Reasonable given the wording, but not a direct card-to-bucket table like the other rows — confirm with the owner if precision matters.
- **`Cold` and `Converted` buckets exist but have no named card of their own here** — `Converted` should be cross-checked against `conversion_rate.md` for consistency (same 3 stages, so should agree).
- **`time_field` is an assumption.** The spreadsheet doesn't state which date field these lead-status cards filter on. Used `lead_date` here (consistent with `lead_volume.md`) — could plausibly be `lead_created_time` instead. Verify before trusting a period-filtered version of this query.
- **Do not build "Dead Leads" or similar cards from the separate "Business Rules → Status Bucket" mapping** (used for a different metric family — Source Wise Summary / Agent Wise Lead Status) — that mapping disagrees with this one on where `50% PAYMENT DONE` lands. See `open_questions.md` item 34.

## Owner

TBD

**Last verified:** 2026-09-12
