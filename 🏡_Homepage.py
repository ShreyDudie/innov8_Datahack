import streamlit as st

st.set_page_config(page_title='Flight Quest', page_icon='🏡')
st.title('Flight Dashboard')
st.write('Comprehensive solution to flights')


container1 = st.container(height=125)
container1.write("Explore real-time flight information, analyze delays, and gain insights into weather conditions that may affect your journey.\n\n" "Our services are listed below:")


st.sidebar.success("Choose your page")
if st.button('ETA Analysis'):
    st.switch_page('pages/3_⌚_ETA.py')

if st.button('Wind Conditions'):
    st.switch_page('pages/4_🍃_Wind.py')

if st.button('See Past Flights'):
    st.switch_page('pages/1_✈️_Flights.py')


