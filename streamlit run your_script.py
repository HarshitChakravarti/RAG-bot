import streamlit as st

st.title("RAGbot Chat")
user_input = st.text_input("Ask a question:")

if user_input:
    # Call your RAGbot's main logic here, e.g.:
    answer = get_ragbot_answer(user_input)  # You'd wrap your main logic in a function
    st.write("**Answer:**", answer)