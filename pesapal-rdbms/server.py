# app.py
from flask import Flask, request, jsonify
from repl.shell import MiniDBShell

app = Flask(__name__)
shell = MiniDBShell()

@app.route("/query", methods=["POST"])
def run_query():
    data = request.get_json()

    if not data or "command" not in data:
        return jsonify({"error": "Missing SQL command"}), 400

    command = data["command"]

    try:
        result = shell.execute(command)
        return jsonify({
            "command": command,
            "result": result
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "MiniDB running"})

if __name__ == "__main__":
    app.run(port=2500, debug=True)