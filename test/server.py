from flask import Flask, request, jsonify
from shared import queue, bot_loop
import asyncio

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    if "ref" not in data or "repository" not in data:
        return jsonify({"error": "Payload inválido"}), 400

    if data["ref"] != "refs/heads/main":
        return jsonify({"status": "ignored"}), 200

    repo = data["repository"]["full_name"]
    pusher = data["pusher"]["name"]
    commit = data["head_commit"]["message"]

    message = f"**{pusher}** fez push na **main** de `{repo}`:\n> {commit}"

    # Envia para a fila do bot usando o loop correto
    if bot_loop is not None:
        asyncio.run_coroutine_threadsafe(queue.put(message), bot_loop)
        return jsonify({"status": "ok"})
    else:
        return jsonify({"error": "Bot ainda não iniciado"}), 503

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
