import streamlit as st
import pandas as pd
from datetime import datetime
import backend

# Predefined shift blocks
shift_blocks = [
    "7:00 AM - 11:00 AM", "11:00 AM - 3:00 PM", "3:00 PM - 7:00 PM",
    "7:00 PM - 11:00 PM", "11:00 AM - 3:00 AM", "3:00 AM - 7:00 AM"
]

def app(employee_data):
    st.header("Overtime Request Form")
    
    # Use the passed employee_data DataFrame
    if employee_data.empty:
        st.error("No employee data found in the database.")
        return

    # Get a sorted list of unique employee names
    employee_names = sorted(employee_data["Name"].unique())
    
    # Let the user select their name, date, and time blocks
    name = st.selectbox("Select Your Name", employee_names)
    date = st.date_input("Date", datetime.today())
    blocks = st.multiselect("Select Time Blocks", shift_blocks)
    
    if st.button("Submit Request"):
        if name and blocks:
            # Save the request in the database (ensure backend.save_request is updated accordingly)
            backend.save_request(name, date, blocks)
            st.success("Request submitted!")
        else:
            st.warning("Select your name and at least one block.")

if __name__ == "__main__":
    # For testing standalone, load employee data from the database.
    emp_data = backend.get_employee_data()
    app(emp_data)
