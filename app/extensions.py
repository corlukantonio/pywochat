from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

db: SQLAlchemy = SQLAlchemy()
socketio: SocketIO = SocketIO()
