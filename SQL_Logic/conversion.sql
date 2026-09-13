-- LD: Total Leads Converted
select 
	lead_owner 
	, date(date_trunc({{frequency}}, call_date::date)) as call_frequency
	-- , sum(case when lead_stage in ('50% PAYMENT DONE', 'CLOSED WON') then expected_revenue::float else 0 end) as total_revenue_generated
	, count(case when lead_stage in ('50% PAYMENT DONE', 'CLOSED WON') then mobile_number  end) as total_leads_converted
from 
	analytics.cratio_leads_analytics
where call_date::date between {{start_date}} and {{end_date}}
[[and {{lead_owner}}]]
group by 1, 2
order by 1, 2


select 
	date(date_trunc({{frequency}}, call_date::date)) as call_frequency
	-- , sum(case when lead_stage in ('50% PAYMENT DONE', 'CLOSED WON') then expected_revenue::float else 0 end) as total_revenue_generated
	, count(case when lead_stage in ('50% PAYMENT DONE', 'CLOSED WON') then mobile_number  end) as total_leads_converted
	, count(case when lead_stage in ('50% PAYMENT DONE', 'CLOSED WON') and call_date = lead_date then mobile_number  end) as same_day_converted
	, count(case when lead_stage in ('50% PAYMENT DONE', 'CLOSED WON') and call_date != lead_date then mobile_number  end) as followup_converted
from 
	analytics.cratio_leads_analytics
where call_date::date between {{start_date}} and {{end_date}}
[[and {{lead_owner}}]]
group by 1
order by 1

select 
	date(date_trunc({{frequency}}, call_date::date)) as call_frequency
	, count(case when lead_stage in ('50% PAYMENT DONE', 'CLOSED WON') and call_date = lead_date then mobile_number end) * 1.00 /nullif(count(case when lead_stage in ('50% PAYMENT DONE', 'CLOSED WON') then mobile_number  end), 0) as "same_day_converted %"
	, count(case when lead_stage in ('50% PAYMENT DONE', 'CLOSED WON') and call_date != lead_date then mobile_number end) * 1.00 /nullif(count(case when lead_stage in ('50% PAYMENT DONE', 'CLOSED WON') then mobile_number  end), 0) as "followup_converted %"
from 
	analytics.cratio_leads_analytics
where call_date::date between {{start_date}} and {{end_date}}
[[and {{lead_owner}}]]
group by 1
order by 1


-- LD: Same Day Converted 
select 
	lead_owner 
	, date(date_trunc({{frequency}}, call_date::date)) as call_frequency
	-- , sum(case when lead_stage in ('50% PAYMENT DONE', 'CLOSED WON') then expected_revenue::float else 0 end) as total_revenue_generated
	, count(case when lead_stage in ('50% PAYMENT DONE', 'CLOSED WON') and lead_date::date = call_date::date then mobile_number  end) as total_leads_converted
from 
	analytics.cratio_leads_analytics
where call_date::date between {{start_date}} and {{end_date}}
[[and {{lead_owner}}]]
group by 1, 2
order by 1, 2



