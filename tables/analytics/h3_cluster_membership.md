# analytics.h3_cluster_membership

**Status:** Live. Part of the [geospatial demand/supply system](_geospatial_demand_overview.md) — read that first.

**Purpose:** Maps each hex to the cluster it belongs to.

**Grain:** One row per hex-to-cluster assignment. 1,374 rows — **fewer than the 2,801 hexes in `h3_grid_bengaluru`**, so not every hex belongs to a cluster.

## Columns

| Column | Type | Notes |
|---|---|---|
| h3_index | text | → `h3_grid_bengaluru.h3_index` |
| cluster_id | integer | → `clusters.id` |
| created_at | timestamp with tz | |

## Relationships

`h3_index` → `h3_grid_bengaluru`; `cluster_id` → `clusters.id`. This table is the join between hex-level and cluster-level data.

**Owner:** TBD
**Last verified:** 2026-09-12
