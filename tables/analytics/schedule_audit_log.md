# analytics.schedule_audit_log

**Status:** ☠️ Not yet in use — 0 rows.

**Purpose (intended):** Before/after audit trail for changes to `Schedule` rows.

**Grain:** One row per change event.

## Columns

`id`, `schedule_id` (→ `Schedule.id`), `old_data`, `new_data` (presumably JSON-shaped snapshots, stored as text), `changed_at` (⚠️ text, not timestamp) — all unpopulated.

## Relationships

`schedule_id` → `Schedule.id` (not enforced, confirm schema).

**Owner:** TBD
**Last verified:** 2026-09-12
