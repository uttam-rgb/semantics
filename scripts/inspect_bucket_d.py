import yaml
import psycopg2
import json

with open("config.yaml") as f:
    cfg = yaml.safe_load(f)

db = cfg["crn_database_analytics"]
conn = psycopg2.connect(
    dbname=db["dbname"], host=db["host"], password=db["password"],
    port=db["port"], user=db["user"],
)
cur = conn.cursor()

tables = ['cratio_leads_analytics','lead_snapshots','alerted_leads_log','alert_resolution_log',
          'alert_metric_snapshots','daily_report_snapshots','lead_owner_target','ll_pipeline_events',
          'll_applications','lesson_tracking','learner_course_feedback','instructor_utilisation',
          'instructor_utilisation_trailing','low_util_instructor_leads']

print("=== CONSTRAINTS ===")
for t in tables:
    cur.execute("""
        SELECT tc.constraint_type, kcu.column_name, ccu.table_schema, ccu.table_name, ccu.column_name
        FROM information_schema.table_constraints tc
        JOIN information_schema.key_column_usage kcu
          ON tc.constraint_name = kcu.constraint_name AND tc.table_schema = kcu.table_schema
        LEFT JOIN information_schema.constraint_column_usage ccu
          ON tc.constraint_name = ccu.constraint_name AND tc.constraint_type = 'FOREIGN KEY'
        WHERE tc.table_schema='analytics' AND tc.table_name=%s
    """, (t,))
    rows = cur.fetchall()
    print(f"{t}: {rows if rows else '(no PK/UNIQUE/FK constraints)'}")

print("\n=== INDEXES ===")
for t in tables:
    cur.execute("SELECT indexname, indexdef FROM pg_indexes WHERE schemaname='analytics' AND tablename=%s", (t,))
    for row in cur.fetchall():
        print(f"{t}: {row[0]} -> {row[1]}")

print("\n=== cratio_leads_analytics sample rows ===")
cur.execute('''SELECT lead_owner, expected_revenue, won_revenue, lead_date, lead_stage, payment_status,
                      amount_due, price_offered, amount_paid, discount, lead_source, next_followup_on,
                      call_date, won_date, lost_date, mobile_number
               FROM analytics.cratio_leads_analytics LIMIT 5''')
cols = [d[0] for d in cur.description]
print("cols:", cols)
for row in cur.fetchall():
    print(row)

print("\n=== cratio_leads_analytics distinct-value checks ===")
for col in ["lead_stage", "payment_status", "lead_source", "call_did_status"]:
    cur.execute(f'SELECT "{col}", count(*) FROM analytics.cratio_leads_analytics GROUP BY 1 ORDER BY 2 DESC LIMIT 20')
    print(f"\n{col}:")
    for row in cur.fetchall():
        print(" ", row)

cur.execute("SELECT count(*), count(distinct mobile_number) FROM analytics.cratio_leads_analytics")
print("\ncratio_leads_analytics total rows vs distinct mobile_number:", cur.fetchone())

print("\n=== ll_applications distinct ===")
for col in ["status", "ll_type", "services"]:
    cur.execute(f'SELECT "{col}", count(*) FROM analytics.ll_applications GROUP BY 1 ORDER BY 2 DESC LIMIT 15')
    print(f"\n{col}:")
    for row in cur.fetchall():
        print(" ", row)

print("\n=== ll_pipeline_events distinct ===")
for col in ["event_type", "from_status", "to_status"]:
    cur.execute(f'SELECT "{col}", count(*) FROM analytics.ll_pipeline_events GROUP BY 1 ORDER BY 2 DESC LIMIT 15')
    print(f"\n{col}:")
    for row in cur.fetchall():
        print(" ", row)

print("\n=== lesson_tracking.type distinct ===")
cur.execute('SELECT "type", count(*) FROM analytics.lesson_tracking GROUP BY 1 ORDER BY 2 DESC')
for row in cur.fetchall():
    print(" ", row)

print("\n=== alerted_leads_log.alert_type distinct ===")
cur.execute('SELECT alert_type, count(*) FROM analytics.alerted_leads_log GROUP BY 1 ORDER BY 2 DESC')
for row in cur.fetchall():
    print(" ", row)

print("\n=== alert_resolution_log.alert_type distinct ===")
cur.execute('SELECT alert_type, count(*) FROM analytics.alert_resolution_log GROUP BY 1 ORDER BY 2 DESC')
for row in cur.fetchall():
    print(" ", row)

print("\n=== learner_course_feedback.checkpoint distinct ===")
cur.execute('SELECT checkpoint, count(*) FROM analytics.learner_course_feedback GROUP BY 1 ORDER BY 2 DESC')
for row in cur.fetchall():
    print(" ", row)

print("\n=== lead_snapshots.funnel_stage distinct ===")
cur.execute('SELECT funnel_stage, count(*) FROM analytics.lead_snapshots GROUP BY 1 ORDER BY 2 DESC')
for row in cur.fetchall():
    print(" ", row)

# date ranges
print("\n=== date ranges ===")
cur.execute("SELECT min(snapshot_date), max(snapshot_date) FROM analytics.daily_report_snapshots")
print("daily_report_snapshots.snapshot_date:", cur.fetchone())
cur.execute("SELECT min(alert_date), max(alert_date) FROM analytics.alerted_leads_log")
print("alerted_leads_log.alert_date:", cur.fetchone())
cur.execute("SELECT min(week_start), max(week_end) FROM analytics.instructor_utilisation")
print("instructor_utilisation week range:", cur.fetchone())
cur.execute("SELECT min(computed_at), max(computed_at) FROM analytics.instructor_utilisation_trailing")
print("instructor_utilisation_trailing computed_at range:", cur.fetchone())

# sample row for daily_report_snapshots and instructor_utilisation
cur.execute("SELECT * FROM analytics.daily_report_snapshots ORDER BY snapshot_date DESC LIMIT 2")
cols = [d[0] for d in cur.description]
print("\ndaily_report_snapshots cols:", cols)
for row in cur.fetchall():
    print(row)

cur.execute("SELECT * FROM analytics.instructor_utilisation ORDER BY week_start DESC LIMIT 2")
cols = [d[0] for d in cur.description]
print("\ninstructor_utilisation cols:", cols)
for row in cur.fetchall():
    print(row)

conn.close()
