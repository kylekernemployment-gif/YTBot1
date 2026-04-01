import discord
import requests
import asyncio
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

DISCORD_TOKEN = os.environ['DISCORD_TOKEN']
CHANNEL_ID = int(os.environ['CHANNEL_ID'])
YOUTUBE_API_KEY = os.environ['YOUTUBE_API_KEY']
YOUTUBE_CHANNEL_ID = os.environ['YOUTUBE_CHANNEL_ID']

CHECK_INTERVAL = 60

intents = discord.Intents.default()
client = discord.Client(intents=intents)

already_notified = False

def is_live():
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "channelId": YOUTUBE_CHANNEL_ID,
        "type": "video",
        "eventType": "live",
        "key": YOUTUBE_API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    return len(data.get("items", [])) > 0

async def check_live():
    await client.wait_until_ready()
    global already_notified
    channel = client.get_channel(CHANNEL_ID)
    while not client.is_closed():
        live = is_live()
        if live and not already_notified:
            await channel.send("🔴 They're live on YouTube! Go watch: https://www.youtube.com/@keylkrne")
            already_notified = True
        elif not live:
            already_notified = False
        await asyncio.sleep(CHECK_INTERVAL)

@client.event
async def on_ready():
    print(f"Bot is online as {client.user}")
    client.loop.create_task(check_live())

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running")
    def log_message(self, format, *args):
        pass

def run_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()

threading.Thread(target=run_server​​​​​​​​​​​​​​​​
