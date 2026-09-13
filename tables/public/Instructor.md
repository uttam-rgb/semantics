# public.Instructor

**Status:** ⚠️ MOSTLY SUPERSEDED — prefer `analytics.Instructor`. `public` is frozen ~2026-03-13 (6 months stale); `analytics` has 20 of `public`'s 23 rows plus 99 more (current through 2026-09-09), and adds onboarding/contract columns (`status`, `contract_signed`, `id_proof_type`, etc.) not present here. **Not a perfect superset** — 3 `public.Instructor` rows aren't in `analytics` at all; see [`schema_map.md`](../../schema_map.md) and [`open_questions.md`](../../open_questions.md). Also note: this table's `car_model` column appears as `car_mode` in `analytics.Instructor` — possible rename/typo, unconfirmed.

**Purpose:** A driving instructor — profile, vehicle details, and service coverage.

**Grain:** One row per instructor.

**⚠️ Primary key is `id_instructor`, not `id`** — the only core table in `public` that breaks the usual `id` naming convention. Every FK to this table (from `Schedule`, `Instructor Unavailability`) points at `id_instructor`.

## Columns (selected — full list has 23 columns)

| Column | Type | Nullable | Notes |
|---|---|---|---|
| id_instructor | text | no | PK |
| name, phone, email | text | yes | |
| password | text | yes | ⚠️ never select/export |
| DL_number | text | yes | the instructor's own driving license number |
| car_make, car_model, car_license, car_number | text | yes | vehicle details |
| car_fuel_type | enum `CarFuelType` | yes | `petrol`, `diesel`, `ev`, `cng`, `lpg`, `hybrid` — observed data only has `petrol` (19) and `diesel` (3); the other values are defined but unused so far |
| experience | smallint | yes | years of experience, presumably |
| enabled | boolean | yes, **no default** | active flag — unlike `Learner.enabled` (defaults `true`), this one has no default, so NULL is possible and its meaning (active? unset?) should be confirmed, not assumed |
| areas | text[] | yes, default `{}` | free-text list of service areas — **not an FK to `Serviceable_Areas`**, just plain strings; don't assume they match `Serviceable_Areas.name` exactly without checking |
| radius | numeric | yes | likely service radius (unit not confirmed — assume km, verify with owner) |
| latitude, longitude, address | numeric/text | yes | |
| unavailability, imported_calendar_events | jsonb | no, default `[]` | freeform, not yet inspected |
| imported_calendar_updated_at | timestamp (no tz) | yes | |
| signed_up | timestamp (no tz) | yes | |

## Relationships

- Referenced by `Instructor Unavailability.instructor_id` and `Schedule.instructor_id`, both pointing at `id_instructor`.

## Gotchas

- **PK is `id_instructor`, not `id`** — easy to write a broken join by assuming otherwise.
- `areas` is a free-text array, not a validated FK to `Serviceable_Areas` — a "coverage by area" report needs explicit normalization/matching, not a join.
- `enabled` has no default — don't assume NULL means either active or inactive without confirming.
- Contains a `password` column — exclude from any report/export.

**Owner:** TBD
**Last verified:** 2026-09-12
