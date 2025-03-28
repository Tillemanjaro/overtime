# setup.py
from database import create_tables, import_csv_to_table

if __name__ == "__main__":
    # Create the necessary tables
    create_tables()
    
    # Import CSV files into the database tables.
    # Adjust the CSV file paths if they are in a different directory.
    import_csv_to_table("assignments_log.csv", "assignments")
    import_csv_to_table("employee_data.csv", "employees")
    import_csv_to_table("requests_log.csv", "requests")
    
    print("Database setup complete.")
