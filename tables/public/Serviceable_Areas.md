# public.Serviceable_Areas

**Status:** ⚠️ SUPERSEDED — use `analytics.Serviceable_Areas` instead (identical columns; `public` is frozen ~2026-03-15, `analytics` has every row plus everything since, through 2026-06-12). See [`schema_map.md`](../../schema_map.md).

**Purpose:** Named geographic areas where the service is offered/enabled.

**Grain:** One row per named area. 136 rows.

## Columns

| Column | Type | Nullable | Notes |
|---|---|---|---|
| id | text | no | PK |
| name | text | no | |
| active | boolean | no, default `true` | filter `active = true` for currently-serviceable areas |
| created_at, updated_at | timestamp (no tz) | no, default CURRENT_TIMESTAMP | |

## Relationships

None enforced — no FK to or from this table. `Instructor.areas` is a free-text array that likely *should* correspond to these names, but there's no database-level link; treat any join between them as a text match, not a guaranteed-consistent FK.

## Gotchas

- No FK relationship to `Instructor.areas` despite the obvious conceptual link — verify text values actually match before joining on area name.

**Owner:** TBD
**Last verified:** 2026-09-12
