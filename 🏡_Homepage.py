import streamlit as st

st.set_page_config(page_title='Flight Quest', page_icon="assets/logo.png")
st.logo(image='assets/logo.png', size='large')
st.image('assets/logo.png', caption='Creating Innov8ing Solutions.')
st.divider()
st.title('Flight Quest Dashboard')
st.divider()
st.write('Comprehensive solution to flights')
# Custom CSS to set the GIF as a background
background_gif = """
<style>
    body {
        background-image: url("assets/airplane2.gif");
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

container1 = st.container(height=125)
container1.write("Explore real-time flight information, analyze delays, and gain insights into weather conditions that may affect your journey.\n\n" "Our services are listed below:")


st.sidebar.success("Choose your page")
if st.button('ETA Analysis'):
    st.switch_page('pages/3_⌚_ETA.py')

if st.button('Safety Predictions'):
    st.switch_page('pages/4_⚠️_Safety_Predictions.py')

if st.button('See Past Flights'):
    st.switch_page('pages/1_✈️_Flights.py')

if st.button('Current Weather Forecast'):
    st.switch_page('pages/2_⛅_Weather.py')

if st.button('Fuel Estimation'):
    st.switch_page('pages/5_⛽_Fuel_Estimation.py')

st.divider()
st.subheader('About Us')
container2 = st.container(height=90)
container2.write("We are team Innov8, A team who focuses on solving real life problems through code, one line at a time")

st.divider()
st.subheader('Rate Us')
if st.button('Rate Us'):
    st.switch_page('pages/6_👤_Reviews.py')
