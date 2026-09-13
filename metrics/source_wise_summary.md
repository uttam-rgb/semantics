---
metric: source_wise_summary
aliases: [lead count by source, source performance]
status: confirmed
owner: TBD
confirmed_by: "Uttam — source-bucket mapping from Lane_Metric_Definitions_v1.xlsx 'Business Rules' tab"
confirmed_date: 2026-09-12
last_verified: 2026-09-12
source: analytics.cratio_leads_analytics
grain: one row per lead
time_field: "not specified in the spreadsheet — no filter applied in the verified figures below (all-time)"
dimensions: [source_bucket]
---

## Definition

Buckets leads by marketing source using a case-insensitive, first-match-wins keyword rule (from the spreadsheet's "Business Rules" tab). This doc covers **only the lead-count side** — "Leads Dialed" and "Leads Spoken To" for this same `source_bucket` dimension are **not duplicated here**; they're the exact same metric as `call_activity.md`'s "Customers Called"/"Customers Connected," just grouped by `source_bucket` instead of `lead_owner` — see that doc's source-bucket-grouped query.

## Source bucket mapping (first match wins, in this order)

1. `lead_source` contains `'facebook'`, `'meta'`, or `'fb'` → **Meta**
2. `lead_source` contains `'google'`, `'paid search'`, or `'cpc'` → **Google Ads**
3. `lead_source` contains `'instagram'`, `'ig'`, `'whatsapp'`, or `'direct message'` → **Instagram DMs** (name is narrower than its contents — WhatsApp lands here too, per the spreadsheet's own note)
4. Anything else (including blank/NULL) → **Offline Activations** — the explicit default bucket, so unmapped or missing sources inflate this one

Verified 2026-09-12 the `'ig'` keyword doesn't false-positive on unrelated strings — it only matched genuine Instagram-related values (`'Website-Popup-ig'`, `'Website-ig'`, `'ig'`).

## Verified SQL

```sql
select
    case
        when lower(lead_source) like '%facebook%' or lower(lead_source) like '%meta%' or lower(lead_source) like '%fb%' then 'Meta'
        when lower(lead_source) like '%google%' or lower(lead_source) like '%paid search%' or lower(lead_source) like '%cpc%' then 'Google Ads'
        when lower(lead_source) like '%instagram%' or lower(lead_source) like '%ig%' or lower(lead_source) like '%whatsapp%' or lower(lead_source) like '%direct message%' then 'Instagram DMs'
        else 'Offline Activations'
    end as source_bucket,
    count(*) as lead_count
from analytics.cratio_leads_analytics
where lead_date::date between {{start_date}} and {{end_date}}
group by 1
order by lead_count desc
```

All-time distribution, verified 2026-09-12 (no date filter applied):

| source_bucket | lead_count |
|---|---|
| Meta | 53,051 |
| Offline Activations | 13,913 |
| Google Ads | 8,344 |
| Instagram DMs | 6,745 |

## Owner

TBD

**Last verified:** 2026-09-12
