import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from db import checkdata
from Pages.globals import insert,get


st.title("Login")
usr=st.text_input("Username")
password=st.text_input("Password",type="password")

if(st.button("Login")):
    Obj1=[usr,password]
    if(checkdata("Users",Obj1)):
        insert("user",usr)
        print("Hi i am global user now- ",get("user"))
        st.success('Login Successfully!', icon="✅")
        st.balloons()
        st.rerun()
    else:
        st.error('Error in Login', icon="🚨")

