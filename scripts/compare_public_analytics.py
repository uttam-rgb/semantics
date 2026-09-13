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

tables = ["Schedule", "payment", "Learner", "reschedule_requests", "enrollment",
          "schedule_preferences", "admin_permissions", "Serviceable_Areas", "Instructor",
          "Lesson", "Courses", "team_bug_reports", "Instructor Unavailability",
          "Learner Availability", "app_settings"]

def cols(schema, table):
    cur.execute("""
        SELECT column_name, data_type FROM information_schema.columns
        WHERE table_schema=%s AND table_name=%s ORDER BY ordinal_position
    """, (schema, table))
    return cur.fetchall()

for t in tables:
    print(f"\n{'='*20} {t} {'='*20}")
    pub = cols("public", t)
    ana = cols("analytics", t)
    pub_names = {c[0] for c in pub}
    ana_names = {c[0] for c in ana}
    print(f"public cols ({len(pub)}):", [c[0] for c in pub])
    print(f"analytics cols ({len(ana)}):", [c[0] for c in ana])
    only_pub = pub_names - ana_names
    only_ana = ana_names - pub_names
    if only_pub:
        print("  ONLY IN PUBLIC:", only_pub)
    if only_ana:
        print("  ONLY IN ANALYTICS:", only_ana)

conn.close()
