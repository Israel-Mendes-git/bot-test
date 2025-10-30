from flask import Flask, request
import requests

app = Flask(__name__)
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/https://discordapp.com/api/webhooks/1433515003008520262/-g830izOhelP34q4zZG2O5zKt2_mEeZejYhVpuoAFjq4zWsKspjqyjOpwx8KG2MpQb0C"

@app.route("/github", methods=["POST"])
def github():
    data = request.json
    ref = data.get("ref", "")

    # Filtra branch main
    if ref != "refs/heads/main":
        return "Ignorado (outra branch)", 200

    repo = data.get("repository", {}).get("full_name", "Desconhecido")
    pusher = data.get("pusher", {}).get("name", "Alguém")
    commits = data.get("commits", [])

    msg = f"📦 **{pusher}** fez push em **{repo}** (branch main)\n"
    for c in commits:
        msg += f"- [{c['id'][:7]}] {c['message']} ({c['url']})\n"

    requests.post(DISCORD_WEBHOOK_URL, json={"content": msg})
    return "ok", 200

if __name__ == "__main__":
    app.run(port=5000)
