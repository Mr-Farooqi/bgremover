from flask import Flask, request, send_file, render_template
import requests
import os
from dotenv import load_dotenv
import io

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("REMOVE_BG_API")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/remove-bg", methods=["POST"])
def remove_bg():
    file = request.files["image"]

    response = requests.post(
        "https://api.remove.bg/v1.0/removebg",
        files={"image_file": file},
        data={"size": "auto"},
        headers={"X-Api-Key": API_KEY},
    )

    if response.status_code == 200:
        return send_file(
            io.BytesIO(response.content),
            mimetype="image/png",
            as_attachment=True,
            download_name="no-bg.png"
        )
    else:
        return "Error removing background", 400

if __name__ == "__main__":
    app.run(debug=True)
