from telethon import TelegramClient
from telethon.sessions import StringSession
import asyncio
from config import API_ID, API_HASH

async def generate_session_string():
    client = TelegramClient(StringSession(), API_ID, API_HASH)
    await client.start()
    print("Session string:", client.session.save())
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(generate_session_string())