# analytics.Admin

**Status:** ✅ Live admin/staff account table. See [naming overview](_admin_user_naming_overview.md) for how this relates to `AdminProfiles`/`adminprofiles` (dead) and why `public.Admin` is a poor match for this table.

**Purpose:** Admin/staff user accounts for the internal platform, including a super-admin flag and self-referencing "created by" hierarchy.

**Grain:** One row per admin account. 17 rows, active 2026-02-19 to 2026-08-27.

## Columns

| Column | Type | Notes |
|---|---|---|
| id | text | intended PK, not enforced |
| phone | text | |
| name | text | ⚠️ NULL for 10 of 17 rows |
| password | text | ⚠️ never select/export |
| is_super_admin, is_admin | boolean | 7/17 have `is_admin = true`; 2/17 have `is_super_admin = true` — the other 10 rows look incomplete/placeholder |
| created_by_admin_id | text | self-referencing — which admin created this one |
| signed_up | text | ⚠️ text, not timestamp |
| created_at | timestamp with tz | |

## Relationships

Referenced conceptually by `User.admin_id`/`User.created_by_admin_id` (39 of 40 `User` rows match an `Admin.id` here).

## Gotchas

- No enforced PK.
- 10 of 17 rows have no `name` and `is_admin = false` — likely incomplete signups, not real active staff. Filter before reporting "number of admins."

**Owner:** TBD
**Last verified:** 2026-09-12
