import streamlit as st
st.write("Are you sure you wanna logout?")
if (st.button("Yes")):
    del st.session_state["user"]
    st.rerun()
