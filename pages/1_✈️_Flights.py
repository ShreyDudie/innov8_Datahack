import streamlit as st
import pandas as pd
import time

st.logo()
st.set_page_config(page_title="Flights",page_icon="✈️")

st.subheader('Past Flights')


#Excel 2: cleane=_flighthistory
with st.spinner(text='Fetching Data...'):
    df = pd.read_csv('pages\data\cleaned_flighthistoryevents.csv')
    df = df.drop(columns='Unnamed: 0')
    df = df.drop(columns='Unnamed: 0.1')
    df = df.drop(columns='id')
    df.rename(columns= {'flighthistory_id': 'FLIGHT ID'}, inplace=True)
    df = df.tail(100)

    st.dataframe(df)

