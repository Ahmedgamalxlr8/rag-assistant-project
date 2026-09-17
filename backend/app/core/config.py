from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # Points to backend/
class Settings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    OLLAMA_MODEL: str = "llama3.2"
    EMBEDDING_MODEL: str = "BAAI/bge-small-en-v1.5"
    TOP_K: int = 4
    COLLECTION_NAME: str = "handbook_docs"

    # Points to backend/data/vector_store
    CHROMA_DIR: Path = BASE_DIR / "data" / "vector_store"

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent.parent / ".env",
        extra="ignore"
    )

settings = Settings()