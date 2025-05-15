import streamlit as st
from db import checkbids
## Convention - [User,From Date,To Date State]

st.title("Available Bids")
from_date_widget, to_date_widget=st.columns([1,1])
from_date=from_date_widget.date_input("From Date")
to_date=to_date_widget.date_input("To Date")
status=st.radio("Status of the Bids",["Selected","Non Selected","Waiting"])

Obj1=["",from_date, to_date, status]
df=checkbids(Obj1)[0]
df.rename(columns={"State": "Status"}, inplace=True)

def center_align_table(df):
    return df.style.set_table_styles(
        [{'selector': 'th', 'props': [('text-align', 'center')]},
         {'selector': 'td', 'props': [('text-align', 'center')]}]
    )


st.write(center_align_table(df).to_html(), unsafe_allow_html=True)
