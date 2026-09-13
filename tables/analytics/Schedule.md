# analytics.Schedule

**Status:** ✅ Authoritative — use this, not `public.Schedule` (frozen ~2026-03-15, see [`schema_map.md`](../../schema_map.md)). 24,584 rows, current through 2026-09-11.

**Purpose:** Calendar slots involving an instructor — both actual learner lesson bookings *and* instructor time-blocking entries with no learner attached.

**Grain:** One row = one calendar slot for an instructor. **Not every row is a learner lesson** (see Gotchas).

## Columns

All columns from `public.Schedule` (see [`tables/public/Schedule.md`](../public/Schedule.md) for the shared column reference: `id`, `learner_id`, `instructor_id`, `course_id`, `lesson_id`, `date`, `start_time`, `end_time`, `status`, `enabled`, `otp`, `calendar_uid`, `calendar_sequence`, `created_at`), **plus these analytics-only columns**:

| Column | Notes |
|---|---|
| isTentative | boolean, presumably — a slot pending confirmation |
| leadName | text — suggests some Schedule rows originate directly from a lead, not an existing Learner |
| tentative_details | freeform, presumably JSON-shaped |
| started_at, ended_at | actual lesson start/end (vs. planned `start_time`/`end_time`) — used directly by [`metrics/instructor_utilization.md`](../../metrics/instructor_utilization.md)'s live booked-hours calculation via `start_time`/`end_time`, not these — confirm whether `started_at`/`ended_at` should be preferred once populated |
| otp_end | a second OTP field, purpose vs. `otp` unclear |
| pause_reason, pause_notes | supports a "paused" lesson state — consistent with `status = 'paused'` observed in the data |

## Relationships

Same as `public.Schedule`: `learner_id` → `Learner.id`, `instructor_id` → `Instructor.id_instructor`, `course_id` → `Courses.id`, `lesson_id` → `Lesson.id`.

## Gotchas

Everything in [`tables/public/Schedule.md`](../public/Schedule.md) applies here too (mixed grain — instructor-blocked slots with no `learner_id` — and undocumented `status` values `paused`/`scheduled`/`topup`). Additionally:
- `leadName` existing as a column suggests some scheduling can happen straight from a lead before a `Learner` record exists — worth understanding if `learner_id` is ever NULL specifically because of this, vs. being a pure instructor-block row.

**Owner:** TBD
**Last verified:** 2026-09-12
