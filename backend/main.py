
from fastapi import FastAPI
from app.api import auth, documents, rag, quiz, progress
from app.db.base import Base, engine
from app.db import models

# ✅ Create all tables at startup (only if they don’t exist)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI RAG App")

# Register routes
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(documents.router, prefix="/documents", tags=["Documents"])
app.include_router(rag.router, prefix="/rag", tags=["RAG Q&A"])
app.include_router(quiz.router, prefix="/quiz", tags=["Quiz"])
# app.include_router(progress.router, prefix="/progress", tags=["Progress"])

@app.get("/")
def root():
    return {"message": "Welcome to AI RAG Backend 🚀"}
