---
metric: instructor_utilization
aliases: [instructor utilization, utilisation %, instructor capacity]
status: confirmed
owner: TBD
confirmed_by: Uttam (derived directly from production Metabase SQL, SQL_Logic/instructor_utz.sql)
confirmed_date: 2026-09-12
last_verified: 2026-09-12
source: "analytics.\"Schedule\" (booked hours) and analytics.instructor_availability (working hours)"
grain: one row per instructor, for a given target week
time_field: "Schedule.date, windowed to a specific week (see gotcha — defaults to NEXT week)"
dimensions: [instructor_id, area, attribute]
---

## Definition

**Not** computed from `analytics.instructor_utilisation` or `analytics.instructor_utilisation_trailing` — both of those tables are stale/single-snapshot (see their table docs) and are **not** what production actually uses. The real, live version recomputes booked hours fresh from the schedule every time it runs.

`utilisation_pct = booked_hours / working_hours * 100`, where:
- `working_hours` = `analytics.instructor_availability.working_hours` for `status = 'active'` instructors
- `booked_hours` = `SUM(EXTRACT(EPOCH FROM (end_time - start_time))/3600.0)` from `analytics."Schedule"` where `status = 'booked' AND enabled = true`, for the target week

## Verified SQL

```sql
with params as (
    select
        date_trunc('week', current_date + interval '7 days')::date as week_start,
        (date_trunc('week', current_date + interval '7 days') + interval '6 days')::date as week_end
),
booked as (
    select
        s.instructor_id,
        round(sum(extract(epoch from (s.end_time - s.start_time)) / 3600.0)::numeric, 1) as booked_hours
    from analytics."Schedule" s
    cross join params p
    where s.date between p.week_start and p.week_end
      and s.status = 'booked'
      and s.enabled = true
    group by s.instructor_id
),
first_class as (
    select instructor_id, min(date) as date_of_class_started
    from analytics."Schedule"
    where status = 'booked' and enabled = true
    group by instructor_id
)
select
    ia.instructor_name, ia.area,
    coalesce(ia.attribute, 'Online') as attribute,
    p.week_start, p.week_end,
    ia.working_hours,
    coalesce(b.booked_hours, 0) as booked_hours,
    round(coalesce(b.booked_hours,0) / nullif(ia.working_hours,0) * 100, 1) as utilisation_pct,
    case
        when coalesce(b.booked_hours, 0) = 0 then 'Zero'
        when coalesce(b.booked_hours, 0) / nullif(ia.working_hours,0) * 100 < 50 then 'Low'
        else 'Healthy'
    end as status,
    greatest(ia.working_hours - coalesce(b.booked_hours,0), 0) as gap_hours,
    round(greatest(ia.working_hours - coalesce(b.booked_hours,0),0) / 4.5, 1) as conversions_needed,
    round(greatest(ia.working_hours - coalesce(b.booked_hours,0),0) / 4.5 / 0.08 / 7, 1) as daily_leads_needed,
    i.created_at::date as date_of_joining,
    fc.date_of_class_started
from analytics.instructor_availability ia
cross join params p
left join analytics."Instructor" i on i.id_instructor = ia.instructor_id
left join booked b on b.instructor_id = ia.instructor_id
left join first_class fc on fc.instructor_id = ia.instructor_id
where ia.status = 'active'
order by utilisation_pct asc nulls first;
```

## Business constants baked into this query (document these as named assumptions, not magic numbers)

- **`week_start`/`week_end` default to *next* week** (`current_date + interval '7 days'`, truncated to week) — this is a forward-looking capacity check ("who has open slots next week"), not a retrospective utilization report. Don't assume it reports on the current or past week without adjusting the date logic.
- **4.5 hours booked = 1 "conversion"** — `conversions_needed = gap_hours / 4.5`. This assumes an average enrolled learner fills ~4.5 hours of an instructor's schedule (course length assumption, not derived from `Courses`/`Lesson` in this query — worth cross-checking against actual course duration data at some point, but treat as a confirmed business constant for now since it's used in production).
- **8% assumed lead-to-conversion rate** — `daily_leads_needed = conversions_needed / 4.5 / 0.08 / 7`, i.e., "how many leads per day, spread over a week, are needed at an assumed 8% close rate, to fill this instructor's schedule gap." This is a planning assumption, not the same as the *actual* measured `conversion_rate` metric — don't silently swap in the real conversion rate here without checking whether that's intended (it would change the staffing recommendation).
- **Utilization status bands:** Zero (0 booked hours), Low (<50%), Healthy (≥50%) — different thresholds from the alert-resolution traffic light (70/40%), don't confuse the two scales.
- **`attribute` (added 2026-09-12):** splits active instructors into `Online` (52) vs `On Break` (7) — `status='inactive'` instructors always show `attribute='Inactive'` and are already excluded by the `WHERE ia.status = 'active'` filter. **`On Break` instructors are still included in this utilization report** — a low/zero utilization score for one of them likely reflects the break, not unmet demand. Don't count an `On Break` instructor's `gap_hours`/`conversions_needed`/`daily_leads_needed` toward a staffing decision without checking `attribute` first.

## Gotchas

- Confirm whether "instructor" here should be scoped to `analytics.Instructor` (per `schema_map.md`, the live one) — the query joins on `id_instructor` which exists on both `public.Instructor` and `analytics.Instructor`.
- `analytics.instructor_utilisation` and `analytics.instructor_utilisation_trailing` (the precomputed tables) should **not** be used for this metric — they appear to be an abandoned/parallel approach. See their table docs, now updated to point here.

## Owner

TBD

**Last verified:** 2026-09-12
