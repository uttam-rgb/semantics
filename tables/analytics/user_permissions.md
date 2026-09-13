# analytics.user_permissions

**Status:** Live (661 rows).

**Purpose:** Permission grants for `analytics.User` (admin-created) accounts — not the same as `analytics.admin_permissions`, which grants permissions to `Admin` accounts.

**Grain:** One row per (user, permission) grant.

## Columns

| Column | Type | Notes |
|---|---|---|
| id | text | |
| user_id | text | → `User.id` (the CamelCase `User` table — see [`_admin_user_naming_overview.md`](_admin_user_naming_overview.md) — **not** `users` lowercase) |
| permission | text | e.g. `'learner_management'` |
| created_at, updated_at | timestamp with tz | |

## Relationships

`user_id` → `User.id` (not enforced).

## Gotchas

- Easy to confuse with `admin_permissions` (grants to `Admin`) — this table grants to `User` accounts specifically. Also easy to confuse `user_id` here with a row in `users` (lowercase) — it's the CamelCase `User` table, per the naming overview.

**Owner:** TBD
**Last verified:** 2026-09-12
