from flask import Flask, request, jsonify
import asyncio
import bot  # importa o bot.py

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

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

    message = f"**{pusher}** fez push na **main** de `{repo}`:\n> {commit}"

    # Envia pra fila do bot
    asyncio.run_coroutine_threadsafe(bot.queue.put(message), bot.bot.loop)

    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
