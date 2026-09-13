# analytics.instructor_status_log

**Status:** Live, low-volume (32 rows).

**Purpose:** Audit trail of instructor status changes (e.g., active ↔ inactive), including who made the change.

**Grain:** One row per status-change event.

## Columns

| Column | Type | Notes |
|---|---|---|
| id | text | |
| instructor_id | text | → `Instructor.id_instructor` |
| old_status, new_status | text | e.g. `'active'`/`'inactive'` — matches `analytics.Instructor.status` and `analytics.instructor_availability.status` vocabulary |
| changed_by | text | free-text name + phone, e.g. `'Ankit Kumar Soni (7501672228)'` — not a foreign key to any admin/user table |
| changed_at | timestamp with tz | |

## Relationships

`instructor_id` → `Instructor.id_instructor` (not enforced).

**Owner:** TBD
**Last verified:** 2026-09-12
