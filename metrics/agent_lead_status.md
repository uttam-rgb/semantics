---
metric: agent_lead_status
aliases: [leads assigned, leads dialled unique, leads connected unique, meaningful conversation unique, agent wise lead status, agent = lead_owner]
status: confirmed
owner: TBD
confirmed_by: "Uttam — Leads Assigned confirmed as genuinely distinct from Leads Generated (2026-09-12); Dialled/Connected confirmed as the same metric as call_activity.md; Meaningful Conversation threshold set to 90s (spreadsheet) over call_activity.md's 120s, as its own separate per-lead metric"
confirmed_date: 2026-09-12
last_verified: 2026-09-12
source: "analytics.cratio_leads_analytics, joined to public.exotel_calls for the call-based metrics"
grain: one row per lead
time_field: "lead_assigned_at for Leads Assigned; call-based metrics are not date-windowed in the verified figures below"
dimensions: [lead_owner]
---

## Leads Assigned — Agent

**Not the same as `lead_volume.md`'s "Leads Generated."** Checked `lead_assigned_at` against `lead_date`: they differ on **64,838 of 79,936 rows (81%)** — assignment to an agent typically happens on a *different* (usually later) day than lead creation, sometimes weeks later. This is a genuinely separate event with its own date field.

```sql
select lead_owner, date(date_trunc({{frequency}}, lead_assigned_at::date)) as frequency,
       count(*) as leads_assigned
from analytics.cratio_leads_analytics
where lead_assigned_at::date between {{start_date}} and {{end_date}}
[[and {{lead_owner}}]]
group by 1, 2
order by 1, 2
```

Verified 2026-09-12, last 30 days (by `lead_assigned_at`): 15,974 leads assigned, all owners combined.

## Leads Dialled(Unique) / Leads Connected(Unique) — Agent

**Same metric as `call_activity.md`'s "Customers Called"/"Customers Connected"** — no new logic. `call_activity.md` already computes both per `lead_owner`; "Connected(Unique)" just wasn't exposed as its own named column there (it was embedded inside the `connected_calls_pct` calculation). Use `call_activity.md`'s verified SQL, grouped by `lead_owner`, reading `count(distinct customer_number)` and `count(distinct case when status='completed' then customer_number end)` directly instead of only their ratio.

## Meaningful Conversation(Unique) — Agent

**A genuinely separate metric from `call_activity.md`'s "meaningful calls"** — different threshold (**90 seconds**, not 120) and different grain (**unique leads**, not call count). Per Uttam (2026-09-12): use the spreadsheet's 90-second threshold for this metric specifically; it does not override or get reconciled with `call_activity.md`'s 120-second, per-call definition — both stay as documented, in their respective docs, for their respective reports.

```sql
with called as (
    select distinct right(to_number, 10) as customer_number
    from public.exotel_calls where direction != 'inbound'
),
meaningful_90s as (
    select distinct right(to_number, 10) as customer_number
    from public.exotel_calls
    where direction != 'inbound' and status = 'completed' and duration_seconds >= 90
)
select
    count(distinct case when ca.customer_number is not null then c.mobile_number end) as leads_dialled_unique,
    count(distinct case when m.customer_number is not null then c.mobile_number end) as meaningful_conversation_unique
from analytics.cratio_leads_analytics c
left join called ca on ca.customer_number = c.mobile_number
left join meaningful_90s m on m.customer_number = c.mobile_number
[[where c.lead_owner = {{lead_owner}}]]
```

Verified 2026-09-12, all-time: 14,041 leads dialled (unique), 4,694 leads with a meaningful conversation (unique, ≥90s) — company-wide. Add `group by lead_owner` (with a `lead_owner` column in the SELECT) for the per-agent breakdown.

## Gotchas

- Don't apply `call_activity.md`'s 120-second "meaningful calls" threshold here, or vice versa — they're intentionally different metrics for different reports, not a bug to reconcile.
- Same phone-matching caveats as `call_activity.md`/`source_wise_summary.md` apply (last-10-digits match, not a real foreign key, small unmatched fraction).
- `call_did_status` is not used anywhere here, per the standing rule in `conventions.md`.

## Owner

TBD

**Last verified:** 2026-09-12
