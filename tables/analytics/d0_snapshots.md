# analytics.d0_snapshots

**Status:** Live. Part of the [lead-alerting/reporting system](_reporting_system_overview.md) — missed from that overview's original table list, added here.

**Purpose:** A "day zero" snapshot of each lead's funnel stage — likely captured once, on the lead's creation day, as a baseline to compare against later stage snapshots (`lead_snapshots`) for measuring same-day vs. follow-up movement.

**Grain:** One row per lead, captured on day 0. 744 rows.

## Columns

| Column | Type | Notes |
|---|---|---|
| id | integer | PK |
| lead_date | date | |
| mobile_number | text | → `cratio_leads_analytics.mobile_number` |
| funnel_stage | text | same simplified vocabulary as `lead_snapshots.funnel_stage` (NEW/CONTACTED/LOST/etc.), not `cratio_leads_analytics.lead_stage`'s 20+ raw values |
| captured_at | timestamp (no tz) | |

## Relationships

`mobile_number` conceptually → `cratio_leads_analytics`. No enforced FK. Structurally a simpler subset of `lead_snapshots` (no `snapshot_day`/`lead_owner` columns) — likely a specific "day 0" cut of that same snapshotting process rather than an independent table.

**Owner:** TBD
**Last verified:** 2026-09-12
