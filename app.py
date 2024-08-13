import streamlit as st
import requests

st.title('Luthor: Chat with your data.')

# Form to accept user queries
form = st.form(key='query_form')
question = form.text_input(label='Hi, how can I help you?')
submit_button = form.form_submit_button(label='Submit')

if submit_button:
    if question:
        # Sending POST request to FastAPI
        response = requests.post(
            "http://localhost:8000/query",
            json={"question": question}
        )
        if response.status_code == 200:
            # Display the answer
            answer = response.json().get('answer', 'No response')
            st.write(f"Answer: {answer}")
        else:
            st.write("Failed to get an answer from the server.")
    else:
        st.write("Please enter a question.")
