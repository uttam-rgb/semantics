# public.Schedule

**Status:** ⚠️ SUPERSEDED — use `analytics.Schedule` instead. `public`'s data is frozen ~2026-03-15 (6 months stale); `analytics` has every row `public` has plus everything since, and is actively current. See [`schema_map.md`](../../schema_map.md). This doc is kept for reference on shared columns/gotchas, which also apply to the `analytics` version.

Also has a mixed grain — read the gotcha below before counting rows as "lessons."

**Purpose:** Calendar slots involving an instructor — both actual learner lesson bookings *and* instructor time-blocking entries with no learner attached.

**Grain:** One row = one calendar slot for an instructor. **Not every row is a learner lesson** (see Gotchas).

## Columns

| Column | Type | Nullable | Notes |
|---|---|---|---|
| id | bigint | no | PK |
| learner_id | text | yes | FK → `Learner.id` — **NULL for instructor-blocked slots** |
| instructor_id | text | no in practice | FK → `Instructor.id_instructor` |
| course_id | text | yes | FK → `Courses.id` |
| lesson_id | text | yes | FK → `Lesson.id` |
| date | date | no | |
| start_time, end_time | time (no tz) | no | |
| status | **text, no enum** | no, default `'booked'` | observed: `booked` (1809), `completed` (704), `paused` (49), `scheduled` (27), `topup` (22). Exact meaning of `paused`, `scheduled` (vs `booked`), and `topup` not yet confirmed with the data owner — don't assume definitions. |
| enabled | boolean | no, default `false` | purpose unclear from schema alone (possibly "instructor confirmed slot" or "slot currently active") — confirm with owner before using in a filter |
| otp | text | yes | check-in verification code, not relevant to reporting |
| calendar_uid, calendar_sequence | text/integer | yes / no default 0 | iCal sync bookkeeping, not relevant to reporting |

## Relationships

- `learner_id` → `Learner.id`
- `instructor_id` → `Instructor.id_instructor` (note: Instructor's PK column is named `id_instructor`, not `id`)
- `course_id` → `Courses.id`
- `lesson_id` → `Lesson.id`
- Not referenced by any other table.

## Gotchas

- **⚠️ Not every row represents a real lesson.** Sample rows show entries with `learner_id`, `course_id`, and `lesson_id` all NULL and only `instructor_id` populated — these look like instructor availability/blocked-time entries, not bookings. **A query like `SELECT count(*) FROM "Schedule" WHERE status = 'booked'` will overcount actual lessons booked.** Filter with `learner_id IS NOT NULL` (and likely `lesson_id IS NOT NULL`) to count real lesson bookings.
- `status` has no enforced enum, and several values (`paused`, `scheduled`, `topup`) have ambiguous meaning — confirm with the owner before building a metric that buckets by status.
- `enabled` defaults to `false`, which is unusual for a "booked" default — don't assume `enabled = true` means "confirmed lesson" without checking with the owner.

**Owner:** TBD
**Last verified:** 2026-09-12
