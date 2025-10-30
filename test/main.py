from flask import Flask, request
import requests

app = Flask(__name__)
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/SEU_WEBHOOK"

@app.route("/gitlab", methods=["POST"])
def gitlab():
    data = request.json
    ref = data.get("ref", "")

    # 🚨 Verifique exatamente se é a branch main
    if ref != "refs/heads/main":
        print(f"Ignorado: push em {ref}")
        return "Ignorado (outra branch)", 200

    user = data.get("user_username") or data.get("pusher", {}).get("name", "Desconhecido")
    project = data.get("project", {}).get("name") or data.get("repository", {}).get("name", "Desconhecido")
    commits = data.get("commits", [])

    msg = f"📦 **{user}** fez push na branch **main** do projeto **{project}**\n"
    for c in commits:
        msg += f"- [{c['id'][:7]}] {c['message']} ({c['url']})\n"

    requests.post(DISCORD_WEBHOOK_URL, json={"content": msg})
    return "ok", 200

if __name__ == "__main__":
    app.run(port=5000)
 