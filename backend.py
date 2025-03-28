import pandas as pd
from datetime import datetime
import os

def load_data():
    """
    Loads the requests and assignments data.
    Expects:
      - requests_log.csv with columns: Name, Date, Request Time, Block, etc.
      - assignments_log.csv with columns: Name, Date, Assignment Time, Block, Line, Position, Type, Override
    """
    # Use errors='ignore' if file might not exist yet
    try:
        req = pd.read_csv("requests_log.csv", parse_dates=["Date", "Request Time"])
    except Exception:
        req = pd.DataFrame()
    try:
        assign = pd.read_csv("assignments_log.csv", parse_dates=["Date", "Assignment Time"])
    except Exception:
        assign = pd.DataFrame()
    return req, assign

def save_assignment(name, date, block, line, position, assignment_type, override=False):
    """
    Saves an assignment to assignments_log.csv.
    Parameters:
      name: Employee name
      date: Assignment date
      block: Shift block
      line: Assigned line
      position: Position assigned
      assignment_type: "Volunteer" or "Mandate"
      override: Boolean flag for override
    """
    entry = pd.DataFrame({
        "Name": [name],
        "Date": [date],
        "Block": [block],
        "Line": [line],
        "Position": [position],
        "Assignment Time": [datetime.now()],
        "Assigned By": ["Coordinator"],
        "Type": [assignment_type],
        "Override": [override]
    })
    entry.to_csv("assignments_log.csv", mode='a', header=not os.path.exists("assignments_log.csv"), index=False)

def save_request(name, date, blocks):
    """
    Saves a new overtime request.
    Parameters:
      name: Employee name
      date: Date of the request
      blocks: List of requested blocks
    """
    new_entries = pd.DataFrame({
        "Name": [name] * len(blocks),
        "Date": [date] * len(blocks),
        "Block": blocks,
        "Request Time": [datetime.now()] * len(blocks)
    })
    new_entries.to_csv("requests_log.csv", mode='a', header=not os.path.exists("requests_log.csv"), index=False)

def remove_request(name, date, block):
    """
    Removes an approved request from requests_log.csv.
    Parameters:
      name: Employee name
      date: Date of the request
      block: Requested block to remove
    """
    try:
        df = pd.read_csv("requests_log.csv", parse_dates=["Date", "Request Time"])
    except Exception:
        return
    df = df[~((df["Name"] == name) & (df["Date"] == pd.to_datetime(date)) & (df["Block"] == block))]
    df.to_csv("requests_log.csv", index=False)
