import asyncio
from pyrogram import Client

api_id = "YOUR_API_ID"          # Replace with your Telegram API ID
api_hash = "YOUR_API_HASH"      # Replace with your Telegram API Hash
session_name = "myuserbot"      # Unique name for your session

async def main():
    async with Client(session_name, api_id, api_hash) as app:
        # Create a supergroup (megagroup)
        supergroup = await app.create_supergroup("Supergroup Name", "This is a new supergroup created by userbot.")
        print(f"Supergroup created: {supergroup.id}")

        # Send a message to the supergroup as the user
        await app.send_message(supergroup.id, "Hello, this message is sent as the user!")

if __name__ == "__main__":
    asyncio.run(main())