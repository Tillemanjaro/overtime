# tv_display.py
import streamlit as st
import pandas as pd
from datetime import datetime

def app(assignments_log, shift_blocks):
    st.header("TV Display")
    
    # Ensure the Date column is in datetime format
    if assignments_log.empty is False and assignments_log["Date"].dtype == "O":
        assignments_log["Date"] = pd.to_datetime(assignments_log["Date"])
    
    display_date = st.date_input("Select Date to Display", datetime.today(), key="tv")
    
    if not assignments_log.empty:
        # Filter assignments for the selected date (compare only date part)
        display_df = assignments_log[assignments_log["Date"].dt.date == display_date]
        if not display_df.empty:
            for block in shift_blocks:
                block_df = display_df[display_df["Block"] == block]
                if not block_df.empty:
                    st.subheader(f"{block}")
                    st.dataframe(block_df[["Line", "Name", "Position", "Type"]].reset_index(drop=True))
                else:
                    st.markdown(f"*No assignments for {block}*")
        else:
            st.warning("No assignments for selected date.")
    else:
        st.info("No assignments data available.")
