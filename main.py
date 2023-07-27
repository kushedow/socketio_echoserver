import eventlet
import socketio

sio = socketio.Server()

app = socketio.WSGIApp(sio)


@sio.event
def connect(sid, data):
    sio.emit('message', to=sid, data={"content": "welcome", "sid": sid})

@sio.on("message")
def broadcast_message(sid, data):
    message = data.get("message")
    sio.emit('message', data={"message": message, "sid": sid})

@sio.event
def disconnect(sid):
    print(sid, "disconnected")



eventlet.wsgi.server(
    eventlet.listen(('', 5000)), app
)
