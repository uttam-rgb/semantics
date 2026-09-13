# analytics schema — triage (84 tables total)

**✅ All buckets below are now documented** (see `tables/analytics/`) — this file is kept as a historical record of the prioritization reasoning, not a to-do list. For anything still unresolved, see `open_questions.md` and `future_work.md`.

Triaged before writing full docs, to avoid spending effort on tables unrelated to revenue/lead reporting. Buckets below; row counts as of 2026-09-12.

## A. Exclude — junk/backup/test data (4 tables)
- `lead_snapshots_backup` (109,422 rows) — explicit backup of `lead_snapshots`
- `apartment_dedup_matches` (4,194), `osm_internal_duplicates` (53) — internal geospatial dedup artifacts
- `demo-payments` (108) — name says demo/test

## B. Duplicate-name variants needing resolution (like schema_map.md, but within `analytics` itself)
- `Admin` (17 rows, 9 cols) vs `AdminProfiles` (0 rows) vs `adminprofiles` (3 rows, 5 cols)
- `User` (40 rows, 7 cols) vs `users` (122 rows, 16 cols)
- `KAM` (5 rows) vs `kam_instructor` (79 rows) — likely different grain (KAM master list vs KAM-to-instructor mapping), not true duplicates, but names are confusable

## C. Same-name as `public` — resolve in `schema_map.md` (not yet done)
`Schedule`, `payment`, `Learner`, `reschedule_requests`, `enrollment`, `schedule_preferences`, `admin_permissions`, `Serviceable_Areas`, `Instructor`, `Lesson`, `Courses`, `team_bug_reports`, `Instructor Unavailability`, `Learner Availability`, `app_settings` — 15 tables that also exist in `public`. Need a per-table authority call, same pattern as the exotel finding.

## D. High-value, analytics-only — the actual reporting/alerting system (prioritize first)
These are almost certainly what your revenue head has been trying to report on. Four of them already have **human-written Postgres comments** describing exact business logic — a gift, not something we have to reverse-engineer:

- `cratio_leads_analytics` (82,053 rows, 44 cols) — very likely the real leads table (resolves the `public.cratio_leads` open question)
- `lead_snapshots` (339,820 rows) — point-in-time lead snapshots
- `alerted_leads_log` (223,091 rows) — **comment:** *"Every lead that appeared in each alert sheet, logged at send time. Join to cratio_leads_analytics 24-48h later to measure resolution rate per alert type per owner."*
- `alert_resolution_log` (10,075 rows) — **comment:** *"Daily resolution check: of leads alerted yesterday, how many moved stage by this morning. Sent as a stakeholder-only email each morning before per-owner reports go out."*
- `alert_metric_snapshots` (1,691 rows) — **comment:** *"Daily snapshot of alert counts per lead owner. Used to track whether alert initiative is reducing problem metrics over time."*
- `daily_report_snapshots` (1,504 rows) — **comment:** *"Daily KPI snapshot per lead owner. Used to track macro business impact: SLA compliance, conversion rates, and revenue trends over time."*
- `lead_owner_target` (1,023 rows, 3 cols) — targets/quota per lead owner
- `ll_pipeline_events` (17,422), `ll_applications` (1,168, 39 cols) — Learner's License application pipeline
- `lesson_tracking` (54,087 rows) — possibly the real source for "lessons completed," cleaner than `Schedule`
- `learner_course_feedback` (768)
- `instructor_utilisation` (32) / `instructor_utilisation_trailing` (50) / `low_util_instructor_leads` (1,713, 18 cols)

## E. Geospatial demand/supply clustering module — separate initiative, likely out of scope (17 tables)
`h3_demand_scores`, `h3_grid_bengaluru`, `h3_instructor_coverage`, `h3_cluster_membership`, `cluster_conversion_supply_verdict`, `cluster_demand_scores`, `cluster_demand_validation`, `cluster_instructor_coverage`, `cluster_lead_conversion_quadrant`, `cluster_micromarket_octant`, `clusters`, `zones`, `demand_master`, `demand_pois`, `customer_pois`, `competitor_pois`, `canonical_localities`

This looks like territory/expansion-planning tooling (H3 hex-grid demand modeling), unrelated to the revenue/lead reporting that triggered this project. Recommend deprioritizing.

## F. E-learning / gamification module — separate feature (5 tables)
`learning_content`, `learning_sessions`, `learning_analytics_settings`, `game_analytics_settings`, `game_launch_events`

## G. Unclear business context — needs a question answered, not a guess (3 tables)
`car_inventory` (147, 19 cols), `sell_leads` (408), `buyer_request` (38) — sound like a car marketplace/sales feature. Not obviously connected to the driving-school business modeled in `public`. Need to ask what this is before documenting.

## H. Instructor payout/earnings system — medium priority (5 tables)
`earning_config`, `earning_program`, `instructor_earning_adjustment`, `instructor_earning_settings`, `instructor_payout` — relevant if cost-side/instructor-payout metrics are ever in scope.

## I. Misc ops/low priority (11 tables)
`support_ticket`, `queries`, `schedule_audit_log`, `schedule_no_show`, `instructor_leave_request`, `instructor_status_log`, `dl_test_slots`, `ll_documents`, `user_permissions`, `qr_codes`, `qr_scans`, `instructors_info`
