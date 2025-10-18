# from sqlalchemy.orm import Session
# from passlib.context import CryptContext
# from app.db import models
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# def get_user_by_email(db: Session, email: str):
#     return db.query(models.User).filter(models.User.email == email).first()

# def create_user(db: Session, email: str, password: str):
#     hashed_password = pwd_context.hash(password)
#     db_user = models.User(email=email, hashed_password=hashed_password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user

# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)


# def save_quiz(db: Session, topic: str, user_id: int, questions: dict):
#     quiz = models.Quiz(topic=topic, user_id=user_id, questions=questions)
#     db.add(quiz)
#     db.commit()
#     db.refresh(quiz)
#     return quiz

# def save_quiz_attempt(db: Session, quiz_id: int, user_id: int, answers: dict, score: float):
#     attempt = models.QuizAttempt(
#         quiz_id=quiz_id, user_id=user_id, answers=answers, score=score
#     )
#     db.add(attempt)
#     db.commit()
#     db.refresh(attempt)
#     return attempt

# def get_user_progress(db: Session, user_id: int):
#     quizzes = db.query(models.Quiz).filter(models.Quiz.user_id == user_id).all()
#     attempts = db.query(models.QuizAttempt).filter(models.QuizAttempt.user_id == user_id).all()
#     return {"quizzes": quizzes, "attempts": attempts}
# from sqlalchemy.orm import Session
# from passlib.context import CryptContext
# from app.db import models
# import json  # <-- add this

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# def get_user_by_email(db: Session, email: str):
#     return db.query(models.User).filter(models.User.email == email).first()

# def create_user(db: Session, email: str, password: str):
#     hashed_password = pwd_context.hash(password)
#     db_user = models.User(email=email, hashed_password=hashed_password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user

# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

# # ---------- FIXED ---------- #
# def save_quiz(db: Session, topic: str, user_id: int, questions: dict):
#     quiz = models.Quiz(
#         topic=topic,
#         user_id=user_id,
#         questions=json.dumps(questions)  # <-- store as JSON string
#     )
#     db.add(quiz)
#     db.commit()
#     db.refresh(quiz)
#     return quiz

# def save_quiz_attempt(db: Session, quiz_id: int, user_id: int, answers: dict, score: float):
#     attempt = models.QuizAttempt(
#         quiz_id=quiz_id,
#         user_id=user_id,
#         answers=json.dumps(answers),  # <-- store as JSON string
#         score=score
#     )
#     db.add(attempt)
#     db.commit()
#     db.refresh(attempt)
#     return attempt

# def get_user_progress(db: Session, user_id: int):
#     quizzes = db.query(models.Quiz).filter(models.Quiz.user_id == user_id).all()
#     attempts = db.query(models.QuizAttempt).filter(models.QuizAttempt.user_id == user_id).all()
#     return {"quizzes": quizzes, "attempts": attempts}
from sqlalchemy.orm import Session
from app.db import models
from passlib.context import CryptContext
import json

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# User functions
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, email: str, password: str):
    hashed_password = pwd_context.hash(password)
    db_user = models.User(email=email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Quiz functions
def save_quiz(db: Session, topic: str, user_id: int, questions: list):
    """
    Save a generated quiz. Questions should be a list of dicts.
    """
    quiz = models.Quiz(topic=topic, user_id=user_id, questions=json.dumps(questions))
    db.add(quiz)
    db.commit()
    db.refresh(quiz)
    return quiz

def save_quiz_attempt(db: Session, quiz_id: int, user_id: int, answers: dict, score: float):
    attempt = models.QuizAttempt(
        quiz_id=quiz_id,
        user_id=user_id,
        answers=json.dumps(answers),
        score=score
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    return attempt

def get_user_progress(db: Session, user_id: int):
    quizzes = db.query(models.Quiz).filter(models.Quiz.user_id == user_id).all()
    attempts = db.query(models.QuizAttempt).filter(models.QuizAttempt.user_id == user_id).all()
    return {"quizzes": quizzes, "attempts": attempts}
