from fastapi import APIRouter
from pydantic import BaseModel
from utils.qdrant_client import search_qdrant
from utils.embedder import embed_chunks
from openai import OpenAI  # ✅ new OpenAI client (>=1.0.0)
import os
from dotenv import load_dotenv

load_dotenv()
router = APIRouter()

# Initialize Groq-compatible client
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",  # ✅ Groq's base URL
    api_key=os.getenv("GROQ_API_KEY")           # ✅ Ensure this is set in your .env
)
GROQ_MODEL = "llama3-70b-8192"              # ✅ Groq-supported model

# Define request schema
class QueryRequest(BaseModel):
    query: str
    top_k: int = 3

@router.post("/query")
def query_rag(request: QueryRequest):
    query = request.query
    top_k = request.top_k

    # Step 1: Embed the user query
    query_embedding = embed_chunks([query])[0]

    # Step 2: Search Qdrant for top-k relevant chunks
    results = search_qdrant(query_embedding, top_k=top_k)

    if not results:
        return {"answer": "No relevant context found.", "sources": []}

    # Step 3: Extract context chunks and sources
    context_chunks = []
    sources = []

    for hit in results:
        payload = hit.payload
        chunk_value = payload.get("chunk") or payload.get("text")  # fallback to old key
        source_value = payload.get("source")

        if chunk_value and source_value:
            context_chunks.append(chunk_value)
            sources.append(source_value)
        else:
            print(f"⚠️ Missing keys in payload: {payload}")

    # Step 4: Construct prompt and call Groq API
    context = "\n\n".join(context_chunks)
    prompt = f"""
You are a helpful assistant. Use the following context to answer the user's question. Be concise, factual, and cite relevant sources when applicable.

Context:
{context}

Question:
{query}

Answer:
"""

    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful document assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        answer = response.choices[0].message.content.strip()
        return {"answer": answer, "sources": list(set(sources))}

    except Exception as e:
        return {"error": str(e), "answer": "", "sources": []}
