import discord
from discord import app_commands
import asyncio

def setup(bot, GUILD_ID, process_message):
    @app_commands.command(
        name="refresh_server",
        description="Scan entire server and embed un-embedded media"
    )
    async def refresh_server(interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        count = 0
        for channel in interaction.guild.text_channels:
            try:
                async for msg in channel.history(limit=None, oldest_first=True):
                    if await process_message(msg):
                        count += 1
                        await asyncio.sleep(0.25)
            except discord.Forbidden:
                continue

        await interaction.followup.send(
            f"✅ Refresh complete. {count} messages embedded.",
            ephemeral=True
        )

    bot.tree.add_command(
        refresh_server,
        guild=discord.Object(id=GUILD_ID)
    )
