# Luthor: A Legal RAG System

## Overview

Luthor is a Retrieval-Augmented Generation (RAG) system designed for law firms to enable lawyers to efficiently "talk to their data". This system allows legal professionals to upload documents (e.g., memos) to a vector database stored in Pinecone and subsequently query this information using a chatbot-like interface built with Streamlit.

## Features

- Document upload and processing (supports .txt, .pdf, and .docx files)
- Text preprocessing and segmentation
- Vector embedding generation using OpenAI's API
- Efficient document storage and retrieval using Pinecone
- Natural language querying interface
- Context-aware answer generation

## Components

1. **Data Loader** (`src/data_loader.py`): Handles reading various file formats.
2. **Preprocessor** (`src/preprocessor.py`): Prepares text for embedding and storage.
3. **Main Application** (`app.py`): Streamlit interface for document upload and querying.
4. **OpenAI Utilities** (not visible in provided files): Presumably handles API interactions for embeddings and answer generation.
5. **Pinecone Utilities** (not visible in provided files): Manages vector database operations.

## Setup

### Prerequisites

- Python 3.10 or higher
- Pinecone account
- OpenAI API key

### Installation

1. Clone the repository:
   ```
   git clone [repository-url]
   cd luthor
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the root directory with the following:
   ```
   OPENAI_API_KEY=your_openai_api_key
   PINECONE_API_KEY=your_pinecone_api_key
   PINECONE_ENVIRONMENT=your_pinecone_environment
   ```

### Running the Application

1. Start the Streamlit app:
   ```
   streamlit run app.py
   ```

2. Access the application in your web browser at `http://localhost:8501`.

## Usage

1. **Document Upload**:
   - Use the file uploader in the Streamlit interface to upload legal documents (.txt, .pdf, or .docx).
   - The system will process the document, generate embeddings, and store them in Pinecone.

2. **Querying**:
   - Enter your legal query in the text input field.
   - Optionally, use the sidebar to refine your search by date range, document type, or legal area.
   - The system will retrieve relevant document chunks, generate an answer, and display it along with source information.

## Docker Support

A Dockerfile is provided for containerisation. To build and run the Docker image:

1. Build the image:
   ```
   docker build -t luthor .
   ```

2. Run the container:
   ```
   docker run -p 8501:8501 luthor
   ```

## Limitations and Future Improvements

- Currently, the system doesn't handle document deduplication effectively.
- The search refinement options (date range, document type, legal area) are not fully implemented in the backend.
- Error handling and logging could be improved for better debugging and user feedback.
- The system could benefit from more advanced NLP techniques for better understanding of legal context.

## License

All rights reserved.

This code and all associated files are the exclusive property of Renato Boemer.
No part of this code, in any form or by any means, may be copied, reproduced, modified,
adapted, stored in a retrieval system, or transmitted without the prior written permission
of Renato Boemer.
