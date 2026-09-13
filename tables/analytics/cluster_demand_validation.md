# analytics.cluster_demand_validation

**Status:** Live. Part of the [geospatial demand/supply system](_geospatial_demand_overview.md) — read that first.

**Purpose:** Checks whether a cluster's predicted demand (`demand_tier`, from `cluster_demand_scores`) matches its actual lead/conversion performance.

**Grain:** One row per cluster. 55 rows.

## Columns

`cluster_id` (→ `clusters.id`), `cluster_name`, `demand_tier`, `total_demand_score`, `lead_count`, `converted_lead_count`, `conversion_rate`, `quadrant` (predicted-vs-actual classification, presumably), `computed_at`.

**Note:** `lead_count`/`conversion_rate` here are computed independently for this geospatial system — not confirmed to use the same "converted" definition as [`metrics/conversion_rate.md`](../../metrics/conversion_rate.md) (`lead_stage IN ('CLOSED WON','50% PAYMENT DONE')`). Verify before comparing the two.

## Relationships

`cluster_id` → `clusters.id`.

**Owner:** TBD
**Last verified:** 2026-09-12
