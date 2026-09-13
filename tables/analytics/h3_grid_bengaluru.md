# analytics.h3_grid_bengaluru

**Status:** Live. Part of the [geospatial demand/supply system](_geospatial_demand_overview.md) — read that first.

**Purpose:** The base H3 hexagonal grid covering Bengaluru — one row per hex cell.

**Grain:** One row per hex. 2,801 rows.

## Columns

| Column | Type | Notes |
|---|---|---|
| h3_index | text | H3 cell identifier — the join key used across every table in this bucket |
| resolution | smallint | H3 grid resolution level |
| centroid_lat, centroid_lng | double precision | |
| polygon_wkt | text | hex boundary as WKT geometry |
| row_index, column_index | integer | grid position |
| created_at | timestamp with tz | |

## Relationships

`h3_index` is referenced by every other `h3_*` table in this bucket.

**Owner:** TBD
**Last verified:** 2026-09-12
