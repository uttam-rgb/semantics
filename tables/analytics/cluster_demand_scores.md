# analytics.cluster_demand_scores

**Status:** Live. Part of the [geospatial demand/supply system](_geospatial_demand_overview.md) — read that first.

**Purpose:** `h3_demand_scores` rolled up to the cluster level, with a `demand_tier` classification.

**Grain:** One row per cluster. 55 rows.

## Columns

| Column | Type | Notes |
|---|---|---|
| cluster_id | integer | → `clusters.id` |
| cluster_name | text | denormalized |
| zone_id | integer | → `zones.id` |
| hex_count | integer | how many hexes make up this cluster |
| apartment_homes_count, residential_poi_count, university_college_count, it_park_count | integer | summed from `h3_demand_scores` across the cluster's hexes |
| total_demand_score, avg_demand_score | numeric | |
| demand_tier | smallint | e.g. a 1–5 tier classification — exact bucketing rule not documented |
| computed_at | timestamp with tz | |

## Relationships

`cluster_id` → `clusters.id`; `zone_id` → `zones.id`.

**Owner:** TBD
**Last verified:** 2026-09-12
