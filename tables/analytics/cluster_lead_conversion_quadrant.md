# analytics.cluster_lead_conversion_quadrant

**Status:** Live. Part of the [geospatial demand/supply system](_geospatial_demand_overview.md) — read that first.

**Purpose:** Plots each cluster on a lead-volume × conversion-rate 2×2 matrix.

**Grain:** One row per cluster. 55 rows.

## Columns

`cluster_id` (→ `clusters.id`), `cluster_name`, `lead_count`, `conversion_rate`, `quadrant` (e.g. high-volume/high-conversion vs. low/low — exact labels not sampled), `computed_at`.

Same caveat as `cluster_demand_validation`: verify `lead_count`/`conversion_rate` definitions match (or don't match) [`metrics/conversion_rate.md`](../../metrics/conversion_rate.md) before cross-referencing.

## Relationships

`cluster_id` → `clusters.id`.

**Owner:** TBD
**Last verified:** 2026-09-12
