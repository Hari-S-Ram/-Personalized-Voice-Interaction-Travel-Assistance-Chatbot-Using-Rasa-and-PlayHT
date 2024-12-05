document.addEventListener("DOMContentLoaded", () => {
    const sendBtn = document.getElementById("send-btn");
    const userInput = document.getElementById("user-input");
    const chatOutput = document.getElementById("chat-output");
    const micBtn = document.getElementById("mic-btn");
    const responseMode = document.getElementById("response-mode");

    sendBtn.addEventListener("click", async () => {
        const message = userInput.value.trim();
        if (message) {
            addMessageToChat("User", message);
            userInput.value = "";
            const response = await fetchResponse(message);
            handleBotResponse(response);
        }
    });

    micBtn.addEventListener("click", () => {
        startVoiceRecognition();
    });

    async function fetchResponse(message) {
        const demoCommands = {
            "hello": "Hello! How can I assist you today?",
            "what is the weather": "The weather is sunny with a high of 75°F.",
            "recommend a place to visit": "I recommend visiting the Grand Canyon for a breathtaking view.",
        };
        return demoCommands[message.toLowerCase()] || "Sorry, I didn’t catch that. Please try again.";
    }

    function addMessageToChat(sender, message) {
        const messageElem = document.createElement("div");
        messageElem.classList.add("message", sender === "User" ? "user-message" : "bot-message");
        messageElem.textContent = message;
        chatOutput.appendChild(messageElem);
        chatOutput.scrollTop = chatOutput.scrollHeight;
    }

    function handleBotResponse(response) {
        addMessageToChat("Bot", response);
        if (responseMode.value === "voice") {
            speakResponse(response);
        }
    }

    function startVoiceRecognition() {
        const greetingMessage = "Hello, please tell me how I can assist you.";
        addMessageToChat("Bot", greetingMessage);

        const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = "en-US";

        recognition.onstart = () => console.log("Voice recognition started.");
        recognition.onresult = async (event) => {
            const voiceText = event.results[0][0].transcript;
            addMessageToChat("User", voiceText);

            const response = await fetchResponse(voiceText);
            handleBotResponse(response);
        };

        recognition.onerror = () => addMessageToChat("Bot", "Sorry, I didn't catch that.");
        recognition.start();
    }

    function speakResponse(response) {
        const utterance = new SpeechSynthesisUtterance(response);
        utterance.lang = "en-US";
        speechSynthesis.speak(utterance);
    }
});
