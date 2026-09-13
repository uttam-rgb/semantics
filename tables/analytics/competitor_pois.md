# analytics.competitor_pois

**Status:** Live. Part of the [geospatial demand/supply system](_geospatial_demand_overview.md) — read that first.

**Purpose:** Competitor driving-school locations, geocoded onto the grid — presumably for competitive-density analysis alongside demand/supply scoring.

**Grain:** One row per competitor location. 684 rows.

## Columns

| Column | Type | Notes |
|---|---|---|
| id | integer | |
| name | text | |
| lat, lng | double precision | |
| h3_index | text | → `h3_grid_bengaluru.h3_index` |
| source, place_id | text | likely a Google Places API source |
| matched_keyword | text | the search term that surfaced this competitor, presumably |
| address | text | |
| fetched_at | timestamp with tz | |

## Relationships

`h3_index` → `h3_grid_bengaluru`.

**Owner:** TBD
**Last verified:** 2026-09-12
