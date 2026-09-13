# analytics.Learner

**Status:** ✅ Authoritative — use this, not `public.Learner` (frozen ~2026-03-17, see [`schema_map.md`](../../schema_map.md)). 4,035 rows, current through 2026-09-11.

**Purpose, grain, and shared columns:** identical to `public.Learner` — see [`tables/public/Learner.md`](../public/Learner.md) for the full shared-column reference and gotchas (dob stored as text, LL_result/DL_result nullable-not-false, password column present, no single "status" field, etc.).

## Analytics-only columns (29 additional, not on `public.Learner`)

Two feature areas not present on the `public` version:

**Car-purchase intent tracking** (likely connects to the [Lane Cars marketplace](_lane_cars_overview.md)): `car_purchase_timeline`, `car_intent_planning`, `car_intent_type`, `car_intent_condition`, `car_intent_timeframe`, `car_intent_source`, `car_intent_updated_at`, `car_onboarding_intent_at`.

**E-signature capture:** `signature_storage_path`, `signature_submitted_at`, `signature_consent_at`, `signature_terms_version`, `signature_privacy_version`, `signature_purpose`, `signature_method`, `signature_mime_type`.

**Other additions:** `two_hour_days`, `LL_approved_date`, `LL_received_date`, `LL_id`, `DL_application_id`, `DL_received`, `DL_received_date`, `has_lesson10_booked`, `address_change_required`, `is_LL_form_filled`, `has_postLL_done`, `has_two_wheeler_license`, `driving_motivation`.

None of these are investigated in depth yet — flagged here so they're not missed, not fully documented.

## Gotchas

Everything in `public.Learner`'s doc applies. Additionally:
- The car-intent fields being present on `Learner` (not a separate table) suggests car-purchase interest is captured as part of the learner profile itself, reinforcing the Lane Cars connection — but there's still no FK from `Learner` to `car_inventory`/`sell_leads`/`buyer_request`.

**Owner:** TBD
**Last verified:** 2026-09-12
