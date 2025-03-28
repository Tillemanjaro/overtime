import streamlit as st
import pandas as pd
import backend  # Assumes backend.py contains save_assignment() and remove_request()
from datetime import datetime

# Path to your employee data CSV file (expects columns: Name, Hire Date, Position)
EMPLOYEE_DATA_PATH = "C:/CodingProjects/overtime/employee_data.csv"

# Predefined shift blocks and lines
shift_blocks = [
    "7:00 AM - 11:00 AM",
    "11:00 AM - 3:00 PM",
    "3:00 PM - 7:00 PM",
    "7:00 PM - 11:00 PM",
    "11:00 PM - 3:00 AM",
    "3:00 AM - 7:00 AM"
]
ALL_LINES = ["L21", "L22", "L23", "L24", "L25", "L31", "L32", "L33", "L35", "L36"]

def load_employee_data():
    """Loads employee data from CSV; expects columns: Name, Hire Date, Position."""
    return pd.read_csv(EMPLOYEE_DATA_PATH, parse_dates=["Hire Date"])

def initialize_volunteer_queue():
    """
    Initializes the volunteer queue in session_state if not set.
    Sorted by ascending Hire Date (most senior first).
    """
    if "volunteer_queue" not in st.session_state:
        df = load_employee_data()
        st.session_state.volunteer_queue = df.sort_values("Hire Date", ascending=True).to_dict("records")

def initialize_mandate_queue():
    """
    Initializes the mandate queue in session_state if not set.
    Sorted by descending Hire Date (most junior first).
    """
    if "mandate_queue" not in st.session_state:
        df = load_employee_data()
        st.session_state.mandate_queue = df.sort_values("Hire Date", ascending=False).to_dict("records")

def rotate_queue(queue, name):
    """
    Rotates the employee with the given name in the queue:
    removes them from the current position and appends them to the end.
    """
    for i, emp in enumerate(queue):
        if emp["Name"] == name:
            candidate = queue.pop(i)
            queue.append(candidate)
            break

def auto_rerun():
    try:
        st.experimental_rerun()
    except AttributeError:
        st.markdown("<meta http-equiv='refresh' content='2'>", unsafe_allow_html=True)

def app(requests_log):
    st.header("Coordinator Portal")
    
    # ------------------------------
    # Section 1: Approve Volunteer Requests
    # ------------------------------
    st.subheader("Approve Volunteer Requests")
    vol_date = st.date_input("Select Date for Requests", datetime.today(), key="vol_date")
    requests_filtered = requests_log[requests_log["Date"] == pd.to_datetime(vol_date)]
    
    initialize_volunteer_queue()
    
    if requests_filtered.empty:
        st.info("No overtime requests for the selected date.")
    else:
        for i, row in requests_filtered.iterrows():
            with st.expander(f"{row['Name']} requested {row['Block']}"):
                st.write(f"**Requested Shift:** {row['Block']}")
                chosen_line = st.selectbox("Assign Line", ALL_LINES, key=f"vol_line_{i}")
                positions_list = ["Case Packer", "Operator", "Denester", "Cheese Harp", "Placer"]
                chosen_position = st.selectbox("Assign Position", positions_list, key=f"vol_pos_{i}")
                if st.button("Approve and Assign", key=f"vol_assign_{i}"):
                    candidate_name = row["Name"]
                    backend.save_assignment(
                        name=candidate_name,
                        date=row["Date"],
                        block=row["Block"],
                        line=chosen_line,
                        position=chosen_position,
                        assignment_type="Volunteer",
                        override=False
                    )
                    # Remove the approved request from the requests_log file
                    backend.remove_request(candidate_name, row["Date"], row["Block"])
                    st.success(f"{candidate_name} assigned as Volunteer to {chosen_line} - {chosen_position}.")
                    rotate_queue(st.session_state.volunteer_queue, candidate_name)
                    auto_rerun()
    
    # ------------------------------
    # Section 2: Mandate Assignment
    # ------------------------------
    st.subheader("Mandate Assignment")
    mandate_date = st.date_input("Select Date for Mandate", datetime.today(), key="mandate_date")
    mandate_shift = st.selectbox("Select Shift", shift_blocks, key="mandate_shift")
    mandate_line = st.selectbox("Select Line", ALL_LINES, key="mandate_line")
    
    initialize_mandate_queue()
    
    # Coordinator selects a Position to filter mandate candidates (from employee_data.csv)
    employee_data = load_employee_data()
    unique_positions = sorted(employee_data["Position"].unique())
    chosen_position_filter = st.selectbox("Select Position for Mandate", unique_positions, key="mandate_position_filter")
    
    # Filter mandate candidates by chosen position
    filtered_mandate_candidates = [emp for emp in st.session_state.mandate_queue if emp["Position"] == chosen_position_filter]
    if not filtered_mandate_candidates:
        st.info(f"No candidates available for position: {chosen_position_filter}")
    else:
        candidate_names = [emp["Name"] for emp in filtered_mandate_candidates]
        selected_candidate = st.selectbox("Select Candidate for Mandate", candidate_names, index=0, key="mandate_candidate")
        candidate_info = next((emp for emp in filtered_mandate_candidates if emp["Name"] == selected_candidate), None)
        st.markdown(f"**Candidate Position:** {candidate_info['Position']}")
        
        # Check if selected candidate is the top candidate (most junior) for this position
        top_candidate = filtered_mandate_candidates[0]
        override_flag = False
        if selected_candidate != top_candidate["Name"]:
            st.warning(f"Warning: {selected_candidate} is not next up (next up is {top_candidate['Name']}). This assignment will be flagged as an override.")
            override_flag = True
        
        if st.button("Confirm Mandate Assignment", key="mandate_confirm"):
            backend.save_assignment(
                name=candidate_info["Name"],
                date=mandate_date,
                block=mandate_shift,
                line=mandate_line,
                position=candidate_info["Position"],
                assignment_type="Mandate",
                override=override_flag
            )
            st.success(f"Mandated {candidate_info['Name']} to {mandate_line} - {candidate_info['Position']} for shift {mandate_shift}{' (Override)' if override_flag else ''}.")
            rotate_queue(st.session_state.mandate_queue, candidate_info["Name"])
            auto_rerun()
