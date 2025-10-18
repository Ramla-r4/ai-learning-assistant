from sentence_transformers import SentenceTransformer

# Use HuggingFace model (free & local). You can swap to OpenAI later.
_model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text: str):
    """Convert text into vector embedding."""
    return _model.encode([text])[0]
