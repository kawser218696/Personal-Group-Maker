import json
import os
from typing import Dict, Optional
from cryptography.fernet import Fernet, InvalidToken
from dotenv import load_dotenv

load_dotenv()

SESSION_DIR = "sessions"
ENC_FILE = os.path.join(SESSION_DIR, "sessions.json.enc")
FERNET_KEY = os.getenv("SESSION_ENCRYPTION_KEY")

if not FERNET_KEY:
    raise RuntimeError("SESSION_ENCRYPTION_KEY must be set in the environment (.env).")

fernet = Fernet(FERNET_KEY.encode())


def _ensure_dir():
    os.makedirs(SESSION_DIR, exist_ok=True)


def load_all_sessions() -> Dict[str, str]:
    _ensure_dir()
    if not os.path.exists(ENC_FILE):
        return {}
    with open(ENC_FILE, "rb") as f:
        data = f.read()
    try:
        dec = fernet.decrypt(data)
    except InvalidToken:
        raise RuntimeError("Failed to decrypt sessions file. Check SESSION_ENCRYPTION_KEY.")
    try:
        return json.loads(dec.decode())
    except Exception as e:
        raise RuntimeError(f"Failed to parse sessions file: {e}")


def save_all_sessions(sessions: Dict[str, str]):
    _ensure_dir()
    payload = json.dumps(sessions).encode()
    enc = fernet.encrypt(payload)
    tmp = ENC_FILE + ".tmp"
    with open(tmp, "wb") as f:
        f.write(enc)
    os.replace(tmp, ENC_FILE)


def get_session(name: str) -> Optional[str]:
    return load_all_sessions().get(name)


def add_session(name: str, string_session: str):
    sess = load_all_sessions()
    sess[name] = string_session
    save_all_sessions(sess)


def remove_session(name: str):
    sess = load_all_sessions()
    if name in sess:
        del sess[name]
        save_all_sessions(sess)
    else:
        raise KeyError("session not found")