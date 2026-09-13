# exotel.sync_history

**Status:** ⚠️ NOT IN USE — companion to `exotel.call_logs`, same caveat applies. Use `public.exotel_sync_history` for the real sync log.

**Purpose (intended):** Tracks each sync run that pulls call data from Exotel into `exotel.call_logs` — status, record counts, timing, errors.

**Grain:** One row per sync run.

**Current state (verified 2026-09-12):** 1 row total — a single run logged as `SUCCESS` on 2026-08-03, but with `records_fetched = 0` and `records_inserted = 0`. No sync has run since; this table has not received a second row.

## Columns

| Column | Type | Nullable | Notes |
|---|---|---|---|
| id | uuid | no | PK, default `gen_random_uuid()` |
| last_synced_at | timestamp (no tz) | no | |
| sync_status | varchar(20) | no | only value observed so far: `SUCCESS` |
| records_fetched | integer | no, default 0 | |
| records_inserted | integer | no, default 0 | |
| error_message | text | yes | |
| sync_started_at | timestamp (no tz) | no, default now() | |
| sync_completed_at | timestamp (no tz) | yes | |

## Relationships

None — no FK to `exotel.call_logs`; purely a log table.

## Gotchas

- Only one historical row — not useful for monitoring sync health right now. Compare against `public.exotel_sync_history`, which is actively updated (latest `last_synced_at` = 2026-09-12, same day this doc was verified) and reflects the real, running sync job.

**Owner:** TBD
**Last verified:** 2026-09-12
