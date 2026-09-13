# analytics.game_analytics_settings

**Status:** Live — a singleton flag marking when in-app "game" tracking began.

**Purpose:** Records when `game_launch_events` tracking was turned on — 2026-09-08 at last check (4 days before this doc's verification date). Explains why `game_launch_events` only has 23 rows: the feature is brand new.

**Grain:** One row, always (`singleton = true`).

## Columns

| Column | Type | Notes |
|---|---|---|
| singleton | boolean | always `true` |
| tracking_since | timestamp with tz | 2026-09-08 at last check |

## Relationships

None.

**Owner:** TBD
**Last verified:** 2026-09-12
