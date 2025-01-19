import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Google Sheets setup
def connect_to_gsheet():
    # Define the scope for Google Sheets and Google Drive
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    # Load credentials from Streamlit secrets
    creds_dict = st.secrets["google_service_account"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    
    # Authorize the client
    client = gspread.authorize(creds)
    
    # Open the Google Sheet (replace with your actual sheet name)
    sheet = client.open("QC Fillable Form").sheet1
    return sheet

# Streamlit app
st.title("South Coast Canine - Facility Checklist")

# Form
with st.form("quality_control_form"):
    st.subheader("Daily and Weekly Checklist")

    # Building selection
    building = st.selectbox("Select the Building", ["New Building", "Old Building", "House"])

    # Daily checklist
    st.subheader(f"Daily Checklist - {building}")
    daily_tasks = [
        "A/C Filters Cleaned",
        "Floors Swept",
        "Floors Mopped",
        "Kennels Moved and Cleaned Around",
        "Kennels Cleaned When Dog Leaves for the Day"
    ]

    daily_answers = {}
    daily_comments = {}

    for task in daily_tasks:
        col1, col2 = st.columns([2, 1])
        with col1:
            daily_answers[task] = st.selectbox(
                task,
                ["Select Answer", "Yes", "No"],
                key=f"{building}_{task}_daily"
            )
        with col2:
            daily_comments[task] = st.text_input(f"Comments for {task}", key=f"{building}_{task}_daily_comments")

    # Weekly checklist
    st.subheader(f"Weekly Checklist - {building}")
    weekly_tasks = [
        "All Kennels Pulled and Cleaned Under and Behind",
        "Clean Upper Kennel Area",
        "Dust",
        "Dust Mirror",
        "A/C Unit Filters Dusted and Cleaned",
        "Walls Wiped",
        "Food Bins Cleaned and Organized",
        "Shop Vac Emptied"
    ]

    weekly_answers = {}
    weekly_comments = {}

    for task in weekly_tasks:
        col1, col2 = st.columns([2, 1])
        with col1:
            weekly_answers[task] = st.selectbox(
                task,
                ["Select Answer", "Yes", "No"],
                key=f"{building}_{task}_weekly"
            )
        with col2:
            weekly_comments[task] = st.text_input(f"Comments for {task}", key=f"{building}_{task}_weekly_comments")

    # Additional daily checklist
    st.subheader("Additional Daily Tasks")
    additional_tasks = [
        "Empty Poop Buckets",
        "Set A/C or Heat to Appropriate Temperature After Checking Weather Forecast"
    ]

    additional_answers = {}
    additional_comments = {}

    for task in additional_tasks:
        col1, col2 = st.columns([2, 1])
        with col1:
            additional_answers[task] = st.selectbox(
                task,
                ["Select Answer", "Yes", "No"],
                key=f"additional_{task}"
            )
        with col2:
            additional_comments[task] = st.text_input(f"Comments for {task}", key=f"additional_{task}_comments")

    # Submit button
    submitted = st.form_submit_button("Submit")

# Handle form submission
if submitted:
    # Validate all questions are answered
    if any(
        answer == "Select Answer"
        for answer in list(daily_answers.values())
        + list(weekly_answers.values())
        + list(additional_answers.values())
    ):
        st.error("Please select an answer for all checklist items before submitting.")
    else:
        # Collect the data
        data = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Building": building
        }

        for task, answer in daily_answers.items():
            data[f"Daily - {task}"] = answer
            data[f"Daily - {task} Comments"] = daily_comments[task]

        for task, answer in weekly_answers.items():
            data[f"Weekly - {task}"] = answer
            data[f"Weekly - {task} Comments"] = weekly_comments[task]

        for task, answer in additional_answers.items():
            data[f"Additional - {task}"] = answer
            data[f"Additional - {task} Comments"] = additional_comments[task]

        # Notify the user of successful submission
        st.success("Checklist report submitted successfully!")

        # Save the data to Google Sheets
        try:
            sheet = connect_to_gsheet()
            sheet.append_row(list(data.values()))
            st.info("Data saved to Google Sheets successfully!")
        except Exception as e:
            st.error(f"Failed to save data to Google Sheets: {e}")
