import discord
from discord.ext import commands, tasks
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

queue = asyncio.Queue()

class MyBot(commands.Bot):
    async def setup_hook(self):
        # Aqui você já tem acesso ao loop assíncrono
        self.loop.create_task(webhook_listener())

async def webhook_listener():
    await bot.wait_until_ready()
    channel = bot.get_channel(CHANNEL_ID)
    while True:
        message = await queue.get()
        await channel.send(message)
        queue.task_done()

bot = MyBot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

bot.run(TOKEN)
