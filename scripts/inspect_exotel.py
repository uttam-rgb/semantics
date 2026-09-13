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

for table in ["call_logs", "sync_history"]:
    print(f"\n=== {table} ===")
    cur.execute("""
        SELECT column_name, data_type, is_nullable, column_default,
               character_maximum_length
        FROM information_schema.columns
        WHERE table_schema = 'exotel' AND table_name = %s
        ORDER BY ordinal_position;
    """, (table,))
    cols = cur.fetchall()
    if not cols:
        print("  (no columns visible to this role)")
    for c in cols:
        print(" ", c)

    # row count
    try:
        cur.execute(f'SELECT count(*) FROM exotel."{table}"')
        print("  row count:", cur.fetchone()[0])
    except Exception as e:
        conn.rollback()
        print("  row count error:", e)

    # sample row
    try:
        cur.execute(f'SELECT * FROM exotel."{table}" LIMIT 3')
        colnames = [d[0] for d in cur.description]
        print("  columns from SELECT *:", colnames)
        for row in cur.fetchall():
            print("  sample:", row)
    except Exception as e:
        conn.rollback()
        print("  sample error:", e)

# check role privileges
cur.execute("SELECT current_user;")
print("\ncurrent_user:", cur.fetchone())

cur.execute("""
    SELECT grantee, privilege_type
    FROM information_schema.role_table_grants
    WHERE table_schema='exotel'
""")
print("grants on exotel:", cur.fetchall())

conn.close()
