from pydantic import BaseModel


class ProcessRequest(BaseModel):
    video_id: str


class ChatRequest(BaseModel):
    video_id: str
    message: str
    session_id: str = "default_session"
