# Geospatial demand/supply planning system (bucket E)

**This looks like a separate initiative from the revenue/lead reporting this semantic layer was built for** — likely connected to a `grid_mapping_utilisation` project already in progress elsewhere. Confirm with the owner whether it belongs in the same Claude Project / documentation effort, or should be split out. Documented here per instruction to cover all tables, but treat as lower-confidence on "why," since no table comments exist to confirm intent — the architecture below is inferred from column names and how the pipeline chains together, not confirmed with the owner.

## The pipeline, in order

1. **`h3_grid_bengaluru`** (2,801 rows) — the base hexagonal grid covering Bengaluru (H3 = Uber's hexagonal geospatial indexing system). Each row is one hex cell: centroid, polygon boundary (WKT), grid position.
2. **Demand signal sources**, geocoded onto the grid via `h3_index`:
   - **`demand_pois`** (15,468) — raw fetched points of interest (apartments, IT parks, universities, etc.), with `duplicate_of_poi_id` for dedup tracking.
   - **`demand_master`** (15,162) — the cleaned/deduplicated master POI list (slightly fewer rows than `demand_pois`, consistent with dedup).
   - **`customer_pois`** (33,054) — actual customer/lead locations geocoded from raw address text (`raw_location` → `matched_locality` → `h3_index`).
   - **`competitor_pois`** (684) — competitor business locations.
   - **`canonical_localities`** (417) — a locality-name → lat/lng/h3_index geocoding reference table, likely used to resolve `customer_pois.matched_locality`.
3. **`h3_demand_scores`** (2,801, one per hex) — per-hex demand score computed from counts of apartment homes/residential POIs/universities/IT parks within that hex.
4. **`h3_instructor_coverage`** (2,801, one per hex) — per-hex instructor supply: instructor count, nearest instructor + distance.
5. **`clusters`** (55) — hexes are grouped into named clusters (via **`h3_cluster_membership`**, 1,374 rows — not every hex belongs to a cluster). Clusters belong to **`zones`** (5 rows) — a higher-level geographic grouping.
6. **Cluster-level rollups** (55 rows each, one per cluster):
   - **`cluster_demand_scores`** — aggregates `h3_demand_scores` up to cluster level, with a `demand_tier` classification.
   - **`cluster_instructor_coverage`** — aggregates `h3_instructor_coverage` up to cluster level.
   - **`cluster_demand_validation`** — checks whether high-demand clusters actually produce leads: `demand_tier` vs. real `lead_count`/`conversion_rate`.
   - **`cluster_lead_conversion_quadrant`** — plots each cluster on a lead-volume × conversion-rate 2×2 matrix (`quadrant`).
   - **`cluster_conversion_supply_verdict`** — combines demand tier, conversion rate, and instructor utilization into a `verdict` (likely a recommendation, e.g. "expand instructor supply here").
   - **`cluster_micromarket_octant`** — a finer 8-way (`octant`) segmentation combining demand tier, lead count, conversion rate, instructor utilization, and `pct_untouched`.

## Why this exists (inferred)

The overall shape strongly suggests a **territory-expansion decision tool**: "which geographic clusters have high demand signals but low instructor supply or low lead conversion, and should get more marketing spend or more instructors." Not confirmed with the owner.

## Gotchas

- No table in this bucket has a Postgres comment — all purpose/architecture notes above are inferred from column names and how tables reference each other, not confirmed.
- `clusters`/`zones` have `is_current`/`deleted_at` — cluster boundaries appear to be versioned/recomputed over time; always filter `is_current = true AND deleted_at IS NULL` unless deliberately looking at history.
- `h3_cluster_membership` (1,374 rows) is less than `h3_grid_bengaluru` (2,801 rows) — not every hex in the grid belongs to a cluster; don't assume full coverage.
