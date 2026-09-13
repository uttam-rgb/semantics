# analytics.cluster_conversion_supply_verdict

**Status:** Live. Part of the [geospatial demand/supply system](_geospatial_demand_overview.md) — read that first.

**Purpose:** Combines demand tier, conversion rate, and instructor utilization into a single per-cluster `verdict` — likely an expansion/staffing recommendation.

**Grain:** One row per cluster. 55 rows.

## Columns

`cluster_id` (→ `clusters.id`), `cluster_name`, `demand_tier`, `conversion_rate`, `quadrant`, `instructor_count`, `avg_covering_utilisation_pct`, `verdict` (text — the recommendation itself, values not sampled), `computed_at`.

## Relationships

`cluster_id` → `clusters.id`.

## Gotchas

- `verdict`'s possible values and the rule that produces them aren't documented anywhere found — treat as a black-box recommendation, don't try to reverse-engineer the decision logic without the owner.

**Owner:** TBD
**Last verified:** 2026-09-12
