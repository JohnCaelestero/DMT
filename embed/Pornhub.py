import discord
import io
import re
from bs4 import BeautifulSoup

PH_REGEX = r"https?://(?:www\.)?pornhub\.com/view_video\.php\?viewkey=[\w-]+"
COLOR = discord.Color.orange()
USER_AGENT = "Mozilla/5.0 (EmbedBot/3.1)"
ARCHIVE_CHANNEL_ID = ID

async def fetch_metadata(session, url):
    async with session.get(url, headers={"User-Agent": USER_AGENT}) as res:
        soup = BeautifulSoup(await res.text(), "html.parser")

    title = soup.find("meta", property="og:title")
    image = soup.find("meta", property="og:image")

    return (
        title["content"] if title else "Media",
        image["content"] if image else None
    )

async def archive_thumbnail(bot, session, title, image_url):
    if not image_url:
        return None

    async with session.get(image_url) as res:
        data = await res.read()

    channel = bot.get_channel(ARCHIVE_CHANNEL_ID)
    if not channel:
        return None

    file = discord.File(io.BytesIO(data), filename="thumb.jpg")
    msg = await channel.send(content=title, file=file)
    return msg.attachments[0].url

async def handle(message: discord.Message, bot, session) -> bool:
    links = re.findall(PH_REGEX, message.content)
    if not links:
        return False

    for link in links:
        title, image = await fetch_metadata(session, link)
        image = await archive_thumbnail(bot, session, title, image) or image

        embed = discord.Embed(title=title, url=link, color=COLOR)
        if image:
            embed.set_image(url=image)
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
