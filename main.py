"""
Listen to new channel posts and detect discussion group
"""

import asyncio
import logging

from telethon import events
from telethon.tl.functions.channels import GetFullChannelRequest

from client import client
from config.settings import CHANNELS, LOG_TO_FILE, LOG_FILE_PATH


# ---------------- Logging Setup ---------------- #

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


# ---------------- Runner ---------------- #

async def main():
    await client.start()
    logging.info("MimicGram is now listening for new posts...")
    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
