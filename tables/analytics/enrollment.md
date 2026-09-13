# analytics.enrollment

**Status:** ✅ Authoritative — use this, not `public.enrollment` (frozen ~2026-03-16, see [`schema_map.md`](../../schema_map.md)). 3,808 rows, current through 2026-09-11.

**Purpose, grain, and full column reference:** identical to `public.enrollment` — see [`tables/public/enrollment.md`](../public/enrollment.md) for the complete column table and gotchas (the `status` vs `payment_status` distinction, the `'compeled'` typo, `amount` type inconsistency, etc.), all of which apply here too.

## Analytics-only column

| Column | Notes |
|---|---|
| course_feedback | not present on `public.enrollment`; likely related to `learner_course_feedback`, not yet investigated |

**Owner:** TBD
**Last verified:** 2026-09-12
