import os
from telethon import TelegramClient
from telethon.sessions import StringSession
from dotenv import load_dotenv

load_dotenv()

API_ID = os.getenv("TELEGRAM_API_ID")
API_HASH = os.getenv("TELEGRAM_API_HASH")

if not API_ID or not API_HASH:
    raise RuntimeError("Set TELEGRAM_API_ID and TELEGRAM_API_HASH in environment or .env file.")


def make_client_from_string(string_session: str) -> TelegramClient:
    return TelegramClient(StringSession(string_session), int(API_ID), API_HASH)