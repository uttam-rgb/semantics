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

for table in ["exotel_calls", "exotel_sync_history"]:
    print(f"\n=== public.{table} ===")
    cur.execute("""
        SELECT column_name, data_type, is_nullable, column_default,
               character_maximum_length
        FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = %s
        ORDER BY ordinal_position;
    """, (table,))
    for c in cur.fetchall():
        print(" ", c)
    cur.execute(f'SELECT count(*) FROM public."{table}"')
    print("  row count:", cur.fetchone()[0])
    cur.execute(f'SELECT * FROM public."{table}" ORDER BY 1 LIMIT 2')
    colnames = [d[0] for d in cur.description]
    print("  cols:", colnames)
    for row in cur.fetchall():
        print("  sample:", row)

# min/max date range for exotel_calls to understand freshness
cur.execute("""
    SELECT min(created_at), max(created_at) FROM public.exotel_calls
""") if False else None

conn.close()
