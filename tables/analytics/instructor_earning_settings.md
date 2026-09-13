# analytics.instructor_earning_settings

**Status:** ☠️ Not yet in use — 0 rows.

**Purpose (intended):** Per-instructor override of the global defaults in `earning_config` (per-class rate, monthly class target).

**Grain:** One row per instructor.

## Columns

All columns are `text` (including `per_class_rate`, `monthly_class_target`, `updated_at`) — will need casting once populated.

| Column | Notes |
|---|---|
| instructor_id | → `Instructor.id_instructor`, intended PK |
| per_class_rate | overrides `earning_config.default_per_class_rate` |
| monthly_class_target | overrides `earning_config.default_monthly_target` |
| updated_at | text, not timestamp |

## Relationships

`instructor_id` → `Instructor.id_instructor` (not enforced).

## Gotchas

- 0 rows — no instructor currently has a custom override; all instructors effectively use `earning_config`'s global defaults.

**Owner:** TBD
**Last verified:** 2026-09-12
