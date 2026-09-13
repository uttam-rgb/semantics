import yaml
import psycopg2
import json

with open("config.yaml") as f:
    cfg = yaml.safe_load(f)

db = cfg["crn_database"]
conn = psycopg2.connect(
    dbname=db["dbname"], host=db["host"], password=db["password"],
    port=db["port"], user=db["user"],
)
cur = conn.cursor()

# all enum types and their labels
cur.execute("""
    SELECT t.typname, array_agg(e.enumlabel ORDER BY e.enumsortorder)
    FROM pg_type t
    JOIN pg_enum e ON t.oid = e.enumtypid
    GROUP BY t.typname
    ORDER BY t.typname;
""")
print("=== ENUM TYPES ===")
for row in cur.fetchall():
    print(row)

queries = {
    "payment.status (actual)": 'SELECT status, count(*) FROM public.payment GROUP BY 1 ORDER BY 2 DESC',
    "payment.payment_type (actual)": 'SELECT payment_type, count(*) FROM public.payment GROUP BY 1 ORDER BY 2 DESC',
    "payment.gateway (actual)": 'SELECT gateway, count(*) FROM public.payment GROUP BY 1 ORDER BY 2 DESC',
    "payment.installment_type (actual)": 'SELECT installment_type, count(*) FROM public.payment GROUP BY 1 ORDER BY 2 DESC',
    "enrollment.status (actual)": 'SELECT status, count(*) FROM public.enrollment GROUP BY 1 ORDER BY 2 DESC',
    "enrollment.payment_status (actual)": 'SELECT payment_status, count(*) FROM public.enrollment GROUP BY 1 ORDER BY 2 DESC',
    "Schedule.status (actual)": 'SELECT status, count(*) FROM public."Schedule" GROUP BY 1 ORDER BY 2 DESC',
    "reschedule_requests.status (actual)": 'SELECT status, count(*) FROM public.reschedule_requests GROUP BY 1 ORDER BY 2 DESC',
    "reschedule_requests.type (actual)": 'SELECT type, count(*) FROM public.reschedule_requests GROUP BY 1 ORDER BY 2 DESC',
    "cratio_leads.status (actual)": 'SELECT status, count(*) FROM public.cratio_leads GROUP BY 1 ORDER BY 2 DESC',
    "cratio_leads.source (actual)": 'SELECT source, count(*) FROM public.cratio_leads GROUP BY 1 ORDER BY 2 DESC',
    "team_bug_reports.status (actual)": 'SELECT status, count(*) FROM public.team_bug_reports GROUP BY 1 ORDER BY 2 DESC',
    "Instructor.car_fuel_type (actual)": 'SELECT car_fuel_type, count(*) FROM public."Instructor" GROUP BY 1 ORDER BY 2 DESC',
}

print("\n=== ACTUAL VALUE DISTRIBUTIONS ===")
for label, q in queries.items():
    try:
        cur.execute(q)
        print(f"\n{label}:")
        for row in cur.fetchall():
            print(" ", row)
    except Exception as e:
        conn.rollback()
        print(f"\n{label}: ERROR {e}")

# sample rows for key tables
print("\n=== SAMPLE ROWS ===")
for schema, table in [("public", "payment"), ("public", "enrollment"), ("public", "Schedule")]:
    cur.execute(f'SELECT * FROM {schema}."{table}" LIMIT 2')
    cols = [d[0] for d in cur.description]
    print(f"\n{schema}.{table} columns: {cols}")
    for row in cur.fetchall():
        print(" ", row)

conn.close()
