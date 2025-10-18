# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from pydantic import BaseModel
# from app.core.security import get_current_user, get_db
# from app.db import crud

# router = APIRouter()

# class SaveQuizRequest(BaseModel):
#     topic: str
#     questions: dict

# class SaveAttemptRequest(BaseModel):
#     quiz_id: int
#     answers: dict
#     score: float

# @router.post("/quiz/save")
# def save_quiz(payload: SaveQuizRequest, db: Session = Depends(get_db), user=Depends(get_current_user)):
#     quiz = crud.save_quiz(db, payload.topic, user.id, payload.questions)
#     return {"message": "Quiz saved", "quiz_id": quiz.id}

# @router.post("/quiz/attempt")
# def save_attempt(payload: SaveAttemptRequest, db: Session = Depends(get_db), user=Depends(get_current_user)):
#     attempt = crud.save_quiz_attempt(db, payload.quiz_id, user.id, payload.answers, payload.score)
#     return {"message": "Attempt saved", "attempt_id": attempt.id}

# @router.get("/progress")
# def get_progress(db: Session = Depends(get_db), user=Depends(get_current_user)):
#     data = crud.get_user_progress(db, user.id)
#     return data
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.security import get_current_user, get_db
from app.db import models, crud

router = APIRouter()

@router.get("/progress")
def get_progress(db: Session = Depends(get_db), user=Depends(get_current_user)):
    data = crud.get_user_progress(db, user.id)
    return {
        "quizzes": [{"id": q.id, "topic": q.topic, "questions": q.questions} for q in data["quizzes"]],
        "attempts": [
            {"id": a.id, "quiz_id": a.quiz_id, "score": a.score, "answers": a.answers}
            for a in data["attempts"]
        ]
    }

@router.delete("/progress/{attempt_id}")
def delete_attempt(attempt_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    attempt = db.query(models.QuizAttempt).filter_by(id=attempt_id, user_id=user.id).first()
    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")
    
    db.delete(attempt)
    db.commit()
    return {"message": "Attempt deleted"}
