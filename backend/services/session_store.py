"""In-memory chat history store, keyed by session_id.

NOTE: this resets on server restart and won't work across multiple workers/
instances. If you ever need that, swap ChatMessageHistory for a
RedisChatMessageHistory here — nothing outside this file has to change.
"""
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory

_store: dict[str, BaseChatMessageHistory] = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in _store:
        _store[session_id] = ChatMessageHistory()
    return _store[session_id]
