import streamlit as st
from backend import load_data
from frontend import overtime_requester, coordinator_portal, manager_reports, tv_display

# Page configuration and custom CSS
st.set_page_config(page_title="Overtime Tracker", layout="wide")
st.markdown("""
<style>
/* Hide the default Streamlit menu & footer */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* Additional custom CSS can go here */
</style>
""", unsafe_allow_html=True)

# Load the requests and assignments data from the backend
requests_log, assignments_log = load_data()

# Global variable: shift blocks (used e.g. in TV display)
shift_blocks = [
    "7:00 AM - 11:00 AM",
    "11:00 AM - 3:00 PM",
    "3:00 PM - 7:00 PM",
    "7:00 PM - 11:00 PM",
    "11:00 PM - 3:00 AM",
    "3:00 AM - 7:00 AM"
]

# Create the tabs for the app
tab1, tab2, tab3, tab4 = st.tabs([
    "Overtime Requester",
    "Coordinator Portal",
    "Manager Reports",
    "TV Display"
])

with tab1:
    overtime_requester.app()

with tab2:
    # The coordinator portal module now implements queue rotation using employee data
    coordinator_portal.app(requests_log)

with tab3:
    manager_reports.app(requests_log, assignments_log)

with tab4:
    tv_display.app(assignments_log, shift_blocks)
