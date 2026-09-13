# public.email_errors

**Status:** Internal ops/error-log table — not relevant to business metrics.

**Purpose:** Logs email-sending failures for debugging.

**Grain:** One row per email error. Only 2 rows.

## Columns

| Column | Type | Nullable | Notes |
|---|---|---|---|
| id | text | no | PK |
| created_at | timestamp (no tz) | no, default CURRENT_TIMESTAMP | |
| error | text | no | |
| stack | text | yes | |
| details | jsonb | yes | |
| resolved | boolean | no, default `false` | |

## Relationships

None.

**Owner:** TBD
**Last verified:** 2026-09-12
