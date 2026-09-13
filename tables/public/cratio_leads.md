# public.cratio_leads

**Status:** ⚠️ UNRESOLVED — do not treat as the main leads dataset without checking `schema_map.md` first.

**Purpose:** Leads synced from the external Cratio CRM system (this database is itself named `cratio_crm`, so this is Inlane's local mirror of Cratio lead records).

**Grain:** One row per lead, keyed by the external `cratio_lead_id`.

**⚠️ Scale mismatch to flag:** this table has only **32 rows**. There is a much larger `analytics.cratio_leads_analytics` table (81,374 rows, 44 columns) that we haven't documented yet (analytics schema comes later in this project). **Do not assume this small `public.cratio_leads` table is the primary leads dataset for reporting — that's an open question to resolve once the `analytics` schema is documented.** Logged in [`open_questions.md`](../../open_questions.md).

## Columns

| Column | Type | Nullable | Notes |
|---|---|---|---|
| id | uuid | no | PK, default `gen_random_uuid()` |
| cratio_lead_id | varchar(255) | no | **unique** — the external Cratio CRM ID, the real join key back to the source system |
| name, email, phone, city | varchar | yes | |
| source | varchar(100) | yes | ⚠️ messy/inconsistent values observed: `Facebook` (16), `Website-Direct` (6), `--Select--` (3, a placeholder/junk value), `website` (2), `manual_test` (1), `tunnel_test` (1), `facebook` (1), `google` (1), `Website-google` (1). **Needs normalization (case, near-duplicates, test-data exclusion) before any "leads by source" grouping.** |
| status | varchar(50) | yes, default `'new'` | ⚠️ only 2 distinct values seen: `50% PAYMENT DONE` (30), `new` (2) — a completely different vocabulary from `payment.status`/`enrollment.payment_status`. This looks like Cratio's own funnel-stage labels, not Inlane's internal statuses — don't conflate the two systems' status fields. |
| campaign | varchar(255) | yes | |
| notes | text | yes | |
| raw_payload | jsonb | yes | full original payload from Cratio |
| created_at, updated_at | timestamp (no tz) | yes, default CURRENT_TIMESTAMP | |

## Relationships

None — no FK to or from this table.

## Gotchas

- **Resolve which leads table is authoritative** (`public.cratio_leads` vs `analytics.cratio_leads_analytics`) before building any leads/conversion metric — see `open_questions.md`.
- `source` values need normalization (case differences, `--Select--` placeholder, test rows like `manual_test`/`tunnel_test`).
- `status` uses Cratio's own vocabulary (`50% PAYMENT DONE`), unrelated to `payment.status` or `enrollment.payment_status` — don't merge these without a defined mapping.

**Owner:** TBD
**Last verified:** 2026-09-12
