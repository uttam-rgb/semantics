# analytics.instructor_leave_request

**Status:** Live, low-volume (29 rows).

**Purpose:** An instructor's request for time off.

**Grain:** One row per leave request.

## Columns

| Column | Type | Notes |
|---|---|---|
| id | text | |
| instructor_id | text | → `Instructor.id_instructor` |
| leave_type | text | e.g. `'planned'`, `'emergency'` |
| from_date, to_date | date | |
| all_day | boolean | |
| start_time, end_time | text | populated only when `all_day = false`, presumably |
| reason | text | mostly NULL in samples seen |
| status | text | e.g. `'pending'` |
| admin_note, reviewed_by, reviewed_at | text/timestamp | approval workflow fields |
| unavailability_applied | boolean | whether this leave has been reflected in the instructor's schedule/availability |
| created_at, updated_at | timestamp with tz | |

## Relationships

`instructor_id` → `Instructor.id_instructor` (not enforced).

**Owner:** TBD
**Last verified:** 2026-09-12
