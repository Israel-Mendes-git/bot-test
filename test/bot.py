from shared import queue, bot_loop
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

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
    while True:
        message = await queue.get()
        await channel.send(message)
        queue.task_done()

bot.run(TOKEN)
