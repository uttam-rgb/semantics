# analytics.AdminProfiles

**Status:** ☠️ DEAD — 0 rows, never populated. See [naming overview](_admin_user_naming_overview.md). Use [`Admin`](Admin.md) instead.

**Note on filename:** Postgres has both `"AdminProfiles"` (this table, CamelCase, 0 rows) and `"adminprofiles"` (lowercase, 3 rows — see [`adminprofiles_lowercase_dead.md`](adminprofiles_lowercase_dead.md)) as **distinct tables** — Postgres identifiers are case-sensitive when quoted. Since Windows/OneDrive filesystems are case-**insensitive**, these two docs cannot use filenames that differ only by case (they'd collide) — hence the disambiguating suffixes here.

**Columns:** `id`, `name`, `phone`, `created_at` — all typed as `text`, including `created_at` (a sign this was never wired up to real application code).

**Owner:** TBD
**Last verified:** 2026-09-12
