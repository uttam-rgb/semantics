# analytics.ll_applications

**Status:** Core table for the Learner's License / Driving License government-application pipeline (a separate subsystem from the lead-alerting tables).

**Purpose:** Current state of each learner's LL (Learner's License) and/or DL (Driving License) government application — a much more granular, operational pipeline than `public.Learner`'s simple boolean flags (`LL_received`, `DL_result`, etc.).

**Grain:** One row per application. **No enforced PK** despite having an `id` column — uniqueness not verified.

## Columns (selected — 39 total)

| Column | Type | Notes |
|---|---|---|
| id | text | intended PK, not enforced |
| learner_id | text | join to `Learner` (schema not confirmed — could be `public.Learner` or `analytics.Learner`, see `schema_map.md`) |
| status | text | **15 distinct granular pipeline stages observed**, no enum: `ll_issued` (269), `dl_date_selection` (197), `classes_in_progress` (195), `payment_received` (158), `dl_test_scheduled` (69), `ob_form_enabled` (53), `dl_results_pending` (40), `dl_date_preference_received` (27), `meet_booking_enabled` (27), `ll_test_enabled` (17), `docs_under_review` (14), `application_ready` (12), `dl_test_passed` (12), `appointment_booked` (11), `waiting_rto_verification` (11). This is a detailed government-paperwork pipeline (RTO = Regional Transport Office) — a status-to-plain-English mapping should come from the owner, not be guessed. |
| ll_type | text | `with_classes` (605), NULL (543), `direct_dl` (20) — whether this application is bundled with driving classes or is a direct-DL-only application |
| services | text (JSON-shaped string, not `jsonb`) | e.g. `'["ll", "classes", "dl"]'` — which services this application covers. Needs a JSON parse/cast, not a `jsonb` type, to query the array contents. |
| application_number, ll_number, dl_number, dl_application_number, batch_code | text | external reference numbers |
| application_date, scrutiny_approved_date, ll_matures_at, dl_test_date, scrutiny_expiry_date, dl_application_date, dl_preferred_date, dl_expiry_date, ll_issue_date, ll_expiry_date, date_of_birth | date | proper `date` type (unlike `cratio_leads_analytics`, these are typed correctly) |
| dl_test_rto, dl_preferred_rto, dl_test_rto_address | text | RTO (government office) details |
| rejection_reason, escalation_reason | text | |
| escalated | boolean | |
| call_missed_count | bigint | |
| reapply_fee | double precision | |
| dl_retest_fee | text | ⚠️ likely a fee amount stored as text, not numeric — inconsistent with `reapply_fee` which is properly typed |
| form_data | text | freeform, likely JSON-shaped |
| form_submitted_at, status_changed_at | timestamp with tz | |
| reminders_sent | text | |
| dl_dispatch_eta, dl_tracking_ref | text | DL card dispatch tracking |
| created_at, updated_at | timestamp with tz | |

## Relationships

`learner_id` conceptually joins to a `Learner` table (confirm which schema). `id` conceptually joins to `ll_pipeline_events.application_id`. No enforced FKs.

## Gotchas

- No enforced PK on `id` — verify uniqueness before treating it as one.
- `status` has 15+ raw values with no documented mapping to plain-English stages — get this from the owner rather than inferring from the string names.
- `dl_retest_fee` is text while its sibling `reapply_fee` is a real numeric type — inconsistent, cast carefully.
- `services` looks like a JSON array but is stored as plain text — needs parsing, not `jsonb` operators.

**Owner:** TBD
**Last verified:** 2026-09-12
