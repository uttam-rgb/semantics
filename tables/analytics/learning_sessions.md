# analytics.learning_sessions

**Status:** Live — engagement tracking for the e-learning feature, launched very recently (`learning_analytics_settings.tracking_since = 2026-09-11`, i.e. the day before this doc was verified). Only 12 rows exist because the feature is one day old at last check, **not** because it's abandoned.

**Purpose:** Per-learner engagement with a piece of `learning_content` — video playback telemetry and quiz performance.

**Grain:** One row per (learner, content item, viewing sequence) — `sequence` suggests a learner can have multiple session rows for the same content (e.g., re-watching).

## Columns

| Column | Type | Notes |
|---|---|---|
| id | text | |
| learner_id | text | → `Learner.id` (confirm schema) |
| course_id, lesson_number, content_id | text/bigint | → `learning_content` |
| sequence | bigint | which viewing attempt this is |
| started_at, updated_at | timestamp with tz | |
| snapshot | text | JSON-shaped telemetry string, e.g. `{"plays":1,"seeks":0,"errors":0,"pauses":0,"ranges":[[0,2.3]],"duration":32.5,"finished":false,"active_ms":2379,"responses":[]}` — needs parsing, not `jsonb` operators |
| coverage | double precision | fraction of the content actually viewed (e.g. `0.07` = 7%) |
| completed | boolean | |
| correct, wrong, timeouts | bigint | quiz performance, if any questions were attached |
| first_correct, first_total | bigint | performance on first attempt specifically |

## Relationships

`learner_id`, `course_id`/`lesson_number`/`content_id` conceptually join to `Learner`/`learning_content`. No enforced FK.

## Gotchas

- Very new feature — don't read a low row count as staleness; check `learning_analytics_settings.tracking_since` for context first.
- `snapshot` is JSON-as-text, not `jsonb`.
- `coverage` in the two samples checked was very low (7%, 0.8%) despite `completed = false` — early-stage data, not yet enough volume to draw engagement conclusions from.

**Owner:** TBD
**Last verified:** 2026-09-12
