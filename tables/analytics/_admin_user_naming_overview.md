# Admin / User naming collisions — what's actually going on

Five tables with confusable names (`Admin`, `AdminProfiles`, `adminprofiles`, `User`, `users`) turn out to be a mix of one live table, two dead ones, and two genuinely different features. Verified 2026-09-12.

| Table | Rows | Status |
|---|---|---|
| `Admin` | 17 | ✅ Live — the real admin/staff account table, active through 2026-08-27 |
| `AdminProfiles` | 0 | ☠️ Dead — never populated, all-text columns (even `created_at`) |
| `adminprofiles` (lowercase) | 3 | ☠️ Dead — rows exist but every field except `id`/`created_at` is NULL; all from a single day, 2025-08-14. Earliest of the three, abandoned attempt. |
| `User` | 40 | ✅ Live — sub-accounts created **by** an admin (see below), active 2026-05-29 to 2026-09-07 |
| `users` | 122 | ✅ Live — a completely different, separate signup/payment flow (see below), active 2025-07-23 to 2026-09-08 (most recent of everything in this group) |

## `Admin` vs `AdminProfiles`/`adminprofiles`

Read as three successive attempts at the same "admin profile" concept, where only the most recent (`Admin`) stuck. **Use `Admin`; treat the other two as dead.** Of `Admin`'s 17 rows: 7 have `name` populated, 7 have `is_admin = true`, 2 have `is_super_admin = true` — the other 10 rows look like incomplete/placeholder signups (no name, `is_admin = false`). Don't assume all 17 rows are real active admins.

**Also note:** `public.Admin` (2 rows) is a poor match for `analytics.Admin` — only 1 of the 2 `public.Admin` phone numbers appears in `analytics.Admin`. Unlike the bucket-C tables (`Learner`, `payment`, etc.), this pair does **not** look like a clean stale-subset relationship. Treat as unresolved, similar to `admin_permissions` (see [`open_questions.md`](../../open_questions.md)).

## `User` vs `users` — two unrelated features, not a naming drift

- **`User`** (40 rows): accounts created *by* an admin — `admin_id`/`created_by_admin_id` on 39 of 40 rows match an `Admin.id`. This looks like admin-assisted account creation (e.g., staff registering someone over the phone), not self-serve signup.
- **`users`** (122 rows, 16 columns): a **structurally different table** — has `email`, `area`, `has_license`, and a full `payment_status`/`payment_txn_ref`/`payment_gateway_ref`/`payment_amount`/`payment_response_code`/`payment_message`/`payment_date` set (all stored as text). This looks like a separate marketing/landing-page lead-capture flow with an attached demo-payment step — unrelated to `Learner`/`payment`/`enrollment`. About 12 of 122 rows (10%) look like test data (`name = 'Test'` or a `test`-containing email) — exclude those before reporting on this table.

**Don't assume `User` and `users` are the same thing with different casing — they serve different purposes and have different schemas.**
