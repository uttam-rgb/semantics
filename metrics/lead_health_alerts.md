---
metric: lead_health_alerts
aliases: [untapped leads, not contacted, no followup set, followups due today, overdue followups, stuck 50pct payment, send payment links, send course details, hot lead priority, lead health check]
status: confirmed
owner: TBD
confirmed_by: "Uttam — from production script SQL_Logic/health_metric.sql, 2026-09-12. Uttam identified and will fix the overdue_followups naming/logic bug in the source script; corrected version documented here per his instruction."
confirmed_date: 2026-09-12
last_verified: 2026-09-12
source: analytics.cratio_leads_analytics
grain: one row per (lead_owner) — each alert type counts DISTINCT mobile_number per owner
time_field: lead_date / next_followup_on, per alert type (see table below)
dimensions: [lead_owner]
---

## What this is

This is the **generating logic behind `alert_metric_snapshots` and `alerted_leads_log`** (the daily lead-alerting system documented back in `tables/analytics/_reporting_system_overview.md`) — previously only known by table schema and Postgres comments, never by the actual computation. `SQL_Logic/health_metric.sql` is that computation. All counts are `COUNT(DISTINCT mobile_number)` grouped by `lead_owner`.

## Reusable building block: "active stages"

Six `lead_stage` values are treated as "still active / worth chasing" across several of these alerts: `'Agreed to pay'`, `'SEND COURSE DETAILS'`, `'RNR_3'`, `'RNR_2'`, `'RNR'`, `'CALL BACK'`. This is a **third** lead-stage grouping in this project, distinct from both `lead_status_buckets.md`'s "Lead Rules" and the "Business Rules → Status Bucket" mapping — don't conflate the three. This one has no name of its own in the spreadsheet; called "active_stages" here for reference.

## The 9 alert conditions

| Alert | Formula | Verified count (all owners, 2026-09-12) |
|---|---|---|
| `untapped_leads_yesterday` | `lead_stage = 'NEW' AND lead_date = yesterday` | 86 |
| `leads_not_contacted_7_days` | `lead_stage = 'NEW' AND lead_date BETWEEN 7 days ago AND 2 days ago` | 3 |
| `leads_no_followup_set` | `lead_stage IN (active_stages) AND next_followup_on IS NULL AND lead_date >= 7 days ago` | 214 |
| `followups_due_today` | `next_followup_on = today AND lead_stage IN (active_stages)` | 945 |
| `overdue_followups_last_3_days` ⚠️ see below | *(as shipped, buggy — see below)* | 2,185 |
| `revenue_stuck_50pct_payment` | `lead_stage = '50% PAYMENT DONE' AND lead_date <= 3 days ago` | 948 |
| `send_payment_links` | `lead_stage = 'Agreed to pay' AND lead_date >= 90 days ago AND (next_followup_on IS NULL OR next_followup_on <= today)` | 18 |
| `send_course_details` | same pattern, `lead_stage = 'SEND COURSE DETAILS'` | 308 |
| `hot_lead_priority` | same pattern, `lead_stage = 'Hot Lead- Close to conversion'` | 78 |

## ⚠️ `overdue_followups_last_3_days` — confirmed bug, fix documented here

**As currently shipped in `health_metric.sql`**: `WHERE next_followup_on >= CURRENT_DATE - INTERVAL '7 days' AND lead_stage IN (active_stages)` — no upper bound, so it's not filtering for "overdue" (past-due) at all, and the window is 7 days, not 3 (the column name lies about both the window and the overdue-ness). Verified by breaking down its 2,186 matching rows:

| Sub-group | Count | % |
|---|---|---|
| Future-dated (`next_followup_on > today`) — **not overdue** | 926 | 42% |
| Due today | 945 | 43% |
| Genuinely overdue (`next_followup_on < today`) | 315 | 14% |

**Per Uttam (2026-09-12): the correct metric is "Overdue Followups, Last 7 Days"** — he's fixing the source script. Corrected formula and SQL below.

### Corrected formula
```
COUNT(DISTINCT mobile_number)
WHERE next_followup_on >= CURRENT_DATE - INTERVAL '7 days'
  AND next_followup_on <  CURRENT_DATE          -- the missing upper bound
  AND lead_stage IN (active_stages)
```

### Corrected SQL
```sql
select lead_owner, count(distinct mobile_number) as overdue_followups_last_7_days
from analytics.cratio_leads_analytics
where nullif(next_followup_on,'')::date >= current_date - interval '7 days'
  and nullif(next_followup_on,'')::date <  current_date
  and lead_stage in ('Agreed to pay','SEND COURSE DETAILS','RNR_3','RNR_2','RNR','CALL BACK')
group by 1
order by 2 desc;
```

Verified 2026-09-12: **315 total** (matches the "genuinely overdue" sub-group above, as expected). Top owners: Sunith kumar (95), Yashas G (65), Shashank s (62).

## Verified SQL (full script, as shipped)

