import yaml
import psycopg2

with open("config.yaml") as f:
    cfg = yaml.safe_load(f)

db = cfg["crn_database"]
conn = psycopg2.connect(
    dbname=db["dbname"], host=db["host"], password=db["password"],
    port=db["port"], user=db["user"],
)
cur = conn.cursor()

targets = [("public", "exotel_calls"), ("public", "exotel_sync_history"),
           ("exotel", "call_logs"), ("exotel", "sync_history")]

for schema, table in targets:
    print(f"\n=== {schema}.{table} ===")
    # constraints (PK/unique/FK)
    cur.execute("""
        SELECT tc.constraint_type, kcu.column_name, ccu.table_schema, ccu.table_name, ccu.column_name
        FROM information_schema.table_constraints tc
        JOIN information_schema.key_column_usage kcu
          ON tc.constraint_name = kcu.constraint_name AND tc.table_schema = kcu.table_schema
        LEFT JOIN information_schema.constraint_column_usage ccu
          ON tc.constraint_name = ccu.constraint_name AND tc.constraint_type = 'FOREIGN KEY'
        WHERE tc.table_schema = %s AND tc.table_name = %s
    """, (schema, table))
    for row in cur.fetchall():
        print("  constraint:", row)

    # indexes
    cur.execute("""
        SELECT indexname, indexdef FROM pg_indexes
        WHERE schemaname = %s AND tablename = %s
    """, (schema, table))
    for row in cur.fetchall():
        print("  index:", row[0], "->", row[1])

    # table + column comments
    cur.execute("""
        SELECT obj_description(%s::regclass, 'pg_class')
    """, (f'"{schema}"."{table}"',))
    print("  table comment:", cur.fetchone()[0])

# any FK anywhere in the db referencing these tables
cur.execute("""
    SELECT tc.table_schema, tc.table_name, kcu.column_name,
           ccu.table_schema AS ref_schema, ccu.table_name AS ref_table, ccu.column_name AS ref_col
    FROM information_schema.table_constraints tc
    JOIN information_schema.key_column_usage kcu ON tc.constraint_name = kcu.constraint_name
    JOIN information_schema.constraint_column_usage ccu ON tc.constraint_name = ccu.constraint_name
    WHERE tc.constraint_type = 'FOREIGN KEY'
      AND ccu.table_name IN ('exotel_calls','exotel_sync_history','call_logs','sync_history')
""")
print("\nFKs referencing these tables from elsewhere:", cur.fetchall())

# distinct status/direction values + date range for exotel_calls
cur.execute("SELECT DISTINCT status FROM public.exotel_calls")
print("\nexotel_calls.status distinct:", [r[0] for r in cur.fetchall()])
cur.execute("SELECT DISTINCT direction FROM public.exotel_calls")
print("exotel_calls.direction distinct:", [r[0] for r in cur.fetchall()])
cur.execute("SELECT min(created_at), max(created_at) FROM public.exotel_calls")
print("exotel_calls.created_at range:", cur.fetchone())
cur.execute("SELECT min(date_created), max(date_created) FROM public.exotel_calls WHERE date_created ~ '^[0-9]'")
print("exotel_calls.date_created (string) range:", cur.fetchone())
cur.execute("SELECT count(*) FROM public.exotel_calls WHERE recording_url = ''")
print("exotel_calls recording_url empty count:", cur.fetchone()[0])
cur.execute("SELECT count(*) FROM public.exotel_calls WHERE recording_url IS NULL")
print("exotel_calls recording_url null count:", cur.fetchone()[0])
cur.execute("SELECT count(distinct account_sid) FROM public.exotel_calls")
print("distinct account_sid count:", cur.fetchone()[0])

conn.close()
