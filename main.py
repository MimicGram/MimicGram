"""
Listen to new channel posts and detect discussion group
"""

import asyncio
import logging
import os
import threading

from telethon import events
from telethon.tl.functions.channels import GetFullChannelRequest
from behavior.decision import DecisionEngine

from client import client
from config.settings import CHANNELS, LOG_TO_FILE, LOG_FILE_PATH
from storage.postgres import init_db
from behavior.humanizer import Humanizer

from http.server import HTTPServer, BaseHTTPRequestHandler
# ---------------- Logging Setup ---------------- #
decision_engine = DecisionEngine()
humanizer = Humanizer()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

if LOG_TO_FILE:
    file_handler = logging.FileHandler(LOG_FILE_PATH)
    file_handler.setLevel(logging.INFO)
    logging.getLogger().addHandler(file_handler)


# ---------------- Event Listener ---------------- #

@client.on(events.NewMessage(chats=CHANNELS))
async def new_post_handler(event):
    if not event.is_channel:
        return

    message = event.message
    channel = await event.get_chat()
    decision = decision_engine.decide(channel.id)
    
    if decision == "ACT":
        if humanizer.allow_action(channel.id):
           logging.info("Humanizer approved action")
        else:
           logging.info("Humanizer blocked action")
        
    logging.info(f"Decision: {decision}")
    logging.info(f"New post detected in: {channel.title}")
    logging.info(f"Message ID: {message.id}")
    logging.info(f"Text preview: {message.text[:100] if message.text else 'No text'}")

    # ---- Detect linked discussion ---- #
    try:
        full_channel = await client(GetFullChannelRequest(channel))
        linked_chat_id = full_channel.full_chat.linked_chat_id

        if linked_chat_id:
            logging.info(f"Discussion group linked: {linked_chat_id}")
        else:
            logging.info("No discussion group linked.")

    except Exception as e:
        logging.error(f"Failed to fetch full channel info: {e}")

    logging.info("-" * 50)

def run_health_server():
    port = int(os.environ.get("PORT", 8080))

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"MimicGram is running")

    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()

threading.Thread(target=run_health_server, daemon=True).start()
# ---------------- Runner ---------------- #

async def main():
    init_db()
    await client.start()
    logging.info("MimicGram is now listening for new posts...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
