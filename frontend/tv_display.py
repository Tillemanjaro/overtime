import streamlit as st
import pandas as pd   # Ensure this import is present
from datetime import datetime

def app(assignments_log, shift_blocks):
    st.header("TV Display")
    display_date = st.date_input("Select Date to Display", datetime.today(), key="tv")
    if not assignments_log.empty:
        display_df = assignments_log[assignments_log["Date"] == pd.to_datetime(display_date)]
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
