from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return "Backend running!"

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    prompt = data.get("prompt", "")
    return jsonify({"status": "ok", "prompt": prompt})
