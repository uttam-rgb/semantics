# analytics.support_ticket

**Status:** Live, low-volume ops table (4 rows).

**Purpose:** Support tickets raised by instructors (and possibly other roles, via `raised_by_role`) — app issues, payment issues, etc.

**Grain:** One row per ticket.

## Columns

| Column | Type | Notes |
|---|---|---|
| id | text | |
| raised_by_role | text | e.g. `'instructor'` |
| instructor_id | text | → `Instructor.id_instructor` (confirm schema) |
| category | text | e.g. `'app'`, `'payment'` |
| priority | text | e.g. `'normal'`, `'urgent'` |
| subject, description | text | free text — sample includes test data (`'Test'`/`'Test'`) |
| status | text | e.g. `'open'` |
| admin_response, assigned_to, resolved_by | text | |
| resolved_at | text | ⚠️ text, not timestamp |
| created_at, updated_at | timestamp with tz | |

## Relationships

`instructor_id` → `Instructor.id_instructor` (not enforced).

## Gotchas

- Contains visible test data (`subject='Test'`).

**Owner:** TBD
**Last verified:** 2026-09-12
