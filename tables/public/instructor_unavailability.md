# public."Instructor Unavailability"

**Status:** Currently empty (0 rows) — likely superseded by another mechanism.

**Note on table name:** the actual Postgres table name contains a space — `"Instructor Unavailability"` — and must be double-quoted in SQL. (This file is named `instructor_unavailability.md` for filesystem-friendliness only.)

**Purpose (intended):** One blocked time-slot per instructor.

**Grain:** One row per (instructor, booked slot).

## Columns

| Column | Type | Nullable | Notes |
|---|---|---|---|
| instructor_id | text | no | PK **and** FK → `Instructor.id_instructor` (one row per instructor, not composite with date — odd for an "unavailability list" unless it's meant to hold just the *next/current* blocked slot) |
| booked_date | date | yes | |
| booked_start_time, booked_end_time | text | yes | stored as text, not `time` |

## Relationships

`instructor_id` → `Instructor.id_instructor`.

## Gotchas

- **0 rows currently.** `Instructor.unavailability` (a `jsonb` column on the `Instructor` table itself) may be the actual mechanism in use instead of this table — confirm with the owner before building anything that depends on this table having data.
- PK is `instructor_id` alone, meaning at most one row per instructor — not a full history/list of blocked slots.

**Owner:** TBD
**Last verified:** 2026-09-12
