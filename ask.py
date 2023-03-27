import openai
import plac
import json
import os
from datetime import datetime
openai.api_key = "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"
def main():
    while True:
        content = input("User: ")
        if content.lower() in ["exit", "quit"]:
            break

        response = generate_response(content)
        print("GPT-4:", response.choices[0].message["content"])
        save_response_to_json(response)

def generate_response(content):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": ""},
            {"role": "user", "content": content},
        ]
    )
    return response

def save_response_to_json(response):
    timestamp = datetime.now().strftime("%y%m%d%H%M%S")
    filename = f"./data/{timestamp}.json"
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "w") as f:
        json.dump(response.to_dict(), f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    plac.call(main)