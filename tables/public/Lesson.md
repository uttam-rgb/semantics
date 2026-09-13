# public.Lesson

**Status:** Simple lookup/reference table. Identical to `analytics.Lesson` (same 49 rows, same columns, same timestamps) — either schema is fine to query.

**Purpose:** A lesson *template* within a course (e.g., "Lesson 3 of the Standard course") — not a scheduled instance. Scheduled/booked occurrences of a lesson live in `Schedule` (via `Schedule.lesson_id`).

**Grain:** One row per lesson-in-course definition. Only 49 rows.

## Columns

| Column | Type | Nullable | Notes |
|---|---|---|---|
| id | text | no | PK |
| course_id | text | yes | FK → `Courses.id` |
| number | bigint | yes | sequence number of this lesson within its course |
| duration | bigint | no, default `1` | unit not confirmed — verify before use |
| description | text | yes | |
| enabled | boolean | no, default `true` | |

## Relationships

- `course_id` → `Courses.id`
- Referenced by `Schedule.lesson_id`

## Gotchas

- Don't confuse "number of `Lesson` rows for a course" with "number of lessons a learner has completed" — the latter comes from `Schedule` (filtered to real bookings, see that table's gotcha) or `enrollment.unlocked_lessons`, not from counting this table.

**Owner:** TBD
**Last verified:** 2026-09-12
