import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv
from shared import queue, bot_loop  # import da fila e loop global

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    global bot_loop
    bot_loop = bot.loop  # define o loop globalmente para o Flask
    print(f"Bot conectado como {bot.user}")
    bot.loop.create_task(webhook_listener())

async def webhook_listener():
    await bot.wait_until_ready()
    channel = bot.get_channel(CHANNEL_ID)
    if channel is None:
        print(f"Erro: Não consegui encontrar o canal {CHANNEL_ID}")
        return
    while True:
        message = await queue.get()
        await channel.send(message)
        queue.task_done()

# ✅ só roda o bot após tudo estar definido
bot.run(TOKEN)
