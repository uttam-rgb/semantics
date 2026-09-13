# analytics.canonical_localities

**Status:** Live. Part of the [geospatial demand/supply system](_geospatial_demand_overview.md) — read that first.

**Purpose:** A standardized locality-name → coordinates geocoding reference table, likely used to resolve `customer_pois.matched_locality`.

**Grain:** One row per canonical locality name. 417 rows.

## Columns

`locality` (text), `lat`, `lng` (double precision), `h3_index` (text, → `h3_grid_bengaluru`), `created_at`.

## Relationships

`h3_index` → `h3_grid_bengaluru`. Conceptually referenced by `customer_pois.matched_locality` (not enforced).

**Owner:** TBD
**Last verified:** 2026-09-12
