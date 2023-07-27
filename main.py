import eventlet
import socketio

sio = socketio.Server()
app = socketio.WSGIApp(sio)

filetree = [

    {"type": "folder", "path": "/"},
    {"type": "file", "path": "/run.py", "content": "hello_world()"},

    {"type": "folder", "path": "/data"},
    {"type": "file", "path": "/data/one.json", "content": "{}"},
    {"type": "file", "path": "/data/two.json", "content": "{}"},

    {"type": "folder", "path": "/src"},
    {"type": "file", "path": "/src/app.py",  "content": "app.run()"},

]


@sio.event
def connect(sid, data):
    sio.emit('message', to=sid, data={"content": "welcome", "sid": sid})

@sio.on("message")
def broadcast_message(sid, data):
    message = data.get("message")
    sio.emit('message', data={"message": message, "sid": sid})

@sio.on("filetree")
def broadcast_filetree(sid, data):
    sio.emit('message', to=sid, data={"filetree": filetree})


@sio.event
def disconnect(sid):
    print(sid, "disconnected")



eventlet.wsgi.server(
    eventlet.listen(('', 5000)), app
)
