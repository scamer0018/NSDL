from libs import BaseCommand, MessageClass


class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "iplookup",
                "category": "search",
                "aliases": ["ip", "ipinfo"],
                "description": {
                    "content": "Get information about an IP address.",
                    "usage": "<optional_ip>",
                },
                "exp": 1,
            },
        )

    def exec(self, M: MessageClass, contex):
        ip = contex.text.strip() if contex.text else ""
        url = f"http://ip-api.com/json/{ip}"

        try:
            data = self.client.utils.fetch(url)

            if data.get("status") != "success":
                return self.client.reply_message(
                    f"❌ Couldn't fetch IP info. Invalid or private IP.",
                    M,
                )

            msg = f"""🌐 *IP Lookup Result*
🧠 *Query:* {data.get("query", "N/A")}
🌍 *Country:* {data.get("country", "N/A")} ({data.get("countryCode", "N/A")})
🏙️ *Region:* {data.get("regionName", "N/A")} - {data.get("region", "N/A")}
🏘️ *City:* {data.get("city", "N/A")}
🛰️ *ISP:* {data.get("isp", "N/A")}
📡 *Org:* {data.get("org", "N/A")}
📍 *Lat/Lon:* {data.get("lat", "N/A")}, {data.get("lon", "N/A")}
🕒 *Timezone:* {data.get("timezone", "N/A")}
"""

            self.client.reply_message(msg.strip(), M)

        except Exception as e:
            self.client.reply_message(
                "⚠️ An error occurred while fetching IP info.", M
            )
            self.client.log.error(f"[IPLookupError] {e}")
