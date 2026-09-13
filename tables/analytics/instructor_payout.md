# analytics.instructor_payout

**Status:** ☠️ Not yet in use — 0 rows.

**Purpose (intended):** Computed payout per instructor per period — classes taught, rate, gross/net amount after adjustments, payment status.

**Grain:** One row per (instructor, payout period).

## Columns

All columns are `text` (including `classes_count`, `per_class_rate`, `gross_amount`, `adjustments_total`, `net_amount`, dates) — will need casting once populated.

| Column | Notes |
|---|---|
| id | |
| instructor_id | → `Instructor.id_instructor` |
| period_start, period_end | text, not date |
| classes_count | text, not integer |
| per_class_rate | text, not numeric — presumably sourced from `instructor_earning_settings` or `earning_config` default |
| gross_amount | text, not numeric — presumably `classes_count * per_class_rate` |
| adjustments_total | text, not numeric — presumably sums `instructor_earning_adjustment` rows for this payout |
| net_amount | text, not numeric — presumably `gross_amount + adjustments_total` |
| status | no data to confirm values yet |
| payout_date | text, not date |
| created_at, updated_at | text, not timestamp |

## Relationships

`instructor_id` → `Instructor.id_instructor`. Referenced by `instructor_earning_adjustment.payout_id`. Neither enforced.

## Gotchas

- 0 rows — this entire instructor-payout system appears built but not yet launched/used. If asked about "instructor payouts" or "how much do we pay instructors," there is currently **no data to answer from** — say so rather than reporting zero as if it were a real figure.

**Owner:** TBD
**Last verified:** 2026-09-12
