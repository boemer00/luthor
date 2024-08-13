import os

from dotenv import load_dotenv
import openai
from openai import OpenAI

load_dotenv()

# Initialise OpenAI client
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


def get_embedding(text: str, model: str="text-embedding-3-small"):
    response = openai.embeddings.create(input=text, model=model)
    return response.data[0].embedding

def generate_answer(question: str, context: str, model: str='gpt-4o-mini'):
    if not context.strip():
        return "I don't know."

    # Identify context source
    if "database" in context:
        context_source = "from the database"
    else:
        context_source = "from llm knowledge"

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

    # Construct the message prompt for the chat completion
    messages = [
        {"role": "system", "content": "You are an experienced lawyer specializing in extracting and interpreting information from legal documents to provide accurate advice."},
        {"role": "user", "content": prompt}
    ]

    # Call the chat completions API
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=250,
        temperature=0
    )

    # Extract the assistant's message from the response
    generated_answer = response.choices[0].message.content.strip()
    return generated_answer
