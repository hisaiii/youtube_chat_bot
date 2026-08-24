// --- API layer ---
// Wraps chrome.runtime.sendMessage in a Promise so callers can use
// async/await instead of nested callbacks. This is the ONLY place
// that knows the backend URL.

const API_BASE_URL = "http://127.0.0.1:8000";

function sendChatMessage(videoId, message, sessionId) {
  return new Promise((resolve, reject) => {
    if (!chrome?.runtime?.sendMessage) {
      reject(new Error("chrome.runtime.sendMessage not available"));
      return;
    }

    chrome.runtime.sendMessage(
      {
        action: "apiCall",
        url: `${API_BASE_URL}/api/chat`,
        body: {
          video_id: videoId,
          message: message,
          session_id: sessionId,
        },
      },
      (response) => {
        if (chrome.runtime.lastError) {
          reject(new Error(chrome.runtime.lastError.message));
          return;
        }

        if (response && response.success && response.data?.success) {
          resolve(response.data.response);
          return;
        }

        const errorMsg =
          response?.error || response?.data?.error || "Backend connection failed.";
        reject(new Error(errorMsg));
      }
    );
  });
}
