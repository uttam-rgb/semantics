# analytics.low_util_instructor_leads

**Status:** ⚠️ STALE — same single-week snapshot issue as `instructor_utilisation` (2026-04-27), which this table is derived from. Note that the *live* utilization report (see [`metrics/instructor_utilization.md`](../../metrics/instructor_utilization.md)) doesn't use `instructor_utilisation` at all, so this table is likely derived from an abandoned approach too — treat as unused unless the owner says otherwise.

**Purpose:** Connects underutilized instructors to nearby leads — likely used to prioritize routing leads toward instructors who have spare capacity.

**Grain:** One row per (week_start, mobile_number, instructor_name) — enforced by a unique constraint. 1,713 rows, all in the single 2026-04-27 week.

## Columns

| Column | Type | Nullable | Notes |
|---|---|---|---|
| id | integer (serial) | no | PK |
| week_start, week_end | date | no | only `2026-04-27`/presumably `2026-05-03` present, matching `instructor_utilisation`'s single week |
| instructor_name, instructor_id | text | yes | |
| utilisation_pct, available_hours, booked_hours | numeric | yes | copied from `instructor_utilisation` for that instructor/week |
| contact_name, mobile_number, customer_location | text | yes | the lead |
| lead_stage, lead_owner | text | yes | same vocabulary as `cratio_leads_analytics.lead_stage`/`.lead_owner` |
| expected_revenue, price_offered | text | yes | ⚠️ stored as text again, matching `cratio_leads_analytics` |
| next_followup_on, lead_date | text | yes | ⚠️ stored as text, not date |
| computed_at | timestamp (no tz) | yes | |

## Relationships

`mobile_number` conceptually → `cratio_leads_analytics.mobile_number`. `instructor_id`/`instructor_name` → `instructor_utilisation`/`Instructor`.

## Gotchas

- Same staleness issue as `instructor_utilisation` — only one week of data, dated 2026-04-27.
- Revenue/date fields are text, same casting caveat as `cratio_leads_analytics`.

**Owner:** TBD
**Last verified:** 2026-09-12
