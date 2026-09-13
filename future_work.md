# Follow-ups (table documentation is complete)

All 107 tables across `exotel`, `public`, and `analytics` are now documented (`analytics_staging` remains explicitly excluded, per original scope). What's left is confirmation/decision work, not further schema exploration:

## Needs an explicit answer from the business owner
- **Is the "Lane Cars" used-car marketplace** (`car_inventory`/`sell_leads`/`buyer_request`/`earning_program`'s `lane_cars` referral program/the car-intent fields on `Learner`) **in scope for this semantic layer**, or does it belong to a separate reporting effort? See [`tables/analytics/_lane_cars_overview.md`](tables/analytics/_lane_cars_overview.md).
- **Is the geospatial demand/supply system** (17 H3/cluster tables) **in scope here**, or does it belong to the separate `grid_mapping_utilisation` project? See [`tables/analytics/_geospatial_demand_overview.md`](tables/analytics/_geospatial_demand_overview.md).
- Everything logged in [`open_questions.md`](open_questions.md) — ~26 items, spanning revenue/status-field ambiguities, unresolved `public`/`analytics` pairs (`admin_permissions`, `Admin`), and a proposed-but-unverified "Touch Rate %" fix.

## Lower-priority, only if a report ever needs them
- Several `analytics.Learner`/`Instructor` columns added since the `public` fork (car-intent tracking, e-signatures, onboarding/contract fields) are documented but not deeply investigated — fine to leave as-is until a specific report needs them.
- The instructor-payout system (`earning_config`, `instructor_payout`, etc.) has 0 rows in most of its tables — nothing to report on until it's actually launched.

## How to resume if new tables appear later

Same pattern used throughout: pull columns/constraints/comments/row-counts/freshness via a Python+psycopg2 script against `crn_database_analytics` (the read-only role; only fall back to the root `crn_database` credential for schemas the read-only role lacks grants on, as happened with `exotel`), then write a doc per table following the template used everywhere in `tables/`: Status / Purpose / Grain / Columns / Relationships / Gotchas / Owner / Last verified.
