# public.Admin

**Status:** Internal auth table — not relevant to business metrics.

**Purpose:** Admin/staff user accounts for the internal platform.

**Grain:** One row per admin user. Only 2 rows.

## Columns

| Column | Type | Nullable | Notes |
|---|---|---|---|
| id | text | no | PK |
| phone | text | no | |
| name | text | yes | |
| password | text | no | ⚠️ never select/export |
| is_super_admin, is_admin | boolean | no, default `false` | role flags |
| created_at, signed_up | timestamp (no tz) | yes | |

## Relationships

Referenced by `admin_permissions.admin_id`.

**Owner:** TBD
**Last verified:** 2026-09-12
