# analytics.users (lowercase)

**Status:** ✅ Live — a separate, unrelated feature from `User` (see [naming overview](_admin_user_naming_overview.md)). Most recently updated of anything in this admin/user group (through 2026-09-08).

**Note on filename:** saved as `users_lowercase_signup_funnel.md` rather than `users.md` to avoid a case-insensitive filename collision with `User_admin_created_accounts.md` on Windows/OneDrive.

**Purpose:** Looks like a marketing/landing-page lead-capture flow with an attached demo-payment step — separate from the core `Learner`/`payment`/`enrollment` system. Not confirmed with the owner; inferred from the column set (payment gateway fields alongside a simple contact form).

**Grain:** One row per signup. 122 rows, active 2025-07-23 to 2026-09-08.

## Columns

| Column | Type | Notes |
|---|---|---|
| id | text | intended PK, not enforced |
| name, phone, email | text | |
| area, custom_area | text | e.g. `'Indiranagar \| '` — has a trailing pipe/space artifact in samples seen, worth checking formatting before grouping by area |
| has_license | boolean | |
| payment_status, payment_txn_ref, payment_gateway_ref, payment_amount, payment_response_code, payment_message, payment_date | text | a full payment-gateway callback record, all stored as text — mostly NULL in samples seen |
| created_at, updated_at | timestamp with tz | |

## Relationships

None enforced. Not obviously linked to `Learner`/`payment` — treat as a separate funnel unless the owner says otherwise.

## Gotchas

- **~10% of rows (12/122) look like test data** — `name = 'Test'` or an email containing `test` — exclude before reporting signup volume.
- `area`/`custom_area` have formatting artifacts (trailing `| `) in the samples checked — normalize before grouping.
- Purpose is inferred, not confirmed — ask the owner what this table/feature actually is before building a metric on it.

**Owner:** TBD
**Last verified:** 2026-09-12
