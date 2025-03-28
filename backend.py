import pandas as pd
import sqlite3
from database import get_connection

def get_employee_data():
    """
    Retrieve employee data from the database.
    """
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM employees", conn)
    conn.close()
    return df

def get_requests():
    """
    Retrieve overtime requests from the database.
    """
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM requests", conn)
    conn.close()
    return df

def get_assignments():
    """
    Retrieve assignments data from the database.
    """
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM assignments", conn)
    conn.close()
    return df

def save_request(name, date, blocks):
    """
    Save an overtime request to the database.
    
    Parameters:
      - name: (str) The employee's name.
      - date: (datetime.date) The date of the overtime request.
      - blocks: (list) A list of selected time blocks.
    
    This function converts the blocks list into a comma-separated string.
    """
    # Convert the list of blocks into a comma-separated string
    blocks_str = ", ".join(blocks)
    
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Insert the request into the 'requests' table.
        # Adjust the SQL if your table schema uses different column names.
        cursor.execute(
            "INSERT INTO requests (Name, Date, Block) VALUES (?, ?, ?)",
            (name, date, blocks_str)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()
