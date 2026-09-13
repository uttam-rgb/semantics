# analytics.schedule_no_show

**Status:** Live, low-volume (57 rows).

**Purpose:** Reports of a learner or instructor not showing up for a scheduled lesson.

**Grain:** One row per no-show report.

## Columns

| Column | Type | Notes |
|---|---|---|
| id | text | |
| schedule_id | bigint | → `Schedule.id` |
| no_show_party | text | e.g. `'learner'` — who didn't show |
| reported_by | text | e.g. `'instructor'` — who filed the report |
| reporter_instructor_id | text | → `Instructor.id_instructor` |
| note | text | mostly NULL in samples seen |
| status | text | e.g. `'open'` |
| resolution, resolved_by | text | |
| resolved_at | text | ⚠️ text, not timestamp |
| created_at, updated_at | timestamp with tz | |

## Relationships

`schedule_id` → `Schedule.id`; `reporter_instructor_id` → `Instructor.id_instructor`. Neither enforced.

**Owner:** TBD
**Last verified:** 2026-09-12
