import os
import jwt
from typing import Annotated
from starlette.requests import Request
from fastapi import Cookie, HTTPException, Depends #, Request

JWT_SECRET = os.getenv('JWT_SECRET')
COOKIE_NAME = 'session_token'

def decode_session_token(token: str) -> str | None:
    if not token: return None
    try: return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except jwt.ExpiredSignatureError: return None
    except jwt.InvalidTokenError as e: return None

def get_current_user_id(session_token: Annotated[str | None, Cookie()] = None) -> str:
    if session_token is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    payload = decode_session_token(session_token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid session")
    return payload["user_id"]

CurrentUserId = Annotated[str, Depends(get_current_user_id)]

def socket_extract_user_id(environ: dict) -> str | None:
    request = Request(environ["asgi.scope"])
    token = request.cookies.get(COOKIE_NAME)
    if not token: return None
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload.get("user_id")
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError as e:
        return None
