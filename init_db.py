from database import get_connection

def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts(
            account_number INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            pin INTEGER NOT NULL,
            balance INTEGER NOT NULL
        )
    """)
    
    cursor.execute("""
        INSERT OR IGNORE INTO accounts(account_number, name, pin, balance)
        VALUES
        (12345, 'Ibrahim', 1111, 12000),
        (23456, 'Ali', 2222, 20000),
        (34567, 'Muhammad', 3333, 25000)
    """)
    
    conn.commit()
    conn.close()
    
create_table()