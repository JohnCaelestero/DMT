#!/usr/bin/env python3
import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
import asyncio
import logging
import os

from embed import Instagram, Pornhub, XV, Tenor, Attachments
from commands import refresh_server  # import command file

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, "token.txt")) as f:
    TOKEN = f.read().strip()

with open(os.path.join(BASE_DIR, "serverID.txt")) as f:
    GUILD_ID = int(f.read().strip())

logging.basicConfig(level=logging.INFO)

intents = discord.Intents.default()
intents.message_content = True

# Prefix does NOT affect slash commands
bot = commands.Bot(command_prefix="!", intents=intents)

# Define guild object for guild-specific commands
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
# LOCK / UNLOCK COMMANDS (guild-specific)
# --------------------

@bot.tree.command(
    name="lock",
    description="Enable age-restricted (NSFW) mode for a channel.",
    guild=GUILD
)
@app_commands.checks.has_permissions(manage_channels=True)
async def lock(interaction: discord.Interaction, channel: discord.TextChannel):
    await channel.edit(nsfw=True)
    await interaction.response.send_message(
        f"🔞 {channel.mention} is now age-restricted (NSFW enabled)."
    )


@bot.tree.command(
    name="unlock",
    description="Disable age-restricted (NSFW) mode for a channel.",
    guild=GUILD
)
@app_commands.checks.has_permissions(manage_channels=True)
async def unlock(interaction: discord.Interaction, channel: discord.TextChannel):
    await channel.edit(nsfw=False)
    await interaction.response.send_message(
        f"✅ {channel.mention} is no longer age-restricted (NSFW disabled)."
    )


# Function to load commands from the commands folder
def load_commands():
    refresh_server.setup(bot, GUILD_ID, process_message)


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