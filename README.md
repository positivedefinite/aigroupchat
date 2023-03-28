# aigroupchat
Create a web application with the following requirements:
1. It uses a CSS template that makes it look pretty
2. Any number of users can chat in one common chat with AI
3. After ANY user input, the AI answers
4. Everybody sees all the messages and message history (stored in a local file)

Use Python with FastAPI and uvicorn.

Use OpenAI API like this:
import openai
response = openai.ChatCompletion.create(
  model="gpt-4",
  messages=[
        {"role": "system", "content": ""},
        {"role": "user", "content": "Please don't stop the music"},
    ]
)

print(response)
