# analytics.instructor_utilisation

**Status:** ⚠️ STALE AND UNUSED — contains data for exactly one week (2026-04-27 to 2026-05-03), despite being designed as a recurring weekly table. As of this doc's verification date (2026-09-12), it is ~4.5 months out of date. **Confirmed (2026-09-12) via production Metabase SQL: the real, live instructor-utilization report does not use this table at all** — it recomputes booked hours fresh from `analytics."Schedule"` joined to `analytics.instructor_availability` every time it runs. See [`metrics/instructor_utilization.md`](../../metrics/instructor_utilization.md) for the actual logic. This table (and [`instructor_utilisation_trailing`](instructor_utilisation_trailing.md)) look like an abandoned earlier approach.

**Purpose:** Weekly utilization percentage per instructor — booked hours vs. working hours.

**Grain:** Intended to be one row per (instructor, week). In practice, only one week exists.

## Columns

| Column | Type | Nullable | Notes |
|---|---|---|---|
| id | integer (serial) | no | PK |
| week_start, week_end | date | no | unique per instructor — only `2026-04-27`/`2026-05-03` present |
| instructor_id | text | yes | conceptual FK → `Instructor.id_instructor` (confirm schema) |
| instructor | text | yes | display name, redundant with `instructor_id` |
| working_hours | numeric | yes | hours the instructor was available that week |
| booked_hours | numeric | yes | hours actually booked |
| utilisation_pct | numeric | yes | `booked_hours / working_hours × 100`, presumably — not independently verified |
| computed_at | timestamp (no tz) | yes | when this batch ran |

## Relationships

`instructor_id` conceptually → `Instructor.id_instructor` (confirm schema — `public.Instructor` or `analytics.Instructor`).

## Gotchas

- **Only one week of data exists.** A "utilization trend over time" report built on this table will look broken (one data point), not because the query is wrong but because the computing job apparently only ran once.
- Confirm with the owner whether this table's batch job is expected to run again, or whether `instructor_utilisation_trailing` has fully replaced it.

**Owner:** TBD
**Last verified:** 2026-09-12
