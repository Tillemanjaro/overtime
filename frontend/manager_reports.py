# manager_reports.py

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime
from io import BytesIO
from matplotlib.backends.backend_pdf import PdfPages

# Colors
color_volunteer = "#e74c3c"  # Red
color_mandate = "#2ecc71"    # Green

def labeled_bar_chart_stacked(df, title, xlabel, ylabel, colors):
    """
    Create a stacked bar chart from a DataFrame.
    'df' should have the category as index and columns like ["Volunteer", "Mandate"].
    'colors' is a list [color_volunteer, color_mandate].
    """
    fig, ax = plt.subplots(figsize=(8, 3))
    indices = np.arange(len(df))
    bottom = np.zeros(len(df))
    for col, col_color in zip(df.columns, colors):
        values = df[col].values
        bars = ax.bar(indices, values, bottom=bottom, label=col, color=col_color)
        # Label each segment if > 0
        for i, bar in enumerate(bars):
            if values[i] > 0:
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bottom[i] + bar.get_height() / 2,
                    f'{int(values[i])}',
                    ha='center',
                    va='center',
                    fontsize=8,
                    color="black"   # Changed to black for better visibility
                )
        bottom += values
    ax.set_xticks(indices)
    ax.set_xticklabels(df.index, rotation=20, ha='right')
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend()
    plt.tight_layout()
    return fig

