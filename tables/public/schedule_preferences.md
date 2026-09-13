# public.schedule_preferences

**Status:** ⚠️ SUPERSEDED — use `analytics.schedule_preferences` instead (identical columns; `public` is frozen ~2026-03-15, `analytics` has every row plus everything since). See [`schema_map.md`](../../schema_map.md).

**Purpose:** A learner's preferred day-of-week + time-slot combinations for scheduling lessons. A learner typically has multiple rows (one per preferred day/slot).

**Grain:** One row = one (learner, day_of_week, time_slot) preference.

## Columns

| Column | Type | Nullable | Notes |
|---|---|---|---|
| id | text | no | PK |
| learner_id | text | no | FK → `Learner.id` |
| day_of_week | smallint | no | numeric day encoding — **which convention (0=Sunday vs 0=Monday) is not confirmed; verify before using in a day-of-week report** |
| time_slot | enum `TimeSlot` | no | hour-range buckets: `5-6`, `6-9`, `9-12`, `12-15`, `15-18`, `18-21`, `21-23` |
| created_at, updated_at | timestamp (no tz) | no, default CURRENT_TIMESTAMP | |

## Relationships

`learner_id` → `Learner.id`. Not referenced by any other table.

## Gotchas

- `day_of_week` numbering convention unverified — don't assume ISO (Monday=0/1) or US (Sunday=0) without checking actual app code or asking the owner.

**Owner:** TBD
**Last verified:** 2026-09-12
