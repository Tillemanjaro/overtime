import streamlit as st
from backend import get_requests, get_assignments, get_employee_data
from frontend import overtime_requester, coordinator_portal, manager_reports, tv_display

# Page configuration and custom CSS
st.set_page_config(page_title="Overtime Tracker", layout="wide")
st.markdown(
    """
    <style>
    /* Hide the default Streamlit menu & footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)

# Load data from the SQLite database using backend functions
requests_log = get_requests()
assignments_log = get_assignments()
employee_data = get_employee_data()

# Global variable: shift blocks (for use in the TV display)
shift_blocks = [
    "7:00 AM - 11:00 AM", "11:00 AM - 3:00 PM", "3:00 PM - 7:00 PM",
    "7:00 PM - 11:00 PM", "11:00 AM - 3:00 AM", "3:00 AM - 7:00 AM"
]

# Create tabs for the app
tab1, tab2, tab3, tab4 = st.tabs([
    "Overtime Requester",
    "Coordinator Portal",
    "Manager Reports",
    "TV Display"
])

with tab1:
    # Pass the preloaded employee_data to overtime_requester.app()
    overtime_requester.app(employee_data)

with tab2:
    coordinator_portal.app(requests_log)

with tab3:
    manager_reports.app(requests_log, assignments_log)

with tab4:
    tv_display.app(assignments_log, shift_blocks)
