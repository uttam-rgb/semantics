---
name: inlane-data-guide
description: Grounds Claude in Inlane's cratio_crm Postgres database (Metabase reporting, driving-school + lead CRM data) before writing SQL, computing a business metric, or answering a question about revenue/conversions/leads/calls/instructor utilization. Covers which of several similarly-named tables is authoritative, verified metric formulas, and known data-quality bugs.
when_to_use: When writing or reviewing SQL against Inlane's database (schemas public/analytics/exotel, table cratio_leads_analytics, exotel_calls, etc.), when asked about a business metric (revenue, conversion rate, ticket size, lead volume, call activity, instructor utilization, alert/follow-up health), or when working with Metabase reports for Inlane/Lane.
disable-model-invocation: false
---

# Inlane data semantic layer

This plugin bundles verified documentation for Inlane's `cratio_crm` Postgres database. **Before generating any SQL or stating a metric value, read the relevant doc(s) below with the Read tool.** If something is ambiguous and not resolved in these docs, say so and ask — do not guess.

## Hard rules (apply every time, no exceptions)

1. **Never query the `analytics_staging` schema.** Explicitly out of scope.
2. **`exotel.call_logs` and `exotel.sync_history` are dead (0 real rows).** Use `public.exotel_calls` / `public.exotel_sync_history` instead.
3. **For `Schedule`, `payment`, `Learner`, `enrollment`, `reschedule_requests`, `schedule_preferences`, `Serviceable_Areas`, and `team_bug_reports`: use the `analytics.*` version, not `public.*`.** `public` is frozen ~March 2026 (stale); `analytics` has everything `public` has plus everything since. Exceptions (`admin_permissions`, `Admin`) are in `${CLAUDE_PLUGIN_ROOT}/schema_map.md`.
4. **`analytics.cratio_leads_analytics` is the real leads table**, not the tiny `public.cratio_leads`.
5. **`analytics.User` and `analytics.users` (lowercase) are two unrelated features**, not the same table with different casing.
6. Any table/column marked "STALE," "SUPERSEDED," "DEAD," or "⚠️ UNRESOLVED" in its doc should not be used without flagging that status first.
7. **Every row count/percentage in these docs is a stale snapshot from its "Last verified" date, not a live fact.** Never answer "how many X" from a number written in a doc — query the live table. See `${CLAUDE_PLUGIN_ROOT}/conventions.md`.
8. **"Agent" = `lead_owner`.** Any question about "by agent" means grouping an existing metric by `lead_owner` — never a separate table or concept.
9. **`analytics.cratio_leads_analytics.call_did_status` must never be used in any metric logic** — confirmed unreliable (almost entirely disjoint from real telephony call data). Use `public.exotel_calls` for all call-activity logic instead.

## Where to look (read on demand, don't preload)

- **`${CLAUDE_PLUGIN_ROOT}/conventions.md`** — cross-cutting rules, read this first.
- **`${CLAUDE_PLUGIN_ROOT}/schema_map.md`** — which schema/table is authoritative when `public`/`analytics` duplicate each other.
- **`${CLAUDE_PLUGIN_ROOT}/open_questions.md`** — things discovered during documentation that still need a human answer. Treat everything there as genuinely unresolved — flag it, don't guess a resolution.
- **`${CLAUDE_PLUGIN_ROOT}/tables/<schema>/<table>.md`** — one file per table: purpose, grain, column meanings, relationships, gotchas. Schemas: `exotel/`, `public/`, `analytics/`.
- **`${CLAUDE_PLUGIN_ROOT}/metrics/<metric>.md`** — one file per business metric, each with a `status` (`confirmed`/`draft`/`deprecated`) and a `verified_sql` block. **Use that query as the template — adapt its date range/dimension filters, don't reconstruct the logic from table docs.** Only treat a metric as settled if `status: confirmed`.
- **`${CLAUDE_PLUGIN_ROOT}/future_work.md`** — tables not yet documented. If a query needs one and no doc exists, say so rather than guessing at the schema.

## Available metrics (as of this writing)

`revenue`, `lead_volume`, `conversion_rate`, `call_activity`, `target_attainment`, `alert_resolution`, `instructor_utilization`, `ticket_size`, `lead_status_buckets`, `source_wise_summary`, `hourly_split`, `agent_lead_status`, `self_reported_agent_calls`, `speed_to_call`, `lead_health_alerts`, `followup_response_time` — see `${CLAUDE_PLUGIN_ROOT}/metrics/` for the full file list; each metric doc names its own aliases.

## Two subsystems that may not be in scope

`car_inventory`/`sell_leads`/`buyer_request` (a used-car marketplace, "Lane Cars") and a 17-table geospatial demand/supply planning system are documented but their relevance to this data model is **unconfirmed** — see `${CLAUDE_PLUGIN_ROOT}/future_work.md` before treating either as in scope for a business question.
