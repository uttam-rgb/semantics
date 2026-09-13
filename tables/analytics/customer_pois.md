# analytics.customer_pois

**Status:** Live. Part of the [geospatial demand/supply system](_geospatial_demand_overview.md) — read that first.

**Purpose:** Actual customer/lead locations, geocoded from raw address text onto the H3 grid — the real-demand counterpart to the POI-based `demand_master`/`demand_pois`.

**Grain:** One row per geocoded customer location. 33,054 rows.

## Columns

| Column | Type | Notes |
|---|---|---|
| id | integer | |
| raw_location | text | the original, unstructured address/area text |
| matched_locality | text | resolved against `canonical_localities`, presumably |
| lat, lng | double precision | |
| h3_index | text | → `h3_grid_bengaluru.h3_index` |
| source | text | |
| fetched_at | timestamp with tz | |

## Relationships

`h3_index` → `h3_grid_bengaluru`. `matched_locality` conceptually → `canonical_localities.locality` (not enforced). Not linked to `cratio_leads_analytics`/`Learner` by any ID — this looks like a separate geocoding pass over location text, not a live join to the CRM tables.

**Owner:** TBD
**Last verified:** 2026-09-12
