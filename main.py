from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional

from telethon import functions
from telethon.errors import RPCError
from telethon.tl.types import Channel

from .utils import make_client_from_string
from .storage import load_all_sessions, add_session, remove_session, get_session
from .auth import require_api_key

app = FastAPI(title="Telegram Userbot Manager")

API_PREFIX = "/api"

class CreateSupergroupRequest(BaseModel):
    session_name: Optional[str] = None
    string_session: Optional[str] = None
    title: str
    about: Optional[str] = None


class SendMessageRequest(BaseModel):
    session_name: Optional[str] = None
    string_session: Optional[str] = None
    target: str
    message: str


class AddSessionRequest(BaseModel):
    name: str
    string_session: str


@app.get(API_PREFIX + "/sessions", dependencies=[Depends(require_api_key)])
async def list_sessions():
    sessions = load_all_sessions()
    return {"sessions": list(sessions.keys())}


@app.post(API_PREFIX + "/sessions", dependencies=[Depends(require_api_key)])
async def api_add_session(req: AddSessionRequest):
    try:
        add_session(req.name, req.string_session)
        return {"success": True, "name": req.name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete(API_PREFIX + "/sessions/{name}", dependencies=[Depends(require_api_key)])
async def api_remove_session(name: str):
    try:
        remove_session(name)
        return {"success": True, "name": name}
    except KeyError:
        raise HTTPException(status_code=404, detail="Session not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post(API_PREFIX + "/create_supergroup", dependencies=[Depends(require_api_key)])
async def create_supergroup(req: CreateSupergroupRequest):
    if not (req.session_name or req.string_session):
        raise HTTPException(status_code=400, detail="Provide session_name or string_session.")

    if req.session_name and not req.string_session:
        ss = get_session(req.session_name)
        if not ss:
            raise HTTPException(status_code=404, detail="Stored session not found")
        req.string_session = ss

    client = make_client_from_string(req.string_session)

    try:
        await client.connect()
        if not await client.is_user_authorized():
            raise HTTPException(status_code=401, detail="Client not authorized. Generate a StringSession via the helper script.")

        result = await client(functions.channels.CreateChannelRequest(
            title=req.title,
            about=req.about or "",
            megagroup=True
        ))

        created = None
        for chat in result.chats:
            if isinstance(chat, Channel) and getattr(chat, "title", "") == req.title:
                created = chat
                break
        if not created and result.chats:
            created = result.chats[0]

        invite_link = None
        try:
            entity = await client.get_entity(created)
            invite_link = await client.export_chat_invite_link(entity)
        except Exception:
            invite_link = None

        return {
            "success": True,
            "title": getattr(created, "title", None),
            "id": getattr(created, "id", None),
            "username": getattr(created, "username", None),
            "invite_link": invite_link
        }
    except RPCError as e:
        raise HTTPException(status_code=500, detail=f"Telegram RPC error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await client.disconnect()


@app.post(API_PREFIX + "/send_message", dependencies=[Depends(require_api_key)])
async def send_message(req: SendMessageRequest):
    if not (req.session_name or req.string_session):
        raise HTTPException(status_code=400, detail="Provide session_name or string_session.")

    if req.session_name and not req.string_session:
        ss = get_session(req.session_name)
        if not ss:
            raise HTTPException(status_code=404, detail="Stored session not found")
        req.string_session = ss

    client = make_client_from_string(req.string_session)

    try:
        await client.connect()
        if not await client.is_user_authorized():
            raise HTTPException(status_code=401, detail="Client not authorized. Generate a StringSession via the helper script.")

        sent = await client.send_message(req.target, req.message)
        return {"success": True, "message_id": getattr(sent, "id", None)}
    except RPCError as e:
        raise HTTPException(status_code=500, detail=f"Telegram RPC error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await client.disconnect()


# Serve static web UI
from fastapi.staticfiles import StaticFiles
app.mount("/", StaticFiles(directory="web", html=True), name="web")