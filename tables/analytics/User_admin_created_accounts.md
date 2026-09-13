# analytics.User

**Status:** ✅ Live. See [naming overview](_admin_user_naming_overview.md) — **not** the same thing as `users` (lowercase), despite the similar name.

**Note on filename:** saved as `User_admin_created_accounts.md` rather than `User.md` to avoid a case-insensitive filename collision with `users.md` on Windows/OneDrive.

**Purpose:** Accounts created *by* an admin on someone else's behalf (e.g., staff registering a customer over the phone), not self-serve signups.

**Grain:** One row per such account. 40 rows, active 2026-05-29 to 2026-09-07.

## Columns

| Column | Type | Notes |
|---|---|---|
| id | text | intended PK, not enforced |
| phone, name | text | the person the account is for |
| admin_id | text | which admin's "workspace" this belongs to |
| created_by_admin_id | text | which admin actually created it — **identical to `admin_id` in the samples checked**, so likely always the same value |
| signed_up | text | ⚠️ text, not timestamp |
| created_at | timestamp with tz | |

## Relationships

`admin_id`/`created_by_admin_id` → `Admin.id` (39 of 40 rows match; 1 does not).

## Gotchas

- Don't confuse with `users` (lowercase) — that's an unrelated marketing/demo-payment signup flow, not a variant spelling of this table.
- 1 of 40 rows has an `admin_id` that doesn't match any `Admin.id` — minor orphan, not a systemic issue.

**Owner:** TBD
**Last verified:** 2026-09-12
