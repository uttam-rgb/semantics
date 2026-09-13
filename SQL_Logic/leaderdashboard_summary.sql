-- LD: Summary Overall

with target_data as (
select 
	lead_owner
	, date(date_trunc({{frequency}}, target_date)) as frequency
	, sum(target) as expected_revenue
from 
	analytics.lead_owner_target
where true
and target_date between {{start_date}} and {{end_date}}
group by 1, 2
)

, lead_data as (
select 
	lead_owner
	, date(date_trunc({{frequency}}, lead_date::date)) as frequency
	, count(mobile_number) as leads_taken
from 
	analytics.cratio_leads_analytics
where true
and lead_date::date between {{start_date}} and {{end_date}}
[[and {{lead_owner}}]]
group by 1, 2
)

, actual_data as (
select 
    coalesce(lead_owner, 'Unknown') as lead_owner
	, date(date_trunc({{frequency}}, call_date::date)) as frequency
    , coalesce(sum(case when lead_stage in ('CLOSED WON', '50% PAYMENT DONE') then nullif(expected_revenue, '')::float end), 0) as total_revenue
	, coalesce(count(mobile_number), 0) as total_customers_called
    , coalesce(count(case when lead_stage in ('CLOSED WON', '50% PAYMENT DONE') then mobile_number end), 0) as lead_conversion
    , coalesce(count(case when call_date::date = lead_date::date
                 and lead_stage in ('CLOSED WON', '50% PAYMENT DONE') then mobile_number end), 0) as d0_lead_conversion
    , coalesce(count(case when call_date::date != lead_date::date
                 and lead_stage in ('CLOSED WON', '50% PAYMENT DONE') then mobile_number end), 0) as followup_lead_conversion
    , coalesce(count(case when lead_stage in ('CLOSED WON', '50% PAYMENT DONE') then mobile_number end), 0) * 1.00
      / nullif(coalesce(count(mobile_number), 0), 0) as "d0_conversion%"
    , coalesce(count(case when call_date::date != lead_date::date
                 and lead_stage in ('CLOSED WON', '50% PAYMENT DONE') then mobile_number end), 0) * 1.00
      / nullif(coalesce(count(mobile_number), 0), 0) as "followup_conversion%"
    , coalesce(count(case when lead_stage in ('CLOSED WON') then mobile_number end), 0) as full_payment_leads
    , coalesce(count(case when lead_stage in ('50% PAYMENT DONE') then mobile_number end), 0) as "50%_payment_leads"
from 
    analytics.cratio_leads_analytics
where true
and call_date::date between {{start_date}} and {{end_date}}
[[and {{lead_owner}}]]
group by 1, 2
order by 2 desc
)

, agg_data as (
select 
	coalesce(l.lead_owner, a.lead_owner) as lead_owner
	, coalesce(l.frequency, a.frequency) as frequency
	, coalesce(leads_taken, 0) as leads_taken
	, coalesce(total_customers_called, 0) as total_customers_called
	, coalesce(total_revenue, 0) as total_revenue
	, coalesce(lead_conversion, 0) as lead_conversion
	, coalesce("d0_lead_conversion", 0) as "d0_lead_conversion"
	, coalesce(followup_lead_conversion, 0) as followup_lead_conversion
	, coalesce("d0_conversion%", 0) as "d0_conversion%"
	, coalesce("followup_conversion%", 0) as "followup_conversion%"
	, coalesce(full_payment_leads, 0) as full_payment_leads
	, coalesce("50%_payment_leads", 0) as "50%_payment_leads"
from 
	actual_data a 
full outer join 
	lead_data l 
	on l.lead_owner = a.lead_owner
	and l.frequency = a.frequency
)

, merged_call_data as (
select 
	o.*
	, a.lead_owner 
from
	(
	select
		date(start_time) as call_date,
		ltrim(from_number, '0') as lead_owner_number,
	    ltrim(to_number, '0') as customer_number,
		status, 
		direction,
		duration_seconds,
		start_time, 
		end_time
	from 
		public.exotel_calls
	where true 
	[[and date(start_time) between {{start_date}} and {{end_date}}]]
	and direction != 'inbound'
	) o
left join 
	(select 
		lead_owner 
		, mobile_number
	from 
		analytics.cratio_leads_analytics
	) a 
	on o.customer_number = a.mobile_number
)

