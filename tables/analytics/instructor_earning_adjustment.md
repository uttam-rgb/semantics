# analytics.instructor_earning_adjustment

**Status:** ☠️ Not yet in use — 0 rows.

**Purpose (intended):** Manual adjustments (bonuses, deductions, corrections) to an instructor's payout, linked to a specific `instructor_payout` record.

**Grain:** One row per adjustment.

## Columns

All columns are `text` (including `amount`, `effective_date`, `created_at`) — will need casting once populated.

| Column | Notes |
|---|---|
| id | |
| instructor_id | → `Instructor.id_instructor` (confirm schema) |
| payout_id | → `instructor_payout.id` |
| type | e.g. bonus/deduction, presumably — no data to confirm values yet |
| amount | text, not numeric |
| reason | |
| effective_date | text, not date |
| created_by | |
| created_at | text, not timestamp |

## Relationships

`payout_id` → `instructor_payout.id`; `instructor_id` → `Instructor.id_instructor`. Neither enforced.

## Gotchas

- 0 rows — this whole payout-adjustment feature appears unlaunched. Confirm with the owner before assuming it's relevant to any current reporting.

**Owner:** TBD
**Last verified:** 2026-09-12
