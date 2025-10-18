# from langchain_openai import OpenAI
# from app.core.config import settings

# # Initialize OpenAI LLM (can swap to HuggingFace model later)
# llm = OpenAI(
#     model_name="gpt-3.5-turbo",  # or "gpt-4o-mini"
#     openai_api_key=settings.OPENAI_API_KEY,
#     temperature=0
# )

# def generate_answer(contexts: list, question: str) -> str:
#     """
#     Given a list of text chunks and a question, generate an answer.
#     """
#     context_text = "\n".join(contexts)
#     prompt = f"Answer the question based on the following context:\n{context_text}\n\nQuestion: {question}\nAnswer:"
#     return llm(prompt)
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from app.core.config import settings

# Initialize ChatOpenAI for chat models
llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",  # or "gpt-4o-mini"
    openai_api_key=settings.OPENAI_API_KEY,
    temperature=0
)

def generate_answer(contexts: list, question: str) -> str:
    """
    Generate answer using chat model.
    """
    context_text = "\n".join(contexts)
    prompt = (
        f"You are an expert assistant. Answer the question based on the following context:\n"
        f"{context_text}\n\nQuestion: {question}\nAnswer:"
    )

    # Chat model expects messages
    messages = [HumanMessage(content=prompt)]
    response = llm(messages=messages)
    return response.content
