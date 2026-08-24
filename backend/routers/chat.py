from fastapi import APIRouter

from backend.models.schemas import ChatRequest
from backend.services.vectorstore_service import get_vectorstore, process_and_store
from backend.services.chat_service import run_chat, run_fallback_no_context

router = APIRouter(prefix="/api", tags=["chat"])


@router.post("/chat")
async def chat(req: ChatRequest):
    vectorstore = get_vectorstore(req.video_id)

    # Auto-process if this video hasn't been embedded yet
    if len(vectorstore.get()["ids"]) == 0:
        if not process_and_store(req.video_id):
            response_text = run_fallback_no_context(req.message)
            return {"success": True, "response": response_text, "mode": "NO_TRANSCRIPT"}
        vectorstore = get_vectorstore(req.video_id)

    try:
        response_text = run_chat(vectorstore, req.message, req.session_id)
        return {
            "success": True,
            "response": response_text,
            "mode": "RAG_WITH_HISTORY_GROQ",
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
