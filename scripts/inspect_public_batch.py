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

tables = [
    "Schedule", "payment", "schedule_preferences", "Learner", "enrollment",
    "reschedule_requests", "Serviceable_Areas", "Lesson", "cratio_leads",
    "Instructor", "Courses", "admin_permissions", "team_bug_reports",
    "Admin", "email_errors", "app_settings", "failed_emails",
    "Instructor Unavailability", "Learner Availability",
]

result = {}
for table in tables:
    entry = {}
    cur.execute("""
        SELECT column_name, data_type, is_nullable, column_default, character_maximum_length
        FROM information_schema.columns
        WHERE table_schema='public' AND table_name=%s
        ORDER BY ordinal_position;
    """, (table,))
    entry["columns"] = cur.fetchall()

    cur.execute("""
        SELECT tc.constraint_type, kcu.column_name, ccu.table_schema, ccu.table_name, ccu.column_name
        FROM information_schema.table_constraints tc
        JOIN information_schema.key_column_usage kcu
          ON tc.constraint_name = kcu.constraint_name AND tc.table_schema = kcu.table_schema
        LEFT JOIN information_schema.constraint_column_usage ccu
          ON tc.constraint_name = ccu.constraint_name AND tc.constraint_type = 'FOREIGN KEY'
        WHERE tc.table_schema='public' AND tc.table_name=%s
    """, (table,))
    entry["constraints"] = cur.fetchall()

    cur.execute("""
        SELECT tc.table_name, kcu.column_name, ccu.table_name AS ref_table, ccu.column_name AS ref_col
        FROM information_schema.table_constraints tc
        JOIN information_schema.key_column_usage kcu ON tc.constraint_name = kcu.constraint_name
        JOIN information_schema.constraint_column_usage ccu ON tc.constraint_name = ccu.constraint_name
        WHERE tc.constraint_type='FOREIGN KEY' AND ccu.table_name=%s AND ccu.table_schema='public'
    """, (table,))
    entry["referenced_by"] = cur.fetchall()

    try:
        cur.execute(f'SELECT obj_description(\'"public"."{table}"\'::regclass, \'pg_class\')')
        entry["table_comment"] = cur.fetchone()[0]
    except Exception as e:
        conn.rollback()
        entry["table_comment"] = f"ERROR: {e}"

    try:
        cur.execute(f'SELECT count(*) FROM public."{table}"')
        entry["row_count"] = cur.fetchone()[0]
    except Exception as e:
        conn.rollback()
        entry["row_count"] = f"ERROR: {e}"

    result[table] = entry

with open("scripts/public_batch_dump.json", "w") as f:
    json.dump(result, f, indent=2, default=str)

print("done, wrote scripts/public_batch_dump.json")
conn.close()
