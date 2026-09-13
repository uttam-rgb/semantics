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

tables = ["h3_demand_scores", "h3_grid_bengaluru", "h3_instructor_coverage", "h3_cluster_membership",
          "cluster_conversion_supply_verdict", "cluster_demand_scores", "cluster_demand_validation",
          "cluster_instructor_coverage", "cluster_lead_conversion_quadrant", "cluster_micromarket_octant",
          "clusters", "zones", "demand_master", "demand_pois", "customer_pois", "competitor_pois",
          "canonical_localities"]

for t in tables:
    print(f"\n{'='*15} analytics.{t} {'='*15}")
    cur.execute("""
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_schema='analytics' AND table_name=%s
        ORDER BY ordinal_position
    """, (t,))
    print(" columns:", cur.fetchall())

    try:
        cur.execute(f'SELECT count(*) FROM analytics."{t}"')
        print(" row count:", cur.fetchone())
    except Exception as e:
        conn.rollback()
        print(" row count ERROR:", e)

    try:
        cur.execute(f'SELECT obj_description(\'"analytics"."{t}"\'::regclass, \'pg_class\')')
        print(" comment:", cur.fetchone()[0])
    except Exception as e:
        conn.rollback()

conn.close()
