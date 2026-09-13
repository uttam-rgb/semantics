# analytics.instructor_availability

**Status:** ✅ Live — this, not `instructor_utilisation`/`instructor_utilisation_trailing`, is what the real production instructor-utilization report actually uses. See [`metrics/instructor_utilization.md`](../../metrics/instructor_utilization.md).

**Purpose:** Each active instructor's expected weekly working hours and area — the denominator for utilization calculations.

**Grain:** One row per instructor. 147 rows at last check.

## Columns

| Column | Type | Notes |
|---|---|---|
| id | integer | PK |
| instructor_id | text | → `Instructor.id_instructor` |
| instructor_name | text | |
| instructor_phone | text | |
| original_name | text | purpose unclear — possibly a pre-normalization name field |
| working_hours | numeric | expected hours/week — the utilization denominator |
| status | text | `active` (59 rows) / `inactive` (92 rows) — production utilization query filters `status = 'active'` |
| area | text | |
| address | text | |
| attribute | text | finer-grained state, added 2026-09-12: `Online` (52), `On Break` (7), `Inactive` (92) — **perfectly correlated with `status`**: every `inactive` row has `attribute='Inactive'`, every `active` row is either `Online` or `On Break`. No NULLs observed despite the production query defensively `COALESCE`-ing to `'Online'`. |

## Relationships

`instructor_id` → `Instructor.id_instructor` (confirm schema — see [`schema_map.md`](../../schema_map.md); `analytics.Instructor` is the live one).

## Gotchas

- Filter `status = 'active'` before computing utilization — inactive instructors shouldn't count toward staffing gap calculations.
- `original_name` purpose is unconfirmed.
- **`On Break` instructors are still included in `status='active'`** — a 0% or low utilization number for one of these instructors may reflect a temporary break, not low demand/lead flow. Don't feed "On Break" instructors' gaps into staffing/lead-need calculations without accounting for this — see [`metrics/instructor_utilization.md`](../../metrics/instructor_utilization.md).

**Owner:** TBD
**Last verified:** 2026-09-12
