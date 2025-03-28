# backend.py
import pandas as pd
from database import get_connection

def get_employee_data():
    """
    Query and return all data from the employees table as a DataFrame.
    """
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM employees", conn)
    conn.close()
    return df

def get_assignments():
    """
    Query and return all data from the assignments table as a DataFrame.
    """
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM assignments", conn)
    conn.close()
    return df

def get_requests():
    """
    Query and return all data from the requests table as a DataFrame.
    """
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM requests", conn)
    conn.close()
    return df
