from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.core.security import get_current_user
from app.services.vector_db import vector_db
from app.services.embeddings import get_embedding
from app.services.quizgen import generate_quiz, safe_parse_quiz

router = APIRouter()

class QuizRequest(BaseModel):
    topic: str
    num_questions: int = 5

@router.post("/generate")
def create_quiz(payload: QuizRequest, user=Depends(get_current_user)):
    # Step 1: Embed topic and search relevant docs
    q_embedding = get_embedding(payload.topic)
    chunks = vector_db.search(q_embedding, top_k=5)

    # Fallback: use ALL stored chunks if none found
    if not chunks and vector_db.documents:
        chunks = vector_db.documents[:5]  # limit for efficiency

    if not chunks:
        raise HTTPException(status_code=404, detail="No content found. Please upload a PDF first.")

    # Step 2: Generate quiz
    quiz_raw = generate_quiz(chunks, payload.num_questions)
    quiz = safe_parse_quiz(quiz_raw)

    return {"topic": payload.topic, "quiz": quiz}
