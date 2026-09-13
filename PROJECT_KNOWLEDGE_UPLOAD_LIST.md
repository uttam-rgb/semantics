# What to upload where (Claude Project setup)

## 1. Project custom instructions (paste as text, not a file)

Paste the full contents of [`_index.md`](_index.md) into the Project's custom instructions field.

## 2. Project Knowledge (upload as files)

- [`conventions.md`](conventions.md)
- [`schema_map.md`](schema_map.md)
- [`open_questions.md`](open_questions.md)
- Every file under `tables/**/*.md` (111 files as of 2026-09-12 — full coverage of all 107 tables across `tables/exotel/`, `tables/public/`, `tables/analytics/`, plus 4 cross-table overview docs)
- Every file under `metrics/**/*.md` (16 files as of 2026-09-12: `revenue.md`, `conversion_rate.md`, `lead_volume.md`, `call_activity.md`, `target_attainment.md`, `alert_resolution.md`, `instructor_utilization.md`, `ticket_size.md`, `lead_status_buckets.md`, `source_wise_summary.md`, `hourly_split.md`, `agent_lead_status.md`, `self_reported_agent_calls.md`, `speed_to_call.md`, `lead_health_alerts.md`, `followup_response_time.md` — most `status: confirmed`; `lead_status_buckets.md` is `status: draft`, newly constructed rather than extracted from production SQL)

## Do NOT upload

- `SQL_Logic/*.sql` — raw source queries (some contain unfixed bugs, e.g. `d0_conversion%` in `leaderdashboard_summary.sql`). The corrected, annotated versions live in `metrics/*.md`; upload those instead.
- `reference/Lane_Metric_Definitions_v1.xlsx` — the business team's own semantic spec, kept for provenance. Its content has been fully cross-checked into `metrics/*.md` (conflicts adjudicated 2026-09-12, see `open_questions.md`); no need to upload the spreadsheet itself.

- `future_work.md` — internal planning, not query-relevant
- `analytics_schema_triage.md` — internal working notes, superseded by the actual table docs
- `config.yaml` — **contains plaintext database credentials, never upload or share this anywhere**
- Anything in `scripts/` or any `*_dump.json`/`*_triage.json` file — raw introspection output, not needed once the `.md` docs exist

## After uploading

Re-run one of the reports that came out wrong before this project started, and check whether the number now matches reality (or whether Claude at least surfaces the right ambiguity/open question instead of guessing).
