# public.Learner

**Status:** ⚠️ SUPERSEDED — use `analytics.Learner` instead. `public`'s data is frozen ~2026-03-17 (6 months stale); `analytics` has every row `public` has plus everything since, **and** 29 additional columns covering car-purchase-intent tracking and e-signature capture (`car_intent_*`, `signature_*`) that don't exist in `public` at all. See [`schema_map.md`](../../schema_map.md). Columns/gotchas below also apply to `analytics.Learner`.

**Purpose:** A student/customer going through the driving-license (LL → DL) journey. Holds profile, license status, onboarding, and scheduling preference fields.

**Grain:** One row per learner.

## Columns (selected — full list has 34 columns)

| Column | Type | Nullable | Notes |
|---|---|---|---|
| id | text | no | PK |
| name, email, city, area, pincode | text | yes | profile fields |
| phone | text | no | |
| dob | **text**, not a date type | yes | ⚠️ free-text date of birth — format not verified; don't use directly in date arithmetic without checking actual formatting first |
| password | text | yes | ⚠️ present on this table — never select/export this column in any report |
| has_a_DL | boolean | yes | already holds a driving license (DL) before joining, e.g. an experienced driver just needing a refresher — NULL likely means unknown, not false |
| LL_test_date, LL_result, LL_application_id, LL_received, LL_application_approved, LL_team_appointment_booked | date/bool/text | yes/no default false | Learner's License (the learner's permit, obtained before behind-the-wheel training) application pipeline. `LL_result` is nullable boolean — NULL likely means "not yet taken," not "failed"; don't treat NULL as false. |
| DL_test_date, DL_result, DL_id | date/bool/text | yes | Driving License (final) test tracking — same NULL-vs-fail caution as `LL_result` |
| enabled | boolean | no, default `true` | active/soft-delete flag — filter `enabled = true` for "active learners" |
| onboarding_completed | boolean | yes | |
| needs_scheduling | boolean | no, default `false` | |
| start_date, preferred_start_date, preferred_completion_days, prefers_two_hour_classes | date/int/bool | yes | scheduling preferences |
| pick_up_location, address_lat, address_lng, aadhar_state | text/numeric | yes | location fields |
| unavailability | jsonb | yes | freeform, not yet inspected |
| signed_up | timestamp (no tz) | yes | |
| comments | text | yes | freeform notes |

## Relationships

Referenced by (all via `learner_id` → `Learner.id`): `Learner Availability`, `Schedule`, `enrollment`, `payment`, `reschedule_requests`, `schedule_preferences`.

## Gotchas

- **No single "status" field** — a learner's overall journey (signed up → LL received → DL passed) has to be derived by combining several boolean/date fields (`LL_received`, `LL_application_approved`, `LL_team_appointment_booked`, `DL_result`, etc.), not read off one column. Don't invent a simplified status without checking which combination of fields the business actually uses.
- `LL_result` / `DL_result` are nullable booleans — treat NULL as "not yet tested," never coerce to `false` (which would wrongly mean "failed").
- `dob` is stored as text, not `date`.
- Contains a `password` column — exclude from any report/export.

**Owner:** TBD
**Last verified:** 2026-09-12
