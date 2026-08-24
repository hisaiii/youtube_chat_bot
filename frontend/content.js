// --- Orchestrator ---
// Wires State + DOM + API together. No DOM building, no state definitions,
// no fetch logic lives here — those are in dom.js / state.js / api.js
// (loaded before this file — see manifest.json).

console.log("CONTENT SCRIPT LOADED");

if (!document.getElementById("yt-rag-toggle")) {
  const { toggleBtn, chatContainer } = createInterface();
  wireUpEvents(toggleBtn, chatContainer);
}

// Poll for SPA navigation (YouTube doesn't full-reload between videos)
setInterval(() => {
  const newVideoId = getCurrentVideoIdFromUrl();
  if (newVideoId && newVideoId !== State.currentVideoId) {
    console.log("Video changed! Resetting chat...");
    State.currentVideoId = newVideoId;
    resetChat();
  }
}, 1000);

function wireUpEvents(toggleBtn, chatContainer) {
  toggleBtn.addEventListener("click", () => {
    toggleBtn.style.display = "none";
    chatContainer.style.display = "flex";
    document.getElementById("chat-input")?.focus();
  });

  document.getElementById("close-chat").addEventListener("click", collapseChatWindow);

  const sendBtn = document.getElementById("send-btn");
  const input = document.getElementById("chat-input");

  sendBtn.addEventListener("click", handleSend);
  input.addEventListener("keypress", (e) => {
    if (e.key === "Enter") handleSend();
  });
}

function resetChat() {
  clearMessages("New video detected! I'm ready to help.");
  State.sessionId = generateSessionId();
  collapseChatWindow();
}

async function handleSend() {
  const input = document.getElementById("chat-input");
  const message = input.value.trim();
  if (!message) return;

  addMessage(message, "user");
  input.value = "";

  const loadingId = "loading-" + Date.now();
  addMessage("Thinking...", "bot-loading", loadingId);

  if (!State.currentVideoId) {
    removeMessage(loadingId);
    addMessage("Error: No video found.", "bot-error");
    return;
  }

  try {
    const reply = await sendChatMessage(State.currentVideoId, message, State.sessionId);
    removeMessage(loadingId);
    addMessage(reply, "bot");
  } catch (err) {
    removeMessage(loadingId);
    addMessage("Error: " + err.message, "bot-error");
  }
}
