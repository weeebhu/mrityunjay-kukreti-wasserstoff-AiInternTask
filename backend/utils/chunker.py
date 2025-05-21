def chunk_text(text,source, chunk_size=200, overlap=50):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk_words = words[i:i + chunk_size]
        chunks.append({
            "text": " ".join(chunk_words),
            "chunk_id": len(chunks),
            "source": source
        })
        i += chunk_size - overlap
    return chunks
