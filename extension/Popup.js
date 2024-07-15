/*
    This script is responsible for the functionality of the Youtube Transcript Summarizer Chrome extension's popup.
    When the "Summarize" button is clicked, it sends a request to the Flask server to fetch the summarized transcript
    of the currently active YouTube video. The maximum length of the summary can be specified.
    The summary is then displayed in the popup.dsf
*/
document.addEventListener('DOMContentLoaded', function () {
    const tablinks = document.querySelectorAll('.tablinks');
    const defaultOpen = document.getElementById('defaultOpen');
    const btn = document.getElementById("summarize");
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const conversationHistory = document.getElementById('conversation-history');

    tablinks.forEach(button => {
        button.addEventListener('click', function (event) {
            openTab(event, this.textContent.trim());
        });
    });

    if (defaultOpen) {
        defaultOpen.click();
    }
    if (btn) {
        btn.addEventListener("click", function () {
            btn.disabled = true;
            btn.innerHTML = "Summarizing...";
            chrome.tabs.query({ currentWindow: true, active: true }, function (tabs) {
                var url = tabs[0].url;
                var maxLength = document.getElementById("max_length").value || 150;
                var xhr = new XMLHttpRequest();
                xhr.open("GET", "http://127.0.0.1:5000/summary?url=" + url + "&max_length=" + maxLength, true);
                console.log("loading function is about to be called")
                xhr.onload = function () {

                    var response = JSON.parse(xhr.responseText);
                    var text = response.description;
                    // var summary = text.description;
                    // var topics = text.topics;
                    // var sentiments = response.sentiments;

                    console.log("Parsed summary:", text);

                    const p = document.getElementById("output");
                    if (p) {
                        console.log("Setting innerHTML of output element");
                        p.innerHTML = text;
                    } else {
                        console.error("Output element not found");
                    }

                    // const topics_div = document.getElementById("topics");

                    // topics_div.innerHTML = "TOPICS: " + topics;

                    // const sentiments_div = document.getElementById("sentiments");

                    // sentiments_div.innerHTML = "SENTIMENTS: " + sentiments;
                    btn.disabled = false;
                    btn.innerHTML = "Summarize";
                }
                xhr.send();
            });
        });
    }
    // New code for chat functionality
    sendButton.addEventListener('click', function () {
        const userMessage = userInput.value.trim();
        if (userMessage !== '') {
            sendMessage(userMessage);
            userInput.value = '';
        }
    });

    function sendMessage(message) {
        // Display user's message in the conversation history
        conversationHistory.innerHTML += `<p><strong>You:</strong> ${message}</p>`;

        // Send user's message to the Flask backend
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "http://127.0.0.1:5000/chat", true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onload = function () {
            if (xhr.status === 200) {
                // var response = JSON.parse(xhr.responseText);
                var response = xhr.responseText;
                // Display the response in the conversation history
                conversationHistory.innerHTML += `<p><strong>Assistant:</strong> ${response}</p>`;
            } else {
                console.log("Error:", xhr.statusText);
            }
        };
        xhr.onerror = function () {
            console.log("Error:", xhr.statusText);
        };
        xhr.send(JSON.stringify({ message: message }));
    }

});

function openTab(evt, tabName) {
        var i, tabcontent, tablinks;
        tabcontent = document.getElementsByClassName("tabcontent");
        for (i = 0; i < tabcontent.length; i++) {
            tabcontent[i].style.display = "none";
        }
        tablinks = document.getElementsByClassName("tablinks");
        for (i = 0; i < tablinks.length; i++) {
            tablinks[i].className = tablinks[i].className.replace(" active", "");
        }
        document.getElementById(tabName).style.display = "block";
        evt.currentTarget.className += " active";
    }

document.getElementById("defaultOpen").click();