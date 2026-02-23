import re
import discord

IG_REGEX = r"https?://(?:www\.)?instagram\.com/\S+"

def instagram_to_kk(url: str) -> str:
    return re.sub(
        r"https?://(?:www\.)?instagram\.com",
        "https://www.kkinstagram.com",
        url
    )

async def handle(message: discord.Message, bot, session) -> bool:
    if message.author.bot:
        return False

    links = re.findall(IG_REGEX, message.content)
    if not links:
        return False

    for link in links:
        await message.channel.send(instagram_to_kk(link))

    try:
        await message.delete()
    except discord.Forbidden:
        pass

    return True
