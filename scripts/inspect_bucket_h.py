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

tables = ["earning_config", "earning_program", "instructor_earning_adjustment",
          "instructor_earning_settings", "instructor_payout"]

for t in tables:
    print(f"\n{'='*15} analytics.{t} {'='*15}")
    cur.execute("""
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns
        WHERE table_schema='analytics' AND table_name=%s
        ORDER BY ordinal_position
    """, (t,))
    for c in cur.fetchall():
        print(" ", c)

    cur.execute("""
        SELECT tc.constraint_type, kcu.column_name, ccu.table_schema, ccu.table_name, ccu.column_name
        FROM information_schema.table_constraints tc
        JOIN information_schema.key_column_usage kcu
          ON tc.constraint_name = kcu.constraint_name AND tc.table_schema = kcu.table_schema
        LEFT JOIN information_schema.constraint_column_usage ccu
          ON tc.constraint_name = ccu.constraint_name AND tc.constraint_type = 'FOREIGN KEY'
        WHERE tc.table_schema='analytics' AND tc.table_name=%s
    """, (t,))
    print(" constraints:", cur.fetchall())

    try:
        cur.execute(f'SELECT obj_description(\'"analytics"."{t}"\'::regclass, \'pg_class\')')
        print(" comment:", cur.fetchone()[0])
    except Exception as e:
        conn.rollback()

    try:
        cur.execute(f'SELECT count(*) FROM analytics."{t}"')
        print(" row count:", cur.fetchone())
    except Exception as e:
        conn.rollback()
        print(" row count ERROR:", e)

    try:
        cur.execute(f'SELECT * FROM analytics."{t}" LIMIT 3')
        cols = [d[0] for d in cur.description]
        print(" sample cols:", cols)
        for row in cur.fetchall():
            print(" sample:", row)
    except Exception as e:
        conn.rollback()
        print(" sample ERROR:", e)

conn.close()
