-- Lead Generated Lead Owner and on certain frequency

select 
	lead_owner 
	, date(date_trunc({{frequency}}, lead_date::date)) 
	, count(*) as total_Leads_generated
from 
	analytics.cratio_leads_analytics
where lead_date::date between {{start_date}} and {{end_date}}
[[and {{lead_owner}}]]
group by 1, 2
order by 1, 2

select 
	date(date_trunc({{frequency}}, lead_date::date)) 
	, count(*) as total_Leads_generated
from 
	analytics.cratio_leads_analytics
where lead_date::date between {{start_date}} and {{end_date}}
[[and {{lead_owner}}]]
group by 1
order by 1

-- Revenue Generated Lead Owner and on certain frequency
select 
	lead_owner 
	, date(date_trunc({{frequency}}, call_date::date)) as call_frequency
	, sum(case when lead_stage in ('50% PAYMENT DONE', 'CLOSED WON') then expected_revenue::float else 0 end) as total_revenue_generated
	-- , count(case when lead_stage in ('50% PAYMENT DONE', 'CLOSED WON') then expected_revenue  end) as total_leads_converted
from 
	analytics.cratio_leads_analytics
where call_date::date between {{start_date}} and {{end_date}}
[[and {{lead_owner}}]]
group by 1, 2
order by 1, 2


select 
	date(date_trunc({{frequency}}, call_date::date)) as call_frequency
	, sum(case when lead_stage in ('50% PAYMENT DONE', 'CLOSED WON') then expected_revenue::float else 0 end) as total_revenue_generated
	, sum(case when lead_stage in ('50% PAYMENT DONE', 'CLOSED WON') and lead_date = call_date then expected_revenue::float else 0 end) as same_day_revenue_generated
	, sum(case when lead_stage in ('50% PAYMENT DONE', 'CLOSED WON') and lead_date != call_date then expected_revenue::float else 0 end) as followup_revenue_generated
	-- , count(case when lead_stage in ('50% PAYMENT DONE', 'CLOSED WON') then expected_revenue  end) as total_leads_converted
from 
	analytics.cratio_leads_analytics
where call_date::date between {{start_date}} and {{end_date}}
[[and {{lead_owner}}]]
group by 1
order by 1

select 
	date(date_trunc({{frequency}}, call_date::date)) as call_frequency
	, sum(case when lead_stage in ('50% PAYMENT DONE', 'CLOSED WON') and lead_date = call_date then expected_revenue::float else 0 end) * 1.00/nullif(sum(case when lead_stage in ('50% PAYMENT DONE', 'CLOSED WON') then expected_revenue::float else 0 end), 0) as "same_day_revenue %"
	, sum(case when lead_stage in ('50% PAYMENT DONE', 'CLOSED WON') and lead_date != call_date then expected_revenue::float else 0 end) * 1.00/nullif(sum(case when lead_stage in ('50% PAYMENT DONE', 'CLOSED WON') then expected_revenue::float else 0 end), 0) as "followup_revenue %"
	-- , count(case when lead_stage in ('50% PAYMENT DONE', 'CLOSED WON') then expected_revenue  end) as total_leads_converted
from 
	analytics.cratio_leads_analytics
where call_date::date between {{start_date}} and {{end_date}}
[[and {{lead_owner}}]]
group by 1
order by 1

