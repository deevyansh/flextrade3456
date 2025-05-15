
import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from db import storethedata

st.title("Register")
usr=st.text_input("Username")
email=st.text_input("Email")
Password=st.text_input("Password", type="password")
st.text_input("Confirm Password", type="password")


if st.button("Confirm Registration"):
    Obj1={
        "User": usr,
        "Email": email,
        "Password": Password
    }
    storethedata("Users",Obj1)
    st.success('Registration Done. Please Login')

