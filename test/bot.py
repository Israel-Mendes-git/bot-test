import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Criamos uma fila assíncrona para o servidor avisar o bot
queue = asyncio.Queue()

@bot.event
async def on_ready():
    # Tarefa que fica escutando mensagens do servidor
    bot.loop.create_task(webhook_listener())

async def webhook_listener():
    channel = bot.get_channel(CHANNEL_ID)
    while True:
        message = await queue.get()
        embed = discord.Embed(
            title="📦 Novo evento do GitHub!",
            description=message,
            color=discord.Color.blurple()
        )
        await channel.send(embed=embed)

bot.run(TOKEN)
