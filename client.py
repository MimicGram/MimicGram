"""
MimicGram - Telegram client setup (Railway Ready)
"""

from telethon import TelegramClient
from telethon.sessions import StringSession
import os

API_ID = int(os.getenv("TG_API_ID"))
API_HASH = os.getenv("TG_API_HASH")
STRING_SESSION = os.getenv("TG_STRING_SESSION")

if not API_ID or not API_HASH:
    raise RuntimeError("TG_API_ID and TG_API_HASH must be set")

if not STRING_SESSION:
    raise RuntimeError("TG_STRING_SESSION must be set")

client = TelegramClient(
    StringSession(STRING_SESSION),
    API_ID,
    API_HASH
)
