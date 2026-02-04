from database import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("SELECT * FROM accounts")
rows = cursor.fetchall()

for row in rows:
    print(row)
    
conn.close()