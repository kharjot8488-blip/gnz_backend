cfrom flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import base64
import os

app = Flask(__name__)
CORS(app)

HF_TOKEN = os.getenv("HF_TOKEN")

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

@app.route("/", methods=["GET"])
def home():
    return "Backend running!"

@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.get_json()
        prompt = data.get("prompt")

        if not prompt:
            return jsonify({"status": "error", "details": "Prompt missing"}), 400

        response = requests.post(API_URL, headers=headers, json={"inputs": prompt})

        content_type = response.headers.get("content-type", "")

        # SUCCESS CASE → Only encode if it's an actual image
        if response.status_code == 200 and "image" in content_type:
            image_base64 = base64.b64encode(response.content).decode("utf-8")
            return jsonify({"status": "success", "image": image_base64})

        # ERROR CASE → Return HuggingFace error safely
        return jsonify({
            "status": "error",
            "code": response.status_code,
            "details": response.text
        }), response.status_code

    except Exception as e:
        # FINAL SAFETY NET → Never crash
        return jsonify({
            "status": "error",
            "details": f"Server crashed: {str(e)}"
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
