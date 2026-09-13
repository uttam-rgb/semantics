# public.app_settings

**Status:** Internal config/key-value store — not relevant to business metrics. Identical to `analytics.app_settings` (same 1 row) — either schema is fine.

**Purpose:** Generic application settings, stored as key/JSON-value pairs.

**Grain:** One row per setting key. Only 1 row currently.

## Columns

| Column | Type | Nullable | Notes |
|---|---|---|---|
| id | text | no | PK |
| key | text | no | |
| value | jsonb | no | |
| description | text | yes | |
| created_at, updated_at | timestamp (no tz) | no, default CURRENT_TIMESTAMP | |

## Relationships

None.

**Owner:** TBD
**Last verified:** 2026-09-12
