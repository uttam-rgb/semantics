# public.payment

**Status:** ⚠️ SUPERSEDED — use `analytics.payment` instead. `public`'s data is frozen ~2026-03-15 (6 months stale); `analytics` has every row `public` has plus everything since. See [`schema_map.md`](../../schema_map.md). Columns/gotchas below also apply to `analytics.payment` (which additionally has a `return_origin` column).

**Purpose:** One row per payment transaction (or installment of one) made by a learner — course fees, reschedule fees, demo fees.

**Grain:** One row = one payment attempt/installment (`id`). Installments of the same overall payment are linked via `parent_payment_id` (self-referencing FK).

## Columns

| Column | Type | Nullable | Notes |
|---|---|---|---|
| id | text | no | PK |
| learner_id | text | no | FK → `Learner.id` |
| amount | numeric | no | amount for *this row* (this installment/attempt) |
| total_amount | numeric | yes | appears to equal the full course/order amount across installments — in the two rows sampled it matched `amount` exactly when `installment_type='full'`. **Not yet confirmed which field (`amount` vs `total_amount`) is correct for a "total revenue" sum when installments are involved — treat as an open question, don't guess.** |
| email, phone, name | text | yes | payer contact snapshot at time of payment — may differ from the linked Learner's current contact info; `name` is often NULL (only populated in some rows, e.g. guest-style checkouts) |
| payment_type | enum `PaymentType` | no | `course`, `reschedule`, `demo`, `custom` (observed: course 541, reschedule 89, demo 7) |
| status | **text, not enforced by an enum** | no, default `'pending'` | **observed values: `completed` (499), `pending` (106), `unpaid` (17), `failed` (8), `half_paid` (3), `partial` (2), `full_paid` (1), `pending_payment` (1)**. `half_paid` and `partial` look like the same concept written two different ways — likely drift between app versions. There is no canonical "successful payment" filter defined anywhere in the schema; decide and document one rather than guessing per-report. |
| gateway | enum `PaymentGateway` | no, default `'icici'` | `icici` (603), `razorpay` (34) |
| gateway_reference | text | yes | often NULL even on completed payments in samples seen |
| installment_type | enum `InstallmentType` | no, default `'full'` | `full` (428), `first_half` (187), `second_half` (22) |
| installment1_amount, installment2_amount | numeric | yes | populated when `installment_type <> 'full'` |
| parent_payment_id | text | yes | FK → `payment.id` (self-referencing) — links split-payment rows together |
| created_at, updated_at | timestamp (no tz) | no, default CURRENT_TIMESTAMP | |

## Relationships

- `learner_id` → `Learner.id`
- `parent_payment_id` → `payment.id` (self)
- Referenced by: `enrollment.payment_id`, `reschedule_requests.payment_id`

## Gotchas

- **`status` has no enum — free text with drifted synonyms.** Before computing any revenue/conversion metric, agree on a canonical mapping (e.g. is `half_paid` the same bucket as `partial`? does `unpaid` mean "still pending" or "will never pay"?). This is exactly the kind of ambiguity likely behind past wrong numbers.
- **`amount` vs `total_amount` — which one to sum for "total revenue" is unresolved.** Do not assume; confirm with the data owner before writing the revenue metric doc.
- Sample data includes a ₹1 `completed` payment — possibly test/demo data leaking into production. Worth checking for a minimum-amount filter or a test-account exclusion list before summing revenue.
- `name`/`email`/`phone` on this table are point-in-time snapshots, not live learner data — don't join back expecting them to match `Learner` today.

**Owner:** TBD
**Last verified:** 2026-09-12
