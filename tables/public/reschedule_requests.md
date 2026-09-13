# public.reschedule_requests

**Status:** ⚠️ SUPERSEDED — use `analytics.reschedule_requests` instead. `public`'s data is frozen ~2026-03-15 (6 months stale); `analytics` has every row `public` has plus everything since (columns are identical between the two). See [`schema_map.md`](../../schema_map.md).

Despite the name, this table also covers requests for brand-new extra lessons, not just reschedules.

**Purpose:** A learner's request to reschedule existing lesson(s) or book new/extra lesson(s), typically requiring a fee and approval.

**Grain:** One row per request.

## Columns

| Column | Type | Nullable | Notes |
|---|---|---|---|
| id | text | no | PK |
| learner_id | text | no | FK → `Learner.id` |
| payment_id | text | yes | FK → `payment.id` — the fee payment for this request, if any |
| lesson_ids | integer[] | yes | which lesson(s) this request concerns |
| amount | numeric | no, default `0` | fee charged |
| status | enum `RescheduleRequestStatus` | no, default `'pending_payment'` | `pending_payment`, `pending`, `completed`, `cancelled` (observed: completed 230, pending 85, pending_payment 1) |
| type | enum `RescheduleRequestType` | no, default `'reschedule'` | **`new`, `reschedule`** — observed: `new` (227), `reschedule` (89). ⚠️ Despite the table name, the majority of rows (`new`) are requests for additional/new lessons, not reschedules of existing ones. Don't assume every row here is a "reschedule" in reports. |
| created_at, updated_at | timestamp (no tz) | no, default CURRENT_TIMESTAMP | |

## Relationships

- `learner_id` → `Learner.id`
- `payment_id` → `payment.id`
- Not referenced by any other table.

## Gotchas

- **Table name is misleading** — `type = 'new'` rows (the majority) are new/extra lesson requests, not reschedules. Split by `type` before labeling a metric "reschedule rate" or similar.

**Owner:** TBD
**Last verified:** 2026-09-12
