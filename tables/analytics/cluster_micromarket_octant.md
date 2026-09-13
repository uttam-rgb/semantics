# analytics.cluster_micromarket_octant

**Status:** Live. Part of the [geospatial demand/supply system](_geospatial_demand_overview.md) — read that first.

**Purpose:** The most granular per-cluster classification in this bucket — an 8-way (`octant`) segmentation combining demand, lead volume, conversion, instructor utilization, and untapped-lead share.

**Grain:** One row per cluster. 55 rows.

## Columns

`cluster_id` (→ `clusters.id`), `cluster_name`, `octant` (text — the 8-way classification label), `demand_tier`, `lead_count`, `conversion_rate`, `avg_instructor_utilisation`, `pct_untouched` (share of leads in this cluster never contacted — same concept as `cratio_leads_analytics.call_did_status = 'Untouched'`, but computed independently here), `computed_at`.

## Relationships

`cluster_id` → `clusters.id`.

**Owner:** TBD
**Last verified:** 2026-09-12
