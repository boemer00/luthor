from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
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

# Initialise FastAPI app
app = FastAPI()

# Add CORS middleware if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str

@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI app!"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Load the document
        text = read_file(file)

        # Preprocess the document
        # original_text, segments, cleaned_text, tokens, structured_text, chunks = preprocessor.preprocess_doc(text)
        chunks = preprocessor.preprocess_doc(text)

        # Generate embeddings and upsert into Pinecone
        upsert_chunks(chunks, get_embedding)

        print(f"Processed a chunk like this: {chunks[:1]} and stored {len(chunks)} chunks from the uploaded file.")
        return JSONResponse(content={"message": "File processed and stored successfully"}, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
async def query_database(query_request: QueryRequest):
    try:
        question = query_request.question

        # Get query embedding
        query_embedding = get_embedding(question)

        # Query Pinecone
        matches = query_pinecone(query_embedding)

        # Extract context from matches
        context = " ".join(match['metadata']['text'] for match in matches)

        # Generate answer
        answer = generate_answer(question, context)

        return JSONResponse(content={"answer": answer}, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("Loading Luthor...")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