, final_call_data as (
select 
	lead_owner 
	, date(date_trunc({{frequency}}, call_date)) as frequency 
	, count(distinct customer_number) as customers_called
	, count(*) as total_calls_made
	, sum(case when status = 'completed' then 1 else 0 end) as total_connected_calls
	, sum(case when status = 'completed' and duration_seconds >= 120 then 1 else 0 end) as meaningful_calls
	, count(distinct case when status = 'completed' then customer_number end) * 1.00/count(distinct customer_number) as "connected_calls%"
	, sum(duration_seconds/60.0) as total_talk_time_mins
	, sum(duration_seconds/60.0)/nullif(sum(case when status = 'completed' then 1 else 0 end), 0) as avg_talk_time
	-- , sum(case when )
from 
	merged_call_data o 
group by 1, 2
)

, final_data as (
select 
	a.lead_owner
	, a.frequency
	, leads_taken
	, total_customers_called
	, f.total_calls_made
	, total_connected_calls
	, meaningful_calls
	, avg_talk_time
	, coalesce(expected_revenue, 0) as expected_revenue
	, total_revenue
	, lead_conversion
	, "d0_lead_conversion"
	, followup_lead_conversion
	, "d0_conversion%"
	, "followup_conversion%"
	, full_payment_leads
	, "50%_payment_leads"
from 
	agg_data a 
left join 
	target_data t 
	on a.lead_owner = t.lead_owner
	and a.frequency = t.frequency
left join 
	final_call_data f
	on a.lead_owner = f.lead_owner
	and a.frequency = f.frequency
)

select 
	sum(leads_taken) as leads_taken
	, sum(total_customers_called) as total_customers_called
	, sum(total_calls_made) as total_calls_made
	, sum(total_connected_calls) as total_connected_calls
	, sum(meaningful_calls) as meaningful_calls
	, avg(avg_talk_time) as avg_talk_time
	, sum(expected_revenue) as expected_revenue
	, sum(total_revenue) as total_revenue
	, sum(lead_conversion) as lead_conversion
	, sum(d0_lead_conversion) as d0_lead_conversion
	, sum(followup_lead_conversion) as followup_lead_conversion
	, sum(lead_conversion) * 1.00/sum(leads_taken) as "l2c_conversion%"
	, avg("d0_conversion%") as "d0_conversion%"
	, avg("followup_conversion%") as "followup_conversion%"
	, sum(full_payment_leads) as full_payment_leads
	, sum("50%_payment_leads") as "50%_payment_leads"
from 
	final_data

-- LD: Summary Lead Owner wise

with target_data as (
select 
	lead_owner
	, date(date_trunc({{frequency}}, target_date)) as frequency
	, sum(target) as expected_revenue
from 
	analytics.lead_owner_target
where true
and target_date between {{start_date}} and {{end_date}}
group by 1, 2
)

, lead_data as (
select 
	lead_owner
	, date(date_trunc({{frequency}}, lead_date::date)) as frequency
	, count(mobile_number) as leads_taken
from 
	analytics.cratio_leads_analytics
where true
and lead_date::date between {{start_date}} and {{end_date}}
[[and {{lead_owner}}]]
group by 1, 2
)

, actual_data as (
select 
    coalesce(lead_owner, 'Unknown') as lead_owner
	, date(date_trunc({{frequency}}, call_date::date)) as frequency
    , coalesce(sum(case when lead_stage in ('CLOSED WON', '50% PAYMENT DONE') then nullif(expected_revenue, '')::float end), 0) as total_revenue
	, coalesce(count(mobile_number), 0) as total_customers_called
    , coalesce(count(case when lead_stage in ('CLOSED WON', '50% PAYMENT DONE') then mobile_number end), 0) as lead_conversion
    , coalesce(count(case when call_date::date = lead_date::date
                 and lead_stage in ('CLOSED WON', '50% PAYMENT DONE') then mobile_number end), 0) as d0_lead_conversion
    , coalesce(count(case when call_date::date != lead_date::date
                 and lead_stage in ('CLOSED WON', '50% PAYMENT DONE') then mobile_number end), 0) as followup_lead_conversion
    , coalesce(count(case when lead_stage in ('CLOSED WON', '50% PAYMENT DONE') then mobile_number end), 0) * 1.00
      / nullif(coalesce(count(mobile_number), 0), 0) as "d0_conversion%"
    , coalesce(count(case when call_date::date != lead_date::date
                 and lead_stage in ('CLOSED WON', '50% PAYMENT DONE') then mobile_number end), 0) * 1.00
      / nullif(coalesce(count(mobile_number), 0), 0) as "followup_conversion%"
    , coalesce(count(case when lead_stage in ('CLOSED WON') then mobile_number end), 0) as full_payment_leads
    , coalesce(count(case when lead_stage in ('50% PAYMENT DONE') then mobile_number end), 0) as "50%_payment_leads"
from 
    analytics.cratio_leads_analytics
where true
and call_date::date between {{start_date}} and {{end_date}}
[[and {{lead_owner}}]]
group by 1, 2
order by 2 desc
)

