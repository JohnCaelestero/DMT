# Discord Media Tool

A lightweight Discord bot that automatically converts user-uploaded media and supported links into clean, consistent embeds.

This project is **content-agnostic**: it does not host, store, or generate media. All embeds are created from **user-provided content** inside Discord servers.

---

## ✨ Features

* Automatically embeds:

  * Images (`png`, `jpg`, `jpeg`, `webp`)
  * GIFs (`gif`)
  * Videos (`mp4`, `webm`, `mov`)
* Supports multiple attachments in a single message
* Uses the **message text as the embed title** (if provided)
* If no text is provided, the embed shows **only the media** (no filename)
* Preserves the original uploader’s name and avatar in embeds
* Optional metadata embedding for supported links
* Server-wide refresh command to retroactively embed older messages

---



## ⚠️ Disclaimer

This software is provided **as-is**, without warranty of any kind.
The author is not responsible for how this bot is deployed or used.
