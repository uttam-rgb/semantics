# analytics.h3_instructor_coverage

**Status:** Live. Part of the [geospatial demand/supply system](_geospatial_demand_overview.md) — read that first.

**Purpose:** Per-hex instructor supply — how many instructors cover this hex, and who's nearest.

**Grain:** One row per hex. 2,801 rows.

## Columns

| Column | Type | Notes |
|---|---|---|
| h3_index | text | → `h3_grid_bengaluru.h3_index` |
| instructor_count | integer | |
| nearest_instructor_id, nearest_instructor_name | text | |
| nearest_instructor_distance_km | numeric | |
| computed_at | timestamp with tz | |

## Relationships

`h3_index` → `h3_grid_bengaluru`. Rolled up into `cluster_instructor_coverage`.

**Owner:** TBD
**Last verified:** 2026-09-12
