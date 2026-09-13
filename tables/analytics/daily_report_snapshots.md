# analytics.daily_report_snapshots

**Status:** ✅ Very likely the right table for "revenue/conversion by owner" reporting. Part of the [lead-alerting/reporting system](_reporting_system_overview.md).

**Purpose (from the table's own Postgres comment):** *"Daily KPI snapshot per lead owner. Used to track macro business impact: SLA compliance, conversion rates, and revenue trends over time."*

**Grain:** One row per (snapshot_date, lead_owner) — enforced by a composite primary key. Cleanly typed (real `numeric`/`integer` columns) — unlike `cratio_leads_analytics`, this table is safe to aggregate directly without casting.

## Columns

| Column | Type | Nullable | Notes |
|---|---|---|---|
| snapshot_date | date | no | part of PK. Data observed from 2026-04-11 through 2026-09-12 (today) |
| lead_owner | text | no | part of PK |
| new_leads_allocated | integer | no, default 0 | |
| yet_to_be_tapped_leads | integer | no, default 0 | |
| first_contact_sla_pct | numeric | yes | e.g. `20.00` = 20% |
| total_calls_made | integer | no, default 0 | |
| calls_made_for_new_leads | integer | no, default 0 | |
| calls_made_for_old_leads | integer | no, default 0 | |
| conversions | integer | no, default 0 | |
| new_lead_conversions | integer | no, default 0 | |
| old_lead_conversions | integer | no, default 0 | |
| conversion_rate | numeric | yes | e.g. `0.0256` = 2.56% — note this is a **fraction, not a percentage** (unlike `first_contact_sla_pct`, which is already ×100) — check the scale before formatting |
| revenue_booked | numeric | no, default 0 | total revenue for this owner/day |
| new_lead_revenue_booked | numeric | no, default 0 | |
| old_lead_revenue_booked | numeric | no, default 0 | |
| avg_revenue_per_conversion | numeric | yes | |
| created_at | timestamp with tz | no, default now() | |

## Relationships

`lead_owner` joins to `cratio_leads_analytics.lead_owner`, `lead_owner_target.lead_owner`, `alerted_leads_log.lead_owner`, `alert_metric_snapshots.lead_owner`. No enforced FK.

## Gotchas

- **`conversion_rate` is a fraction (0–1), while `first_contact_sla_pct` is already a percentage (0–100).** Don't apply the same ×100 formatting to both.
- This is a **daily snapshot per owner**, not a running total — summing `revenue_booked` across a date range for one owner gives that owner's revenue over that range; summing across owners for one day gives that day's total revenue. Be explicit about which dimension you're aggregating over.

**Owner:** TBD
**Last verified:** 2026-09-12
