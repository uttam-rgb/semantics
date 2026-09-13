# analytics.payment

**Status:** ✅ Authoritative — use this, not `public.payment` (frozen ~2026-03-15, see [`schema_map.md`](../../schema_map.md)). 5,509 rows, current through 2026-09-11.

**Purpose, grain, and full column reference:** identical to `public.payment` — see [`tables/public/payment.md`](../public/payment.md) for the complete column table and gotchas (all of which apply here too: no enum on `status`, `amount` vs `total_amount` ambiguity, ₹1 test-looking payments, etc.).

**Note:** despite the column-level ambiguities documented there, **this table is not actually the source for the `revenue` metric** — see [`metrics/revenue.md`](../../metrics/revenue.md), which uses `cratio_leads_analytics.expected_revenue` instead, confirmed from production SQL. Don't assume `payment.amount` is what "revenue" means in a report just because it looks like the obvious candidate.

## Analytics-only column

| Column | Notes |
|---|---|
| return_origin | not present on `public.payment`; purpose not yet investigated |

**Owner:** TBD
**Last verified:** 2026-09-12
