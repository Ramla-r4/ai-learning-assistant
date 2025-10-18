# from fastapi import APIRouter, Depends
# from pydantic import BaseModel
# from app.core.security import get_current_user
# from app.services.vector_db import vector_db
# from app.services.embeddings import get_embedding
# from app.services.llm import generate_answer

# router = APIRouter()

# class QuestionRequest(BaseModel):
#     question: str

# class AnswerResponse(BaseModel):
#     answer: str
#     retrieved_chunks: list

# @router.post("/ask", response_model=AnswerResponse)
# def ask_question(payload: QuestionRequest, user=Depends(get_current_user)):
#     # Step 1: Embed the question
#     q_embedding = get_embedding(payload.question)
    
#     # Step 2: Retrieve relevant chunks from FAISS
#     top_chunks = vector_db.search(q_embedding, top_k=3)
    
#     if not top_chunks:
#         return {"answer": "No relevant information found.", "retrieved_chunks": []}
    
#     # Step 3: Send to LLM with context
#     answer = generate_answer(top_chunks, payload.question)
    
#     return {"answer": answer, "retrieved_chunks": top_chunks}
# from fastapi import APIRouter, Depends
# from pydantic import BaseModel
# from app.core.security import get_current_user
# from app.services.vector_db import vector_db
# from app.services.embeddings import get_embedding
# from app.services.llm import generate_answer

# router = APIRouter()

# class QuestionRequest(BaseModel):
#     question: str

# class AnswerResponse(BaseModel):
#     answer: str
#     retrieved_chunks: list

# @router.post("/ask", response_model=AnswerResponse)
# def ask_question(payload: QuestionRequest, user=Depends(get_current_user)):
#     # Step 1: Embed the question
#     q_embedding = get_embedding(payload.question)
    
#     # Step 2: Retrieve relevant chunks from FAISS
#     top_chunks = vector_db.search(q_embedding, top_k=3)
    
#     if not top_chunks:
#         return {"answer": "No relevant information found.", "retrieved_chunks": []}
    
#     # Step 3: Send to ChatOpenAI with context
#     answer = generate_answer(top_chunks, payload.question)
    
#     return {"answer": answer, "retrieved_chunks": top_chunks}
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.core.security import get_current_user
from app.services.vector_db import vector_db
from app.services.embeddings import get_embedding
from app.services.llm import generate_answer
import numpy as np

router = APIRouter()

class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str
    retrieved_chunks: list

@router.post("/ask", response_model=AnswerResponse)
def ask_question(payload: QuestionRequest, user=Depends(get_current_user)):
    print("===== RAG Q&A Debug Start =====")
    
    # 1️⃣ FAISS total vectors
    total_vectors = vector_db.index.ntotal
    print(f"[RAG] FAISS total vectors: {total_vectors}")
    if total_vectors == 0:
        print("[RAG] WARNING: VectorDB index is empty!")
    
    # 2️⃣ Embed question
    q_embedding = get_embedding(payload.question)
    print(f"[RAG] Question embedding shape: {q_embedding.shape}")
    print(f"[RAG] First 5 values of question embedding: {q_embedding[:5]}")

    # 3️⃣ Ensure correct dtype & shape for FAISS
    query_vector = np.array([q_embedding], dtype="float32")
    
    # 4️⃣ FAISS search
    top_k = min(3, total_vectors) if total_vectors > 0 else 1
    distances, indices = vector_db.index.search(query_vector, top_k)
    print(f"[RAG] FAISS distances: {distances}")
    print(f"[RAG] FAISS indices: {indices}")

    # 5️⃣ Retrieve actual chunks
    retrieved_chunks = []
    for i in indices[0]:
        if i != -1 and i < len(vector_db.documents):
            retrieved_chunks.append(vector_db.documents[i])
    
    print(f"[RAG] Retrieved chunks: {retrieved_chunks}")

    if not retrieved_chunks:
        print("[RAG] No chunks retrieved. Returning empty response.")
        return {"answer": "No relevant information found.", "retrieved_chunks": []}

    # 6️⃣ Generate answer via LLM
    answer = generate_answer(retrieved_chunks, payload.question)

    print("===== RAG Q&A Debug End =====\n")
    return {"answer": answer, "retrieved_chunks": retrieved_chunks}
