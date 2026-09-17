from .instance import sio
from .state import sessions, live_count

@sio.event
async def join_room(sid, cam_id: str):
    print(sid, 'joined room', cam_id)

    prev_cam_id = sessions.get(sid).get('room')
    if prev_cam_id == cam_id:
        return

    if prev_cam_id:
        await sio.leave_room(sid, prev_cam_id)
        live_count[prev_cam_id] -= 1
        if live_count[prev_cam_id] <= 0: del live_count[prev_cam_id]
        else: await sio.emit('live_count', live_count.get(prev_cam_id), room=prev_cam_id)

    await sio.enter_room(sid, cam_id)
    sessions[sid]['room'] = cam_id
    live_count[cam_id] = live_count.get(cam_id, 0) + 1

    await sio.emit('live_count', live_count.get(cam_id), room=cam_id)
