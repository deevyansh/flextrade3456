import streamlit as st
import pandas as pd
from Pages.globals import insert, get
import os

st.title("Available Flexible Hours")
if(os.path.exists(f"""Data/{get("user")}.csv""")):
    df=pd.read_csv(f"""Data/{get("user")}.csv""")
else :
    df=pd.read_csv("Data/NO.csv")
df=df[['hour','date','month','value']]
df=df.sort_values(['month','date','hour'])
df=df.reset_index(drop=True)

df['month']=df['month'].astype(int)
df['hour']=df['hour'].astype(int)
df['date']=df['date'].astype(int)
df["hour+1"]=df["hour"]+1
df['day(dd/mm)'] = df['date'].astype(str) + '/' + df['month'].astype(str)
df["hour"]=df['hour'].astype(str) + ":00-" +df["hour+1"].astype(str) +":00"
df.drop(columns=["date","month","hour+1"], inplace=True)


def center_align_table(df):
    return df.style.set_table_styles(
        [{'selector': 'th', 'props': [('text-align', 'center')]},
         {'selector': 'td', 'props': [('text-align', 'center')]}]
    )


st.write(center_align_table(df).to_html(), unsafe_allow_html=True)
