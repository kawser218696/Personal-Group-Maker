from fastapi import Header, HTTPException
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise RuntimeError("API_KEY must be set in the environment (.env).")

async def require_api_key(x_api_key: str = Header(None), authorization: str = Header(None)):
    key = None
    if x_api_key:
        key = x_api_key
    elif authorization and authorization.lower().startswith("bearer "):
        key = authorization.split(" ", 1)[1].strip()
    if not key or key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key.")
    return True