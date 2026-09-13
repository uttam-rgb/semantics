# analytics.admin_permissions

**Status:** ⚠️ UNRESOLVED relationship to `public.admin_permissions` — does not follow the usual superset pattern (see [`schema_map.md`](../../schema_map.md) and [`open_questions.md`](../../open_questions.md) item 18). 411 rows, current through 2026-09-09, vs. `public`'s 10 rows (all sharing one identical timestamp, 2026-03-16) — **zero overlapping IDs between the two**. Not confirmed which (if either) is the "real" one, or whether they're genuinely disjoint datasets.

**Purpose, grain, columns:** see [`tables/public/admin_permissions.md`](../public/admin_permissions.md) — identical schema (`id`, `admin_id` → `Admin.id`, `permission`, `created_at`, `updated_at`).

## Gotchas

- Given the volume and freshness (411 rows, current), this is the more likely candidate to use if forced to pick one — but treat this as a working assumption, not a confirmed fact, until the owner clarifies what `public.admin_permissions`'s 10 rows actually represent.

**Owner:** TBD
**Last verified:** 2026-09-12
