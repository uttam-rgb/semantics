---
metric: speed_to_call
aliases: [lead response time, speed to call, leads called within, time to first call]
status: confirmed
owner: TBD
confirmed_by: "Uttam — logic newly constructed by Claude from the spreadsheet's plain-English definitions (no SQL_Logic file covers this), verified against live data 2026-09-12; independently reproduces the spreadsheet's own Known Caveat C-03"
confirmed_date: 2026-09-12
last_verified: 2026-09-12
source: "analytics.cratio_leads_analytics joined to public.exotel_calls"
grain: one row per office-hours lead
time_field: lead_created_time
dimensions: []
---

## Definition

For each lead created during office hours, find its **first matched outbound call** (earliest `exotel_calls` row, by phone match, with `start_time >= lead_created_time`) and bucket the elapsed time: within 5 min / 15 min / 60 min / 24 hours / after 24 hours / no matched call at all.

**Office hours filter (D-07 in the spreadsheet)**: only leads created between **10:00 and 20:00 IST** count — this keeps overnight leads (which naturally wait until morning) from making response times look artificially slow. Implemented as `EXTRACT(HOUR FROM lead_created_time) BETWEEN 10 AND 19` — `lead_created_time` is already IST wall-clock (see `conventions.md`), no timezone conversion needed.

## ⚠️ Expect this metric to look bad — that's a confirmed data pattern, not a bug

**Independently reproduced the spreadsheet's Known Caveat C-03** rather than just trusting it: of 45,801 office-hours leads, **38,093 (83%) have no matched outbound call at all**, and **zero** fall into the 5/15/60-minute buckets. The fastest lead-to-first-call gap found here is **1h53m** (the spreadsheet states 1h23m — close but not identical, likely a small scope difference in exactly which leads/calls were included; the core finding is the same either way: **no lead in this dataset has ever been called within roughly 1.5–2 hours of creation**).

Two live hypotheses from the spreadsheet, neither confirmed: (a) fast calls happen through a channel that doesn't phone-match (agent mobile, WhatsApp — consistent with `call_did_status`'s near-total disjointness from this same telephony data, see `conventions.md`), or (b) there's a genuine ~1.5+ hour floor in real response time. **Don't report this metric's fast buckets as "0, needs fixing"** — they're zero because of a measurement/process reality already flagged by the business, not a query error.

## Verified SQL

```sql
with office_hours_leads as (
    select mobile_number, lead_owner, lead_created_time
    from analytics.cratio_leads_analytics
    where lead_created_time is not null
      and mobile_number is not null
      and extract(hour from lead_created_time) between 10 and 19
      and lead_created_time::date between {{start_date}} and {{end_date}}
),
first_call as (
    select right(to_number, 10) as customer_number, min(start_time::timestamp) as first_call_time
    from public.exotel_calls
    where direction != 'inbound'
    group by 1
)
select
    case
        when fc.first_call_time is null then 'No Matched Call'
        when fc.first_call_time < l.lead_created_time then 'Call before lead_created_time (edge case, ~0.05% of rows)'
        when fc.first_call_time - l.lead_created_time <= interval '5 minutes' then 'Within 5 min'
        when fc.first_call_time - l.lead_created_time <= interval '15 minutes' then 'Within 15 min'
        when fc.first_call_time - l.lead_created_time <= interval '60 minutes' then 'Within 60 min'
        when fc.first_call_time - l.lead_created_time <= interval '24 hours' then 'Within 24 hours'
        else 'After 24 hours'
    end as bucket,
    count(*) as lead_count
from office_hours_leads l
left join first_call fc on fc.customer_number = l.mobile_number
group by 1
order by lead_count desc;
```

Verified 2026-09-12, all-time, office-hours leads only (45,801 total):

| Bucket | Lead count |
|---|---|
| No Matched Call | 38,093 (83.2%) |
| After 24 hours | 4,258 |
| Within 24 hours | 3,424 |
| Within 60 min | 0 |
| Within 15 min | 0 |
| Within 5 min | 0 |
| Call before lead_created_time (edge case) | 21 |

## Gotchas

- **`exotel_calls.start_time` is `varchar`, not a real timestamp** — must `::timestamp` cast before any date arithmetic (already documented in `tables/public/exotel_calls.md`, re-confirmed here after hitting the type error directly while building this).
- The "first call" is the earliest call **at or after** `lead_created_time` for that phone number — a call to the same number *before* the lead was created (21 edge-case rows here) is excluded from the bucketing, since it can't be a response to this lead.
- Phone-number matching (last-10-digits) is the same best-effort join as `call_activity.md` — a lead with a real call that never phone-matches looks identical to a lead that was genuinely never called. This is very likely the dominant reason "No Matched Call" is 83%, not proof that 83% of leads are truly untouched by any human.
- `call_did_status` was **not** used anywhere in this calculation, per the standing rule in `conventions.md`.

## Owner

TBD

**Last verified:** 2026-09-12
