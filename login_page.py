# import streamlit as st
import streamlit as st

# create login page
def show_login_page():
    st.title("Login Page")
    st.markdown("#### Please enter your login credentials")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "admin" and password == "admin":
            st.markdown("#### Welcome, you are logged in")
        else:
            st.markdown("#### Invalid credentials")

