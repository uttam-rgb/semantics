# analytics.apartment_dedup_matches

**Status:** ☠️ EXCLUDED — an internal deduplication artifact for the [geospatial demand system](_geospatial_demand_overview.md), not relevant to business reporting. 4,194 rows.

**Purpose:** Matches candidate duplicate apartment POIs between two data sources (labeled "NoBroker" and "OSM" — likely the NoBroker real-estate listing site and OpenStreetMap), with a match confidence and shared H3 location, feeding the cleanup that produces `demand_master` from `demand_pois`.

**Columns:** `id`, `nobroker_poi_id`, `nobroker_name`, `nobroker_homes`, `osm_poi_id`, `osm_name`, `osm_category`, `distance_m`, `shared_words`, `confidence`, `h3_index`, `created_at`.

**Owner:** TBD
**Last verified:** 2026-09-12
