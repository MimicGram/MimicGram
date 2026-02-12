"""
Session creation & connection test
"""

from telethon import TelegramClient
from telethon.sessions import StringSession
import os

# ================================
# Environment variables required:
# TG_API_ID
# TG_API_HASH
# ================================

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_NAME = os.getenv("SESSION_NAME")

if not API_ID or not API_HASH:
    raise RuntimeError("TG_API_ID and TG_API_HASH must be set as environment variables")


client = TelegramClient(SESSION_NAME, API_ID, API_HASH)


async def start_client():
    """Start Telegram client and verify session."""
    await client.start()
    me = await client.get_me()

    print("Connected successfully")
    print(f"User ID: {me.id}")
    print(f"Username: {me.username}")


if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(start_client())
