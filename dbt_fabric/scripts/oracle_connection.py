import cx_Oracle

conn = cx_Oracle.connect(
    "oracle_user/oracle_password@hostname:1521/ORCLPDB1"
)

cursor = conn.cursor()

# list tables
cursor.execute("""
    SELECT table_name
    FROM user_tables
""")

for row in cursor.fetchall():
    print(row)

cursor.close()
conn.close()
