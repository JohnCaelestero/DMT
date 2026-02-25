import discord
from discord import app_commands, Interaction
from discord.ext import commands

def setup(bot: commands.Bot, guild):
    @app_commands.command(
        name="link",
        description="Post a URL and let Discord embed it normally."
    )
    async def link(interaction: Interaction, url: str):
        await interaction.response.send_message(url)

    bot.tree.add_command(link, guild=guild)
