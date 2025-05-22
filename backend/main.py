from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from utils.file_handler import save_uploaded_files
from utils.ocr_extractor import extract_text
from utils.chunker import chunk_text
from utils.embedder import embed_chunks
from utils.qdrant_client import insert_into_qdrant
# from utils.theme_detector import detect_themes_for_docs

from routers.query import router as rag_router
from routers.themes import router as themes_router

app = FastAPI()

origins = [
    "https://mrityunjay-kukreti-wasserstoff-ai-intern-task-fhvwbc82z.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or ["*"] for all (less secure)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(rag_router)
app.include_router(themes_router)

@app.post("/upload/")
async def upload_doc(files: List[UploadFile] = File(...)):  # note plural 'files'
    results = []
    for file in files:
        filepath = await save_uploaded_files(file)
        text = extract_text(filepath)
        chunks = chunk_text(text,source=file.filename)
        embedded = embed_chunks(chunks)
        insert_into_qdrant(chunks, embedded, filename=file.filename)
        # theme = detect_themes_for_docs(text)
        results.append({
            "filename": file.filename,
            # "theme": theme
        })
        
    return {"filenames": results}

@app.get("/")
def root():
    return {"message": "Backend is live 🚀"}