WITH params AS (
    SELECT
        DATE_TRUNC('week', CURRENT_DATE + INTERVAL '7 days')::date                       AS week_start,
        (DATE_TRUNC('week', CURRENT_DATE + INTERVAL '7 days') + INTERVAL '6 days')::date AS week_end
),
booked AS (
    SELECT
        s.instructor_id,
        ROUND(
            SUM(EXTRACT(EPOCH FROM (s.end_time - s.start_time)) / 3600.0)::numeric, 1
        ) AS booked_hours
    FROM analytics."Schedule" s
    CROSS JOIN params p
    WHERE s.date    BETWEEN p.week_start AND p.week_end
      AND s.status  = 'booked'
      AND s.enabled = true
    GROUP BY s.instructor_id
),
first_class AS (
    SELECT
        instructor_id,
        MIN(date) AS date_of_class_started
    FROM analytics."Schedule"
    WHERE status = 'booked' AND enabled = true
    GROUP BY instructor_id
)
SELECT
    ROW_NUMBER() OVER (
        ORDER BY
            CASE
                WHEN COALESCE(b.booked_hours, 0) = 0                                     THEN 1
                WHEN COALESCE(b.booked_hours, 0) / NULLIF(ia.working_hours,0) * 100 < 50 THEN 2
                ELSE 3
            END,
            COALESCE(b.booked_hours, 0) / NULLIF(ia.working_hours, 0) ASC NULLS FIRST
    )                                                                                      AS "#",
    ia.instructor_name,
    ia.area,
    COALESCE(ia.attribute, 'Online')                                                       AS attribute,
    p.week_start,
    p.week_end,
    ia.working_hours,
    COALESCE(b.booked_hours, 0)                                                            AS booked_hours,
    ROUND(COALESCE(b.booked_hours,0) / NULLIF(ia.working_hours,0) * 100, 1)               AS utilisation_pct,
    CASE
        WHEN COALESCE(b.booked_hours, 0) = 0                                              THEN 'Zero'
        WHEN COALESCE(b.booked_hours, 0) / NULLIF(ia.working_hours,0) * 100 < 50         THEN 'Low'
        ELSE 'Healthy'
    END                                                                                    AS status,
    GREATEST(ia.working_hours - COALESCE(b.booked_hours,0), 0)                            AS gap_hours,
    ROUND(GREATEST(ia.working_hours - COALESCE(b.booked_hours,0),0) / 4.5, 1)             AS conversions_needed,
    ROUND(GREATEST(ia.working_hours - COALESCE(b.booked_hours,0),0) / 4.5 / 0.08 / 7, 1) AS daily_leads_needed,
    i.created_at::date                                                                     AS date_of_joining,
    fc.date_of_class_started

FROM analytics.instructor_availability ia
CROSS JOIN params p
LEFT JOIN analytics."Instructor" i  ON i.id_instructor = ia.instructor_id
LEFT JOIN booked b                  ON b.instructor_id  = ia.instructor_id
LEFT JOIN first_class fc            ON fc.instructor_id = ia.instructor_id
WHERE ia.status = 'active'
ORDER BY
    CASE
        WHEN COALESCE(b.booked_hours, 0) = 0                                     THEN 1
        WHEN COALESCE(b.booked_hours, 0) / NULLIF(ia.working_hours,0) * 100 < 50 THEN 2
        ELSE 3
    END,
    COALESCE(b.booked_hours, 0) / NULLIF(ia.working_hours, 0) ASC NULLS FIRST
