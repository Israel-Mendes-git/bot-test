from flask import Flask, request, jsonify
import asyncio
from bot import queue, bot  # só importa a fila, não roda o bot

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
<<<<<<< Updated upstream

    print("Payload recebido do GitHub:", data)

    # Garante que o payload é de push
    if "ref" not in data or "repository" not in data:
        return jsonify({"error": "Payload inválido"}), 400

    # Só aceita push na branch main
    if data["ref"] != "refs/heads/main":
        print(f"Ignorando push em {data['ref']}")
        return jsonify({"status": "ignored"}), 200

    repo = data["repository"]["full_name"]
    pusher = data["pusher"]["name"]
    commit = data["head_commit"]["message"]
=======
    repo = data.get("repository", {}).get("full_name")
    pusher = data.get("pusher", {}).get("name")
    commit = data.get("head_commit", {}).get("message", "Sem mensagem")
>>>>>>> Stashed changes

    message = f"**{pusher}** fez push na **main** de `{repo}`:\n> {commit}"

    asyncio.run_coroutine_threadsafe(queue.put(message), bot.loop)

    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)