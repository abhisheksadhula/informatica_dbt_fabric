import psycopg2

conn = psycopg2.connect(
    "postgresql://pg_user:pg_password@localhost:5432/mydb"
)

cur = conn.cursor()

cur.execute("""
    SELECT table_schema, table_name
    FROM information_schema.tables
    WHERE table_type='BASE TABLE'
""")

for row in cur.fetchall():
    print(row)

cur.close()
conn.close()
