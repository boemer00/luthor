import streamlit as st
from io import BytesIO
from transformers import LongformerTokenizer

from src.data_loader import read_file
from src.preprocessor import FileTextPreprocessor, setup_nltk
from src.utils.openai_utils import generate_answer, get_embedding
from src.utils.pinecone_utils import query_pinecone, upsert_chunks

# Setup NLTK
setup_nltk()

# Initialize tokenizer
tokenizer = LongformerTokenizer.from_pretrained("allenai/longformer-base-4096")

# Initialize preprocessor
preprocessor = FileTextPreprocessor(tokenizer)

def main():
    st.set_page_config(page_title="Luthor Interface", page_icon="🤖", layout="wide")
    st.title("Luthor Interface - v1")

    st.sidebar.header("About")
    st.sidebar.info("This app processes documents and answers questions based on their content.")

    uploaded_file = st.file_uploader("Upload a document", type=["txt", "pdf", "docx"])

    if uploaded_file is not None:
        process_uploaded_file(uploaded_file)

    query = st.text_input("Enter your query")

    if query:
        process_query(query)

def process_uploaded_file(uploaded_file):
    try:
        with st.spinner("Processing file..."):
            # Convert the uploaded file to BytesIO and pass it along with the filename
            file_content = BytesIO(uploaded_file.read())
            text = read_file(file_content, uploaded_file.name)

            # Preprocess the document
            chunks = preprocessor.preprocess_doc(text)

            # Generate embeddings and upsert into Pinecone
            upsert_chunks(chunks, get_embedding)

        st.success("File processed and stored successfully!")

    except Exception as e:
        st.error(f"An error occurred while processing the file: {str(e)}")
        st.exception(e)

def process_query(query):
    if not query.strip():
        st.warning("Please enter a valid query.")
        return

    try:
        with st.spinner("Generating answer..."):
            # Get query embedding using OpenAI's model
            query_embedding = get_embedding(query)

            # Query Pinecone
            matches = query_pinecone(query_embedding)

            # Extract context from matches
            context = " ".join(
                " ".join(match['metadata']['text'])
                if isinstance(match['metadata']['text'], list)
                else match['metadata']['text']
                for match in matches
            )

            # Generate answer
            answer = generate_answer(query, context)

        st.subheader("Answer:")
        st.write(answer)

    except Exception as e:
        st.error(f"An error occurred while processing your query: {str(e)}")
        st.exception(e)

if __name__ == "__main__":
    main()