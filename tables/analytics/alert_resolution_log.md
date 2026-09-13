# analytics.alert_resolution_log

**Status:** Part of the [lead-alerting/reporting system](_reporting_system_overview.md).

**Purpose (from the table's own Postgres comment):** *"Daily resolution check: of leads alerted yesterday, how many moved stage by this morning. Sent as a stakeholder-only email each morning before per-owner reports go out."*

**Grain:** One row per (check_date, alert_date, alert_type, lead_owner) — enforced by a composite primary key.

## Columns

| Column | Type | Nullable | Notes |
|---|---|---|---|
| check_date | date | no | part of PK — the morning this resolution check ran |
| alert_date | date | no | part of PK — the day the original alert (in `alerted_leads_log`) went out |
| alert_type | text | no | part of PK — same 10 values as `alerted_leads_log.alert_type` |
| lead_owner | text | no | part of PK |
| total_alerted | integer | no, default 0 | how many leads were alerted for this owner/type/date |
| moved | integer | no, default 0 | how many of those moved to a different stage by `check_date` |
| not_moved | integer | no, default 0 | |
| movement_rate_pct | numeric | yes | `moved / total_alerted` as a percentage, presumably — not verified against the raw counts |
| called | integer | yes, default 0 | how many of the alerted leads were called |
| created_at | timestamp with tz | no, default now() | |

## Relationships

Conceptual join to `alerted_leads_log` on `(alert_date, alert_type, lead_owner)` — this table aggregates that one up to a per-owner/per-type/per-day resolution rate.

## Gotchas

None specific — well-defined table with its own doc comment and enforced composite PK.

**Owner:** TBD
**Last verified:** 2026-09-12
