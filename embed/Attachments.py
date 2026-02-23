import discord

def attachment_type(att: discord.Attachment):
    name = att.filename.lower()
    if name.endswith(".gif"):
        return "GIF"
    if name.endswith((".png", ".jpg", ".jpeg", ".webp")):
        return "IMAGE"
    if name.endswith((".mp4", ".webm", ".mov")):
        return "VIDEO"
    return None

COLORS = {
    "GIF": discord.Color.purple(),
    "IMAGE": discord.Color.blue(),
    "VIDEO": discord.Color.green(),
}

async def handle(message: discord.Message, bot, session) -> bool:
    embedded = False

    for att in message.attachments:
        media = attachment_type(att)
        if not media:
            continue

        file = await att.to_file()
        embed = discord.Embed(
            title=message.content or att.filename,
            color=COLORS[media]
        )
        embed.set_author(
            name=message.author.display_name,
            icon_url=message.author.display_avatar.url
        )

        if media != "VIDEO":
            embed.set_image(url=f"attachment://{file.filename}")

        await message.channel.send(embed=embed, file=file)
        embedded = True

    if embedded:
        try:
            await message.delete()
        except discord.Forbidden:
            pass

    return embedded
