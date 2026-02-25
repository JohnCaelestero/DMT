#!/usr/bin/env python3
import discord
from discord.ext import commands
import aiohttp
import logging
import os

from embed import Instagram, Pornhub, XV, Tenor, Attachments
from commands import lock, unlock, refresh_server, link

# --------------------
# Config
# --------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, "token.txt")) as f:
    TOKEN = f.read().strip()

with open(os.path.join(BASE_DIR, "serverID.txt")) as f:
    GUILD_ID = int(f.read().strip())

logging.basicConfig(level=logging.INFO)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
GUILD = discord.Object(id=GUILD_ID)

session: aiohttp.ClientSession | None = None

# --------------------
# Media Handlers
# --------------------

HANDLERS = [
    Instagram.handle,
    Attachments.handle,
    Pornhub.handle,
    XV.handle,
    Tenor.handle,
]

async def process_message(message: discord.Message) -> bool:
    if message.author.bot or message.embeds:
        return False

    for handler in HANDLERS:
        if await handler(message, bot, session):
            return True

    return False

# --------------------
# Slash Command Loader
# --------------------

def load_commands():
    lock.setup(bot, GUILD)
    unlock.setup(bot, GUILD)
    refresh_server.setup(bot, GUILD, process_message)
    link.setup(bot, GUILD)

# --------------------
# Events
# --------------------

@bot.event
async def on_ready():
    global session

    if session is None:
        session = aiohttp.ClientSession()

    print("🧹 Resetting application commands...")

    # Clear GLOBAL commands (removes old global ones like /panel)
    bot.tree.clear_commands(guild=None)
    await bot.tree.sync()

    # Clear GUILD commands
    bot.tree.clear_commands(guild=GUILD)
    await bot.tree.sync(guild=GUILD)

    # Load current commands
    load_commands()

    # Sync only guild commands
    synced = await bot.tree.sync(guild=GUILD)

    print(f"✅ Synced {len(synced)} commands.")
    print(f"✅ Logged in as {bot.user}")

@bot.event
async def on_message(message: discord.Message):
    await process_message(message)
    await bot.process_commands(message)

# Proper shutdown handling
async def close_bot():
    global session
    if session:
        await session.close()
    await bot.close()

# --------------------
# Run
# --------------------

try:
    bot.run(TOKEN)
finally:
    if session and not session.closed:
        import asyncio
        asyncio.run(session.close())
