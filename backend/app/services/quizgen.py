import json
from langchain_core.prompts import ChatPromptTemplate
from app.services.llm import llm

QUIZ_PROMPT = """
You are a quiz generator. Based on the following context, generate {num_questions} questions.
Format them in JSON with fields:
- type: "mcq" or "short"
- question: the question text
- options: list of choices (only for mcq)
- answer: correct answer

Context:
{context}
"""

def generate_quiz(context_chunks: list, num_questions: int = 5):
    context_text = "\n".join(context_chunks)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant that generates quizzes."),
        ("user", QUIZ_PROMPT)
    ])
    chain = prompt | llm
    response = chain.invoke({"num_questions": num_questions, "context": context_text})
    return response.content

def safe_parse_quiz(output: str):
    try:
        return json.loads(output)
    except:
        return {"error": "Invalid JSON", "raw_output": output}
