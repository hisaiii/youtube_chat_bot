"""Builds and runs the RAG chain for a single chat turn."""
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory

from backend.config import LLM
from backend.services.session_store import get_session_history

SYSTEM_PROMPT = """You are a helpful YouTube assistant.
Answer based strictly on the context provided.
If user greets, then you also greet politely.
If the answer is not in the context, say you don't know.

Context:
{context}"""


def _format_docs(docs) -> str:
    return "\n\n".join(doc.page_content for doc in docs)


def build_chain(vectorstore):
    """Build a history-aware RAG chain bound to one video's vectorstore."""
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{question}"),
        ]
    )

    chain = (
        RunnablePassthrough.assign(
            context=lambda x: _format_docs(retriever.invoke(x["question"]))
        )
        | prompt
        | LLM
        | StrOutputParser()
    )

    return RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="question",
        history_messages_key="history",
    )


def run_chat(vectorstore, query: str, session_id: str) -> str:
    """Run one chat turn against a video's vectorstore and return the reply text."""
    chain_with_history = build_chain(vectorstore)
    return chain_with_history.invoke(
        {"question": query},
        config={"configurable": {"session_id": session_id}},
    )


def run_fallback_no_context(query: str) -> str:
    """No transcript available — just hit the raw LLM, no retrieval."""
    return LLM.invoke(query).content
