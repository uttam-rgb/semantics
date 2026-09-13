# public.enrollment

**Status:** ⚠️ SUPERSEDED — use `analytics.enrollment` instead. `public`'s data is frozen ~2026-03-16 (6 months stale); `analytics` has every row `public` has plus everything since, plus a `course_feedback` column not present here. See [`schema_map.md`](../../schema_map.md). Columns/gotchas below also apply to `analytics.enrollment`.

**Purpose:** One row per learner-course enrollment: which course, lesson-unlock progress, and payment/installment tracking for that enrollment.

**Grain:** One row = one learner's enrollment in one course.

## Columns

| Column | Type | Nullable | Notes |
|---|---|---|---|
| id | text | no | PK |
| learner_id | text | no | FK → `Learner.id` |
| course_id | text | yes | FK → `Courses.id` |
| payment_id | text | yes | FK → `payment.id` — the (first/primary) payment tied to this enrollment |
| status | enum `EnrollmentStatus` | no, default `'pending'` | `pending`, `active`, `completed`, `cancelled`. **Observed data only has `active` (356) and `pending` (30) — no enrollment has ever been marked `completed` or `cancelled` in this table**, which is itself worth confirming with the owner (does course completion get tracked elsewhere, e.g. via `progress`/`unlocked_lessons`, rather than flipping this status?). |
| payment_status | **free text, separate concept from `status` above** | yes | observed: `completed` (125), `half_paid` (117), NULL (75!), `full_paid` (51), `unpaid` (9), `pending` (6), `partial` (2), **`compeled`** (1 — typo, likely meant `completed`). ⚠️ This is a different axis from `status`: `status` tracks the enrollment lifecycle, `payment_status` tracks how much has been paid. Don't conflate "active enrollments" with "fully paid enrollments." |
| amount | bigint | yes | whole-number amount (sample: `6000`) — matched `installment1_amount` in the one full-payment sample seen |
| installment1_amount, installment2_amount | numeric | yes | |
| installment_mode | text, no enum | no, default `'full'` | free text, mirrors `payment.installment_type` — not validated against that enum |
| progress | jsonb | no, default `{}` | freeform progress data — shape not yet inspected, treat as opaque unless a specific report needs it |
| unlocked_lessons | integer[] | yes, default `{}` | array of `Lesson.number` values unlocked for this learner in this course — **not a count of completed lessons**, just what's been unlocked/made available |
| created_at, updated_at | timestamp (no tz) | no, default CURRENT_TIMESTAMP | |

## Relationships

- `learner_id` → `Learner.id`
- `course_id` → `Courses.id`
- `payment_id` → `payment.id`
- Not referenced by any other table.

## Gotchas

- **`status` and `payment_status` are two different, easily-confused fields** — 75 rows (~19%) have `payment_status IS NULL` despite having a real `status`. Any "how many learners have paid in full" metric must use `payment_status`, not `status`.
- **Known typo:** `payment_status = 'compeled'` (1 row) — should be treated as `completed` if you're bucketing this field.
- `amount` (bigint, whole number) vs the numeric `installment*_amount` fields — same unit (rupees) in the one sample checked, but not confirmed across all rows.

**Owner:** TBD
**Last verified:** 2026-09-12