```sql
WITH base AS (
    SELECT
        lead_owner, mobile_number, lead_stage,
        NULLIF(lead_date, '')::date        AS lead_date,
        NULLIF(next_followup_on, '')::date AS next_followup_on
    FROM analytics.cratio_leads_analytics
),
active_stages(stage) AS (
    VALUES ('Agreed to pay'), ('SEND COURSE DETAILS'), ('RNR_3'), ('RNR_2'), ('RNR'), ('CALL BACK')
),
untapped_yesterday AS (
    SELECT lead_owner, COUNT(DISTINCT mobile_number) AS untapped_leads_yesterday
    FROM base WHERE lead_stage = 'NEW' AND lead_date = CURRENT_DATE - INTERVAL '1 day'
    GROUP BY lead_owner
),
not_contacted_7d AS (
    SELECT lead_owner, COUNT(DISTINCT mobile_number) AS leads_not_contacted_7_days
    FROM base WHERE lead_stage = 'NEW'
      AND lead_date BETWEEN CURRENT_DATE - INTERVAL '7 days' AND CURRENT_DATE - INTERVAL '2 days'
    GROUP BY lead_owner
),
no_followup AS (
    SELECT lead_owner, COUNT(DISTINCT mobile_number) AS leads_no_followup_set
    FROM base WHERE lead_stage IN (SELECT stage FROM active_stages)
      AND next_followup_on IS NULL AND lead_date >= CURRENT_DATE - INTERVAL '7 days'
    GROUP BY lead_owner
),
followups_today AS (
    SELECT lead_owner, COUNT(DISTINCT mobile_number) AS followups_due_today
    FROM base WHERE next_followup_on = CURRENT_DATE
      AND lead_stage IN (SELECT stage FROM active_stages)
    GROUP BY lead_owner
),
-- overdue_followups: shown here AS SHIPPED (buggy) — see corrected version above
overdue_followups AS (
    SELECT lead_owner, COUNT(DISTINCT mobile_number) AS overdue_followups_last_3_days
    FROM base WHERE next_followup_on >= CURRENT_DATE - INTERVAL '7 days'
      AND lead_stage IN (SELECT stage FROM active_stages)
    GROUP BY lead_owner
),
stuck_50_payment AS (
    SELECT lead_owner, COUNT(DISTINCT mobile_number) AS revenue_stuck_50pct_payment
    FROM base WHERE lead_stage = '50% PAYMENT DONE' AND lead_date <= CURRENT_DATE - INTERVAL '3 days'
    GROUP BY lead_owner
),
send_payment_links AS (
    SELECT lead_owner, COUNT(DISTINCT mobile_number) AS send_payment_links
    FROM base WHERE lead_stage = 'Agreed to pay' AND lead_date >= CURRENT_DATE - INTERVAL '90 days'
      AND (next_followup_on IS NULL OR next_followup_on <= CURRENT_DATE)
    GROUP BY lead_owner
),
send_course_details AS (
    SELECT lead_owner, COUNT(DISTINCT mobile_number) AS send_course_details
    FROM base WHERE lead_stage = 'SEND COURSE DETAILS' AND lead_date >= CURRENT_DATE - INTERVAL '90 days'
      AND (next_followup_on IS NULL OR next_followup_on <= CURRENT_DATE)
    GROUP BY lead_owner
),
hot_lead_priority AS (
    SELECT lead_owner, COUNT(DISTINCT mobile_number) AS hot_lead_priority
    FROM base WHERE lead_stage = 'Hot Lead- Close to conversion' AND lead_date >= CURRENT_DATE - INTERVAL '90 days'
      AND (next_followup_on IS NULL OR next_followup_on <= CURRENT_DATE)
    GROUP BY lead_owner
)
-- final SELECT: one row per lead_owner, all 9 alert counts, COALESCEd to 0 — see full script for the join
```

(Full script with the final `owners`/`SELECT`/`LEFT JOIN` assembly: `SQL_Logic/health_metric.sql`.)

Verified 2026-09-12, company-wide sums: `send_payment_links`=18, `send_course_details`=308, `hot_lead_priority`=78, `followups_due_today`=945, `overdue_followups_last_3_days` (as shipped)=2,185, `untapped_leads_yesterday`=86, `leads_no_followup_set`=214, `leads_not_contacted_7_days`=3, `revenue_stuck_50pct_payment`=948. 40 distinct owners appear across these alerts.

## Gotchas

- **Column name says "3 days," logic uses 7 days, and doesn't check overdue-ness at all** — see the correction above. Uttam is fixing the source script; until that ships, treat `overdue_followups_last_3_days` as reporting "active leads with a followup date from the last week or later, including future dates" — not "overdue."
- **`followups_due_today` (and the corrected `overdue_followups_last_7_days`) are restricted to the 6 "active stages"** — a broader, unrestricted "any lead with `next_followup_on = today`, regardless of stage" count is **1,209**, materially higher than the active-stages-restricted **944**. If "Follow ups Scheduled for Today - Agent and Total" (as named in the spreadsheet) is meant to cover *all* leads rather than just active ones, use the unrestricted version instead — not yet confirmed which is intended.
- **`leads_not_contacted_7_days` returns tiny numbers (3 company-wide)** — this looks low relative to the other alerts; not investigated further, but worth a sanity check against expectations before reporting it as-is.
- **A third, unnamed `lead_stage` grouping exists here** (`active_stages`) — don't confuse with `lead_status_buckets.md`'s "Lead Rules" or the "Business Rules → Status Bucket" mapping. Three different groupings of the same field, for three different purposes.
- `lead_date` and `next_followup_on` are cast via `NULLIF(x,'')::date` here (both are `text` columns) — empty-string-to-NULL handling matters, a raw `::date` cast on `''` errors.

## Owner

TBD

**Last verified:** 2026-09-12
