import streamlit as st
import pandas as pd
from datetime import datetime

# Set page title and layout
st.set_page_config(page_title="South Coast Canine - Quality Control", layout="centered")

# Add header with logo and title
st.image("South Coast Canine_8e.jpg", width=100)
st.title("South Coast Canine - Quality Control")

# Define the form
with st.form("quality_control_form"):
    st.subheader("Daily Checklist")
    
    # Employee dropdown box
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
    
    # Submit button
    submitted = st.form_submit_button("Submit")

# Handle form submission
if submitted:
    # Collect and display the submitted data
    data = {
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Employee": employee,
        "Fed and Watered": fed_water,
        "Bowls Washed": bowls_washed,
        "Small Yard Scooped": small_yard_scooped,
        "Big Yard Scooped": big_yard_scooped,
        "Pictures Taken": pictures_taken,
        "Trello Updated": trello_updated,
        "Calendar Checked": calendar_checked
    }
    
    st.success("Quality control report submitted successfully!")
    
    # Show the collected data
    st.subheader("Submitted Data")
    st.write(pd.DataFrame([data]))
    
    # Optional: Save data to a CSV file for record-keeping
    df = pd.DataFrame([data])
    df.to_csv("quality_control_report.csv", mode="a", index=False, header=False)
    st.info("The data has been saved to 'quality_control_report.csv'.")
