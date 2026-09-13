# public.team_bug_reports

**Status:** ⚠️ SUPERSEDED — use `analytics.team_bug_reports` instead (identical columns; `public` is frozen ~2026-02-20, `analytics` has all 5 rows plus 3 more through 2026-05-14). Internal ops table either way — not relevant to business metrics.

**Purpose:** Bug reports filed by the internal team about the platform.

**Grain:** One row per bug report. Only 5 rows.

## Columns (selected — 24 total)

| Column | Type | Nullable | Notes |
|---|---|---|---|
| id | text | no | PK |
| reporter_name, reporter_role, reporter_phone, reporter_email | varchar | mostly no | |
| report_type | varchar(50) | no, default `'bug'` | |
| platform_section, feature_category | varchar | no | |
| issue_title, issue_description, steps_to_reproduce | varchar/text | no/no/yes | |
| affected_user_phone, affected_user_name | varchar | yes | |
| status | varchar(50) | no, default `'open'` | observed: `open` (5) — only value seen so far |
| priority | varchar(20) | no, default `'medium'` | |
| assigned_to, resolution_notes, resolved_at, resolved_by | varchar/text/timestamp | yes | |
| created_at, updated_at | timestamp (no tz) | no, default CURRENT_TIMESTAMP | |

## Relationships

None.

**Owner:** TBD
**Last verified:** 2026-09-12
