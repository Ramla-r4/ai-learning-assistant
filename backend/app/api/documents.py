from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from pypdf import PdfReader
from app.services.embeddings import get_embedding
from app.services.vector_db import vector_db
from app.core.security import get_current_user

router = APIRouter()

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50):
    """Split text into overlapping chunks."""
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...), user=Depends(get_current_user)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    # Read PDF text
    pdf_reader = PdfReader(file.file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""

    if not text.strip():
        raise HTTPException(status_code=400, detail="No text found in PDF")

    # Chunk, embed, store in FAISS
    chunks = chunk_text(text)
    for chunk in chunks:
        embedding = get_embedding(chunk)
        vector_db.add(embedding, chunk)

    return {"message": f"Uploaded {file.filename}", "chunks": len(chunks)}
