# public.admin_permissions

**Status:** ⚠️ UNRESOLVED — does not follow the usual public/analytics pattern. Unlike the other shared tables, `public.admin_permissions` and `analytics.admin_permissions` have **zero overlapping IDs** — they look genuinely disjoint, not a stale-subset relationship. `public`'s 10 rows also all share one identical `created_at` timestamp (2026-03-16), suggesting a one-time bulk seed rather than organic growth. See [`open_questions.md`](../../open_questions.md) item 18. Internal auth/ops table either way — not relevant to business metrics.

**Purpose:** Grants specific permissions to admin users.

**Grain:** One row per (admin, permission) grant.

## Columns

| Column | Type | Nullable | Notes |
|---|---|---|---|
| id | text | no | PK |
| admin_id | text | no | FK → `Admin.id` |
| permission | text | no | free-text permission name |
| created_at, updated_at | timestamp (no tz) | no, default CURRENT_TIMESTAMP | |

## Relationships

`admin_id` → `Admin.id`. Not referenced elsewhere.

**Owner:** TBD
**Last verified:** 2026-09-12
