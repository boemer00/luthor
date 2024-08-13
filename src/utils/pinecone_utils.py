import os
from typing import List

from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

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
    """
    Upserts text chunks into a Pinecone index by converting each chunk into embeddings.

    Args:
        chunks (List[str]): A list of text chunks to be upserted into the index.
        get_embedding_func (callable): A function that generates embeddings from a text string.
            This function will be imported from `openai_utils` in the `main.py` file.

    This function processes each text chunk using `get_embedding_func` to obtain its
    corresponding embedding. It then creates vectors that are upserted into a Pinecone index,
    where each vector includes metadata about the original text and its source.
    """
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

def query_pinecone(query_vector: list, top_k: int=3):
    """
    Retrieves the top-k most similar vectors from the Pinecone index based on the query vector.

    Args:
        query_vector (list): The vector to query against the index.
        top_k (int, optional): The number of similar vectors to return. Defaults to 3.

    Returns:
        list: A list of the top-k similar vectors with their metadata.
    """
    response = index.query(vector=query_vector, top_k=top_k, include_values=True, include_metadata=True)
    print(f"Query successful. Found {response['matches']} matches.")
    return response['matches']
