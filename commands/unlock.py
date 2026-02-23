import asyncio
from discord import app_commands, Interaction, TextChannel
from discord.ext import commands

def setup(bot: commands.Bot, guild):
    @bot.tree.command(
        name="unlock",
        description="Disable age-restricted (NSFW) mode for a channel.",
        guild=guild
    )
    @app_commands.checks.has_permissions(manage_channels=True)
    async def unlock(interaction: Interaction, channel: TextChannel):
        await channel.edit(nsfw=False)
        await interaction.response.send_message(
            f"✅ {channel.mention} is no longer age-restricted (NSFW disabled).",
            ephemeral=True
        )
        await asyncio.sleep(5)
        try:
            await interaction.delete_original_response()
        except Exception:
            pass
