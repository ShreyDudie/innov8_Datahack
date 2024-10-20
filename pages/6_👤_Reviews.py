import streamlit as st

st.logo(image='assets/logo.png', size='large')
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
        reviewcontainer = st.container(border=True)
        reviewcontainer.write(f"**YOUR Review:** {review}")
        reviewcontainer.write(f"**YOUR Rating:** {st.session_state.rating} stars")
        yourreview = {'name': name, 'review': review, 'rating': st.session_state.rating}
    else:
        st.error("Please provide a rating, name, and review.")


st.subheader('Past Reviews')

yourreview = {'name': name, 'review': review, 'rating': st.session_state.rating}
reviews = [
    {'name': 'Shreyas', 'review': 'Amazing Service, Works flawlessly! I got into all my flights!', 'rating': 5},
    {'name': 'Darshan', 'review': 'Very nice', 'rating': 5}
]
reviews.insert(0,yourreview)
for review in reviews:
    st.write(f"**{review['name']}**")
    st.write(f"Review: {review['review']}")
    st.write(f"Rating: {review['rating']} stars")
    st.markdown("---")


