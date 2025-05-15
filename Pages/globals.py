import streamlit as st
def insert(key, value):
    st.session_state[key]=value

def get(key):
    return st.session_state[key]