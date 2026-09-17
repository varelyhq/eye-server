from . import service
from .instance import sio
from .state import sessions

@sio.event
async def message(sid, content: str):
    user_session = sessions.get(sid)
    room = user_session.get('room')
    user_id = user_session.get('user_id')
    # username = user_session.get('username')
    msg = await service.send_message(room, user_id, content)
    await sio.emit('message', msg, room=room)#, skip_sid=sid)
    # return msg

@sio.event
async def messages(sid, cam_id: int):
    messages = await service.get_messages(cam_id)
    return messages
