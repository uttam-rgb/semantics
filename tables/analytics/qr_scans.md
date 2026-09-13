# analytics.qr_scans

**Status:** ☠️ Not yet in use — 0 rows.

**Purpose (intended):** Per-scan detail for `qr_codes` — device, location, referrer.

**Grain:** One row per scan event.

## Columns

All unpopulated: `id`, `created_at` (⚠️ text, not timestamp), `user_id`, `ip_address`, `device`, `os`, `browser`, `city`, `country`, `user_type`, `user_agent`, `referrer`, `qr_code_id` (→ `qr_codes.id`).

## Relationships

`qr_code_id` → `qr_codes.id` (not enforced).

## Gotchas

- Despite this table being empty, `qr_codes.total_scans`/`unique_users` show non-zero values in one row — those rollups aren't derived from this table's data (or aren't kept in sync with it). Don't assume this table is where scan counts come from.

**Owner:** TBD
**Last verified:** 2026-09-12
