# The lead-alerting/reporting system (analytics schema)

This is a set of interconnected tables that together implement a daily lead-alerting and per-owner KPI reporting system. Read this before touching any individual table below — the tables only make sense together.

## The pieces

1. **`cratio_leads_analytics`** (82,053 rows) — the raw leads table, synced from the external Cratio CRM. Every lead a sales/lead-owner is working, with stage, revenue, and follow-up fields. This is the source of truth for "what does this lead look like right now." **Resolves the earlier open question**: this is the real leads dataset, not the 32-row `public.cratio_leads`.
2. **`lead_snapshots`** (339,820 rows) — a daily point-in-time copy of each lead's funnel stage (`funnel_stage`), keyed by `(lead_date, snapshot_day, mobile_number)`-ish. Lets you answer "what stage was this lead in on day X," not just its current stage.
3. **`alerted_leads_log`** (223,091 rows) — every time a lead gets flagged into a daily "problem" alert (e.g. "hasn't been contacted in 7 days"), a row is logged here. PK is `(alert_date, alert_type, mobile_number, lead_owner)`.
4. **`alert_resolution_log`** (10,075 rows) — the next-day follow-up: of the leads alerted on day D, how many had moved to a different stage by the morning of D+1. One row per `(check_date, alert_date, alert_type, lead_owner)`.
5. **`alert_metric_snapshots`** (1,691 rows) — daily counts of each alert type, per lead owner, in wide form (one column per alert type) rather than the long form used by `alerted_leads_log`.
6. **`daily_report_snapshots`** (1,504 rows) — the daily KPI rollup per lead owner: calls made, conversions, revenue booked, conversion rate, SLA%. This is very likely **the table to use for "what's our conversion rate / revenue by owner" reporting** — it's cleanly typed (real `numeric`/`integer` columns, unlike the source leads table) and has an explicit comment describing its purpose.
7. **`lead_owner_target`** (1,023 rows) — target/quota per lead owner per date, to compare against `daily_report_snapshots.conversions` / `.revenue_booked`.
8. **`d0_snapshots`** (744 rows) — a "day zero" funnel-stage snapshot per lead, likely a baseline cut of the same snapshotting process behind `lead_snapshots`. See [`d0_snapshots.md`](d0_snapshots.md).

## How the alert_type values map across tables

`alerted_leads_log.alert_type` and `alert_resolution_log.alert_type` use these values (long form); `alert_metric_snapshots` has one column per value (wide form) — **same underlying concept, different shape**:

| alert_type value | alert_metric_snapshots column |
|---|---|
| `untapped_yesterday` | `untapped_leads_yesterday` |
| `not_contacted_7_days` | `leads_not_contacted_7_days` |
| `no_followup_set` | `leads_no_followup_set` |
| `followups_due_today` | `followups_due_today` |
| `overdue_followups_last_3_days` | `overdue_followups_last_3_days` |
| `stuck_50pct_payment` | `revenue_stuck_50pct_payment` |
| `send_payment_links` | `send_payment_links` |
| `send_course_details` | `send_course_details` |
| `instructor_priority_leads` | `instructor_priority_leads` |
| `hot_lead_priority` | `hot_lead_priority` |

## Typical query pattern

- "How many leads did owner X get alerted about for stalled payments last week, and how many actually moved?" → join `alerted_leads_log` (filtered `alert_type='stuck_50pct_payment'`) to `alert_resolution_log` on `(alert_date, alert_type, lead_owner)`.
- "What's owner X's conversion rate this month vs their target?" → `daily_report_snapshots` joined to `lead_owner_target` on `(lead_owner, date)`.
- "Trace one lead's full history" → join `cratio_leads_analytics` (current state) to `lead_snapshots` (historical stage-by-day) on `mobile_number`, and to `alerted_leads_log` for its alert history.

## Cross-cutting gotchas (see individual table docs for detail)

- `cratio_leads_analytics` has **no primary key** and `mobile_number` is not unique (82,053 rows, 77,016 distinct numbers) — decide what "one lead" means before counting.
- Money and date fields in `cratio_leads_analytics` are stored as **text**, not `numeric`/`date` — need explicit casting.
- `cratio_leads_analytics.lead_stage` has 20+ raw values needing a canonical won/lost/in-progress grouping before any funnel/conversion metric.
