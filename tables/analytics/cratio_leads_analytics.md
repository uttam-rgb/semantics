# analytics.cratio_leads_analytics

**Status:** ✅ Authoritative leads table (resolves the `public.cratio_leads` open question — see [`schema_map.md`](../../schema_map.md)). Part of the [lead-alerting/reporting system](_reporting_system_overview.md) — read that first.

**Purpose:** Every lead synced from the external Cratio CRM, with current funnel stage, revenue, and follow-up fields.

**Grain:** Intended to be one row per lead. **Not enforced** — see gotchas.

**⚠️ No primary key, no unique constraint at all.** 82,053 rows total, but only 77,016 distinct `mobile_number` values — roughly 5,000 rows are either true duplicate leads or the same person re-entering the funnel and getting a new row. **Decide with the data owner whether "number of leads" means `count(*)` or `count(distinct mobile_number)` before building any leads-volume metric.**

## Columns (44 total — grouped by purpose; all are `text` except the 4 real timestamps noted)

**Identity/contact:** `contact_name`, `email_address`, `mobile_number`, `two_wheeler_dl`, `four_wheeler_dl`, `customer_location`, `contact_reference`

**Funnel/ownership:**
- `lead_stage` — the funnel stage. **20+ raw values observed**, no enum. Examples: `CLOSED WON` (4,011), `CLOSED LOST` (53,145 — the single largest bucket), `50% PAYMENT DONE` (976), `SEND COURSE DETAILS` (759), `NEW` (264), plus operational buckets like `RNR`/`RNR_2`/`RNR_3`/`RNR_4` (ring-no-response, presumably by attempt count), `OUT OF BANGALORE`, `Area not servisable` (typo for "serviceable"), `Paused Lead`, `CALL BACK`, `No Car`, `2 W non geared - we cannot teach`. **Building a "conversion rate" or funnel metric requires a canonical grouping of these into won/lost/in-progress buckets — don't invent one; get it from the owner.**
- `lead_owner` — the salesperson/lead owner. Joins to `daily_report_snapshots.lead_owner`, `alerted_leads_log.lead_owner`, `lead_owner_target.lead_owner`.
- `lead_source`, `campaign_name`, `campaign_term`, `campaign_content` — marketing attribution. `lead_source` has heavy near-duplicate drift: `Facebook` vs values like `Website-Popup-google`, `Website-direct`, `website`, `Website-google`, `Website-Direct`, `Website-InstagramFeed`, `Website-Popup-instagramfeed`, `Website`, `Website-instagramfeed`, `Website-Popup-ig`, plus a placeholder value `--Select--` (5,352 rows). **Normalize before grouping by source.**
- `call_did_status` — how quickly the lead was first called (`Call <24Hr`, `Call >72Hr`, etc.). **87% of rows (71,279 / 82,053) are `Untouched`**. **⚠️ Confirmed unreliable (2026-09-12, per Uttam) — do not use this field in any metric logic.** Cross-checked against real telephony data (`public.exotel_calls`): of 10,770 leads this field marks as "dialed," only 579 also match an actual telephony call — almost entirely disjoint, not just incomplete. See `conventions.md` and `metrics/call_activity.md` for the correct (telephony-based) way to determine call activity.

**Revenue (⚠️ all stored as `text`, not `numeric`):** `expected_revenue`, `won_revenue`, `amount_due`, `price_offered`, `amount_paid`, `discount`. Sample values look like plain decimal strings (`'599.00'`, `'6000'`) — cast explicitly (`::numeric`) and check for blanks/non-numeric strings before aggregating; not fully verified across all 82k rows.

**Payment status:** `payment_status` — **`--Select--` placeholder in 69,777 rows (85%) and NULL in 9,852 more (12%)** — only ~2,424 rows (3%) have a real value (`Full Payment Done`: 2,415, `50% Payment Done`: 9). This field is **not usable** as a general payment-status indicator at the lead level; use `public.payment`/`public.enrollment` for actual payment status once a learner has converted.

**Dates (⚠️ all stored as `text`, not `date`, except the 4 listed under "Real timestamps" below):** `lead_date`, `next_followup_on`, `followup_date`, `call_date`, `won_date`, `lost_date`, `lead_assigned_at`, `first_touch_at`. Sample values look like `'YYYY-MM-DD'` — cast explicitly and verify formatting consistency before using in date logic.

**Real timestamps (proper `timestamp` type):** `created_at`, `updated_at`, `lead_created_time`, `lead_updated_time`.

**Other:** `course_applicable`, `instructor_name`, `next_followup_notes`, `additional_notes`, `course_details`, `course_tenure`, `lost_reason`, `lost_description`, `lead_automation_email`, `segmentation`, `customer_intent`

## Relationships

No enforced FKs (matches having no PK). Conceptual joins (by value, not constraint):
- `mobile_number` → `alerted_leads_log.mobile_number`, `lead_snapshots.mobile_number`, `low_util_instructor_leads.mobile_number`
- `lead_owner` → `daily_report_snapshots.lead_owner`, `alerted_leads_log.lead_owner`, `lead_owner_target.lead_owner`, `alert_metric_snapshots.lead_owner`

## Gotchas (summary — see inline notes above for detail)

1. No PK; `mobile_number` not unique — clarify what "one lead" means before counting.
2. Revenue and date fields are `text`, not `numeric`/`date` — cast before computing.
3. `lead_stage` needs a canonical won/lost/in-progress grouping, not ad hoc filtering.
4. `lead_source` needs normalization (case + near-duplicate "Website-*" variants + `--Select--` placeholder).
5. `payment_status` is a placeholder value in 85% of rows — don't use it as a real signal.
6. ~~`call_did_status` shows mostly "Untouched" — verify this field is actually maintained before trusting it.~~ **Resolved 2026-09-12: confirmed unreliable, do not use.**

**Owner:** TBD
**Last verified:** 2026-09-12
