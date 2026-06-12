from flask import Flask, request, jsonify
from diffusers import StableDiffusionPipeline
import torch

app = Flask(__name__)

pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16
).to("cuda")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    prompt = data.get("prompt", "cute cartoon")
    image = pipe(prompt).images[0]
    image.save("output.png")
    return jsonify({"status": "ok", "file": "output.png"})
