from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.query import router as query_router
from app.services.retrieval import vector_service
from app.utils.logging_config import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code BEFORE yield runs once when server starts
    logger.info("Server starting: Initializing ChromaDB vector store...")
    vector_service.initialize()
    yield
    # Code AFTER yield runs when server stops
    logger.info("Server shutting down.")

app = FastAPI(
    title="RAG Document Assistant API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS: Allows your Streamlit frontend on port 8501 to make requests to port 8000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(query_router)