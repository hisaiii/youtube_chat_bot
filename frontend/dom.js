// --- DOM / UI layer ---
// No business logic here — just building the widget and rendering messages.
// Depends on nothing else; content.js wires this up to actual behavior.

function createInterface() {
  const toggleBtn = document.createElement("div");
  toggleBtn.id = "yt-rag-toggle";
  toggleBtn.innerHTML = `
    <svg viewBox="0 0 24 24">
      <path d="M12,2A2,2 0 0,1 14,4C14,4.74 13.6,5.39 13,5.73V7H14A7,7 0 0,1 21,14H22A1,1 0 0,1 23,15V18A1,1 0 0,1 22,19H21V20A2,2 0 0,1 19,22H5A2,2 0 0,1 3,20V19H2A1,1 0 0,1 1,18V15A1,1 0 0,1 2,14H3A7,7 0 0,1 10,7H11V5.73C10.4,5.39 10,4.74 10,4A2,2 0 0,1 12,2M7.5,13A2.5,2.5 0 0,0 5,15.5A2.5,2.5 0 0,0 7.5,18A2.5,2.5 0 0,0 10,15.5A2.5,2.5 0 0,0 7.5,13M16.5,13A2.5,2.5 0 0,0 14,15.5A2.5,2.5 0 0,0 16.5,18A2.5,2.5 0 0,0 19,15.5A2.5,2.5 0 0,0 16.5,13Z" />
    </svg>
  `;
  document.body.appendChild(toggleBtn);

  const chatContainer = document.createElement("div");
  chatContainer.id = "yt-rag-chat";
  chatContainer.innerHTML = `
    <div class="chat-header">
      <span>AI Assistant</span>
      <span style="cursor:pointer; font-size:20px;" id="close-chat">✖</span>
    </div>
    <div class="chat-messages" id="chat-messages">
      <div class="message bot">Hello! I'm listening to this video. What do you want to know?</div>
    </div>
    <div class="input-area">
      <input type="text" id="chat-input" placeholder="Ask a question..." autocomplete="off" />
      <button id="send-btn">Send</button>
    </div>
  `;
  document.body.appendChild(chatContainer);

  return { toggleBtn, chatContainer };
}

function addMessage(text, type, id = null) {
  const div = document.createElement("div");
  div.className = `message ${type}`;
  div.innerText = text;
  if (id) div.id = id;

  const container = document.getElementById("chat-messages");
  if (container) {
    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
  }
}

function removeMessage(id) {
  const el = document.getElementById(id);
  if (el) el.remove();
}

function clearMessages(placeholderText) {
  const container = document.getElementById("chat-messages");
  if (container) {
    container.innerHTML = `<div class="message bot">${placeholderText}</div>`;
  }
}

function collapseChatWindow() {
  const chatContainer = document.getElementById("yt-rag-chat");
  const toggleBtn = document.getElementById("yt-rag-toggle");
  if (chatContainer && toggleBtn) {
    chatContainer.style.display = "none";
    toggleBtn.style.display = "flex";
  }
}
