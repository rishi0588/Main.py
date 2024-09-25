import streamlit as st
import pandas as pd
import plotly.express as px
import os
import json
import datetime
 
# Constants
USER_DATA_FILE = 'users.json'
 
# Helper Functions
def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as f:
            return json.load(f)
    return {}
 
def save_user_data(users):
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(users, f)
 
def create_user_folder(email):
    if not os.path.exists(email):
        os.mkdir(email)
 
def save_marks(email, marks_df):
    csv_path = os.path.join(email, 'marks.csv')
    marks_df.to_csv(csv_path, index=False)
 
def generate_charts(marks_df):
    # Bar Chart for Average Marks
    avg_marks = marks_df.mean().reset_index()
    avg_marks.columns = ['Subject', 'Average Marks']
    bar_fig = px.bar(avg_marks, x='Subject', y='Average Marks', title="Average Marks Per Subject")
 
    # Line Chart for Marks
    line_fig = px.line(marks_df.T, title="Marks Per Subject", labels={"value": "Marks", "index": "Subject"})
 
    # Pie Chart for Marks Distribution
    total_marks = marks_df.sum().reset_index()
    total_marks.columns = ['Subject', 'Total Marks']
    pie_fig = px.pie(total_marks, names='Subject', values='Total Marks', title="Marks Distribution")
 
    return bar_fig, line_fig, pie_fig
 
# Pages
def sign_up():
    st.title("Sign Up Page")
    name = st.text_input("Name")
    phone = st.text_input("Phone")
    dob = st.date_input("DOB",min_value=datetime.datetime(1999,1,1))
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
   
    if st.button("Sign Up"):
        users = load_user_data()
        if email in users:
            st.error("User with this email already exists!")
        else:
            users[email] = {"name": name, "phone": phone, "dob": str(dob), "password": password}
            save_user_data(users)
            create_user_folder(email)
            st.success("User registered successfully! Please log in.")
 
def login():
    st.title("Login Page")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
   
    if st.button("Login"):
        users = load_user_data()
        if email in users and users[email]["password"] == password:
            st.session_state["user"] = email
            st.success("Logged in successfully!")
            st.experimental_rerun()
        else:
            st.error("Invalid email or password")
 
def enter_marks():
    st.title(f"Welcome {st.session_state['user']}")
   
    subjects = ["DDPA","AAI","FOML","ATSA","IMAP"]
    marks = {}
   
    for subject in subjects:
        marks[subject] = st.slider(f"Choose your marks for {subject}", 0, 100, 0)
 
    if st.button("Submit"):
        marks_df = pd.DataFrame([marks])
        save_marks(st.session_state["user"], marks_df)
        st.success("Marks submitted successfully!")
 
def view_reports():
    st.title("Your Reports are Ready!")
    email = st.session_state["user"]
    csv_path = os.path.join(email, 'marks.csv')
 
    if os.path.exists(csv_path):
        marks_df = pd.read_csv(csv_path)
 
        # Generate charts
        bar_fig, line_fig, pie_fig = generate_charts(marks_df)
 
        # Display charts
        st.plotly_chart(bar_fig)
        st.plotly_chart(line_fig)
        st.plotly_chart(pie_fig)
    else:
        st.error("No marks data found!")
 
# Main App Logic
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Go to", ["Sign Up", "Log In", "Enter Marks", "View Reports"])
 
if "user" not in st.session_state:
    st.session_state["user"] = None
 
if page == "Sign Up":
    sign_up()
elif page == "Log In":
    login()
elif page == "Enter Marks" and st.session_state["user"]:
    enter_marks()
elif page == "View Reports" and st.session_state["user"]:
    view_reports()
else:
    st.error("Please log in to access this page.")