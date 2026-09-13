--- ARR: Detail by Alert Type — Total Alerted


select
    lead_owner,
	alert_type,
	case 
		when alert_type = 'send_payment_links' then 1
		when alert_type = 'send_course_details' then 2
		when alert_type = 'followups_due_today' then 3
		when alert_type = 'overdue_followups_last_3_days' then 4
		when alert_type = 'untapped_yesterday' then 5
		when alert_type = 'instructor_priority_leads' then 6
		when alert_type = 'no_followup_set' then 7
		when alert_type = 'not_contacted_7_days' then 8
		when alert_type = 'stuck_50pct_payment' then 9
	end as status_order,
    total_alerted
from 
	analytics.alert_resolution_log
where check_date - interval '1 day' = {{resolution_date}}::date 
and {{lead_owner}}
-- group by 1, 2
order by status_order, lead_owner


-- ARR: Detail by Alert Type — Total Called

select
    lead_owner,
	alert_type,
	case 
		when alert_type = 'send_payment_links' then 1
		when alert_type = 'send_course_details' then 2
		when alert_type = 'followups_due_today' then 3
		when alert_type = 'overdue_followups_last_3_days' then 4
		when alert_type = 'untapped_yesterday' then 5
		when alert_type = 'instructor_priority_leads' then 6
		when alert_type = 'no_followup_set' then 7
		when alert_type = 'not_contacted_7_days' then 8
		when alert_type = 'stuck_50pct_payment' then 9
	end as status_order,
    "called" as total_called
from 
	analytics.alert_resolution_log
where check_date - interval '1 day' = {{resolution_date}}::date 
and {{lead_owner}}
-- group by 1, 2
order by status_order, lead_owner


-- ARR: Detail by Alert Type — Touch Rate % (Called / Alerted)

select
    lead_owner,
	alert_type,
	case 
		when alert_type = 'send_payment_links' then 1
		when alert_type = 'send_course_details' then 2
		when alert_type = 'followups_due_today' then 3
		when alert_type = 'overdue_followups_last_3_days' then 4
		when alert_type = 'untapped_yesterday' then 5
		when alert_type = 'instructor_priority_leads' then 6
		when alert_type = 'no_followup_set' then 7
		when alert_type = 'not_contacted_7_days' then 8
		when alert_type = 'stuck_50pct_payment' then 9
	end as status_order,
    "called" as total_called
from 
	analytics.alert_resolution_log
where check_date - interval '1 day' = {{resolution_date}}::date 
[[and {{lead_owner}}]]
-- group by 1, 2
order by status_order, lead_owner

-- ARR: Owner Summary

select
    lead_owner,
    sum(total_alerted)                                                  as total_alerted,
    sum(called)                                                         as called,
    sum(moved)                                                          as moved,
    sum(total_alerted) - sum(moved)                                     as not_moved,
    round(100.0 * sum(moved) / nullif(sum(total_alerted), 0), 1)       as resolution_pct,
    case
        when round(100.0 * sum(moved) / nullif(sum(total_alerted), 0), 1) >= 70 then 'Green'
        when round(100.0 * sum(moved) / nullif(sum(total_alerted), 0), 1) >= 40 then 'Yellow'
        else 'Red'
    end                                                                  as status
from 
	analytics.alert_resolution_log
where check_date - interval '1 day' = {{resolution_date}}::date 
[[and {{lead_owner}}]]
group by 1
order by total_alerted desc
