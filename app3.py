# app.py
import json, os, openai
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder=".")
openai.api_key = os.environ["OPENAI_API_KEY"]
instruction = "Keep your answers short and to the point, while following the instructions and being helpful if they are unclear."

@app.route('/')
def index():
    return send_from_directory('.', 'index3.html')

@app.route('/store_text', methods=['POST'])
def store_text():
    text = request.form.get('text')
    if not text:
        return jsonify({"error": "Text not provided"}), 400

    # Send text to OpenAI API
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": ""},
                {"role": "user", "content": "Hello?"},
            ]
        )
        openai_response = response.choices[0].message.content
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Store text and OpenAI API response in history.json
    with open('history.json', 'a+') as f:
        f.seek(0)
        try:
            history = json.load(f)
        except json.JSONDecodeError:
            history = []

        history.append({"input": text, "response": openai_response})

        f.seek(0)
        f.truncate()
        json.dump(history, f)

    return jsonify({"message": f"Text stored successfully with history {history}"}), 200


if __name__ == '__main__':
    app.run(debug=True)
