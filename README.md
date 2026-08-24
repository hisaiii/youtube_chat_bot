# YouTube RAG Fullstack Project 🚀

A fullstack application that allows users to **chat with YouTube videos**
using **Retrieval-Augmented Generation (RAG)**.

This project extracts YouTube transcripts, converts them into embeddings,
stores them in a vector database, and enables **context-aware Q&A with memory**
using a large language model — accessible via a Chrome extension right on the
YouTube watch page.

---

## ✨ Features

- 🔍 Chat with any YouTube video
- 🧠 RAG-based Question Answering
- 💬 Session-based conversation memory
- ⚡ FastAPI backend
- 🤖 Groq LLM (`openai/gpt-oss-20b`)
- 📦 ChromaDB for vector storage
- 🧩 Chrome extension frontend (Manifest V3, no build step)
- 🏗️ Modular, layered backend architecture (config → services → routers)

---

## 🏗️ Tech Stack

### Backend
- FastAPI
- LangChain (LCEL chains + `RunnableWithMessageHistory`)
- Groq
- ChromaDB
- YouTube Transcript API
- HuggingFace Embeddings (`all-MiniLM-L6-v2`)

### Frontend
- Vanilla JavaScript Chrome Extension (Manifest V3)

---

## 📂 Project Structure

```
youtube_chat_bot/
├── backend/
│   ├── main.py                   # FastAPI app factory, mounts routers
│   ├── config.py                 # env vars, EMBEDDINGS/LLM singletons
│   ├── requirements.txt
│   ├── .env.example
│   ├── models/
│   │   └── schemas.py            # ProcessRequest, ChatRequest
│   ├── services/
│   │   ├── transcript_service.py     # fetch + flatten YouTube transcript
│   │   ├── vectorstore_service.py    # chunk, embed, store, retrieve (Chroma)
│   │   ├── chat_service.py           # LCEL RAG chain + invoke logic
│   │   └── session_store.py          # in-memory chat history per session_id
│   └── routers/
│       ├── process.py            # POST /api/process
│       └── chat.py               # POST /api/chat
│
├── frontend/
│   ├── manifest.json             # loads state.js → dom.js → api.js → content.js
│   ├── state.js                  # currentVideoId, sessionId
│   ├── dom.js                    # widget UI, message rendering
│   ├── api.js                    # wraps chrome.runtime.sendMessage in a Promise
│   ├── content.js                # orchestrator: wires events, handleSend()
│   ├── background.js             # service worker, relays fetch to backend
│   └── styles.css
│
├── .gitignore
└── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/hisaiii/youtube_chat_bot
cd youtube_chat_bot
```

### 2️⃣ Backend Setup

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # Linux / Mac

pip install -r backend/requirements.txt
```

Create a `.env` file inside `backend/` (copy `backend/.env.example`):
```env
GROQ_API_KEY=your_groq_api_key_here
HF_TOKEN=optional
```

**Run the backend from the repo root** (not from inside `backend/` —
the modules use package-style imports like `backend.config`):
```bash
uvicorn backend.main:app --reload
```

Backend runs at:
```
http://127.0.0.1:8000
```

### 3️⃣ Frontend Setup (Chrome Extension)

1. Open `chrome://extensions`
2. Enable **Developer mode** (top-right toggle)
3. Click **Load unpacked** → select the `frontend/` folder
4. Open any `https://www.youtube.com/watch?v=...` page — the chat bubble
   appears bottom-right

No `npm install` needed — it's plain JS, no build step. If you edit any
frontend file, hit the reload icon on the extension card in
`chrome://extensions`.

---

## 🔌 API Endpoints

### Health Check
```
GET /health
```

### Process YouTube Video
```
POST /api/process
{
  "video_id": "VIDEO_ID"
}
```

### Chat with YouTube Video
```
POST /api/chat
{
  "video_id": "VIDEO_ID",
  "message": "Your question",
  "session_id": "optional-session-id"
}
```

---

## 🧠 How It Works (RAG Pipeline)

1. **Fetch transcript** — `services/transcript_service.py`
2. **Chunk transcript** (1000 chars, 200 overlap) — `services/vectorstore_service.py`
3. **Embed + store in ChromaDB** — `services/vectorstore_service.py`
4. **Retrieve top-k relevant chunks** (k=5) — `services/chat_service.py`
5. **Build LCEL chain** (`retriever | prompt | LLM | StrOutputParser`) and
   wrap with `RunnableWithMessageHistory` for memory — `services/chat_service.py`
6. **Invoke chain** per chat turn, return the answer — `routers/chat.py`

If a video has no transcript available, `/api/chat` falls back to a plain
(non-RAG) LLM response and flags `mode: "NO_TRANSCRIPT"`.

---

## 🚀 Future Improvements

- Timestamp-based answers
- Multi-language support
- Cloud deployment
- CI/CD pipeline (lint + import smoke test on push)

---

## 🔐 Security Notes

- `.env`, `chroma_db/`, and virtual environments are ignored via `.gitignore`
- `backend/.env.example` is provided for reference only

---

## 👨‍💻 Author

**Sai Hiware**
Computer Science Student
Interested in Backend Development, GenAI, and System Design

---

## ⭐ Support

If you find this project useful, consider giving it a ⭐ on GitHub.
