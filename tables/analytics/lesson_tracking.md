# analytics.lesson_tracking

**Status:** GPS/location tracking log — **not** a "lessons completed" count table (correcting an earlier assumption from the triage pass).

**Purpose:** Location pings captured during a scheduled lesson — start/end markers plus periodic tracking pings, presumably for safety/verification purposes.

**Grain:** One row per location ping (or start/end marker) during a lesson.

## Columns

| Column | Type | Nullable | Notes |
|---|---|---|---|
| id | text | yes | |
| schedule_id | bigint | yes | conceptual FK → a `Schedule.id` (confirm which schema — `public.Schedule.id` is `bigint`, matches this type) |
| latitude, longitude | double precision | yes | |
| captured_at | timestamp with tz | yes | |
| type | text | yes | `tracking` (35,966 — periodic pings during the lesson), `start` (9,145), `end` (8,976) |

## Relationships

`schedule_id` conceptually joins to `Schedule.id`. No enforced FK.

## Gotchas

- **Don't use this table to count "lessons completed."** Counting `type = 'end'` rows would approximate completed lesson sessions, but with ~9,145 `start` vs 8,976 `end` (a ~170 gap), some lessons have a start but no matching end logged — verify this gap's cause before trusting a raw count.
- `schedule_id` type (`bigint`) matches `public.Schedule.id`, but confirm which schema's `Schedule` this actually points to before joining.

**Owner:** TBD
**Last verified:** 2026-09-12
