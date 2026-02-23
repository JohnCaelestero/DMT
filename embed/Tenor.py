import discord
import re

TENOR_REGEX = r"https?://(?:www\.)?tenor\.com/view/\S+"
COLOR = discord.Color.purple()

async def handle(message: discord.Message, bot, session) -> bool:
    links = re.findall(TENOR_REGEX, message.content)
    if not links:
        return False

    for link in links:
        embed = discord.Embed(url=link, color=COLOR)
        embed.set_author(
            name=message.author.display_name,
            icon_url=message.author.display_avatar.url
        )
        await message.channel.send(embed=embed)

    try:
        await message.delete()
    except discord.Forbidden:
        pass

    return True
