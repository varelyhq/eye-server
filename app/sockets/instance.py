import socketio

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins=['http://localhost:3000', 'https://cams.varely.co'], cors_credentials=True)
