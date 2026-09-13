# analytics.lead_snapshots

**Status:** Part of the [lead-alerting/reporting system](_reporting_system_overview.md).

**Purpose:** A daily point-in-time copy of each lead's funnel stage — lets you answer "what stage was lead X in on day D," not just its current stage (which lives on `cratio_leads_analytics`).

**Grain:** One row per (lead, snapshot day) — a lead gets a new row each day it's captured.

## Columns

| Column | Type | Nullable | Notes |
|---|---|---|---|
| id | integer (serial) | no | PK |
| lead_date | date | no | the lead's original creation date |
| snapshot_day | text | no | the day this snapshot was taken — text, not date; format not verified |
| mobile_number | text | yes | join key back to `cratio_leads_analytics.mobile_number` |
| funnel_stage | text | no | observed: `NEW` (162,817), `CONTACTED` (99,891), `LOST` (51,137), `SEND COURSE DETAILS` (12,065), `Send Payment link` (6,955), `WON` (6,955). **Note this is a different, smaller vocabulary than `cratio_leads_analytics.lead_stage`** (which has 20+ granular values) — this looks like a simplified/rolled-up version of stage for trend tracking. Don't assume they use identical category names. |
| captured_at | timestamp (no tz) | no, default now() | when this row was written |
| created_at | timestamp with tz | no, default now() | |
| lead_owner | text | yes | |

## Relationships

Conceptual join via `mobile_number` to `cratio_leads_analytics` and `alerted_leads_log`. No enforced FK.

## Gotchas

- `funnel_stage` here (6 values) is a simplified vocabulary compared to `cratio_leads_analytics.lead_stage` (20+ values) — confirm the mapping between them before treating this as a drop-in replacement for trend analysis.
- `snapshot_day` is text, not `date` — check format before using in date logic.

**Owner:** TBD
**Last verified:** 2026-09-12
