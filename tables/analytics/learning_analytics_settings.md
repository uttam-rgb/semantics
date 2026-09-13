# analytics.learning_analytics_settings

**Status:** Live — a singleton flag marking when e-learning tracking began.

**Purpose:** Records when the `learning_content`/`learning_sessions` tracking feature was turned on — 2026-09-11 at last check (one day before this doc's verification date). Explains why `learning_sessions` only has 12 rows: the feature is brand new, not abandoned.

**Grain:** One row, always (`singleton = true`).

## Columns

| Column | Type | Notes |
|---|---|---|
| singleton | boolean | always `true` |
| tracking_since | timestamp with tz | 2026-09-11 at last check |

## Relationships

None.

**Owner:** TBD
**Last verified:** 2026-09-12
