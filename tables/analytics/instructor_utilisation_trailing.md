# analytics.instructor_utilisation_trailing

**Status:** ⚠️ UNUSED — confirmed 2026-09-12 via production Metabase SQL that the real, live instructor-utilization report does not use this table (or [`instructor_utilisation`](instructor_utilisation.md)) at all; it recomputes booked hours fresh from `analytics."Schedule"` joined to `analytics.instructor_availability` every time it runs. See [`metrics/instructor_utilization.md`](../../metrics/instructor_utilization.md) for the actual logic. Still more current than `instructor_utilisation` (last computed 2026-08-27 vs. that table's stale 2026-04-27), but appears to be an abandoned earlier approach either way. Still a **single point-in-time snapshot**, not a time series — every row shares the same `computed_at` value.

**Purpose:** A trailing/rolling-window utilization figure per instructor (28-day realized hours vs. weekly working hours), as opposed to the fixed-week version in `instructor_utilisation`.

**Grain:** One row per instructor — enforced by PK on `id_instructor`. 50 rows, 50 distinct instructors.

## Columns

| Column | Type | Nullable | Notes |
|---|---|---|---|
| id_instructor | text | no | PK |
| instructor_name | text | yes | |
| working_hours_weekly | numeric | yes | expected/available hours per week |
| realized_hours_28d | numeric | yes | actual booked/worked hours over the trailing 28 days |
| utilisation_pct | numeric | yes | derived from the two fields above, presumably — not independently verified |
| computed_at | timestamp with tz | yes, default now() | **all 50 rows share the same timestamp (2026-08-27)** — this is a single batch snapshot, not updated per-instructor independently |

## Relationships

`id_instructor` conceptually → `Instructor.id_instructor` (confirm schema).

## Gotchas

- All rows share one `computed_at` — there's no historical trend here, just "current utilization as of the last time this job ran." If the job hasn't rerun since 2026-08-27, this data is stale by however long it's been since then.
- Confirm with the owner how often this batch job is supposed to run, since neither utilization table currently looks like a live/continuously-updated metric.

**Owner:** TBD
**Last verified:** 2026-09-12
