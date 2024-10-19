import streamlit as st

st.set_page_config(page_title='Flight Quest', page_icon='🏡')
st.title('Flight Dashboard')
st.write('Comprehensive solution to flights')
container1 = st.container(height=100)
container1.write("This is inside the container")
st.sidebar.success("Choose your page")

