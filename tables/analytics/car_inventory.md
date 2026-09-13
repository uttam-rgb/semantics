# analytics.car_inventory

**Status:** Live. Part of the [Lane Cars marketplace](_lane_cars_overview.md) — read that first.

**Purpose:** Used cars currently listed for sale.

**Grain:** One row per car listing. 147 rows.

## Columns

| Column | Type | Notes |
|---|---|---|
| id | bigint | |
| name, phone | text | seller contact |
| registration_number | text | |
| make, model | text | |
| year | double precision | ⚠️ numeric type for a year value, unusual but harmless |
| segment | text | e.g. `Sedan`, `SUV` |
| transmission, fuel_type | text | |
| km_driven | double precision | |
| price | double precision | |
| emi | double precision | monthly EMI (installment) figure, presumably for a financing option shown to buyers |
| condition | text | e.g. `Good Condition` — free text, not an enum |
| vehicle_type | text | e.g. `Used` |
| ownership | text | e.g. `'5'`, `'2'` (looks like ownership count/number, stored as text) |
| availability | boolean | is this listing currently active/available |
| photos | text | mostly NULL in samples seen |
| created_at | timestamp with tz | |

## Relationships

None enforced, and none to `sell_leads`/`buyer_request` either, despite the obvious conceptual link (a sell lead presumably becomes an inventory listing once accepted).

**Owner:** TBD
**Last verified:** 2026-09-12
