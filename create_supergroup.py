from telethon.sync import TelegramClient
import json
import argparse

SESSIONS_FILE = "sessions.json"

def load_session(name):
    with open(SESSIONS_FILE, "r") as f:
        sessions = json.load(f)
    s = sessions[name]
    return name, s["api_id"], s["api_hash"]

def create_supergroup(session_name, group_name):
    name, api_id, api_hash = load_session(session_name)
    with TelegramClient(name, api_id, api_hash) as client:
        result = client(functions.messages.CreateChatRequest(
            users=[],  # Empty users, will prompt for contacts
            title=group_name
        ))
        chat_id = result.chats[0].id
        # Convert to supergroup
        client(functions.messages.MigrateChatRequest(chat_id))
        print(f"Supergroup '{group_name}' created with id {chat_id}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--session", required=True)
    parser.add_argument("--group_name", required=True)
    args = parser.parse_args()
    create_supergroup(args.session, args.group_name)