from fastapi import APIRouter

from backend.models.schemas import ProcessRequest
from backend.services.vectorstore_service import is_processed, process_and_store

router = APIRouter(prefix="/api", tags=["process"])


@router.post("/process")
async def process_video(req: ProcessRequest):
    if is_processed(req.video_id):
        return {"success": True, "cached": True}

    ok = process_and_store(req.video_id)
    if not ok:
        return {"success": False, "error": "NO_TRANSCRIPT"}

    return {"success": True}
