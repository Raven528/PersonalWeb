from flask import Flask, jsonify, render_template, request, redirect
import os
import json

app = Flask(__name__)

# 图像目录路径
IMAGE_DIR = "static/images"
PROGRESS_FILE = "progress.json"


# 获取图像名称列表
def get_image_names():
    return [
        {"name": f} for f in os.listdir(IMAGE_DIR) if f.endswith(("jpg", "jpeg", "png"))
    ]


# 获取进度
def get_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f)
    return {"index": 0, "judgments": {}}


# 保存进度
def save_progress(progress):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/review")
def review():
    return render_template("review.html")


@app.route("/get_images")
def get_images():
    image_names = get_image_names()
    return jsonify(image_names)


@app.route("/save_progress", methods=["POST"])
def save_user_progress():
    progress_data = request.json
    save_progress(progress_data)
    return jsonify({"status": "success"}), 200


@app.route("/get_progress")
def get_user_progress():
    progress_data = get_progress()
    return jsonify(progress_data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
