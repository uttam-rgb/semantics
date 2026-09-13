# analytics.lead_owner_target

**Status:** Part of the [lead-alerting/reporting system](_reporting_system_overview.md).

**Purpose:** Target/quota per lead owner per date — for comparing against actuals in `daily_report_snapshots`.

**Grain:** One row per (lead_owner, target_date), presumably — **not enforced** (no PK/unique constraint declared).

## Columns

| Column | Type | Nullable | Notes |
|---|---|---|---|
| lead_owner | text | yes | |
| target_date | date | yes | |
| target | bigint | yes | **✅ confirmed: this is a revenue target** — see [`metrics/target_attainment.md`](../../metrics/target_attainment.md), confirmed from production SQL that compares `sum(target)` directly against the `revenue` metric |

## Relationships

`lead_owner` joins conceptually to `daily_report_snapshots.lead_owner`. No enforced FK, no enforced PK.

## Gotchas

- No PK/unique constraint — verify there's actually one row per (lead_owner, target_date) before joining 1:1 against `daily_report_snapshots`; a duplicate row would silently inflate a join.
- ~~`target` unit is unconfirmed~~ — resolved, see column note above.

**Owner:** TBD
**Last verified:** 2026-09-12
