import sqlite3

DB_NAME = "atm.db"

def get_connection():
    return sqlite3.connect(DB_NAME)