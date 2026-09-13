WITH base AS (
    SELECT
        lead_owner,
        mobile_number,
        lead_stage,
        NULLIF(lead_date, '')::date        AS lead_date,
        NULLIF(next_followup_on, '')::date AS next_followup_on
    FROM analytics.cratio_leads_analytics
),
active_stages(stage) AS (
    VALUES ('Agreed to pay'), ('SEND COURSE DETAILS'), ('RNR_3'), ('RNR_2'), ('RNR'), ('CALL BACK')
),
untapped_yesterday AS (
    SELECT lead_owner, COUNT(DISTINCT mobile_number) AS untapped_leads_yesterday
    FROM base
    WHERE lead_stage = 'NEW' AND lead_date = CURRENT_DATE - INTERVAL '1 day'
    GROUP BY lead_owner
),
not_contacted_7d AS (
    SELECT lead_owner, COUNT(DISTINCT mobile_number) AS leads_not_contacted_7_days
    FROM base
    WHERE lead_stage = 'NEW'
      AND lead_date BETWEEN CURRENT_DATE - INTERVAL '7 days' AND CURRENT_DATE - INTERVAL '2 days'
    GROUP BY lead_owner
),
no_followup AS (
    SELECT lead_owner, COUNT(DISTINCT mobile_number) AS leads_no_followup_set
    FROM base
    WHERE lead_stage IN (SELECT stage FROM active_stages)
      AND next_followup_on IS NULL
      AND lead_date >= CURRENT_DATE - INTERVAL '7 days'
    GROUP BY lead_owner
),
followups_today AS (
    SELECT lead_owner, COUNT(DISTINCT mobile_number) AS followups_due_today
    FROM base
    WHERE next_followup_on = CURRENT_DATE
      AND lead_stage IN (SELECT stage FROM active_stages)
    GROUP BY lead_owner
),
overdue_followups AS (
    SELECT lead_owner, COUNT(DISTINCT mobile_number) AS overdue_followups_last_3_days
    FROM base
    WHERE next_followup_on >= CURRENT_DATE - INTERVAL '7 days'
      AND lead_stage IN (SELECT stage FROM active_stages)
    GROUP BY lead_owner
),
stuck_50_payment AS (
    SELECT lead_owner, COUNT(DISTINCT mobile_number) AS revenue_stuck_50pct_payment
    FROM base
    WHERE lead_stage = '50% PAYMENT DONE'
      AND lead_date <= CURRENT_DATE - INTERVAL '3 days'
    GROUP BY lead_owner
),
send_payment_links AS (
    SELECT lead_owner, COUNT(DISTINCT mobile_number) AS send_payment_links
    FROM base
    WHERE lead_stage = 'Agreed to pay'
      AND lead_date >= CURRENT_DATE - INTERVAL '90 days'
      AND (next_followup_on IS NULL OR next_followup_on <= CURRENT_DATE)
    GROUP BY lead_owner
),
send_course_details AS (
    SELECT lead_owner, COUNT(DISTINCT mobile_number) AS send_course_details
    FROM base
    WHERE lead_stage = 'SEND COURSE DETAILS'
      AND lead_date >= CURRENT_DATE - INTERVAL '90 days'
      AND (next_followup_on IS NULL OR next_followup_on <= CURRENT_DATE)
    GROUP BY lead_owner
),
hot_lead_priority AS (
    SELECT lead_owner, COUNT(DISTINCT mobile_number) AS hot_lead_priority
    FROM base
    WHERE lead_stage = 'Hot Lead- Close to conversion'
      AND lead_date >= CURRENT_DATE - INTERVAL '90 days'
      AND (next_followup_on IS NULL OR next_followup_on <= CURRENT_DATE)
    GROUP BY lead_owner
),
owners AS (
    SELECT lead_owner FROM untapped_yesterday
    UNION SELECT lead_owner FROM not_contacted_7d
    UNION SELECT lead_owner FROM no_followup
    UNION SELECT lead_owner FROM followups_today
    UNION SELECT lead_owner FROM overdue_followups
    UNION SELECT lead_owner FROM stuck_50_payment
    UNION SELECT lead_owner FROM send_payment_links
    UNION SELECT lead_owner FROM send_course_details
    UNION SELECT lead_owner FROM hot_lead_priority
)
SELECT
    o.lead_owner,
    COALESCE(spl.send_payment_links, 0)          AS send_payment_links,
    COALESCE(scd.send_course_details, 0)         AS send_course_details,
    COALESCE(hlp.hot_lead_priority, 0)           AS hot_lead_priority,
    COALESCE(ft.followups_due_today, 0)          AS followups_due_today,
    COALESCE(ovf.overdue_followups_last_3_days, 0) AS overdue_followups_last_3_days,
    COALESCE(uy.untapped_leads_yesterday, 0)     AS untapped_leads_yesterday,
    COALESCE(nf.leads_no_followup_set, 0)        AS leads_no_followup_set,
    COALESCE(nc7.leads_not_contacted_7_days, 0)  AS leads_not_contacted_7_days,
    COALESCE(s50.revenue_stuck_50pct_payment, 0) AS revenue_stuck_50pct_payment
FROM owners o
LEFT JOIN untapped_yesterday  uy  ON uy.lead_owner  = o.lead_owner
LEFT JOIN not_contacted_7d    nc7 ON nc7.lead_owner = o.lead_owner
LEFT JOIN no_followup         nf  ON nf.lead_owner  = o.lead_owner
LEFT JOIN followups_today     ft  ON ft.lead_owner  = o.lead_owner
LEFT JOIN overdue_followups   ovf ON ovf.lead_owner = o.lead_owner
LEFT JOIN stuck_50_payment    s50 ON s50.lead_owner = o.lead_owner
LEFT JOIN send_payment_links  spl ON spl.lead_owner = o.lead_owner
LEFT JOIN send_course_details scd ON scd.lead_owner = o.lead_owner
LEFT JOIN hot_lead_priority   hlp ON hlp.lead_owner = o.lead_owner
ORDER BY lead_owner;
