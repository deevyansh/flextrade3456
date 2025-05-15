import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pandas as pd
from datetime import datetime
from google.cloud.firestore_v1.base_query import  FieldFilter, BaseCompositeFilter
import streamlit as st

firebase_secrets = st.secrets["FIREBASE"]

cred = credentials.Certificate({
    "type": firebase_secrets["type"],
    "project_id": firebase_secrets["project_id"],
    "private_key_id": firebase_secrets["private_key_id"],
    "private_key": firebase_secrets["private_key"],
    "client_email": firebase_secrets["client_email"],
    "client_id": firebase_secrets["client_id"],
    "auth_uri": firebase_secrets["auth_uri"],
    "token_uri": firebase_secrets["token_uri"],
    "auth_provider_x509_cert_url": firebase_secrets["auth_provider_x509_cert_url"],
    "client_x509_cert_url": firebase_secrets["client_x509_cert_url"],
    "universe_domain": firebase_secrets["universe_domain"]
})
app = firebase_admin.initialize_app(cred)

def storethedata(collection,Obj1):
# Use a service account.

    db = firestore.client()
    data=[Obj1]
    #
    for record in data:
        db.collection(f"{collection}").add(record)

def checkdata(collection,Obj1):
    db = firestore.client()
    users_ref = db.collection(f"{collection}")
    docs = users_ref.stream()
    for doc in docs:
        if(doc.to_dict()["User"]==Obj1[0] and doc.to_dict()["Password"]==Obj1[1]):
            return True
    return False


def is_there(Obj1):
    # ["User", "Year", "Month", "Date", "Hour"]
    db = firestore.client()
    bids_ref = db.collection("Bids")
    filter_1 = FieldFilter("Year", "==", Obj1[1])
    if(Obj1[0]=="admin"):
        filter_2=FieldFilter("State","==", "Selected")
    else:
        filter_2 = FieldFilter("User", "==", Obj1[0])
    filter_3 = FieldFilter("Month", "==", Obj1[2])
    filter_4 = FieldFilter("Date", "==", Obj1[3])
    filter_5 = FieldFilter("Hour", "==", Obj1[4])
    docs = bids_ref.where(filter=filter_1).where(filter=filter_2).where(filter=filter_3).where(filter=filter_4).where(filter=filter_5).stream()
    return len(list(docs)) != 0



def checkbids(Obj1):
    ## Convention - [User,From Date,To Date State]
    db=firestore.client()
    bids_ref=db.collection("Bids")
    docs=bids_ref.stream()
    df=pd.DataFrame()
    list=[]
    for doc in docs:
        date=datetime(doc.to_dict()["Year"], doc.to_dict()["Month"], doc.to_dict()["Date"]).date()
        if((doc.to_dict()["User"]==Obj1[0] or Obj1[0]=="") and doc.to_dict()["State"]==Obj1[3] and date>=Obj1[1] and date<=Obj1[2]):
            df_dict=pd.DataFrame([doc.to_dict()])
            df=pd.concat([df,df_dict], ignore_index=True)
            list.append(doc.id)
    if(len(df)>0):

        df['Month'] = df['Month'].astype(int)
        df['Hour'] = df['Hour'].astype(int)
        df['Date'] = df['Date'].astype(int)
        df["Hour+1"] = df["Hour"] + 1
        df['day(dd/mm/yyyy)'] = df['Date'].astype(str) + '/' + df['Month'].astype(str) + "/" +df["Year"].astype(str)
        df["Hour"] = df['Hour'].astype(str) + ":00-" + df["Hour+1"].astype(str) + ":00"
        df.drop(columns=["Date", "Month", "Hour+1","Year"], inplace=True)

    return df,list

def changebids(Obj1, doc_id):
    db=firestore.client()
    if(Obj1["Finalized Quantities"]==0):
        db.collection("Bids").document(doc_id).update({"State": "Non Selected"})
    else:
        db.collection("Bids").document(doc_id).update({"State":"Selected", "Quantity_Selected":Obj1["Finalized Quantities"]})
    return True

def return_email(Obj1):
    db=firestore.client()
    users_ref=db.collection("Users")
    docs=users_ref.stream()
    for doc in docs:
        if(doc.to_dict()["User"]==Obj1["User"]):
            return doc.to_dict()["Email"]


def checkbids1(Obj1):
    ## Convention - [User,From Date,To Date State]
    db=firestore.client()
    bids_ref=db.collection("Bids")
    docs=bids_ref.stream()
    df=pd.DataFrame()
    list=[]
    for doc in docs:
        date=datetime(doc.to_dict()["Year"], doc.to_dict()["Month"], doc.to_dict()["Date"]).date()
        if((doc.to_dict()["User"]==Obj1[0] or Obj1[0]=="") and doc.to_dict()["State"]==Obj1[3] and date>=Obj1[1] and date<=Obj1[2]):
            df_dict=pd.DataFrame([doc.to_dict()])
            df=pd.concat([df,df_dict], ignore_index=True)
            list.append(doc.id)
    return df,list