from .instance import sio
from .usernames import generate_username
from .state import sessions, live_count, used_usernames

from ..auth.dependencies import socket_extract_user_id

@sio.event
async def connect(sid, environ):
    user_id = socket_extract_user_id(environ)
    if not user_id: return False
    sessions[sid] = {
        'user_id': user_id,
        'room': None,
        'username': generate_username()
    }

@sio.event
async def disconnect(sid):
    session = sessions.pop(sid)
    cam_id = session.get('room')
    used_usernames.discard(session['username'])
    if cam_id and live_count.get(cam_id):
        live_count[cam_id] -= 1
        if live_count[cam_id] <= 0: del live_count[cam_id]
        else: await sio.emit('live_count', live_count.get(cam_id), room=cam_id)
    print('rozłączono:', sid, session['username'])
