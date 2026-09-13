---
metric: followup_response_time
aliases: [follow-ups called within, follow-up response time, days late on followup]
status: confirmed
owner: TBD
confirmed_by: "Uttam — proposed anchoring to next_followup_on + first call after that date, 2026-09-12; bucketed in days (not minutes) per his call, since next_followup_on has no time component"
confirmed_date: 2026-09-12
last_verified: 2026-09-12
source: "analytics.cratio_leads_analytics joined to public.exotel_calls"
grain: one row per lead with a set next_followup_on
time_field: next_followup_on
dimensions: []
---

## Definition

For each lead with a `next_followup_on` date set, find the first matched outbound call **on or after that date**, and bucket how many days late it was.

**Why days, not minutes** (per Uttam, 2026-09-12): `next_followup_on` is stored with **no time component at all** — every one of 40,814 populated values is exactly `'YYYY-MM-DD'` (verified directly, not a format assumption). There's no due-*moment* to measure minutes against, only a due-*date*. The spreadsheet's original "Follow-ups Called within 5/15/60 min" framing isn't computable as literally stated; this doc measures days-late instead, which the data can actually support.

## A correction made while building this

The first version of this query used each lead's **globally first-ever call** and compared it to the due date — which is wrong, because a lead's first call is often what *caused* the follow-up to be scheduled in the first place, so it commonly predates the due date (19% of rows showed a "negative" gap under that approach). Fixed to look for the first call **on or after** the specific due date instead — same "anchor forward, not globally first" principle as `speed_to_call.md`.

## Verified SQL

```sql
with followups as (
    select mobile_number, nullif(next_followup_on,'')::date as due_date
    from analytics.cratio_leads_analytics
    where next_followup_on is not null and next_followup_on != ''
      and nullif(next_followup_on,'')::date between {{start_date}} and {{end_date}}
),
call_arrays as (
    -- pre-aggregate per phone number first — a per-row correlated subquery against
    -- the raw exotel_calls table timed out (server closed the connection); this is
    -- the same data, just computed once instead of once per lead row
    select right(to_number, 10) as customer_number,
           array_agg(start_time::timestamp order by start_time::timestamp) as call_times
    from public.exotel_calls
    where direction != 'inbound'
    group by 1
)
select
    case
        when fc.first_call_after_due is null then 'No Matched Call At/After Due Date'
        when fc.first_call_after_due::date = f.due_date then 'Same day as due'
        when fc.first_call_after_due::date - f.due_date = 1 then '1 day late'
        when fc.first_call_after_due::date - f.due_date between 2 and 7 then '2-7 days late'
        else '7+ days late'
    end as bucket,
    count(*) as lead_count
from followups f
left join call_arrays ca on ca.customer_number = f.mobile_number
left join lateral (
    select min(t) as first_call_after_due
    from unnest(ca.call_times) as t
    where t::date >= f.due_date
) fc on true
group by 1
order by lead_count desc;
```

Verified 2026-09-12, all-time (40,814 total leads with a follow-up date set):

| Bucket | Lead count |
|---|---|
| No Matched Call At/After Due Date | 36,026 (88.3%) |
| Same day as due | 2,907 |
| 7+ days late | 1,006 |
| 2-7 days late | 460 |
| 1 day late | 415 |

Same expected pattern as `speed_to_call.md` — the vast majority show no matched call, consistent with the same telephony phone-matching gap (agent-mobile/WhatsApp calls invisible here) documented throughout this project, not evidence that follow-ups are being ignored.

## Gotchas

- **Performance**: don't write this as a per-row correlated subquery against raw `exotel_calls` (`WHERE customer_number = ... AND call_time >= due_date`, computed once per lead) — that killed the database connection on a ~40k-row test. Pre-aggregate calls into an array per phone number first (`call_arrays` CTE above), then look up against the small array per row instead.
- "No Matched Call" here is a lower bar to clear than it sounds — it means no call *at or after* the due date matched, not that the lead was never called at all (they may well have had calls before the due date, e.g. the one that led to scheduling it).
- Same phone-matching caveats apply throughout (last-10-digits match, `call_did_status` not used per the standing rule in `conventions.md`).

## Owner

TBD

**Last verified:** 2026-09-12
