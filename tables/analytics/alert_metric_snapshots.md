# analytics.alert_metric_snapshots

**Status:** Part of the [lead-alerting/reporting system](_reporting_system_overview.md).

**Purpose (from the table's own Postgres comment):** *"Daily snapshot of alert counts per lead owner. Used to track whether alert initiative is reducing problem metrics over time."*

**Grain:** One row per (snapshot_date, lead_owner) — enforced by a composite primary key. This is the **wide-form** equivalent of `alerted_leads_log`'s long-form `alert_type` dimension — see the [overview](_reporting_system_overview.md) for the exact column ↔ alert_type mapping.

**The actual generating logic for 8 of these 10 columns is now known** — see [`metrics/lead_health_alerts.md`](../../metrics/lead_health_alerts.md), sourced from the production script `SQL_Logic/health_metric.sql`. That doc also documents a confirmed bug: `overdue_followups_last_3_days` doesn't filter for overdue-ness at all (includes future-dated followups) and actually uses a 7-day window, not 3 — a corrected version is provided there. `instructor_priority_leads` isn't in that script; its source is still unknown.

## Columns

| Column | Type | Nullable | Notes |
|---|---|---|---|
| snapshot_date | date | no | part of PK |
| lead_owner | text | no | part of PK |
| untapped_leads_yesterday | integer | no, default 0 | ↔ `alert_type = 'untapped_yesterday'` |
| leads_not_contacted_7_days | integer | no, default 0 | ↔ `alert_type = 'not_contacted_7_days'` |
| leads_no_followup_set | integer | no, default 0 | ↔ `alert_type = 'no_followup_set'` |
| followups_due_today | integer | no, default 0 | ↔ `alert_type = 'followups_due_today'` |
| overdue_followups_last_3_days | integer | no, default 0 | ↔ `alert_type = 'overdue_followups_last_3_days'` |
| revenue_stuck_50pct_payment | integer | no, default 0 | ↔ `alert_type = 'stuck_50pct_payment'` |
| send_payment_links | integer | yes, default 0 | ↔ `alert_type = 'send_payment_links'` |
| send_course_details | integer | yes, default 0 | ↔ `alert_type = 'send_course_details'` |
| instructor_priority_leads | integer | yes | ↔ `alert_type = 'instructor_priority_leads'` |
| hot_lead_priority | integer | yes | ↔ `alert_type = 'hot_lead_priority'` |
| created_at | timestamp with tz | no, default now() | |

## Relationships

Same underlying data as `alerted_leads_log`, aggregated to per-day/per-owner counts, in wide form.

## Gotchas

- **`overdue_followups_last_3_days` is mislabeled** — see `metrics/lead_health_alerts.md`. As shipped, ~85% of what it counts isn't actually overdue (42% future-dated, 43% due today). Uttam is fixing the generating script; until then, don't trust this column's face value.

**Owner:** TBD
**Last verified:** 2026-09-12
