from flask import Flask, request, jsonify
import requests
import base64
import os

app = Flask(__name__)

HF_TOKEN = os.getenv("HF_TOKEN")

API_URL = "API_URL = "API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

@app.route("/", methods=["GET"])
def home():
    return "Backend running!"

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    prompt = data.get("prompt")

    if not prompt:
        return jsonify({"status": "error", "details": "Prompt missing"}), 400

    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})

    if response.status_code == 200:
        image_base64 = base64.b64encode(response.content).decode("utf-8")
        return jsonify({"status": "success", "image": image_base64})
    else:
        return jsonify({
            "status": "error",
            "code": response.status_code,
            "details": response.text
        }), response.status_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
