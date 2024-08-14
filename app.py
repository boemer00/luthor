import streamlit as st
from io import BytesIO
from transformers import LongformerTokenizer

from src.data_loader import read_file
from src.preprocessor import FileTextPreprocessor, setup_nltk
from src.utils.openai_utils import generate_answer, get_embedding
from src.utils.pinecone_utils import query_pinecone, upsert_chunks

# Setup NLTK
setup_nltk()

# Initialise tokenizer
tokenizer = LongformerTokenizer.from_pretrained("allenai/longformer-base-4096")

# Initialise preprocessor
preprocessor = FileTextPreprocessor(tokenizer)

# Streamlit interface
st.title("Luthor Interface - v0")

uploaded_file = st.file_uploader("Upload a document", type=["txt", "pdf", "docx"])

if uploaded_file is not None:
    try:
        # Convert the uploaded file to BytesIO and pass it along with the filename
        file_content = BytesIO(uploaded_file.read())
        text = read_file(file_content, uploaded_file.name)

        # Preprocess the document
        chunks = preprocessor.preprocess_doc(text)

        # Generate embeddings and upsert into Pinecone
        upsert_chunks(chunks, get_embedding)

        st.success("File processed and stored successfully!")

    except Exception as e:
        st.error(f"An error occurred: {e}")

query = st.text_input("Enter your query")

if query:
    try:
        # Get query embedding using OpenAI's model
        query_embedding = get_embedding(query)

        # Query Pinecone
        matches = query_pinecone(query_embedding)

        # Extract context from matches
        # context = " ".join(match['metadata']['text'] for match in matches)
        context = " ".join(" ".join(match['metadata']['text']) if isinstance(match['metadata']['text'], list) else match['metadata']['text'] for match in matches)

        # Generate answer
        answer = generate_answer(query, context)

        st.write("Answer:", answer)

    except Exception as e:
        st.error(f"An error occurred: {e}")
