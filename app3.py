# app.py
import json
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder=".")

@app.route('/')
def index():
    return send_from_directory('.', 'index3.html')

@app.route('/store_text', methods=['POST'])
def store_text():
    text = request.form.get('text')
    if not text:
        return jsonify({"error": "Text not provided"}), 400

    with open('history3.json', 'a+') as f:
        f.seek(0)
        try:
            history = json.load(f)
        except json.JSONDecodeError:
            history = []

        history.append(text)

        f.seek(0)
        f.truncate()
        json.dump(history, f)

    return jsonify({"message": "Text stored successfully"}), 200


if __name__ == '__main__':
    app.run(debug=True)
