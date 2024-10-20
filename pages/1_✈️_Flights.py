import streamlit as st
import pandas as pd
import time

# Set page configuration
st.set_page_config(page_title="Flights", page_icon="✈️")
st.logo(image='assets/logo.png', size='large')

# Adding a GIF background using custom HTML


# Display logo
st.image('assets/logo.png', width=200)

# Display subheader
st.subheader('✈️ Flight Data Dashboard')

# Excel 2: cleaned_flighthistory
with st.spinner(text='Fetching Data...'):
    df = pd.read_csv('pages/data/cleaned_flighthistoryevents.csv')
    df = df.drop(columns=['Unnamed: 0', 'Unnamed: 0.1', 'id'])
    df.rename(columns={'flighthistory_id': 'FLIGHT ID'}, inplace=True)
    df = df.tail(100)

    # Display dataframe
    st.dataframe(df)
# Custom CSS to set the GIF as a background

background_gif = """
<style>
    body {
        background-image: url('assets/airplane2.gif');
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        color: white;
    }
</style>
"""

# Insert the custom CSS into the app
st.markdown(background_gif, unsafe_allow_html=True)

# App content
