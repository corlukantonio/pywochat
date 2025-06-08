from flask import Flask

from app import create_app
from app.extensions import socketio

app: Flask = create_app(environment='development')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
