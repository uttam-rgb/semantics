# analytics.clusters

**Status:** Live. Part of the [geospatial demand/supply system](_geospatial_demand_overview.md) — read that first.

**Purpose:** Named geographic clusters — groups of hexes (see `h3_cluster_membership`) used as the unit of analysis for demand/supply/conversion decisions.

**Grain:** One row per cluster. 55 rows.

## Columns

| Column | Type | Notes |
|---|---|---|
| id | integer | PK, referenced as `cluster_id` everywhere else in this bucket |
| name | text | |
| geo_region_id | integer | |
| zone_id | integer | → `zones.id` |
| is_current | boolean | **filter `is_current = true`** — cluster boundaries appear to be versioned/recomputed |
| deleted_at | timestamp with tz | soft-delete — **filter `deleted_at IS NULL`** for active clusters |
| geom | text | geometry, presumably WKT/GeoJSON |
| gap_filled_cells | integer | hexes without direct data that were interpolated/filled, presumably |
| created_at, updated_at | timestamp with tz | |

## Relationships

`zone_id` → `zones.id`. Referenced as `cluster_id` by every `cluster_*` table and by `h3_cluster_membership`.

## Gotchas

- Always filter `is_current = true AND deleted_at IS NULL` unless deliberately looking at historical cluster versions.

**Owner:** TBD
**Last verified:** 2026-09-12
