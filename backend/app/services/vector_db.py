# import faiss
# import numpy as np

# class VectorDB:
#     def __init__(self, dim: int = 384):  # all-MiniLM-L6-v2 outputs 384-dim vectors
#         self.index = faiss.IndexFlatL2(dim)
#         self.documents = []  # keep track of original text chunks

#     def add(self, embedding, text):
#         vector = np.array([embedding]).astype("float32")
#         self.index.add(vector)
#         self.documents.append(text)

#     def search(self, query_embedding, top_k: int = 3):
#         query_vector = np.array([query_embedding]).astype("float32")
#         distances, indices = self.index.search(query_vector, top_k)
#         results = [self.documents[i] for i in indices[0] if i < len(self.documents)]
#         return results

# # Global singleton for simplicity
# # vector_db = VectorDB()
# import faiss
# import numpy as np
# from typing import List, Tuple

# class VectorDB:
#     def __init__(self, dim: int = 384):
#         """
#         Simple FAISS-based vector database.
#         Args:
#             dim: Dimension of the embedding vectors.
#         """
#         self.dim = dim
#         self.index = faiss.IndexFlatL2(dim)  # L2 (Euclidean) similarity
#         self.documents: List[str] = []       # store original text chunks

#     def add(self, embedding: np.ndarray, text: str):
#         """
#         Add a new embedding + text chunk to the database.
#         Args:
#             embedding: 1D numpy array of shape (dim,)
#             text: Original text chunk
#         """
#         vector = np.array([embedding], dtype="float32")
#         self.index.add(vector)
#         self.documents.append(text)

#     def search(self, query_embedding: np.ndarray, top_k: int = 3) -> List[str]:
#         """
#         Search the database for the most similar vectors.
#         Args:
#             query_embedding: 1D numpy array of shape (dim,)
#             top_k: Number of top results to return
#         Returns:
#             List of text chunks corresponding to top_k nearest neighbors
#         """
#         if self.index.ntotal == 0:
#             return []  # empty index

#         query_vector = np.array([query_embedding], dtype="float32")
#         distances, indices = self.index.search(query_vector, top_k)

#         results = []
#         for i in indices[0]:
#             if i < len(self.documents):
#                 results.append(self.documents[i])
#         return results

# # Global singleton for simplicity
# vector_db = VectorDB()
# app/services/vector_db.py
import faiss
import numpy as np
from typing import List

class VectorDB:
    def __init__(self, dim: int = 384):
        self.dim = dim
        self.index = faiss.IndexFlatL2(dim)
        self.documents: List[str] = []

    def add(self, embedding: np.ndarray, text: str):
        vector = np.array([embedding], dtype="float32")
        self.index.add(vector)
        self.documents.append(text)

    def search(self, query_embedding: np.ndarray, top_k: int = 3) -> List[str]:
        if self.index.ntotal == 0:
            return []
        query_vector = np.array([query_embedding], dtype="float32")
        distances, indices = self.index.search(query_vector, top_k)
        results = []
        for i in indices[0]:
            if i != -1 and i < len(self.documents):
                results.append(self.documents[i])
        return results

vector_db = VectorDB()  # GLOBAL singleton
