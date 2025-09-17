```markdown
# Telegram Userbot Manager

A small repository that provides an HTTP API and simple web/CLI tools to manage multiple Telegram *user* sessions (userbots) so you can:

- Create a Telegram supergroup (megagroup) using any of your user accounts.
- Send messages as those user accounts (i.e. messages come from the user, not a bot account).
- Manage multiple sessions with persistent encrypted storage.
- Protect the HTTP API with an API key.
- Use a minimal web UI or CLI to manage sessions and bulk-create groups.

Security notes
- This uses Telegram user sessions (not bot tokens). Actions run as real user accounts. Abuse can get accounts restricted or banned.
- Keep your TELEGRAM_API_ID, TELEGRAM_API_HASH, StringSessions and SESSION_ENCRYPTION_KEY secret.
- The HTTP API is protected by an API key (API_KEY) — set a strong random value.

Quickstart
1. Install requirements:
   pip install -r requirements.txt

2. Generate secrets:
   - TELEGRAM_API_ID and TELEGRAM_API_HASH from https://my.telegram.org
   - API_KEY: a strong random string for protecting the HTTP API.
   - SESSION_ENCRYPTION_KEY: a Fernet key:
     python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

3. Copy .env.example -> .env and fill values.

4. Create StringSessions (local safe machine):
   python scripts/generate_string_session.py

5. Start server:
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

6. Open the web UI at http://localhost:8000/ and provide the API key (stored in localStorage). Or use CLI:
   python scripts/cli.py --api-key <API_KEY> list-sessions

Notes
- Losing SESSION_ENCRYPTION_KEY will make stored sessions irrecoverable.
- The web UI stores the API key in localStorage for convenience; do not use it on untrusted machines.
```