def app(requests_log, assignments_log):
    """
    Manager Reports tab with only Volunteer vs Mandate data (no Requested).
    """
    st.header("Manager Reports")
    
    # Date range filters
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime.today().replace(day=1))
    with col2:
        end_date = st.date_input("End Date", datetime.today())
    
    if start_date > end_date:
        st.error("Start date must be before or equal to end date.")
        return
    
    # Filter assignments by date range
    f_assign = assignments_log[
        (assignments_log["Date"] >= pd.to_datetime(start_date)) &
        (assignments_log["Date"] <= pd.to_datetime(end_date))
    ]
    
    # Build filter options
    blocks = sorted(f_assign["Block"].unique()) if not f_assign.empty else []
    lines = sorted(f_assign["Line"].unique()) if not f_assign.empty else []
    positions = sorted(f_assign["Position"].unique()) if not f_assign.empty else []
    types = ["Volunteer", "Mandate"]
    
    selected_blocks = st.multiselect("Filter by Block", blocks, default=blocks)
    selected_lines = st.multiselect("Filter by Line", lines, default=lines)
    selected_positions = st.multiselect("Filter by Position", positions, default=positions)
    selected_types = st.multiselect("Filter by Type", types, default=types)
    
    # Apply filters
    filtered_assignments = f_assign[
        (f_assign["Block"].isin(selected_blocks)) &
        (f_assign["Line"].isin(selected_lines)) &
        (f_assign["Position"].isin(selected_positions)) &
        (f_assign["Type"].isin(selected_types))
    ]
    
    # Summary metrics
    total_assignments = filtered_assignments["Name"].nunique()
    
    col_m1, col_m2 = st.columns(2)
    col_m1.metric("Total Assignments", total_assignments)
    
    most_used_position = "N/A"
    if not filtered_assignments.empty:
        most_used_position = filtered_assignments["Position"].value_counts().idxmax()
    
    col_m2.markdown(f"""
    <div style='text-align:center; font-size:1rem; background-color:#F0F2F6; 
                padding:0.5rem; border-radius:8px;'>
      <strong>Most Used Position</strong><br/>{most_used_position}
    </div>
    """, unsafe_allow_html=True)
    
    # ------------------------------------------------------------
    # Charts
    # ------------------------------------------------------------
    with st.expander("View Charts"):
        if filtered_assignments.empty:
            st.info("No assignments match the selected filters.")
        else:
            # 1) Assignments by Block (Grouped)
            df_block = filtered_assignments.groupby(["Block", "Type"])["Name"].nunique().unstack(fill_value=0)
            for t in ["Volunteer", "Mandate"]:
                if t not in df_block.columns:
                    df_block[t] = 0
            df_block = df_block[["Volunteer", "Mandate"]].sort_index()
            
            fig_block, ax_block = plt.subplots(figsize=(9, 4))
            x_vals = np.arange(len(df_block))
            width = 0.35
            ax_block.bar(x_vals - width/2, df_block["Volunteer"], width, label="Volunteer", color=color_volunteer)
            ax_block.bar(x_vals + width/2, df_block["Mandate"], width, label="Mandate", color=color_mandate)
            ax_block.set_xticks(x_vals)
            ax_block.set_xticklabels(df_block.index, rotation=20, ha='right')
            ax_block.set_title("Assignments by Block")
            ax_block.legend(loc="upper left", bbox_to_anchor=(1.05, 1))
            
            # Numeric labels
            for container in ax_block.containers:
                ax_block.bar_label(container, padding=3, color="black")
            
            plt.tight_layout()
            st.pyplot(fig_block)
            
            # 2) Assignments by Line (Stacked)
            df_line = filtered_assignments.groupby(["Line", "Type"])["Name"].nunique().unstack(fill_value=0)
            for t in ["Volunteer", "Mandate"]:
                if t not in df_line.columns:
                    df_line[t] = 0
            df_line = df_line[["Volunteer", "Mandate"]].sort_index()
            
            fig_line = labeled_bar_chart_stacked(
                df_line,
                "Assignments by Line",
                "Line",
                "Count",
                [color_volunteer, color_mandate]
            )
            st.pyplot(fig_line)
            
            # 3) Assignments by Position (Stacked)
            df_pos = filtered_assignments.groupby(["Position", "Type"])["Name"].nunique().unstack(fill_value=0)
            for t in ["Volunteer", "Mandate"]:
                if t not in df_pos.columns:
                    df_pos[t] = 0
            df_pos = df_pos[["Volunteer", "Mandate"]].sort_index()
            
            fig_pos = labeled_bar_chart_stacked(
                df_pos,
                "Assignments by Position",
                "Position",
                "Count",
                [color_volunteer, color_mandate]
            )
            st.pyplot(fig_pos)
            
            # 4) Pie Chart (Volunteer vs Mandate)
            type_counts = filtered_assignments["Type"].value_counts()
            fig_pie, ax_pie = plt.subplots(figsize=(4, 4))
            pie_colors = [color_volunteer, color_mandate] if len(type_counts) == 2 else [color_volunteer, color_mandate]
            ax_pie.pie(type_counts, labels=type_counts.index, autopct="%1.1f%%", startangle=90, colors=pie_colors)
            ax_pie.set_title("Volunteer vs Mandate")
            st.pyplot(fig_pie)
    
    # ------------------------------------------------------------
    # DOWNLOAD BUTTONS: CSV, Excel
    # ------------------------------------------------------------
    st.download_button(
        "Download Filtered CSV",
        filtered_assignments.to_csv(index=False).encode("utf-8"),
        "filtered_assignments.csv"
    )
    
    excel_buffer = BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
        filtered_assignments.to_excel(writer, index=False, sheet_name="FilteredAssignments")
    st.download_button(
        "Download Filtered Excel",
        data=excel_buffer.getvalue(),
        file_name="filtered_assignments.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    
    # ------------------------------------------------------------
    # PDF REPORT
    # ------------------------------------------------------------
    if not filtered_assignments.empty:
        buffer = BytesIO()
        fig_all = plt.figure(figsize=(12, 9))
        gs = fig_all.add_gridspec(3, 2, hspace=0.7, wspace=0.5)
        
        # Row 0: Title + Summary
        ax0 = fig_all.add_subplot(gs[0, :])
        ax0.axis('off')
        metrics_text = (
            f"Manager Report: {start_date.strftime('%m/%d/%Y')} - {end_date.strftime('%m/%d/%Y')}\n"
            f"Total Assignments: {total_assignments}\n"
        )
        if most_used_position != "N/A":
            metrics_text += f"Most Used Position: {most_used_position}"
        ax0.text(0.5, 0.5, metrics_text, ha='center', va='center', fontsize=11)
        
        # Row 1, Col 0: Assignments by Block (Grouped)
        ax1 = fig_all.add_subplot(gs[1, 0])
        x_vals = np.arange(len(df_block))
        ax1.bar(x_vals - width/2, df_block["Volunteer"], width, label="Volunteer", color=color_volunteer)
        ax1.bar(x_vals + width/2, df_block["Mandate"], width, label="Mandate", color=color_mandate)
        ax1.set_xticks(x_vals)
        ax1.set_xticklabels(df_block.index, rotation=20, ha='right')
        ax1.set_title("Assignments by Block")
        # Move legend outside
        ax1.legend(loc="upper left", bbox_to_anchor=(1.05, 1))
        # Label each bar
        for container in ax1.containers:
            ax1.bar_label(container, padding=3, color="black")
        
        # Row 1, Col 1: Assignments by Line (Stacked)
        ax2 = fig_all.add_subplot(gs[1, 1])
        df_line_pdf = df_line.copy()
        idx_line = np.arange(len(df_line_pdf))
        bottom_line = np.zeros(len(df_line_pdf))
        for col, col_color in zip(df_line_pdf.columns, [color_volunteer, color_mandate]):
            vals = df_line_pdf[col].values
            bars = ax2.bar(idx_line, vals, width=0.5, bottom=bottom_line, label=col, color=col_color)
            # Label each stacked segment
            for i, bar in enumerate(bars):
                if vals[i] > 0:
                    ax2.text(
                        bar.get_x() + bar.get_width()/2,
                        bottom_line[i] + bar.get_height()/2,
                        f"{int(vals[i])}",
                        ha='center',
                        va='center',
                        fontsize=8,
                        color="black"
                    )
            bottom_line += vals
        ax2.set_xticks(idx_line)
        ax2.set_xticklabels(df_line_pdf.index, rotation=20, ha='right')
        ax2.set_title("Assignments by Line")
        ax2.set_xlabel("Line")
        ax2.set_ylabel("Count")
        ax2.legend()
        
        # Row 2, Col 0: Assignments by Position (Stacked)
        ax3 = fig_all.add_subplot(gs[2, 0])
        df_pos_pdf = df_pos.copy()
        idx_pos = np.arange(len(df_pos_pdf))
        bottom_pos = np.zeros(len(df_pos_pdf))
        for col, col_color in zip(df_pos_pdf.columns, [color_volunteer, color_mandate]):
            vals = df_pos_pdf[col].values
            bars = ax3.bar(idx_pos, vals, width=0.5, bottom=bottom_pos, label=col, color=col_color)
            # Label each stacked segment
            for i, bar in enumerate(bars):
                if vals[i] > 0:
                    ax3.text(
                        bar.get_x() + bar.get_width()/2,
                        bottom_pos[i] + bar.get_height()/2,
                        f"{int(vals[i])}",
                        ha='center',
                        va='center',
                        fontsize=8,
                        color="black"
                    )
            bottom_pos += vals
        ax3.set_xticks(idx_pos)
        ax3.set_xticklabels(df_pos_pdf.index, rotation=20, ha='right')
        ax3.set_title("Assignments by Position")
        ax3.set_xlabel("Position")
        ax3.set_ylabel("Count")
        ax3.legend()
        
        # Row 2, Col 1: Pie Chart
        ax4 = fig_all.add_subplot(gs[2, 1])
        type_counts_pdf = filtered_assignments["Type"].value_counts()
        pie_colors = [color_volunteer, color_mandate] if len(type_counts_pdf) == 2 else [color_volunteer, color_mandate]
        ax4.pie(type_counts_pdf, labels=type_counts_pdf.index, autopct="%1.1f%%", startangle=90, colors=pie_colors)
        ax4.set_title("Volunteer vs Mandate")
        
        plt.tight_layout()
        # Save PDF
        pdf_buffer = BytesIO()
        with PdfPages(pdf_buffer) as pdf:
            pdf.savefig(fig_all)
            d = pdf.infodict()
            d["Title"] = "Overtime Summary Report"
            d["Author"] = "Overtime Tracker"
        pdf_buffer.seek(0)
        
        st.download_button("Download PDF Report", pdf_buffer, "overtime_summary.pdf")
