# app.py
from flask import Flask, request, jsonify
from safeai import memory, rules, reasoner
import os

app = Flask(__name__)

# -----------------------------
# Logging setup
# -----------------------------
LOG_FILE = "logs.txt"
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("SafeAI-1 Logs\n\n")

def log_thoughts(thoughts, question, response):
    """Append AI thoughts and input/output to logs.txt"""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[QUESTION] {question}\n")
        for t in thoughts:
            f.write(f"[THOUGHT] {t}\n")
        f.write(f"[RESPONSE] {response}\n\n")

# -----------------------------
# API Endpoints
# -----------------------------
@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question", "")
    thoughts = []

    # Run AI reasoning
    try:
        response, success = reasoner.think(question, thoughts)
    except Exception as e:
        response = f"Error processing question: {str(e)}"
        success = False

    log_thoughts(thoughts, question, response)
    return jsonify({"response": response, "success": success})


@app.route("/learn", methods=["POST"])
def learn():
    data = request.json
    concept = data.get("concept")
    value = data.get("value")
    if concept and value:
        memory.add_concept(concept, value)
        memory.link(concept, value)
        msg = f"{concept} = {value} learned"
        log_thoughts([f"Learned concept {concept}"], f"@learn: {concept} = {value}", msg)
        return jsonify({"status": "success", "msg": msg})
    return jsonify({"status": "error", "msg": "Missing concept or value"})


@app.route("/improve", methods=["POST"])
def improve():
    data = request.json
    pattern = data.get("pattern")
    result = data.get("result")
    if pattern and result:
        rules.add_rule(pattern, result)
        msg = f"Rule improved: {pattern} -> {result}"
        log_thoughts([f"Improved rule"], f"@improve: {pattern} -> {result}", msg)
        return jsonify({"status": "success", "msg": msg})
    return jsonify({"status": "error", "msg": "Missing pattern or result"})

# -----------------------------
# Run the server
# -----------------------------
if __name__ == "__main__":
    # For Render / free hosting platforms, dynamically get port
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
