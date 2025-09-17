from telethon.sync import TelegramClient
import os
import json

SESSIONS_FILE = "sessions.json"

def save_session(name, api_id, api_hash, phone):
    with TelegramClient(name, api_id, api_hash) as client:
        client.start(phone=phone)
        sessions = {}
        if os.path.exists(SESSIONS_FILE):
            with open(SESSIONS_FILE, "r") as f:
                sessions = json.load(f)
        sessions[name] = {"api_id": api_id, "api_hash": api_hash}
        with open(SESSIONS_FILE, "w") as f:
            json.dump(sessions, f)
        print(f"Session {name} saved.")

def main():
    name = input("Session name: ")
    api_id = int(input("API ID: "))
    api_hash = input("API Hash: ")
    phone = input("Phone number: ")
    save_session(name, api_id, api_hash, phone)

if __name__ == "__main__":
    main()