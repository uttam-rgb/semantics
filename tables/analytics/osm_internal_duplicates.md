# analytics.osm_internal_duplicates

**Status:** ☠️ EXCLUDED — an internal deduplication artifact for the [geospatial demand system](_geospatial_demand_overview.md), not relevant to business reporting. 53 rows.

**Purpose:** Pairs of OpenStreetMap POIs (within the demand-signal data) that appear to be duplicates of each other, by name and distance.

**Columns:** `id`, `poi_id_a`, `poi_id_b`, `shared_name`, `distance_m`, `created_at`.

**Owner:** TBD
**Last verified:** 2026-09-12
