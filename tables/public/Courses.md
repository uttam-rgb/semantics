# public.Courses

**Status:** Simple lookup/reference table. Identical to `analytics.Courses` (same 11 rows, same columns, same timestamps) — either schema is fine to query.

**Purpose:** The catalog of course offerings (e.g., a standard driving course package) — name, price, structure.

**Grain:** One row per course offering. Only 11 rows — small, static reference data.

## Columns

| Column | Type | Nullable | Notes |
|---|---|---|---|
| id | text | no | PK |
| name | text | yes | |
| code | bigint | yes | short course code |
| duration | bigint | yes | unit not confirmed (days? weeks?) — verify with owner before using in a metric |
| total_lessons | bigint | yes | expected number of lessons in the course |
| price | bigint | yes | list price, whole-number rupees presumably |
| enabled | boolean | yes | active/available flag |

## Relationships

Referenced by `Lesson.course_id`, `Schedule.course_id`, `enrollment.course_id`.

## Gotchas

- `duration` unit is not obvious from the schema — confirm before using in any duration-based metric.
- `price` here is the *list* price for the course; actual amount paid lives on `payment`/`enrollment` and may differ (discounts, partial payments).

**Owner:** TBD
**Last verified:** 2026-09-12
