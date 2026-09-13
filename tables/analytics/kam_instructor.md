# analytics.kam_instructor

**Status:** Live mapping table — the (kam, instructor) assignment, not a duplicate of `KAM`.

**Purpose:** Which instructors each Key Account Manager is responsible for.

**Grain:** One row per (kam, instructor) assignment. 79 rows.

## Columns

| Column | Type | Notes |
|---|---|---|
| kam_id | text | → `KAM.id` |
| instructor_id | text | → `Instructor.id_instructor` (confirm schema — likely `analytics.Instructor` per [`schema_map.md`](../../schema_map.md)) |
| assigned_at | timestamp with tz | |

## Relationships

`kam_id` → `KAM.id`; `instructor_id` → `Instructor.id_instructor`. No enforced FKs.

**Owner:** TBD
**Last verified:** 2026-09-12
