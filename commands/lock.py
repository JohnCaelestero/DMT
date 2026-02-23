import asyncio
from discord import app_commands, Interaction, TextChannel
from discord.ext import commands

def setup(bot: commands.Bot, guild):
    @bot.tree.command(
        name="lock",
        description="Enable age-restricted (NSFW) mode for a channel.",
        guild=guild
    )
    @app_commands.checks.has_permissions(manage_channels=True)
    async def lock(interaction: Interaction, channel: TextChannel):
        await channel.edit(nsfw=True)
        await interaction.response.send_message(
            f"🔞 {channel.mention} is now age-restricted (NSFW enabled).",
            ephemeral=True
        )
        await asyncio.sleep(5)
        try:
            await interaction.delete_original_response()
        except Exception:
            pass
