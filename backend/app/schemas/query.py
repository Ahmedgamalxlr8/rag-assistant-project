from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    # Enforces that a user cannot submit an empty question
    question: str = Field(..., min_length=3, description="User question")

class QueryResponse(BaseModel):
    # Guarantees the server always returns both an answer and citation sources
    answer: str
    sources: list[str]