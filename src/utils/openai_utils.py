import os
import logging
from dotenv import load_dotenv
import openai
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_random_exponential

load_dotenv()

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize OpenAI client
try:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
except Exception as e:
    logger.error(f"Failed to initialize OpenAI client: {str(e)}")
    raise

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(3))
def get_embedding(text: str, model: str="text-embedding-3-small"):
    try:
        response = openai.embeddings.create(input=text, model=model)
        return response.data[0].embedding
    except Exception as e:
        logger.error(f"Error in get_embedding: {str(e)}")
        raise

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(3))
def generate_answer(question: str, context: str, model: str='gpt-4o-mini'):
    if not context.strip():
        return "I don't have enough information to answer this question."

    context_source = "from the database" if "database" in context else "from llm knowledge"

    prompt = f"""You are an experienced lawyer specializing in extracting and interpreting information from legal
    documents, past memos, and other records to answer questions accurately. Your goal is to provide the most
    reliable and detailed advice possible based on the available information.

    Context (Source: {context_source}): {context}

    Question: {question}

    Guidelines:
    - Use the context provided to support your answer.
    - If the answer is not available, suggest potential research avenues or considerations that may help.
    - Structure your response to address the question clearly and logically.
    - If unable to answer, state 'I don't know,' but also indicate why (e.g., insufficient context, unclear question).
    """

    messages = [
        {"role": "system", "content": "You are an experienced lawyer specializing in extracting and interpreting information from legal documents to provide accurate advice."},
        {"role": "user", "content": prompt}
    ]

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=250,
            temperature=0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Error in generate_answer: {str(e)}")
        raise
