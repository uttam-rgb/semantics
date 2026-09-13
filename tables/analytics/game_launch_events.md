# analytics.game_launch_events

**Status:** Live — very new feature (see `game_analytics_settings`, tracking since 2026-09-08). 23 rows reflects a 4-day-old feature, not staleness.

**Purpose:** Logs each time a learner opens an in-app educational "game" (e.g., `'master-the-roads'` seen in samples — a road-rules game, presumably).

**Grain:** One row per launch event.

## Columns

| Column | Type | Notes |
|---|---|---|
| id | text | |
| learner_id | text | → `Learner.id` (confirm schema) |
| game_id | text | e.g. `'master-the-roads'` — only value seen in the small sample checked; there may be others |
| opened_at | timestamp with tz | |

## Relationships

`learner_id` conceptually → `Learner`. No enforced FK.

## Gotchas

- Only one `game_id` value observed in a small sample — don't assume this is the only game without checking a fuller distinct-value list once more data accumulates.

**Owner:** TBD
**Last verified:** 2026-09-12
