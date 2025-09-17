from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from telethon import TelegramClient
from telethon.tl.functions.channels import CreateChannelRequest
from telethon.tl.functions.messages import SendMessageRequest
import asyncio
from config import BOT_TOKEN, API_ID, API_HASH
from database import AccountManager

# Initialize
app = Client("group_creator_bot", bot_token=BOT_TOKEN)
account_manager = AccountManager()

@app.on_message(filters.command(["start"]))
async def start(client, message: Message):
    await message.reply_text(
        "🤖 **Supergroup Creator Bot**\n\n"
        "I can create Telegram supergroups on your behalf!\n\n"
        "**Commands:**\n"
        "/addaccount - Add your Telegram account\n"
        "/creategroup <name> - Create a new supergroup\n"
        "/listaccounts - List your connected accounts",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Add Account", callback_data="add_account")]
        ])
    )

@app.on_message(filters.command(["addaccount"]))
async def add_account(client, message: Message):
    # This would typically involve a more complex setup to generate
    # session strings for user accounts
    await message.reply_text(
        "To add your account, please visit our web dashboard or "
        "send your API credentials securely."
    )

@app.on_message(filters.command(["creategroup"]))
async def create_group(client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("Please provide a group name. Usage: /creategroup GroupName")
        return
    
    group_name = " ".join(message.command[1:])
    user_id = message.from_user.id
    account_data = account_manager.get_account(user_id)
    
    if not account_data:
        await message.reply_text("No account linked. Use /addaccount first.")
        return
    
    try:
        # Create group using user's account via Telethon
        user_client = TelegramClient(
            session=account_data["session_string"],
            api_id=account_data["api_id"],
            api_hash=account_data["api_hash"]
        )
        
        await user_client.start()
        
        # Create the supergroup
        result = await user_client(CreateChannelRequest(
            title=group_name,
            about="Group created via bot",
            megagroup=True
        ))
        
        group_id = result.chats[0].id
        group_link = f"https://t.me/c/{group_id}/1"
        
        await message.reply_text(f"✅ Supergroup created successfully!\n\n🔗 Link: {group_link}")
        
        await user_client.disconnect()
        
    except Exception as e:
        await message.reply_text(f"❌ Error creating group: {str(e)}")

if __name__ == "__main__":
    print("Bot started...")
    app.run()