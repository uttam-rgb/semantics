import yaml
import psycopg2
import json
import sys

with open("config.yaml") as f:
    cfg = yaml.safe_load(f)

db = cfg["crn_database_analytics"]

conn = psycopg2.connect(
    dbname=db["dbname"],
    host=db["host"],
    password=db["password"],
    port=db["port"],
    user=db["user"],
)
cur = conn.cursor()

# List schemas
cur.execute("""
    SELECT schema_name FROM information_schema.schemata
    WHERE schema_name NOT IN ('pg_catalog','information_schema')
    ORDER BY schema_name;
""")
schemas = [r[0] for r in cur.fetchall()]
print("SCHEMAS:", schemas, file=sys.stderr)

# List tables with row estimates, per schema
cur.execute("""
    SELECT n.nspname AS schema, c.relname AS table, c.reltuples::bigint AS est_rows
    FROM pg_class c
    JOIN pg_namespace n ON n.oid = c.relnamespace
    WHERE c.relkind = 'r'
      AND n.nspname NOT IN ('pg_catalog','information_schema')
    ORDER BY n.nspname, c.relname;
""")
tables = cur.fetchall()
print(f"TOTAL TABLES: {len(tables)}", file=sys.stderr)

result = {}
for schema, table, est_rows in tables:
    cur.execute("""
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns
        WHERE table_schema = %s AND table_name = %s
        ORDER BY ordinal_position;
    """, (schema, table))
    cols = cur.fetchall()
    result.setdefault(schema, {})[table] = {
        "est_rows": est_rows,
        "columns": [
            {"name": c[0], "type": c[1], "nullable": c[2] == "YES", "default": c[3]}
            for c in cols
        ],
    }

with open("schema_dump.json", "w") as f:
    json.dump(result, f, indent=2, default=str)

print("Wrote schema_dump.json", file=sys.stderr)
conn.close()
