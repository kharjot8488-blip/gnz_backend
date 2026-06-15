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
        return jsonify({
            "status": "error",
            "code": response.status_code,
            "details": response.text
        })
