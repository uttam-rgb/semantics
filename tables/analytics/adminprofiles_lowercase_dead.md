# analytics.adminprofiles (lowercase)

**Status:** ☠️ DEAD — 3 rows, all from a single day (2025-08-14), and every field except `id`/`created_at` is NULL. Looks like the earliest, abandoned attempt at the "admin profile" concept. See [naming overview](_admin_user_naming_overview.md). Use [`Admin`](Admin.md) instead.

**Note on filename:** see [`AdminProfiles_camelcase_empty.md`](AdminProfiles_camelcase_empty.md) — Postgres has this as a separate, case-sensitive table name from `"AdminProfiles"`; the filenames here are disambiguated because Windows/OneDrive filesystems are not case-sensitive.

**Columns:** `id` (bigint — the only one of the three admin-ish tables with an integer PK instead of text/uuid), `name`, `phone`, `created_at`, `password` — all NULL except `id`/`created_at` in the 3 existing rows.

**Owner:** TBD
**Last verified:** 2026-09-12
