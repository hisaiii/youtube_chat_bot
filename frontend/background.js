// Service worker: relays fetch requests from the content script.
// Content scripts can't always hit localhost directly depending on CORS/
// extension context, so this proxies the call and returns the result.

console.log("BACKGROUND SCRIPT LOADED");

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "apiCall") {
    fetch(request.url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(request.body),
    })
      .then((response) => response.json())
      .then((data) => sendResponse({ success: true, data: data }))
      .catch((error) => sendResponse({ success: false, error: error.message }));

    return true; // keep the message channel open for the async response
  }
});
