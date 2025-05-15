import streamlit as st
from Pages.globals import insert,get
import pandas as pd
from db import storethedata
import smtplib
from email.mime.text import MIMEText
from db import return_email,is_there
import os


st.subheader("Welcome")
st.write(get("user"))

Bid_Input=st.radio("How many bids you want to make", ["Single Bid", "Multiple Bid"])

l=[[],[],[]]#(Convention)- (Quantity, Price, Date , From hour, To hour)
quantity_widget1, price_widget1, date_widget1, from_widget1, to_widget1=st.columns([1,1,1,1,1])
l[0].append(quantity_widget1.number_input("Quantity1"))
l[0].append(price_widget1.number_input("Price1"))
l[0].append(date_widget1.date_input("Date1"))
l[0].append(from_widget1.number_input("From Hour1", min_value=0, max_value=23))
l[0].append(to_widget1.number_input("To Hour1", min_value=0, max_value=23))

if(Bid_Input=="Multiple Bid"):
    quantity_widget2, price_widget2, date_widget2, from_widget2, to_widget2 = st.columns([1, 1, 1, 1, 1])
    l[1].append(quantity_widget2.number_input("Quantity2"))
    l[1].append(price_widget2.number_input("Price2"))
    l[1].append(date_widget2.date_input("Date2"))
    l[1].append(from_widget2.number_input("From Hour2", min_value=0, max_value=23))
    l[1].append(to_widget2.number_input("To Hour2", min_value=0, max_value=23))

    quantity_widget3, price_widget3, date_widget3, from_widget3, to_widget3 = st.columns([1, 1, 1, 1, 1])
    l[2].append(quantity_widget3.number_input("Quantity3"))
    l[2].append(price_widget3.number_input("Price3"))
    l[2].append(date_widget3.date_input("Date3"))
    l[2].append(from_widget3.number_input("From Hour3", min_value=0, max_value=23))
    l[2].append(to_widget3.number_input("To Hour3", min_value=0, max_value=23))


options=st.radio("Send Me a Email Receipt of the Bids",["Yes","No"])


if(st.button("Submit the Bids")):
    if (os.path.exists(f"""Data/{get("user")}.csv""")):
        df = pd.read_csv(f"""Data/{get("user")}.csv""")
    else:
        df = pd.read_csv("Data/NO.csv")

    if (Bid_Input == "Single Bid"):
        l=[l[0]]

    p=True  ## if everything is correct
    for j in range (len(l)):
        for i in range (l[j][3], l[j][4]):
            Obj1=[get("user"), l[j][2].year, l[j][2].month, l[j][2].day, i]
            Obj2=["admin", l[j][2].year, l[j][2].month, l[j][2].day, i]
            df_temp=df[(df['date']==l[j][2].day) & (df['hour']==i) & (df['month']==l[j][2].month)]
            if(is_there(Obj1)):
                p=False
                st.error("Bids are already submitted for the given hour and date.")
                break
            if(is_there(Obj2)):
                p = False
                st.error("Market is already cleared for this hour")
                break
            if(len(df_temp)==0):
                p = False
                st.error("Please recheck the bids")
                break
            if(len(df_temp)!=0):
                if(df_temp.iloc[0].loc['value']<l[j][0] or l[j][0]<=0):
                    p=False
                    st.error("Please recheck the bids Quantity")
                    break

    if(p):
        st.success("Bids Submitted")
        str="The bids submitted by you are the following: \n"
        for j in  range (len(l)):
            for i in range (l[j][3],(l[j][4])):
                Obj={"User": get("user"),
                     "Quantity": l[j][0],
                     "Price": l[j][1],
                     "Date":l[j][2].day,
                     "Month": l[j][2].month,
                     "Year": l[j][2].year,
                     "Hour": i,
                     "State": "Waiting"}
                str=str+(f"""Price={Obj["Price"]}, Quantity={Obj["Quantity"]}, Date={Obj["Date"]}/{Obj["Month"]}/{Obj["Year"]}, Hour={Obj["Hour"]}\n""")
                storethedata("Bids",Obj)
        if (options == "Yes"):
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            # server.login('deevyansh.iitd@gmail.com', 'fvay qntl tetx bdyo')
            server.login('flexiblemarket0@gmail.com', 'uvpk bdlk vqdl icmh')
            message=MIMEText(str,"plain")
            message["Subject"]= "Regarding the Bids submitted on the Flexible Market Portal"
            message["From"]="flexiblemarket0@gmail.com"
            Obj={"User":get("user")}
            message["To"] = return_email(Obj)
            print(message["To"], message.as_string())
            server.sendmail("flexiblemarket0@gmail.com",return_email(Obj),message.as_string())
            server.quit












