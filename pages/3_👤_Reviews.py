import streamlit as st

st.set_page_config(page_title='Reviews',page_icon='👤')
st.title('Reviews')
st.subheader('Share your experience with our service')
st.write("How would you rate us?")
st.feedback("stars", key="rating")

name = st.text_input("Enter Your Name: ", key='name')
review = st.text_area("Write your detailed review", key="review")

if st.button('Submit Review'):
    if name and st.session_state.rating and review:
       
        st.success(f"Thank you {name} for your feedback!")
        st.write(f"**Review:** {review}")
        st.write(f"**Rating:** {st.session_state.rating} stars")
    else:
        st.error("Please provide a rating, name, and review.")


st.subheader('Past Reviews')


reviews = [
    {'name': 'Shreyas', 'review': 'Amazing Service, Works flawlessly! I got into all my flights!', 'rating': 5},
    {'name': 'Darshan', 'review': 'Very nice', 'rating': 5}
]

for review in reviews:
    st.write(f"**{review['name']}**")
    st.write(f"Review: {review['review']}")
    st.write(f"Rating: {review['rating']} stars")
    st.markdown("---")