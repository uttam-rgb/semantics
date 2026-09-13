# analytics.Instructor

**Status:** ✅ Mostly authoritative — prefer this over `public.Instructor`, but **not a perfect superset**: 3 of `public.Instructor`'s 23 rows don't appear here at all (see [`schema_map.md`](../../schema_map.md) and [`open_questions.md`](../../open_questions.md) item 19). 122 rows, current through 2026-09-09.

**Purpose, grain, PK (`id_instructor`, not `id`), and shared columns:** see [`tables/public/Instructor.md`](../public/Instructor.md) for the full shared reference and gotchas (password column, `areas` not FK'd to `Serviceable_Areas`, etc.).

## Analytics-only columns (not on `public.Instructor`)

| Column | Notes |
|---|---|
| status | e.g. `active`/`inactive` — same vocabulary as `instructor_availability.status` and tracked historically in `instructor_status_log` |
| contract_signed, contract_signed_at | onboarding/compliance |
| id_proof_type, id_proof_number | onboarding/compliance |
| onboarding_completed, onboarding_completed_at | |

## Renamed/inconsistent column

**`public.Instructor.car_model` appears as `car_mode` here** — likely a rename or typo somewhere in the pipeline between the two schemas. Confirm which is correct before trusting either; don't assume `car_mode` is a meaningful field distinct from "car model."

## Gotchas

- Not a full superset of `public.Instructor` — 3 rows are missing. Spot-check before assuming this table has every instructor `public` ever had.
- Cross-reference `instructor_status_log` for the history behind the `status` column, and `instructor_availability`/`instructor_leave_request` for current/planned unavailability.

**Owner:** TBD
**Last verified:** 2026-09-12
