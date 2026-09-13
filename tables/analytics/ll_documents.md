# analytics.ll_documents

**Status:** Live (136 rows). Part of the LL/DL application pipeline alongside [`ll_applications`](ll_applications.md)/[`ll_pipeline_events`](ll_pipeline_events.md).

**Purpose:** Documents uploaded for an LL/DL application (signature, age proof, etc.) and their review status.

**Grain:** One row per uploaded document.

## Columns

| Column | Type | Notes |
|---|---|---|
| id | text | |
| application_id | text | → `ll_applications.id` |
| learner_id | text | → `Learner.id` |
| doc_type | text | e.g. `'signature'`, `'age_proof'` |
| doc_subtype | text | e.g. `'tenth_marksheet'` for an age_proof doc |
| storage_path, file_name, mime_type | text | file storage metadata |
| status | text | e.g. `'pending'` |
| rejection_reason | text | |
| reviewed_by, reviewed_at | text/timestamp | |
| created_at | timestamp with tz | |
| doc_slot | text | e.g. `'primary'` — suggests a document type can have multiple slots (primary/secondary?) |

## Relationships

`application_id` → `ll_applications.id`; `learner_id` → `Learner.id`. Neither enforced.

**Owner:** TBD
**Last verified:** 2026-09-12
