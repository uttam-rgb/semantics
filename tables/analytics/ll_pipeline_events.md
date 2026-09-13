# analytics.ll_pipeline_events

**Status:** Event log companion to [`ll_applications`](ll_applications.md).

**Purpose:** Every status transition (and a few other event types) in an LL/DL application's lifecycle — the audit trail behind `ll_applications`'s current-state snapshot.

**Grain:** One row per pipeline event. **No enforced PK** despite having an `id` column.

## Columns

| Column | Type | Nullable | Notes |
|---|---|---|---|
| id | text | yes | intended PK, not enforced |
| application_id | text | yes | conceptual FK → `ll_applications.id` |
| learner_id | text | yes | |
| event_type | text | yes | `status_change` (16,449 — the vast majority), `field_update` (864), `status_reversal` (72), `note` (32), `escalation` (5) |
| from_status, to_status | text | yes | only populated for `status_change`/`status_reversal` events; same vocabulary as `ll_applications.status` |
| actor_name | text | yes | who made the change |
| note | text | yes | |
| changes | text | yes | likely a JSON-shaped diff of a `field_update` event — not verified |
| created_at | timestamp with tz | yes | |

## Relationships

`application_id` → `ll_applications.id` (conceptual, not enforced). `learner_id` → `Learner` (schema unconfirmed).

## Gotchas

- No enforced PK or FK — treat `application_id` matches as best-effort, not guaranteed-consistent joins.
- To reconstruct "how long did application X spend in status Y," use consecutive `status_change` rows ordered by `created_at` per `application_id` — there's no duration field precomputed here.

**Owner:** TBD
**Last verified:** 2026-09-12
