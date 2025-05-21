from sentence_transformers import SentenceTransformer

# Load once at startup
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_chunks(chunks):
    """
    Embed a list of text chunks using a sentence-transformer model.

    :param chunks: List[str], text chunks
    :return: List[List[float]], embeddings
    """
    embeddings = model.encode(chunks, show_progress_bar=True, convert_to_numpy=True)
    return embeddings
