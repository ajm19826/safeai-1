from flask import Flask, request, jsonify
from safeai import memory, rules, reasoner
import os

app = Flask(__name__)

# Ensure logs exist
LOG_FILE = "logs.txt"
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("SafeAI-1 Logs\n\n")

def log_thoughts(thoughts):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        for t in thoughts:
            f.write("[THOUGHT] " + t + "\n")
        f.write("\n")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question", "")
    thoughts = []
    response, success = reasoner.think(question, thoughts)
    log_thoughts(thoughts)
    return jsonify({"response": response, "success": success})

@app.route("/learn", methods=["POST"])
def learn():
    data = request.json
    concept = data.get("concept")
    value = data.get("value")
    if concept and value:
        memory.add_concept(concept, value)
        memory.link(concept, value)
        return jsonify({"status": "success", "msg": f"{concept} = {value} learned"})
    return jsonify({"status": "error", "msg": "Missing concept or value"})

@app.route("/improve", methods=["POST"])
def improve():
    data = request.json
    pattern = data.get("pattern")
    result = data.get("result")
    if pattern and result:
        rules.add_rule(pattern, result)
        return jsonify({"status": "success", "msg": f"Rule improved: {pattern} -> {result}"})
    return jsonify({"status": "error", "msg": "Missing pattern or result"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
