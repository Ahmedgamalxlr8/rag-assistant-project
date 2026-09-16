from fastapi import APIRouter, HTTPException
from app.schemas.query import QueryRequest, QueryResponse
from app.services.retrieval import vector_service
from app.services.generation import generation_service
from app.utils.logging_config import logger

router = APIRouter()

@router.get("/health")
def health_check():
    """Healthcheck endpoint so monitoring systems verify the backend is running."""
    return {
        "status": "healthy",
        "chunks_indexed": vector_service.collection.count() if vector_service.collection else 0
    }

@router.post("/query", response_model=QueryResponse)
def query_documents(request: QueryRequest):
    """Processes incoming user question through the RAG pipeline."""
    try:
        # Step 1: Vector similarity retrieval
        chunks = vector_service.retrieve(request.question)
        if not chunks:
            return QueryResponse(
                answer="I don't have enough information to answer that.",
                sources=[]
            )
        
        # Step 2: Grounded generation
        result = generation_service.generate_answer(request.question, chunks)
        
        return QueryResponse(
            answer=result["answer"],
            sources=result["sources"]
        )
    except Exception as e:
        logger.error(f"Error handling query: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error while generating response.")