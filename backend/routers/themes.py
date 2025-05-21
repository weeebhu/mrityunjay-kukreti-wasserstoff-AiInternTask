# routers/themes.py
from fastapi import APIRouter
from utils.qdrant_client import get_all_docs
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
router = APIRouter()

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

GROQ_MODEL = "llama3-70b-8192"

@router.get("/themes")
def get_themes():
    docs = get_all_docs()
    themes = []
    for doc in docs:
        filename = doc["filename"]
        text = doc["text"]

        # Use only the first 500 characters to limit tokens
        snippet = text[:500].replace("\n", " ")

        prompt = f"""
You are a helpful assistant. Please provide a single-word theme or very short keyword that best describes the following document text:

{snippet}

Theme:
"""

        try:
            response = client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[
                    {"role": "system", "content": "You are a helpful document summarizer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0,
                max_tokens=5  # Very short answer expected
            )
            theme = response.choices[0].message.content.strip().lower()
            # Clean theme: keep only first word or phrase, remove punctuation
            theme = theme.split("\n")[0].strip().strip(".")
        except Exception as e:
            theme = f"Error: {str(e)}"

        themes.append({"filename": filename, "theme": theme})

    return {"themes": themes}
