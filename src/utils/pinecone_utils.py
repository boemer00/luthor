import os
import logging
from typing import List

from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from tenacity import retry, stop_after_attempt, wait_random_exponential

load_dotenv()

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Pinecone client
try:
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
except Exception as e:
    logger.error(f"Failed to initialize Pinecone client: {str(e)}")
    raise

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(3))
def upsert_chunks(vectors: List[dict]):
    """
    Upserts vectors into the Pinecone index.

    Args:
        vectors (List[dict]): A list of dictionaries, each containing 'id', 'values', and 'metadata'.
    """
    try:
        index.upsert(vectors=vectors)
        logger.info(f"Successfully upserted {len(vectors)} vectors to index {index_name}.")
    except Exception as e:
        logger.error(f"Error upserting chunks to Pinecone: {str(e)}")
        raise

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(3))
def query_pinecone(query_vector: list, filters: dict = None, top_k: int = 5):
    """
    Retrieves the top-k most similar vectors from the Pinecone index based on the query vector.

    Args:
        query_vector (list): The vector to query against the index.
        filters (dict, optional): Metadata filters to apply to the query. Defaults to None.
        top_k (int, optional): The number of similar vectors to return. Defaults to 5.

    Returns:
        list: A list of the top-k similar vectors with their metadata.
    """
    try:
        response = index.query(vector=query_vector, filter=filters, top_k=top_k, include_values=True, include_metadata=True)
        logger.info(f"Query successful. Found {len(response['matches'])} matches.")
        return response['matches']
    except Exception as e:
        logger.error(f"Error querying Pinecone: {str(e)}")
        raise
