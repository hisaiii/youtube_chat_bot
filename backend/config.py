"""
Central config: env vars, constants, and shared singletons (embeddings, LLM).
Import EMBEDDINGS / LLM from here everywhere instead of re-initializing.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceEmbeddings

# Resolve paths relative to this file, NOT the current working directory —
# so it doesn't matter if you launch uvicorn from repo root or from backend/.
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

PERSIST_DIRECTORY = os.getenv("CHROMA_PERSIST_DIR", str(BASE_DIR / "chroma_db"))

GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")
GROQ_TEMPERATURE = float(os.getenv("GROQ_TEMPERATURE", "0.3"))

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

# --------------------------------------------------
# Shared singletons — created once, imported everywhere
# --------------------------------------------------
EMBEDDINGS = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

LLM = ChatGroq(
    model=GROQ_MODEL,
    temperature=GROQ_TEMPERATURE,
)
