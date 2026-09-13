# analytics.learner_course_feedback

**Status:** Simple feedback/ratings table.

**Purpose:** Learner-submitted ratings and comments about their course/instructor, collected at defined checkpoints.

**Grain:** One row per feedback submission.

## Columns

| Column | Type | Nullable | Notes |
|---|---|---|---|
| id | text | yes | |
| enrollment_id | text | yes | conceptual FK → `enrollment.id` (confirm schema) |
| learner_id | text | yes | conceptual FK → `Learner.id` (confirm schema) |
| checkpoint | text | yes | `mid` (636), `final` (132) — only two checkpoints in the learner journey get feedback collected |
| overall_rating, instructor_rating, course_rating | bigint | yes | rating scale not confirmed (1–5? 1–10?) — verify before computing averages |
| comment | text | yes | |
| created_at | timestamp with tz | yes | |

## Relationships

`enrollment_id` and `learner_id` conceptually join to `enrollment`/`Learner` (schema unconfirmed). No enforced FK.

## Gotchas

- Rating scale (e.g. 1–5 vs 1–10) not documented in the schema — confirm before computing/displaying averages.
- Only `mid` and `final` checkpoints exist — a "feedback trend over the course" metric only has two data points per learner, not a continuous timeline.

**Owner:** TBD
**Last verified:** 2026-09-12
