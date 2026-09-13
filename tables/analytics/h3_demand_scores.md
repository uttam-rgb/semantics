# analytics.h3_demand_scores

**Status:** Live. Part of the [geospatial demand/supply system](_geospatial_demand_overview.md) — read that first.

**Purpose:** Per-hex demand score, computed from counts of demand-signal POIs within that hex.

**Grain:** One row per hex. 2,801 rows.

## Columns

| Column | Type | Notes |
|---|---|---|
| h3_index | text | → `h3_grid_bengaluru.h3_index` |
| apartment_homes_count, residential_poi_count, university_college_count, it_park_count | integer | raw counts within the hex |
| pct_apartment_homes, pct_residential_poi, pct_university_college, pct_it_park | numeric | each count's share, presumably of the city-wide total or of all POIs in the hex — not confirmed |
| hex_demand_score | numeric | the composite score — weighting formula not documented |
| computed_at | timestamp with tz | |

## Relationships

`h3_index` → `h3_grid_bengaluru`. Rolled up into `cluster_demand_scores` via `h3_cluster_membership`.

## Gotchas

- `hex_demand_score`'s weighting formula (how the 4 pct fields combine into one score) isn't documented anywhere found — treat as a black-box score, don't try to reverse-derive its formula without the owner.

**Owner:** TBD
**Last verified:** 2026-09-12
