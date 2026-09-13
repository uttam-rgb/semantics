# Conventions — read alongside every table/metric doc

## Numbers in these docs are stale snapshots, not live facts

Every row count, value distribution, and percentage in these docs (e.g. "82,053 rows," "only 20 of 23 overlap," "77,016 distinct mobile numbers") was measured once, on the date marked "Last verified," and will have changed by the time you read it — the underlying tables are live and change constantly.

**Never cite a number from these docs as a current fact in an answer.** If a user asks "how many leads do we have," query `analytics.cratio_leads_analytics` directly — don't answer "82,053" because that's what a doc said.

**Do** treat these numbers as evidence for a structural finding that doesn't expire with time:
- "0 rows" → this table is dead/unused (re-verify it's still 0 before fully trusting this, but it's unlikely a dead integration suddenly started working)
- "X distinct out of Y total" → this table has a duplication/grain issue that needs a decision, regardless of the current exact counts
- "public rows are a subset of analytics rows, frozen at date D" → this schema-authority finding is structural (a migration event), not something that un-happens — but the exact row counts on either side will keep changing

When in doubt: the finding ("this table is stale," "this field has no enum," "these two tables overlap imperfectly") is durable. The specific number attached to it is not.

## Naming: business terms and what they map to

- **"Agent" = `lead_owner`.** Every "X - Agent" metric (Revenue - Agent, Calls Made - Agent, Leads Assigned - Agent, etc.) means "group the base metric by `lead_owner`" — it is not a separate table, entity, or concept. If a user asks about "agent performance," "which agent," or "by agent," read that as a `lead_owner` grouping on whichever base metric applies (`revenue.md`, `conversion_rate.md`, `ticket_size.md`, `call_activity.md`, `agent_lead_status.md`, `self_reported_agent_calls.md` — all already support this dimension).
- **L2C** = "Lead to Conversion" (a lead that reached `CLOSED WON`/`50% PAYMENT DONE`/`DP PAID` — see `metrics/conversion_rate.md`).
- **AHT** = Average Handle Time (per-call talk-time average — see `metrics/call_activity.md`'s `avg_talk_time`).
- **D0** = "day zero" — same-day (the lead converted/was contacted the same day it was created), as opposed to a follow-up on a later day.

## Data-quality patterns seen repeatedly across this schema

- **Status/stage fields are usually free text, not enums, and drift over time** (`payment.status`, `cratio_leads_analytics.lead_stage`, `enrollment.payment_status`). Check `open_questions.md` for whether a canonical grouping has been agreed before bucketing by any status-like field.
- **Money and dates are sometimes stored as `text`**, especially in `cratio_leads_analytics` and `users` (analytics, lowercase) — cast explicitly, don't assume a column's name implies its type.
- **`enabled`/`active` boolean flags are used as soft-delete/active markers, inconsistently** — some default `true`, some `false`, some have no default at all. Check the specific table's doc rather than assuming a convention applies schema-wide.
- **Placeholder values masquerade as real data**: `--Select--` (a form default that was never changed) appears across multiple `text` status/source fields and should usually be treated the same as NULL, not as a real category.
- **`timestamp without time zone` columns in this database appear to store IST wall-clock time, not UTC** — verified for `cratio_leads_analytics.lead_created_time` and `exotel_calls.date_created` (2026-09-12, see `metrics/hourly_split.md`): applying `AT TIME ZONE 'Asia/Kolkata'` on top of the raw value double-shifts it and produces a nonsensical hour-of-day pattern; using the raw value directly produces a realistic one. Not verified for every naive-timestamp column in the schema — check per-column before relying on this for precise hour-of-day or elapsed-time logic.
- **`analytics.cratio_leads_analytics.call_did_status` must never be used in any metric logic.** Per Uttam (2026-09-12): it doesn't populate reliably. Confirmed independently — checked it against real telephony data (`public.exotel_calls`) and found the two almost entirely disjoint (of 10,770 leads it marks "dialed," only 579 also match a real telephony call). `exotel_calls` is the only source of truth for "was this lead called" — see `metrics/call_activity.md`.
