# analytics.buyer_request

**Status:** Live. Part of the [Lane Cars marketplace](_lane_cars_overview.md) — read that first.

**Purpose:** Leads from people wanting to **buy** a used car — their preferences, to be matched against `car_inventory`.

**Grain:** One row per buyer request. 38 rows.

## Columns

| Column | Type | Notes |
|---|---|---|
| id | bigint | |
| name, phone | text | |
| budget | text | free text (likely contains currency formatting, e.g. "₹X-Y lakh" style ranges — not verified in detail) |
| body_types | text | preferred vehicle segment(s) |
| fuel, transmission | text | preferences |
| created_at | timestamp with tz | |

## Relationships

None enforced, and no link to `car_inventory` — matching a buyer request to available inventory would have to happen outside the database (manually, or in application code not reflected here).

## Gotchas

- `budget` is free text, not a structured numeric range — don't assume it can be parsed/filtered numerically without checking its actual format first.

**Owner:** TBD
**Last verified:** 2026-09-12
