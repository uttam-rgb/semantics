# exotel.call_logs

**Status:** ⚠️ NOT IN USE — do not query this table for reporting. Use `public.exotel_calls` instead.

**Purpose (intended):** Call records synchronized from the Exotel telephony API — one row per phone call leg (inbound/outbound), with call metadata, duration, recording, and the raw provider payload.

**Grain:** One row = one Exotel call leg (`sid`), if populated.

**Current state (verified 2026-09-12 via direct DB introspection):** 0 rows. Its companion table `exotel.sync_history` shows exactly one sync run ever — status `SUCCESS`, but `records_fetched = 0` and `records_inserted = 0`. This schema looks like a newer, better-typed rewrite of the Exotel integration (`uuid` PK, `jsonb` raw_response, richer indexing) that was created but never actually wired up to a working sync job. **The live, actively-syncing table is `public.exotel_calls`** — see [`tables/public/exotel_calls.md`](../public/exotel_calls.md).

## Columns

| Column | Type | Nullable | Notes |
|---|---|---|---|
| id | uuid | no | PK, default `gen_random_uuid()` |
| sid | varchar(100) | no | Exotel call SID, unique |
| parent_sid | varchar(100) | yes | parent call leg, for transfers/conferences |
| account_sid | varchar(100) | yes | Exotel account identifier |
| phone_number_sid | varchar(100) | yes | Exotel-side phone number ID |
| from_number | varchar(20) | no | |
| to_number | varchar(20) | no | |
| status | varchar(30) | no | e.g. completed/busy/failed/no-answer (values observed on the live table, see public.exotel_calls doc) |
| direction | varchar(30) | no | inbound / outbound-api / outbound-dial |
| answered_by | varchar(20) | yes | e.g. human/machine |
| duration_seconds | integer | no, default 0 | total call duration |
| conversation_duration_seconds | integer | yes | talk time, if tracked separately from ring/total duration |
| price | numeric | yes | cost of the call |
| recording_url | text | yes | |
| date_created / date_updated / start_time / end_time | timestamp (no tz) | yes | stored as a **proper timestamp** here (contrast with `public.exotel_calls`, where these same fields are strings) |
| raw_response | jsonb | no | full Exotel API payload, queryable as JSON |
| created_at / updated_at | timestamp (no tz) | no, default now() | row bookkeeping |

## Relationships

None. No foreign keys are defined on this table, and nothing else in the database references it. If this table is ever populated, joining to leads/learners/instructors would have to go through phone-number matching (`from_number`/`to_number`), not an ID — there's no direct relational link to CRM entities.

## Gotchas

- **Table is empty.** A query against it returns zero rows silently, not an error — if a report accidentally points here instead of `public.exotel_calls`, the result looks like "no calls happened" rather than an obvious failure.
- No table/column comments exist in Postgres for this schema (unlike `public.exotel_calls`, which has a table comment) — another signal this is scaffolding, not production.

**Owner:** TBD — confirm with whoever owns the Exotel integration whether this schema is a planned migration or dead code to be dropped.
**Last verified:** 2026-09-12
