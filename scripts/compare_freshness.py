import yaml
import psycopg2

with open("config.yaml") as f:
    cfg = yaml.safe_load(f)

db = cfg["crn_database_analytics"]
conn = psycopg2.connect(
    dbname=db["dbname"], host=db["host"], password=db["password"],
    port=db["port"], user=db["user"],
)
cur = conn.cursor()

checks = [
    ("Schedule", "id", "created_at"),
    ("payment", "id", "created_at"),
    ("Learner", "id", "created_at"),
    ("enrollment", "id", "created_at"),
    ("reschedule_requests", "id", "created_at"),
    ("schedule_preferences", "id", "created_at"),
    ("admin_permissions", "id", "created_at"),
    ("Serviceable_Areas", "id", "created_at"),
    ("Instructor", "id_instructor", "created_at"),
    ("Lesson", "id", "created_at"),
    ("Courses", "id", "created_at"),
    ("team_bug_reports", "id", "created_at"),
    ("app_settings", "id", "created_at"),
]

for table, idcol, tscol in checks:
    print(f"\n=== {table} ===")
    for schema in ["public", "analytics"]:
        try:
            cur.execute(f'SELECT count(*), max("{tscol}"), min("{tscol}") FROM {schema}."{table}"')
            cnt, mx, mn = cur.fetchone()
            print(f"  {schema}: count={cnt} min({tscol})={mn} max({tscol})={mx}")
        except Exception as e:
            conn.rollback()
            print(f"  {schema}: ERROR {e}")

    # ID overlap
    try:
        cur.execute(f'''
            SELECT
              (SELECT count(*) FROM public."{table}") AS pub_count,
              (SELECT count(*) FROM analytics."{table}") AS ana_count,
              (SELECT count(*) FROM public."{table}" p WHERE EXISTS (SELECT 1 FROM analytics."{table}" a WHERE a."{idcol}" = p."{idcol}")) AS pub_ids_in_ana,
              (SELECT count(*) FROM analytics."{table}" a WHERE EXISTS (SELECT 1 FROM public."{table}" p WHERE p."{idcol}" = a."{idcol}")) AS ana_ids_in_pub
        ''')
        print("  overlap:", cur.fetchone())
    except Exception as e:
        conn.rollback()
        print("  overlap ERROR:", e)

conn.close()
