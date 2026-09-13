# public.exotel_sync_history

**Status:** ✅ Authoritative — the real, actively-updated sync log. (Do not use `exotel.sync_history` — see [`schema_map.md`](../../schema_map.md).)

**Purpose:** Records the timestamp of the last successful sync run pulling call data from Exotel into `public.exotel_calls`.

**Table comment (from Postgres):** "Tracks the last successful synchronization timestamp"

**Grain:** One row per sync run — though in practice this table appears to hold a small, rolling set of rows (row count = 1 at time of writing, with `id` already at 4), suggesting rows may be updated/replaced rather than strictly appended. Confirm this with whoever owns the sync job before relying on it for a full sync history/audit trail.

## Columns

| Column | Type | Nullable | Notes |
|---|---|---|---|
| id | integer (serial) | no | PK |
| last_synced_at | timestamp (no tz) | no | most recent successful sync time |
| created_at | timestamp (no tz) | yes, default CURRENT_TIMESTAMP | |
| updated_at | timestamp (no tz) | yes, default CURRENT_TIMESTAMP | |

## Relationships

None.

## Gotchas

- Only tracks `last_synced_at`, not per-run record counts or errors (unlike the unused `exotel.sync_history`, which has richer columns for that but no real data). If you need sync health/volume monitoring, this table alone isn't enough — you'd derive it from `public.exotel_calls.created_at` instead.

**Owner:** TBD
**Last verified:** 2026-09-12
