# analytics.demand_master

**Status:** Live. Part of the [geospatial demand/supply system](_geospatial_demand_overview.md) — read that first.

**Purpose:** The cleaned/deduplicated master list of demand-signal points of interest (apartments, IT parks, universities, etc.) feeding `h3_demand_scores`.

**Grain:** One row per POI. 15,162 rows — slightly fewer than `demand_pois` (15,468), consistent with this being the deduplicated output of that raw table.

## Columns

| Column | Type | Notes |
|---|---|---|
| id | integer | |
| name, category | text | |
| lat, lng | double precision | |
| h3_index | text | → `h3_grid_bengaluru.h3_index` |
| source | text | data provenance |
| units | integer | e.g. number of housing units, for an apartment complex |
| address | text | |
| created_at, updated_at | timestamp with tz | |

## Relationships

`h3_index` → `h3_grid_bengaluru`. Conceptually derived from `demand_pois` (not an enforced FK).

**Owner:** TBD
**Last verified:** 2026-09-12
