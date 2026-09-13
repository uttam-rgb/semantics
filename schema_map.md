# Schema Map — which table is authoritative

Some tables exist in more than one schema under the same or similar name. When that happens, this file says which one to actually use for reporting. **Check here before writing any query that touches a table listed below.**

| Domain | Use this | Not this | Why |
|---|---|---|---|
| Exotel call logs | `public.exotel_calls` | `exotel.call_logs` | `exotel.call_logs` is an empty, never-synced rewrite (0 rows). `public.exotel_calls` is the live table, actively syncing (51k+ rows and growing). See [`tables/exotel/call_logs.md`](tables/exotel/call_logs.md). |
| Exotel sync log | `public.exotel_sync_history` | `exotel.sync_history` | Same reason — `exotel.sync_history` has one stale row from 2026-08-03 with 0 records synced. `public.exotel_sync_history` is updated on every real sync run. |

## `public` vs `analytics` — the big one

**Verified 2026-09-12 via row-count, timestamp, and ID-overlap checks (see `scripts/compare_freshness.py`).** For every core business table that exists in both schemas, `public`'s data **stops around mid-March 2026** and every one of its rows also exists in `analytics` — `analytics` is a superset that kept receiving new rows all the way to today (2026-09-12), while `public` appears to have been frozen (a migration/cutover, most likely) around March 2026.

**Rule: use `analytics.<table>`, not `public.<table>`, for all of the tables below — `public` is ~6 months stale.**

| Table | public rows (frozen ~Mar 2026) | analytics rows (current) | ID overlap |
|---|---|---|---|
| `Schedule` | 2,611 | 24,584 | 100% of public ⊆ analytics |
| `payment` | 637 | 5,509 | 100% of public ⊆ analytics |
| `Learner` | 413 | 4,035 | 100% of public ⊆ analytics |
| `enrollment` | 386 | 3,808 | 100% of public ⊆ analytics |
| `reschedule_requests` | 316 | 3,829 | 100% of public ⊆ analytics |
| `schedule_preferences` | 489 | 2,796 | 100% of public ⊆ analytics |
| `Serviceable_Areas` | 136 | 403 | 100% of public ⊆ analytics |
| `team_bug_reports` | 5 | 8 | 100% of public ⊆ analytics |
| `Instructor` | 23 | 122 | ⚠️ only 20/23 — see gotcha below |
| `Lesson` | 49 | 49 | 100% identical — static catalog data, either is fine |
| `Courses` | 11 | 11 | 100% identical — static catalog data, either is fine |
| `app_settings` | 1 | 1 | 100% identical |
| `admin_permissions` | 10 | 411 | ⚠️ **0% overlap — see gotcha below, does not fit the pattern** |
| `Instructor Unavailability` | 0 | 0 | both empty — moot, neither is used (see [`tables/public/instructor_unavailability.md`](tables/public/instructor_unavailability.md)) |
| `Learner Availability` | 0 | 0 | both empty — moot (see [`tables/public/learner_availability.md`](tables/public/learner_availability.md)) |

**Gotchas:**
- **`admin_permissions` doesn't follow the pattern above.** `public.admin_permissions`'s 10 rows all share one identical `created_at` timestamp (2026-03-16) — looks like a one-time bulk seed/reset, not a live-then-frozen table — and **none** of its IDs appear in `analytics.admin_permissions`. These look like two genuinely disjoint tables, not a stale-subset relationship. Confirm with the owner before assuming `analytics.admin_permissions` is simply "the same data, more of it."
- **`Instructor`**: 3 of `public.Instructor`'s 23 rows are **not** present in `analytics.Instructor` — a near-superset, not a perfect one. Worth a spot-check with the owner on those 3 instructors before assuming `analytics` has everyone.
- **Also also note (from bucket-C column comparison):** `analytics.Instructor` and `analytics.Schedule` have several columns `public` doesn't (e.g. `Instructor.status`, `Instructor.contract_signed`, `Schedule.isTentative`, `Schedule.started_at`/`ended_at`, `Schedule.pause_reason`) — consistent with `analytics` being the actively-developed, currently-used schema. One field was possibly renamed/typo'd between the two: `public.Instructor.car_model` vs `analytics.Instructor.car_mode`.

**Working theory (not confirmed with the owner):** `public` was the production app schema before some migration/cutover around March 2026, after which the live app started writing to what's now `analytics`. If true, `public` is effectively a historical fork frozen at cutover, not a "core" vs "reporting" split. This would also explain why the revenue head's Metabase reports were wrong if they queried `public.*` — half a year of activity would simply be invisible.
