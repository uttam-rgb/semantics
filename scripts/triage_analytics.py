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

cur.execute("""
    SELECT c.relname
    FROM pg_class c
    JOIN pg_namespace n ON n.oid = c.relnamespace
    WHERE c.relkind = 'r' AND n.nspname = 'analytics'
    ORDER BY c.relname;
""")
tables = [r[0] for r in cur.fetchall()]
print(f"Total analytics tables: {len(tables)}")

result = {}
for t in tables:
    entry = {}
    try:
        cur.execute(f'SELECT count(*) FROM analytics."{t}"')
        entry["row_count"] = cur.fetchone()[0]
    except Exception as e:
        conn.rollback()
        entry["row_count"] = f"ERR: {e}"

    try:
        cur.execute("SELECT obj_description(%s::regclass, 'pg_class')", (f'"analytics"."{t}"',))
        entry["comment"] = cur.fetchone()[0]
    except Exception as e:
        conn.rollback()
        entry["comment"] = None

    cur.execute("""
        SELECT count(*) FROM information_schema.columns
        WHERE table_schema='analytics' AND table_name=%s
    """, (t,))
    entry["col_count"] = cur.fetchone()[0]

    # last write time via pg_stat_user_tables if available
    cur.execute("""
        SELECT n_tup_ins, n_tup_upd, n_tup_del, last_autoanalyze, last_analyze
        FROM pg_stat_user_tables
        WHERE schemaname='analytics' AND relname=%s
    """, (t,))
    row = cur.fetchone()
    entry["stats"] = row

    result[t] = entry

with open("scripts/analytics_triage.json", "w") as f:
    json.dump(result, f, indent=2, default=str)

# print a sorted summary
for t, e in sorted(result.items(), key=lambda x: -x[1]["row_count"] if isinstance(x[1]["row_count"], int) else 0):
    rc = e["row_count"]
    print(f"{t:45s} rows={rc!s:>10} cols={e['col_count']:>3} comment={e['comment']}")

conn.close()
