# analytics.dl_test_slots

**Status:** Live, brand new/tiny (1 row, created the day before this doc's verification date).

**Purpose:** Available Driving License test slots at a given RTO (government transport office), for scheduling learners' DL tests.

**Grain:** One row per test-date/RTO slot.

## Columns

| Column | Type | Notes |
|---|---|---|
| id | text | |
| test_date | date | |
| rto | text | e.g. `'KR Puram RTO - KA53'` |
| is_active | boolean | |
| uploaded_by | text | free-text name, not a user/admin FK |
| created_at, updated_at | timestamp with tz | |

## Relationships

None enforced. Conceptually relevant to `Learner.DL_test_date`/`ll_applications.dl_test_date` but no FK links them.

**Owner:** TBD
**Last verified:** 2026-09-12
