# analytics.demand_pois

**Status:** Live. Part of the [geospatial demand/supply system](_geospatial_demand_overview.md) — read that first.

**Purpose:** Raw, un-deduplicated demand-signal POIs as fetched from source. `demand_master` is the cleaned version of this.

**Grain:** One row per fetched POI. 15,468 rows.

## Columns

| Column | Type | Notes |
|---|---|---|
| id | integer | |
| name, category | text | |
| lat, lng | double precision | |
| h3_index | text | → `h3_grid_bengaluru.h3_index` |
| source | text | |
| fetched_at | timestamp with tz | |
| weight | integer | |
| duplicate_of_poi_id | integer | self-referencing — non-NULL means this row is a known duplicate of another row here |

## Relationships

`h3_index` → `h3_grid_bengaluru`. `duplicate_of_poi_id` → `demand_pois.id` (self).

## Gotchas

- Filter `duplicate_of_poi_id IS NULL` if you want only non-duplicate rows from this raw table — or just use `demand_master` instead, which appears to already be deduplicated.

**Owner:** TBD
**Last verified:** 2026-09-12
