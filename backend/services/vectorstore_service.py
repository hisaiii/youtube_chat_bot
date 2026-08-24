"""Chroma vectorstore access + populating it from a transcript."""
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from backend.config import EMBEDDINGS, PERSIST_DIRECTORY
from backend.services.transcript_service import extract_video_transcript

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


def get_vectorstore(video_id: str) -> Chroma:
    """Return the (possibly empty) Chroma collection for a video."""
    return Chroma(
        collection_name=f"video_{video_id}",
        embedding_function=EMBEDDINGS,
        persist_directory=PERSIST_DIRECTORY,
    )


def is_processed(video_id: str) -> bool:
    """True if this video already has embeddings stored."""
    vs = get_vectorstore(video_id)
    return len(vs.get()["ids"]) > 0


def process_and_store(video_id: str) -> bool:
    """Fetch transcript, chunk it, embed it, and persist to Chroma.
    Returns False if no transcript could be fetched.
    """
    print(f"📥 Processing video: {video_id}...")

    transcript = extract_video_transcript(video_id)
    if not transcript:
        return False

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
    )
    docs = [
        Document(page_content=chunk, metadata={"video_id": video_id})
        for chunk in splitter.split_text(transcript)
    ]

    Chroma.from_documents(
        documents=docs,
        embedding=EMBEDDINGS,
        collection_name=f"video_{video_id}",
        persist_directory=PERSIST_DIRECTORY,
    )
    print("✅ Video processed and stored successfully.")
    return True
