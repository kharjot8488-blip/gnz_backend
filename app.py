from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import base64
import os

app = Flask(__name__)
CORS(app)

HF_TOKEN = os.getenv("HF_TOKEN")

@app.route("/", methods=["GET"])
def home():
    return "Backend running!"

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    prompt = data.get("prompt", "")

    response = requests.post(
        "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0?wait_for_model=true",
        headers={
            "Authorization": f"Bearer {HF_TOKEN}",
            "Accept": "image/png"
        },
        json={"inputs": prompt},
    )

    if response.status_code == 200:
        img_base64 = base64.b64encode(response.content).decode("utf-8")
        return jsonify({"status": "ok", "image": img_base64})
    else:
        return jsonify({"status": "error", "details": response.text})
