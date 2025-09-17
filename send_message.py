from telethon.sync import TelegramClient
import json
import argparse

SESSIONS_FILE = "sessions.json"

def load_session(name):
    with open(SESSIONS_FILE, "r") as f:
        sessions = json.load(f)
    s = sessions[name]
    return name, s["api_id"], s["api_hash"]

def send_message(session_name, group_id, text):
    name, api_id, api_hash = load_session(session_name)
    with TelegramClient(name, api_id, api_hash) as client:
        client.send_message(int(group_id), text)
        print(f"Message sent to group {group_id}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--session", required=True)
    parser.add_argument("--group_id", required=True)
    parser.add_argument("--text", required=True)
    args = parser.parse_args()
    send_message(args.session, args.group_id, args.text)