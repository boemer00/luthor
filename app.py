import streamlit as st
import logging
from io import BytesIO
from transformers import LongformerTokenizer
import hashlib
import matplotlib.pyplot as plt
import time
from wordcloud import WordCloud

from src.data_loader import read_file
from src.preprocessor import FileTextPreprocessor, setup_nltk
from src.utils.openai_utils import generate_answer, get_embedding
from src.utils.pinecone_utils import query_pinecone, upsert_chunks
from src.utils.exceptions import DuplicateDocumentError, DatabaseConnectionError, InvalidQueryError

st.set_page_config(page_title='Luthor - Chat with your work', page_icon='🤖', layout='wide')

# Setup NLTK
setup_nltk()

@st.cache_resource
def load_models():
    return {'tokenizer': LongformerTokenizer.from_pretrained('allenai/longformer-base-4096')}

models = load_models()
tokenizer = models['tokenizer']

# Initialise preprocessor
preprocessor = FileTextPreprocessor(tokenizer)

def setup_logging():
    logging.basicConfig(filename='luthor_app.log', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

def get_file_hash(file_content):
    return hashlib.md5(file_content.getvalue()).hexdigest()

@st.cache_data
def generate_word_cloud(text):
    wordcloud = WordCloud(width=600, height=300, background_color='white', colormap='binary').generate(text)
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    return fig

def measure_processing_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        processing_time = end_time - start_time
        st.sidebar.write(f'{func.__name__} processing time: {processing_time:.2f} seconds')
        return result
    return wrapper

def main():
    setup_logging()
    st.title('Luthor Interface - v1')

    st.sidebar.header('About')
    st.sidebar.info('This app processes documents and answers questions based on their content.')

    uploaded_files = st.file_uploader('Upload documents', type=['txt', 'pdf', 'docx'], accept_multiple_files=True)

    if uploaded_files:
        for uploaded_file in uploaded_files:
            process_uploaded_file(uploaded_file)

        all_text = ' '.join([read_file(file, file.name) for file in uploaded_files])
        st.subheader('Word Cloud of Uploaded Documents')
        st.pyplot(generate_word_cloud(all_text))

    query = st.text_input('Enter your query')

    # Search refinement options
    st.sidebar.header('Search Refinement')
    date_range = st.sidebar.date_input('Date Range', [])
    doc_type = st.sidebar.multiselect('Document Type', ['memo', 'contract', 'case law', 'statute'])
    legal_area = st.sidebar.text_input('Legal Area')

    if query:
        process_query(query, date_range, doc_type, legal_area)

@measure_processing_time
def process_uploaded_file(uploaded_file):
    try:
        with st.spinner('Processing file...'):
            file_content = BytesIO(uploaded_file.read())
            file_content.seek(0)
            file_hash = get_file_hash(file_content)

            if check_duplicate_document(file_hash):
                raise DuplicateDocumentError('This document has already been uploaded and stored.')

            text = read_file(file_content, uploaded_file.name)
            _, segments, _, _, _, chunks = preprocessor.preprocess_doc(text)

            vectors = create_vectors(chunks, file_hash, uploaded_file.name)

            upsert_chunks(vectors)

        st.success('File processed and stored successfully!')
        logging.info(f'File uploaded and processed: {uploaded_file.name}')

    except DuplicateDocumentError as e:
        st.warning(str(e))
        logging.info(f'Duplicate document upload attempt: {uploaded_file.name}')
    except Exception as e:
        st.error(f'An unexpected error occurred while processing the file: {str(e)}')
        logging.exception(f'Unexpected error processing file: {uploaded_file.name}')

def create_vectors(chunks, file_hash, file_name):
    vectors = []
    for i, chunk in enumerate(chunks):
        chunk_embedding = get_embedding(chunk)
        vector = {
            "id": f"{file_hash}_{i}",
            "values": chunk_embedding,
            "metadata": {
                "file_hash": file_hash,
                "file_name": file_name,
                "chunk_id": str(i),
                "text": chunk[:1000]  # Limit text to 1000 characters
            }
        }
        vectors.append(vector)
    return vectors

def check_duplicate_document(file_hash):
    # Implement this function to check if the document already exists
    # Return True if it's a duplicate, False otherwise
    # Return False as a placeholder
    return False

@measure_processing_time
def process_query(query, date_range, doc_type, legal_area):
    if not query.strip():
        raise InvalidQueryError('Please enter a valid query.')

    try:
        with st.spinner('Generating answer...'):
            query_embedding = get_embedding(query)

            filters = create_filters(date_range, doc_type, legal_area)
            matches = query_pinecone(query_embedding, filters=filters)

            context = create_context(matches)
            answer = generate_answer(query, context)

        display_results(answer, matches)
        logging.info(f'Query processed: {query}')

    except DatabaseConnectionError:
        st.error('Error: Unable to connect to the database. Please try again later.')
        logging.error('Database connection error during query processing')
    except Exception as e:
        st.error(f'An unexpected error occurred while processing your query: {str(e)}')
        logging.exception(f'Unexpected error processing query: {query}')

def create_filters(date_range, doc_type, legal_area):
    filters = {}
    if date_range:
        filters["date"] = {"$gte": date_range[0], "$lte": date_range[1]}
    if doc_type:
        filters["doc_type"] = {"$in": doc_type}
    if legal_area:
        filters["legal_area"] = legal_area
    return filters

def create_context(matches):
    context = []
    for match in matches:
        text = match['metadata'].get('text', '')
        file_name = match['metadata'].get('file_name', 'Unknown File')
        citation = f"[Source: {file_name}]"
        context.append(f"{text} {citation}")
    return " ".join(context)

def display_results(answer, matches):
    st.subheader("Answer:")
    st.write(answer)

    st.subheader("Sources:")
    unique_sources = set(match['metadata'].get('file_name', 'Unknown File') for match in matches)
    for source in unique_sources:
        st.write(f"- {source}")

if __name__ == "__main__":
    main()
