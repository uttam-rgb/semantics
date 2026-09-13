# analytics.sell_leads

**Status:** Live. Part of the [Lane Cars marketplace](_lane_cars_overview.md) — read that first.

**Purpose:** Leads from people wanting to **sell** their car.

**Grain:** One row per sell lead. 408 rows.

## Columns

| Column | Type | Notes |
|---|---|---|
| id | bigint | |
| registration_number, make, model, trim | text | `model` often empty string, `trim` mostly NULL in samples seen |
| year | text | ⚠️ text, not numeric — inconsistent with `car_inventory.year` (double precision) |
| fuel_type, transmission, ownership, condition, accident_type | text | |
| km_driven | text | ⚠️ text, not numeric |
| name, phone | text | ⚠️ samples include obvious test data (`name='Test1'`, `phone='0000000000'`) — filter before reporting lead volume |
| created_at | timestamp with tz | |

## Relationships

None enforced, and no link to `car_inventory` despite the conceptual flow (sell lead → accepted → becomes an inventory listing).

## Gotchas

- Contains visible test rows — exclude before counting real leads.
- `year`/`km_driven` are text here but numeric on `car_inventory` — inconsistent typing between the two tables if ever joined/compared.

**Owner:** TBD
**Last verified:** 2026-09-12
