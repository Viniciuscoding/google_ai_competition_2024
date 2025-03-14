chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "GET_ACTIVE_TAB_URL") {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs.length > 0) {
        console.log("url detected")
        sendResponse({ url: tabs[0].url });
      } else {
        console.log("no url detected")
        sendResponse({ url: null });
      }
    });
    // Return true to indicate the response will be sent asynchronously
    return true;
  }
});
