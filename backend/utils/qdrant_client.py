from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
)
import uuid
import os
from dotenv import load_dotenv

load_dotenv()
# Qdrant client config (modify if running in Docker or cloud)
client = QdrantClient(
    url="https://9a813689-87e4-4830-8d4c-50f3968e51ba.us-east4-0.gcp.cloud.qdrant.io:6333",  
    api_key= os.getenv("QDRANT_API_KEY")  
)

COLLECTION_NAME = "document_chunks"

def create_collection_if_not_exists(dim: int = 384):
    """
    Checks if collection exists; if not, creates one with specified vector dimension.
    """
    collections = [col.name for col in client.get_collections().collections]
    if COLLECTION_NAME not in collections:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=dim, distance=Distance.COSINE),
        )

def insert_into_qdrant(chunks, embeddings, filename):
    """
    Uploads each chunk and its vector into Qdrant with metadata.
    
    :param chunks: List[str] — raw text chunks
    :param embeddings: List[List[float]] — corresponding vectors
    :param filename: str — original filename for metadata
    """
    create_collection_if_not_exists(dim=len(embeddings[0]))

    points = []
    for i, (chunk, vector) in enumerate(zip(chunks, embeddings)):
        points.append(PointStruct(
            id=str(uuid.uuid4()),
            vector=vector.tolist(),
            payload={
                "id": i,
                "embedding": vector.tolist(),  # or just omit this if not needed
                "text": chunk["text"],
                "filename":filename,
                "chunk_id": chunk["chunk_id"],
                "source": filename
            }
        ))

    client.upsert(collection_name=COLLECTION_NAME, points=points)

def search_qdrant(query_vector, top_k=3):
    """
    Searches Qdrant for top_k most similar vectors to query_vector.
    
    :param query_vector: List[float] — embedded query vector
    :param top_k: int — number of top matches to return
    :return: List of search results with payloads
    """
    search_result = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=top_k,
        with_payload=True
    )
    return search_result

def get_all_docs():
    """
    Fetch all stored documents (grouped by filename) from Qdrant.
    Returns a list of dicts: [{ "filename": ..., "text": ... }, ...]
    """
    scroll_result = client.scroll(
        collection_name=COLLECTION_NAME,
        with_payload=True,
        limit=10000  # or use a loop for full pagination
    )[0]

    doc_map = {}
    for item in scroll_result:
        payload = item.payload
        filename = payload.get("filename") or payload.get("source")
        text = payload.get("text", "")

        if filename not in doc_map:
            doc_map[filename] = []

        doc_map[filename].append(text)

    # Combine chunks per file
    return [{"filename": fname, "text": " ".join(chunks)} for fname, chunks in doc_map.items()]