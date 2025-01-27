from flask import Flask
from flask_sock import Sock # type: ignore

# TODO: flask best practices on application config?
app = Flask(__name__)
sock = Sock(app)

@app.route("/")
def index():
    return "Hello, world!"

@sock.route("/ws")
def websocket(ws):
    while True:
        print (ws.receive())