from yt_dlp import YoutubeDL
from libs import BaseCommand, MessageClass


class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "ytsearch",
                "category": "media",
                "aliases": ["yts", "ysearch"],
                "description": {
                    "content": "Search YouTube and get top 20 results.",
                    "usage": "<search>",
                },
                "exp": 2,
            },
        )

    def exec(self, M: MessageClass, contex):
        query = contex.text.strip()
        if not query:
            return self.client.reply_message(
                "🔍 Please provide a *search query*.", M
            )

        try:
            with YoutubeDL(
                {
                    "quiet": True,
                    "skip_download": True,
                    "extract_flat": "in_playlist",
                    "forcejson": True,
                }
            ) as ytdl:
                results = ytdl.extract_info(
                    f"ytsearch20:{query}", download=False
                )["entries"]

            if not results:
                return self.client.reply_message("❌ No results found.", M)

            output = "🎬 *Top YouTube Results:*\n\n"
            for idx, video in enumerate(results, start=1):
                duration = self.client.utils.format_duration(
                    video.get("duration", 0)
                )
                filesize = self.client.utils.format_filesize(
                    video.get("filesize", 0)
                )
                output += (
                    f"{idx}. 🎵 *{video.get('title', 'N/A')}*\n"
                    f"    ⏱️ *Duration:* {duration}\n"
                    f"    👤 *Uploader:* {video.get('uploader', 'Unknown')}\n"
                    f"    🔗 {video.get('url')}\n\n"
                )

            self.client.reply_message(output.strip(), M)

        except Exception as e:
            self.client.reply_message(
                "⚠️ Something went wrong while fetching the YouTube data.", M
            )
            self.client.log.error(f"[YTSearchError] {e}")
