from flask import Flask, request, jsonify
import time

app = Flask(__name__)

current_status = {
    "status": "离线",
    "last_update": 0
}

@app.route("/update", methods=["POST"])
def update():
    data = request.json
    current_status["status"] = data.get("status", "未知")
    current_status["last_update"] = time.time()
    return "OK"

@app.route("/status")
def status():
    if time.time() - current_status["last_update"] > 15:
        return jsonify({"status": "离线"})
    return jsonify({"status": current_status["status"]})

if __name__ == "__main__":
    app.run()
