# analytics.learning_content

**Status:** Live reference/catalog table — part of a newly-launched in-app e-learning feature (see `learning_analytics_settings`, tracking since 2026-09-11).

**Purpose:** The video/quiz content library, organized by course and lesson number.

**Grain:** One row per content item (a video, with optional quiz questions attached). 142 rows.

## Columns

| Column | Type | Notes |
|---|---|---|
| course_id | text | → `Courses.id` (confirm schema) |
| lesson_number | bigint | matches `Lesson.number` presumably |
| content_id | text | e.g. `'video:43e5d63e'` |
| course_title | text | denormalized display copy |
| title | text | e.g. `'parallel parking'` |
| kind | text | e.g. `'video'` — only value seen in samples |
| questions | text | JSON-array-shaped string, `'[]'` in samples seen — quiz questions attached to this content, if any |
| active | boolean | |

## Relationships

`course_id`/`lesson_number` conceptually → `Courses`/`Lesson` (schema unconfirmed). No enforced FK.

## Gotchas

- `questions` is a JSON-shaped string, not `jsonb` — needs parsing, not JSON operators.
- Small row count (142) reflects a genuinely new feature, not staleness — cross-check `learning_analytics_settings.tracking_since` before assuming this is dead.

**Owner:** TBD
**Last verified:** 2026-09-12
