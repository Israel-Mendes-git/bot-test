import os
import discord
from discord.ext import commands
import asyncio
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))

# ----------------- Discord -----------------
intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix="!", intents=intents)
queue = asyncio.Queue()
bot_loop = None  # vai ser definido quando o bot iniciar

@bot.event
async def on_ready():
    global bot_loop
    bot_loop = bot.loop
    print(f"Bot conectado como {bot.user}")
    bot.loop.create_task(webhook_listener())

async def webhook_listener():
    await bot.wait_until_ready()
    channel = bot.get_channel(CHANNEL_ID)
    if channel is None:
        print(f"Erro: canal {CHANNEL_ID} não encontrado")
        return
    while True:
        message_data = await queue.get()
        
        embed = discord.Embed(
            title="Novo push na main!",
            color=discord.Color.blurple()

        )
        thumb_arquivo = discord.File('test/imagens/logo_fundo_transparente.png', filename='thumb.png')
        embed.set_thumbnail(url='attachment://thumb.png')

        
        embed.add_field(name="Repositório", value=message_data["repo"], inline=True)
        embed.add_field(name="Autor", value=message_data["pusher"], inline=True)
        embed.add_field(name="Commit", value=message_data["commit"], inline=False)
        
        await channel.send(file=thumb_arquivo, embed=embed)
        queue.task_done()


# ----------------- Flask -----------------
app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    if not data or "ref" not in data or "repository" not in data:
        return jsonify({"error": "Payload inválido"}), 400

    if data["ref"] != "refs/heads/main":
        return jsonify({"status": "ignored"}), 200

    repo = data["repository"]["full_name"]
    pusher = data["pusher"]["name"]
    commit = data["head_commit"]["message"]
    message_dict = {
        "repo": repo,
        "pusher": pusher,
        "commit": commit
    }

    if bot_loop is None:
        return jsonify({"error": "Bot ainda não iniciado"}), 500

    # adiciona a mensagem na fila de forma thread-safe
    asyncio.run_coroutine_threadsafe(queue.put(message_dict), bot_loop)

    return jsonify({"status": "ok"})

# ----------------- Runner -----------------
if __name__ == "__main__":
    from threading import Thread

    # roda Flask em uma thread separada
    def run_flask():
        app.run(host="0.0.0.0", port=5000)

    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()

    # roda o bot no loop principal
    bot.run(TOKEN)
