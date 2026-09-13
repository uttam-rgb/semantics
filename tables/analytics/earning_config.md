# analytics.earning_config

**Status:** Live — global configuration for the instructor earnings/payout feature (a singleton row).

**Purpose:** Platform-wide defaults for instructor pay and the earnings-leaderboard feature.

**Grain:** One row, global config (id=1). Not per-instructor.

## Columns

| Column | Type | Notes |
|---|---|---|
| id | bigint | always 1 in practice |
| default_per_class_rate | double precision | ₹425 at last check — default pay per class taught |
| default_monthly_target | bigint | 30 (classes/month) at last check |
| payout_day | text | e.g. `'Monday'` — day of week payouts run |
| leaderboard_top_n | bigint | e.g. 10 — how many instructors shown on the earnings leaderboard |
| leaderboard_bonus_amount | double precision | 0.0 at last check |
| tip_copy | text | UI copy shown to instructors (e.g. referral tips) |
| availability_message_template | text | UI template string for an instructor's "I have free slots" message |
| updated_at | timestamp with tz | |

## Relationships

None — a config singleton, not linked to other tables.

**Owner:** TBD
**Last verified:** 2026-09-12
