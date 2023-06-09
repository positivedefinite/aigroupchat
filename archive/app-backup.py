from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import openai
openai.api_key = "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"
app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def index():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chat with GPT-4</title>
</head>
<body>
    <div id="chat">
    </div>
    <input type="text" id="message" autofocus>
    <button onclick="sendMessage()">Send</button>

    <script>
        const chat = document.getElementById("chat");
        const messageInput = document.getElementById("message");

        async function sendMessage() {
            const content = messageInput.value;
            messageInput.value = "";

            const userMessage = document.createElement("p");
            userMessage.textContent = "User: " + content;
            chat.appendChild(userMessage);

            const response = await fetch("/generate_response", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({content}),
            });
            const data = await response.json();
            const gpt4Message = document.createElement("p");
            gpt4Message.textContent = "AI: " + data.message;
            chat.appendChild(gpt4Message);
        }

        messageInput.addEventListener("keydown", (event) => {
            if (event.key === "Enter") {
                event.preventDefault();
                sendMessage();
            }
        });
    </script>
</body>
</html>
    """
from pydantic import BaseModel
class InputData(BaseModel):
    content: str


@app.post("/generate_response")
async def generate_response_endpoint(input_data: InputData):
    messages = [
            {"role": "system", "content": "ADAM loves ALICE."},
            {"role": "user", "content": input_data.content},
        ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages)
        # Open the history.txt file in append mode
    with open("history.txt", "a") as file:
        # Loop through the messages and write them to the file
        for message in messages:
            file.write(f'{message["content"]}')
    return {"message": response.choices[0].message["content"]}