# analytics.cluster_instructor_coverage

**Status:** Live. Part of the [geospatial demand/supply system](_geospatial_demand_overview.md) — read that first.

**Purpose:** `h3_instructor_coverage` rolled up to the cluster level.

**Grain:** One row per cluster. 55 rows.

## Columns

`cluster_id` (→ `clusters.id`), `cluster_name`, `instructor_count`, `instructor_ids`/`instructor_names` (comma-or-similar delimited text lists, not arrays — confirm delimiter before parsing), `avg_nearest_distance_km`, `computed_at`.

## Relationships

`cluster_id` → `clusters.id`.

**Owner:** TBD
**Last verified:** 2026-09-12
