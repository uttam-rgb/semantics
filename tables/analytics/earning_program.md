# analytics.earning_program

**Status:** Live — the list of referral/bonus programs shown to instructors in-app. Small, static-ish reference table (4 rows).

**Purpose:** Defines each earning/referral program's display copy and payout amount.

**Grain:** One row per program.

## Columns

| Column | Type | Notes |
|---|---|---|
| id | text | |
| key | text | program identifier, e.g. `refer_learner`, `refer_instructor`, `lane_cars`, `leaderboard_bonus` |
| title | text | display title |
| description | text | |
| amount_label | text | free-text payout description (not a structured number), e.g. `"₹500 per referral"` |
| status_pill | text | |
| cta_label, cta_url | text | call-to-action button |
| icon_bg | text | UI styling |
| is_active | boolean | |
| sort_order | bigint | |
| updated_at | timestamp with tz | |

## Programs observed (verified 2026-09-12)

| key | title | amount_label | is_active |
|---|---|---|---|
| `refer_learner` | Refer a new learner | ₹500 per referral | true |
| `refer_instructor` | Refer a new instructor | ₹3000 per instructor (after 50 classes) | true |
| **`lane_cars`** | **Refer a car buyer** | ₹1500 per sale | true |
| `leaderboard_bonus` | Monthly top instructor bonus | 0 (inactive) | false |

**⚠️ Notable: the `lane_cars` program ("Refer a car buyer") is very likely the connection to the unexplained `car_inventory`/`sell_leads`/`buyer_request` tables** (bucket G in `future_work.md`) — instructors referring car buyers to a separate car-sales side of the business, earning a ₹1,500 commission per sale. **Not confirmed with the owner** — a strong lead, not a verified fact.

## Relationships

None enforced. `amount_label` is free text, not a structured amount — don't parse it programmatically without care (currency symbol, conditional clauses like "after 50 classes").

**Owner:** TBD
**Last verified:** 2026-09-12
