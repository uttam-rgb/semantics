# analytics.zones

**Status:** Live. Part of the [geospatial demand/supply system](_geospatial_demand_overview.md) — read that first.

**Purpose:** The highest-level geographic grouping — clusters roll up into zones.

**Grain:** One row per zone. Only 5 rows.

## Columns

Same shape as `clusters` minus `gap_filled_cells`: `id`, `name`, `geo_region_id`, `is_current`, `geom`, `deleted_at`, `created_at`, `updated_at`.

## Relationships

Referenced by `clusters.zone_id`.

## Gotchas

- Same versioning caveat as `clusters` — filter `is_current = true AND deleted_at IS NULL`.

**Owner:** TBD
**Last verified:** 2026-09-12
