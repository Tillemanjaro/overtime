# database.py
import sqlite3
import pandas as pd

DATABASE_PATH = "my_database.db"

def get_connection():
    """Return a connection to the SQLite database."""
    return sqlite3.connect(DATABASE_PATH)

def create_tables():
    """Create tables if they do not exist."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create assignments table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assignments (
            id INTEGER PRIMARY KEY,
            assignment_name TEXT,
            assigned_to TEXT,
            due_date TEXT
            -- add more columns as needed
        )
    """)
    
    # Create employees table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY,
            name TEXT,
            role TEXT,
            department TEXT
            -- add more columns as needed
        )
    """)
    
    # Create requests table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY,
            request_type TEXT,
            employee_id INTEGER,
            request_date TEXT
            -- add more columns as needed
        )
    """)
    
    conn.commit()
    conn.close()

def import_csv_to_table(csv_path, table_name):
    """Import a CSV file into the specified table (overwrites existing data)."""
    df = pd.read_csv(csv_path)
    conn = get_connection()
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()
