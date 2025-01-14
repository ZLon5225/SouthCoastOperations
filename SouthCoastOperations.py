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
st.title("South Coast Canine - Quality Control")

# Form
with st.form("quality_control_form"):
    st.subheader("Daily Checklist")
    
    employee = st.selectbox(
        "Who is completing this form?",
        ["Kimberly", "Brittany", "Anastasia", "Landen", "Ashley"]
    )
    fed_water = st.radio("Have all dogs been fed and given clean water?", ["Yes", "No"])
    bowls_washed = st.radio("Have all bowls been washed?", ["Yes", "No"])
    small_yard_scooped = st.radio("Has the small yard been scooped?", ["Yes", "No"])
    big_yard_scooped = st.radio("Has the big yard been scooped?", ["Yes", "No"])
    pictures_taken = st.radio("Have pictures been taken?", ["Yes", "No"])
    trello_updated = st.radio("Is Trello updated?", ["Yes", "No"])
    calendar_checked = st.radio("Is the calendar checked and updated?", ["Yes", "No"])
    submitted = st.form_submit_button("Submit")

# Handle form submission
if submitted:
    # Collect the data
    data = {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Employee": employee,
        "Fed and Watered": fed_water,
        "Bowls Washed": bowls_washed,
        "Small Yard Scooped": small_yard_scooped,
        "Big Yard Scooped": big_yard_scooped,
        "Pictures Taken": pictures_taken,
        "Trello Updated": trello_updated,
        "Calendar Checked": calendar_checked
    }
    
    # Notify the user of successful submission
    st.success("Quality control report submitted successfully!")
    
    # Save the data to Google Sheets
    try:
        sheet = connect_to_gsheet()
        sheet.append_row(list(data.values()))
        st.info("Data saved to Google Sheets successfully!")
    except Exception as e:
        st.error(f"Failed to save data to Google Sheets: {e}")
