# import streamlit as st
# import requests

# # FastAPI server URL
# API_URL = "http://localhost:8000"

# def main():
#     st.title("Luthor: Chat with Your Data")

#     # Section for uploading a file
#     st.header("Upload a Document")
#     uploaded_file = st.file_uploader("Choose a file", type=["txt", "pdf", "docx"])

#     if uploaded_file is not None:
#         # Display file details
#         st.write("Filename:", uploaded_file.name)
#         st.write("File type:", uploaded_file.type)

#         # Button to process the uploaded file
#         if st.button("Process File"):
#             process_file(uploaded_file)

#     # Section for asking questions
#     st.header("Ask a Question")
#     question = st.text_input("Enter your question here")

#     if st.button("Get Answer"):
#         if question:
#             get_answer(question)
#         else:
#             st.error("Please enter a question.")

# def process_file(file):
#     try:
#         # Send file to the FastAPI server for processing
#         files = {"file": (file.name, file, file.type)}
#         response = requests.post(f"{API_URL}/upload", files=files)

#         if response.status_code == 200:
#             st.success("File processed and stored successfully!")
#         else:
#             st.error(f"Failed to process file: {response.text}")
#     except Exception as e:
#         st.error(f"Error occurred: {e}")

# def get_answer(question):
#     try:
#         # Send the question to the FastAPI server
#         data = {"question": question}
#         response = requests.post(f"{API_URL}/query", json=data)

#         if response.status_code == 200:
#             answer = response.json().get("answer", "No answer found.")
#             st.success(f"Answer: {answer}")
#         else:
#             st.error(f"Failed to get answer: {response.text}")
#     except Exception as e:
#         st.error(f"Error occurred: {e}")

# if __name__ == "__main__":
#     main()


import streamlit as st
import numpy as np

# Title
st.title("Luthor: Test App")

# Text Input
name = st.text_input("Enter your name:")

# Display a message based on input
if name:
    st.write(f"Hello, {name}!")

# Additional example text
st.write("Streamlit is working correctly if you can interact with the text input.")
