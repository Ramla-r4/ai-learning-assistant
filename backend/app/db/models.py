# # from sqlalchemy import Column, Integer, String, ForeignKey, Text
# # from sqlalchemy.orm import relationship
# # from app.db.base import Base

# # class User(Base):
# #     __tablename__ = "users"
# #     id = Column(Integer, primary_key=True, index=True)
# #     email = Column(String, unique=True, index=True)
# #     hashed_password = Column(String)

# # class Document(Base):
# #     __tablename__ = "documents"
# #     id = Column(Integer, primary_key=True, index=True)
# #     user_id = Column(Integer, ForeignKey("users.id"))
# #     content = Column(Text)

# # class Quiz(Base):
# #     __tablename__ = "quizzes"
# #     id = Column(Integer, primary_key=True, index=True)
# #     user_id = Column(Integer, ForeignKey("users.id"))
# #     questions = Column(Text)  # JSON string

# # class Progress(Base):
# #     __tablename__ = "progress"
# #     id = Column(Integer, primary_key=True, index=True)
# #     user_id = Column(Integer, ForeignKey("users.id"))
# #     score = Column(Integer)
# from sqlalchemy import Column, Integer, String, ForeignKey, Text, JSON, Float
# from sqlalchemy.orm import relationship
# from app.db.base import Base

# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String, unique=True, index=True)
#     hashed_password = Column(String)

#     documents = relationship("Document", back_populates="user")
#     quizzes = relationship("Quiz", back_populates="user")
#     quiz_attempts = relationship("QuizAttempt", back_populates="user")

# class Document(Base):
#     __tablename__ = "documents"
#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.id"))
#     content = Column(Text)

#     user = relationship("User", back_populates="documents")

# class Quiz(Base):
#     __tablename__ = "quizzes"
#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.id"))
#     topic = Column(String, index=True)
#     questions = Column(JSON)  # Store questions as JSON

#     user = relationship("User", back_populates="quizzes")
#     attempts = relationship("QuizAttempt", back_populates="quiz")

# class QuizAttempt(Base):
#     __tablename__ = "quiz_attempts"
#     id = Column(Integer, primary_key=True, index=True)
#     quiz_id = Column(Integer, ForeignKey("quizzes.id"))
#     user_id = Column(Integer, ForeignKey("users.id"))
#     answers = Column(JSON)   # User-submitted answers
#     score = Column(Float)    # percentage score

#     quiz = relationship("Quiz", back_populates="attempts")
#     user = relationship("User", back_populates="quiz_attempts")
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON  # if using PostgreSQL
from sqlalchemy.ext.declarative import declarative_base
import json

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    quizzes = relationship("Quiz", back_populates="user")
    attempts = relationship("QuizAttempt", back_populates="user")


class Quiz(Base):
    __tablename__ = "quizzes"
    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    questions = Column(String, nullable=False)  # Store JSON string

    user = relationship("User", back_populates="quizzes")
    attempts = relationship("QuizAttempt", back_populates="quiz")

    def get_questions(self):
        return json.loads(self.questions)


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"
    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    answers = Column(String, nullable=False)  # Store JSON string
    score = Column(Float, nullable=False)

    quiz = relationship("Quiz", back_populates="attempts")
    user = relationship("User", back_populates="attempts")

    def get_answers(self):
        return json.loads(self.answers)
