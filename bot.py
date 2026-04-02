async def check_live():
    await client.wait_until_ready()
    global already_notified
    channel = client.get_channel(CHANNEL_ID)
    print(f"Discord channel found: {channel}")
    while not client.is_closed():
        live = is_live()
        print(f"Is live: {live} | Already notified: {already_notified}")
        if live and not already_notified:
            await channel.send("🔴 We're live on YouTube! Go watch: https://www.youtube.com/@keylkrne")
            already_notified = True
        elif not live:
            if already_notified:
                print("Stream ended, cooling down...")
                already_notified = False
                await asyncio.sleep(300)
            else:
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

threading.Thread(target=run_server, daemon=True).start()
client.run(DISCORD_TOKEN)

threading.Thread(target=run_server, daemon=True).start()
client.run(DISCORD_TOKEN)
