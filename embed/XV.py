import discord
import re
from bs4 import BeautifulSoup

XV_REGEX = r"https?://(?:www\.)?xvideos\.com/video\.\w+/\w+"
COLOR = discord.Color.red()
USER_AGENT = "Mozilla/5.0 (EmbedBot/3.1)"

async def handle(message: discord.Message, bot, session) -> bool:
    links = re.findall(XV_REGEX, message.content)
    if not links:
        return False

    for link in links:
        async with session.get(link, headers={"User-Agent": USER_AGENT}) as res:
            soup = BeautifulSoup(await res.text(), "html.parser")

        title = soup.find("meta", property="og:title")
        image = soup.find("meta", property="og:image")

        embed = discord.Embed(
            title=title["content"] if title else "Media",
            url=link,
            color=COLOR
        )
        if image:
            embed.set_image(url=image["content"])

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
