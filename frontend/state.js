// --- Shared state for the current tab ---
// Plain vanilla-JS, no build step: this file is loaded first (see manifest.json)
// so `State` is available as a global to every script after it.

const State = {
  currentVideoId: new URLSearchParams(window.location.search).get("v"),
  sessionId: null,
};

State.sessionId = generateSessionId();

function generateSessionId() {
  return "session-" + Math.random().toString(36).substring(2, 15);
}

function getCurrentVideoIdFromUrl() {
  return new URLSearchParams(window.location.search).get("v");
}
