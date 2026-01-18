const API_URL = "http://localhost:5000";

async function sendMessage() {
    const input = document.getElementById("user-input");
    const message = input.value.trim();
    if(!message) return;

    addMessage(message, "user-msg");
    input.value = "";

    // Determine if it's @learn or @improve
    let endpoint = "/ask";
    let payload = {question: message};

    if(message.startsWith("@learn:")) {
        endpoint = "/learn";
        const data = message.replace("@learn:", "").trim().split("=");
        if(data.length != 2) return alert("Use '@learn: concept = value'");
        payload = {concept: data[0].trim(), value: data[1].trim()};
    }
    else if(message.startsWith("@improve:")) {
        endpoint = "/improve";
        const data = message.replace("@improve:", "").trim().split("->");
        if(data.length != 2) return alert("Use '@improve: pattern -> result'");
        payload = {pattern: data[0].trim(), result: data[1].trim()};
    }

    const res = await fetch(API_URL + endpoint, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(payload)
    });
    const data = await res.json();
    addMessage(data.response || data.msg, "ai-msg");
}

function addMessage(text, type) {
    const chatWindow = document.getElementById("chat-window");
    const msg = document.createElement("div");
    msg.className = "message " + type;
    msg.innerText = text;
    chatWindow.appendChild(msg);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}
