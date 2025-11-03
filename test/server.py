import discord
from discord.ext import commands, tasks
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))  # converte para int

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Fila assíncrona para receber mensagens do servidor
queue = asyncio.Queue()

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")
    # Inicia a tarefa de escuta
    bot.loop.create_task(webhook_listener())

async def webhook_listener():
    await bot.wait_until_ready()  # garante que o bot está totalmente carregado
    channel = bot.get_channel(CHANNEL_ID)
    if channel is None:
        print(f"Erro: Não consegui encontrar o canal {CHANNEL_ID}")
        return

    while True:
        message = await queue.get()
        embed = discord.Embed(
            title="📦 Novo evento do GitHub!",
            description=message,
            color=discord.Color.blurple()
        )
        await channel.send(embed=embed)
        queue.task_done()  # marca a mensagem como processada

bot.run(TOKEN)
