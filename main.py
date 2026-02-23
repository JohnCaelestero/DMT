#!/usr/bin/env python3
import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
import asyncio
import logging
import os

from embed import Instagram, Pornhub, XV, Tenor, Attachments
from commands import lock, unlock, refresh_server

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
# Load commands from commands folder
# --------------------
def load_commands():
    lock.setup(bot, GUILD)
    unlock.setup(bot, GUILD)


@bot.event
async def on_ready():
    global session
    session = aiohttp.ClientSession()

    load_commands()

    synced = await bot.tree.sync(guild=GUILD)
    print(f"Synced {len(synced)} commands.")
    print(f"✅ Logged in as {bot.user}")


@bot.event
async def on_message(message: discord.Message):
    await process_message(message)
    await bot.process_commands(message)


@bot.event
async def on_close():
    global session
    if session:
        await session.close()


bot.run(TOKEN)