, agg_data as (
select 
	coalesce(l.lead_owner, a.lead_owner) as lead_owner
	, coalesce(l.frequency, a.frequency) as frequency
	, coalesce(leads_taken, 0) as leads_taken
	, coalesce(total_customers_called, 0) as total_customers_called
	, coalesce(total_revenue, 0) as total_revenue
	, coalesce(lead_conversion, 0) as lead_conversion
	, coalesce("d0_lead_conversion", 0) as "d0_lead_conversion"
	, coalesce(followup_lead_conversion, 0) as followup_lead_conversion
	, coalesce("d0_conversion%", 0) as "d0_conversion%"
	, coalesce("followup_conversion%", 0) as "followup_conversion%"
	, coalesce(full_payment_leads, 0) as full_payment_leads
	, coalesce("50%_payment_leads", 0) as "50%_payment_leads"
from 
	actual_data a 
full outer join 
	lead_data l 
	on l.lead_owner = a.lead_owner
	and l.frequency = a.frequency
)

, merged_call_data as (
select 
	o.*
	, a.lead_owner 
from
	(
	select
		date(start_time) as call_date,
		ltrim(from_number, '0') as lead_owner_number,
	    ltrim(to_number, '0') as customer_number,
		status, 
		direction,
		duration_seconds,
		start_time, 
		end_time
	from 
		public.exotel_calls
	where true 
	[[and date(start_time) between {{start_date}} and {{end_date}}]]
	and direction != 'inbound'
	) o
left join 
	(select 
		lead_owner 
		, mobile_number
	from 
		analytics.cratio_leads_analytics
	) a 
	on o.customer_number = a.mobile_number
)

, final_call_data as (
select 
	lead_owner 
	, date(date_trunc({{frequency}}, call_date)) as frequency 
	, count(distinct customer_number) as customers_called
	, count(*) as total_calls_made
	, sum(case when status = 'completed' then 1 else 0 end) as total_connected_calls
	, sum(case when status = 'completed' and duration_seconds >= 120 then 1 else 0 end) as meaningful_calls
	, count(distinct case when status = 'completed' then customer_number end) * 1.00/count(distinct customer_number) as "connected_calls%"
	, sum(duration_seconds/60.0) as total_talk_time_mins
	, sum(duration_seconds/60.0)/nullif(sum(case when status = 'completed' then 1 else 0 end), 0) as avg_talk_time
	-- , sum(case when )
from 
	merged_call_data o 
group by 1, 2
)

select 
	a.lead_owner
	, a.frequency
	, leads_taken
	, total_customers_called
	, f.total_calls_made
	, total_connected_calls
	, meaningful_calls
	, avg_talk_time
	, coalesce(expected_revenue, 0) as expected_revenue
	, total_revenue
	, lead_conversion
	, "d0_lead_conversion"
	, followup_lead_conversion
	, coalesce(lead_conversion * 1.00/nullif(leads_taken, 0), 0) as "l2c_conversion%"
	, "d0_conversion%"
	, "followup_conversion%"
	, full_payment_leads
	, "50%_payment_leads"
from 
	agg_data a 
left join 
	target_data t 
	on a.lead_owner = t.lead_owner
	and a.frequency = t.frequency
left join 
	final_call_data f
	on a.lead_owner = f.lead_owner
	and a.frequency = f.frequency

	