# analytics.qr_codes

**Status:** Live, tiny (2 rows) — a marketing QR-code generator/tracker.

**Purpose:** QR codes generated for marketing campaigns, with scan-count rollups.

**Grain:** One row per QR code.

## Columns

| Column | Type | Notes |
|---|---|---|
| id | text | |
| created_at | timestamp with tz | |
| name, description, campaign | text | one sample is explicitly test data (`name='Test QR 1750446399768'`) |
| destination_url | text | where the QR code redirects to |
| short_code | text | |
| qr_image_url | text | |
| total_scans, unique_users | bigint | precomputed rollups — presumably kept in sync with `qr_scans`, but that table is currently empty (see below), so these may not be live-updating |
| is_active | boolean | |

## Relationships

Referenced by `qr_scans.qr_code_id` (not enforced).

## Gotchas

- One of the two existing rows is explicit test data.
- `qr_scans` (the presumed source of `total_scans`/`unique_users`) has 0 rows — these rollup columns may be static/manually set rather than derived, or the scan-logging pipeline may not be wired up yet. Don't assume they're live.

**Owner:** TBD
**Last verified:** 2026-09-12
