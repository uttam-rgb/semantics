---
metric: hourly_split
aliases: [leads created by hour, calls made by hour, hourly split, time of day analysis]
status: confirmed
owner: TBD
confirmed_by: "Uttam — same underlying metrics as lead_volume.md/call_activity.md, just broken out by hour-of-day instead of owner/date; timezone handling verified empirically by Claude against real data, 2026-09-12"
confirmed_date: 2026-09-12
last_verified: 2026-09-12
source: "analytics.cratio_leads_analytics (leads) and public.exotel_calls (calls)"
grain: "one row per lead (Leads Created) / one row per outbound call (Calls Made)"
time_field: "lead_created_time (leads) / date_created (calls) — NOT lead_date or created_at, see gotchas"
dimensions: [hour_of_day]
---

## Definition

**Not new metrics** — "Leads Created by Hour" is `lead_volume.md`'s lead count, and "Calls Made by Hour" is `call_activity.md`'s call count, both broken out by hour-of-day instead of owner/date. Same duplication-check as `source_wise_summary.md` — don't re-derive the underlying counts, just add the hour breakout.

## ⚠️ Timezone finding, verified against real data (2026-09-12)

The spreadsheet's convention says all hour-of-day bucketing should be in **IST (Asia/Kolkata)**. Checked whether the relevant timestamp columns need conversion or are already in IST:

- **`cratio_leads_analytics.lead_created_time`** (`timestamp without time zone`) — tested `EXTRACT(HOUR FROM lead_created_time)` with no conversion vs. with an explicit `AT TIME ZONE 'Asia/Kolkata'` shift. The **unconverted** version produces a sensible daytime curve (low overnight, rising through the morning, peaking around 2pm and 5pm, tapering by 11pm); the "converted" version produces a nonsensical curve (heavy overnight activity, dead during business hours) — because the column is **already stored as IST wall-clock time**, despite having no timezone suffix. Applying `AT TIME ZONE` on top double-shifts it. **Use `EXTRACT(HOUR FROM lead_created_time)` directly — no conversion.**
- **`public.exotel_calls.date_created`** (stored as `text`, format `'YYYY-MM-DD HH24:MI:SS'`) — same check: `EXTRACT(HOUR FROM date_created::timestamp)` with no conversion produces a clean pattern matching the spreadsheet's documented 10:00–20:00 IST office hours almost exactly (near-zero 0–4am, ramping from 5am, sustained 10am–8pm, dropping off after 9pm). **Also already IST, use directly, no conversion.**

**This confirms the spreadsheet's own fix** (Change Log: switched from `exotel_calls.created_at` to `date_created` for this exact reason) — verified independently here rather than just taken on faith: `created_at`'s hour distribution is heavily clustered into 3 hours (6, 16, 8 — tens of thousands of rows each), the batch-sync artifact the spreadsheet describes, completely unlike a real calling pattern.

**Caution, not yet checked elsewhere**: naive (`timestamp without time zone`) columns in this database appear to store IST wall-clock time rather than UTC, at least for these two. Don't assume this holds for every timestamp column in the schema without checking — verify per-column if hour-of-day or elapsed-time precision matters (as it will for the Speed-to-Call metrics, still unbuilt).

## Verified SQL

```sql
-- Leads Created by Hour
select
    extract(hour from lead_created_time) as hour_of_day,
    count(*) as leads_created
from analytics.cratio_leads_analytics
where lead_created_time::date between {{start_date}} and {{end_date}}
group by 1
order by 1;
```

```sql
-- Calls Made by Hour (outbound only, same direction filter as call_activity.md)
select
    extract(hour from date_created::timestamp) as hour_of_day,
    count(*) as calls_made
from public.exotel_calls
where date_created::date between {{start_date}} and {{end_date}}
  and direction != 'inbound'
group by 1
order by 1;
```

All-time hour distributions, verified 2026-09-12:

| Hour (IST) | Leads Created | Calls Made |
|---|---|---|
| 0–4 | low, ramps from ~640 (0h) to ~3,540 (4h) | negligible (≤3 each) |
| 5–9 | rising, ~3,975–4,640 | ramping, 20→191 |
| 10–13 | steady ~4,150–4,400 | jumps to 2,000–6,400 (office hours begin) |
| 14 | spike: 7,872 | dips to 1,734 (notable dip mid-peak, not investigated) |
| 15–19 | 4,260–5,326 | sustained 4,670–5,600 |
| 20–23 | falling to ~480 by 23h | falls off sharply after 20h |

Calls Made tracks the spreadsheet's documented 10:00–20:00 IST office-hours window closely. Leads Created has a broader spread (leads arrive around the clock, presumably from ads/website traffic that doesn't stop at night) — makes sense since lead generation isn't restricted to office hours the way outbound calling is.

## Gotchas

- **`lead_created_time` is a real timestamp; `lead_date` is not the same thing to use here** — `lead_date` is used elsewhere (`lead_volume.md`) for day-level windowing, but for hour-of-day specifically, use `lead_created_time` (has the actual time-of-day; other date fields on this table are `text` or date-only).
- **`date_created` is `text`, not a real timestamp** — must `::timestamp` cast before extracting the hour. Confirmed clean format (`'YYYY-MM-DD HH24:MI:SS'`) in the rows checked, but not exhaustively verified across all rows.
- The hour-14 dip in Calls Made (a notable drop right after the 10–13 ramp) is visible in the data but not explained — could be a lunch break pattern, could be something else. Not investigated further.

## Owner

TBD

**Last verified:** 2026-09-12
