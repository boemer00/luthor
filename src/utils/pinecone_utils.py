import os
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
from typing import List

load_dotenv()

# Initialise Pinecone client
pinecone_api_key = os.getenv('PINECONE_API_KEY')
index_name = 'luthor-test-nb-0'
client = Pinecone(api_key=pinecone_api_key)

# Ensure the index is created
if index_name not in client.list_indexes().names():
    client.create_index(
        name=index_name,
        dimension=1536,
        metric='cosine',
        spec=ServerlessSpec(cloud='aws', region='us-east-1')
    )

# Retrieve the index
index = client.Index(index_name)

def upsert_chunks(chunks: List[str], get_embedding_func):
    chunk_embeddings = [get_embedding_func(chunk) for chunk in chunks]

    vectors = [
        {
            "id": f"doc_{i}",
            "values": chunk_embeddings[i],
            "metadata": {"text": chunks[i], "source": "database"}
        }
        for i in range(len(chunks))
    ]

    index.upsert(vectors=vectors)
    print(f"Successfully upserted {len(vectors)} vectors to index {index_name}.")

def query_pinecone(query_vector: list, top_k: int = 3):
    response = index.query(vector=query_vector, top_k=top_k, include_values=True, include_metadata=True)
    return response['matches']
