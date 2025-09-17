#!/usr/bin/env python3
"""
Helper to generate a Telethon StringSession locally.
This script must be run on a machine where you can receive the Telegram login code/2FA.
"""
import os
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
from dotenv import load_dotenv

load_dotenv()

API_ID = os.getenv("TELEGRAM_API_ID")
API_HASH = os.getenv("TELEGRAM_API_HASH")

if not API_ID or not API_HASH:
    print("Set TELEGRAM_API_ID and TELEGRAM_API_HASH in environment or .env file.")
    raise SystemExit(1)

async def main():
    async with TelegramClient(StringSession(), int(API_ID), API_HASH) as client:
        print("Sign in with your phone number or bot token now...")
        if not await client.is_user_authorized():
            await client.start()
        print("StringSession:")
        print(StringSession.save(client.session))

if __name__ == "__main__":
    asyncio.run(main())