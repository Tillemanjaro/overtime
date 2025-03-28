import streamlit as st
import pandas as pd
from datetime import datetime
import backend

shift_blocks = [
    "7:00 AM - 11:00 AM", "11:00 AM - 3:00 PM", "3:00 PM - 7:00 PM",
    "7:00 PM - 11:00 PM", "11:00 PM - 3:00 AM", "3:00 AM - 7:00 AM"
]

def app():
    st.header("Overtime Request Form")
    # Load employee data to get names from employee_data.csv
    employee_df = pd.read_csv("C:/CodingProjects/overtime/employee_data.csv", parse_dates=["Hire Date"])
    employee_names = sorted(employee_df["Name"].unique())
    
    # Use a dropdown to select the employee's name
    name = st.selectbox("Select Your Name", employee_names)
    date = st.date_input("Date", datetime.today())
    blocks = st.multiselect("Select Time Blocks", shift_blocks)
    
    if st.button("Submit Request"):
        if name and blocks:
            backend.save_request(name, date, blocks)
            st.success("Request submitted!")
        else:
            st.warning("Select your name and at least one block.")

if __name__ == "__main__":
    app()
