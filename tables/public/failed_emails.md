# public.failed_emails

**Status:** Internal ops/error-log table — not relevant to business metrics.

**Purpose:** Tracks failed lesson/calendar-notification emails to learners, instructors, and admins, including retry state per recipient type.

**Grain:** One row per notification event (which may target multiple recipients). Only 1 row currently.

## Columns (selected — 18 total)

| Column | Type | Nullable | Notes |
|---|---|---|---|
| id | text | no | PK |
| learner_email, instructor_email, admin_email | text | yes | |
| learner_sent, instructor_sent, admin_sent | boolean | no, default `false` | per-recipient delivery status |
| is_multi_event | boolean | no, default `false` | |
| events_data, learner_ics_array, instructor_ics_array | jsonb | yes | calendar event payloads |
| errors | text[] | yes | |
| subject, message | text | yes | |
| resolved | boolean | no, default `false` | |
| created_at | timestamp (no tz) | no, default CURRENT_TIMESTAMP | |

## Relationships

None.

**Owner:** TBD
**Last verified:** 2026-09-12
