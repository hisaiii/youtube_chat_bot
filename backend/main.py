from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routers import process, chat

app = FastAPI(title="YouTube RAG (Groq Edition)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(process.router)
app.include_router(chat.router)


@app.get("/")
def root():
    return {"message": "YouTube RAG (Groq Edition) Running 🚀"}


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    # Run this with:  python -m backend.main   (from the repo root)
    # or:              uvicorn backend.main:app --reload   (from the repo root)
    import uvicorn

    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
