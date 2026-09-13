# public.exotel_calls

**Status:** ✅ Authoritative — this is the live, actively-syncing call-log table. (Do not use `exotel.call_logs` — see [`schema_map.md`](../../schema_map.md).)

**Purpose:** Call records synchronized from the Exotel telephony API. One row per call leg — inbound/outbound, with status, duration, recording, and the raw provider payload.

**Grain:** One row = one Exotel call (`sid`).

**Table comment (from Postgres):** "Stores call records synchronized from Exotel API"

**Freshness (verified 2026-09-12):** 51,228 rows and actively growing (was 48,059 rows earlier the same day). Indexed on `created_at`, and syncs are logged in `public.exotel_sync_history`, whose `last_synced_at` matches today.

## Columns

| Column | Type | Nullable | Notes |
|---|---|---|---|
| id | integer (serial) | no | PK |
| sid | varchar(255) | no | Exotel call SID, **unique** |
| parent_sid | varchar(255) | yes | parent call leg (transfers/conferences); empty string `''` when not applicable, not NULL |
| account_sid | varchar(255) | no | single value in practice: `'inlane1m'` (not a useful filter/partition — only one Exotel account) |
| phone_number_sid | varchar(255) | yes | Exotel-side number ID; in sample data this equals the raw phone number, not a separate ID |
| from_number | varchar(50) | yes | |
| to_number | varchar(50) | yes | |
| status | varchar(50) | yes | observed values: `completed`, `busy`, `failed`, `no-answer` |
| direction | varchar(20) | yes | observed values: `inbound`, `outbound-api`, `outbound-dial` |
| duration_seconds | integer | yes | total call duration including ring time |
| conversation_duration_seconds | integer | yes | mostly NULL in samples — not reliably populated, confirm before using for talk-time metrics |
| price | double precision | yes | cost of the call; `0.0` for many rows (inbound calls appear to be free/untracked) |
| answered_by | varchar(255) | yes | e.g. `human` |
| recording_url | text | yes | **empty string `''` for ~62% of rows (31,770 / 51,228), never NULL** — filter with `recording_url <> ''`, not `IS NOT NULL`, to find calls with a recording |
| date_created, date_updated, start_time, end_time | **varchar(50)** | yes | ⚠️ stored as plain strings (format `'YYYY-MM-DD HH:MI:SS'`), not real timestamps — do not use directly in date arithmetic; cast explicitly (`::timestamp`) or prefer `created_at`/`updated_at` for time-based filtering |
| raw_response | text | yes | full Exotel payload as a **JSON string** (not `jsonb`) — must `::jsonb` cast before using JSON operators |
| created_at, updated_at | timestamp (no tz) | yes, default CURRENT_TIMESTAMP | row-insert bookkeeping; range observed 2026-08-04 to 2026-09-12 (today) — this is when Inlane started syncing Exotel data, not when calls actually happened (use `start_time`/`date_created` for the latter, with the string-cast caveat above) |

## Relationships

None — no foreign keys defined, and no other table references this one via FK. To connect a call to a lead/learner/instructor, you must match `from_number`/`to_number` against phone columns on those tables — watch for formatting differences (with/without country code, leading zeros; sample data shows numbers like `08040266035` without a `+91`/`91` prefix).

## Gotchas

- **Timestamps as strings** (see above) — the single biggest risk for query correctness on this table.
- **`recording_url` and `parent_sid` use `''` instead of NULL** for "no value" — `IS NOT NULL` checks will silently include these empty-string rows.
- **`account_sid` is constant** — not a useful grouping/filter column today (only one Exotel account is configured).
- **`conversation_duration_seconds` is sparsely populated** — check for NULLs before averaging; `duration_seconds` is the more reliable field for "how long was this call."
- No direct relational join to CRM entities (leads/learners/instructors) — any "calls per lead" style metric requires phone-number matching, which needs normalization first.

**Owner:** TBD
**Last verified:** 2026-09-12
