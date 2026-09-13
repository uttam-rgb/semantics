# analytics.KAM

**Status:** Live, small reference table. Not a duplicate of `kam_instructor` — different grain (see below).

**Purpose:** Key Account Manager (KAM) master list — the people, not an assignment table.

**Grain:** One row per KAM. Only 5 rows.

## Columns

| Column | Type | Notes |
|---|---|---|
| id | text | intended PK, not enforced |
| name, phone, email | text | `email` often NULL |
| created_at, updated_at | timestamp with tz | |

## Relationships

Referenced conceptually by `kam_instructor.kam_id`.

**Owner:** TBD
**Last verified:** 2026-09-12
