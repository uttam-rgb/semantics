# public."Learner Availability"

**Status:** Currently empty (0 rows) — likely superseded by another mechanism.

**Note on table name:** the actual Postgres table name contains a space — `"Learner Availability"` — and must be double-quoted in SQL. (This file is named `learner_availability.md` for filesystem-friendliness only.)

**Purpose (intended):** A learner's available timeslots per day of week.

**Grain:** One row per (learner, day of week).

## Columns

| Column | Type | Nullable | Notes |
|---|---|---|---|
| learner_id | text | no | PK **and** FK → `Learner.id` (one row per learner — see gotcha) |
| day_of_the_week | text | yes | free text, not the `smallint` encoding used in `schedule_preferences.day_of_week` |
| list_of_available_timeslots | jsonb | yes | |

## Relationships

`learner_id` → `Learner.id`.

## Gotchas

- **0 rows currently.** `schedule_preferences` (day_of_week + time_slot enum) looks like the actively-used replacement for this concept — confirm with the owner before relying on this table.
- PK is `learner_id` alone (not composite with day), so this table structurally can't hold more than one row per learner despite "day of week" suggesting multiple rows — another sign it's deprecated in favor of `schedule_preferences`.

**Owner:** TBD
**Last verified:** 2026-09-12
