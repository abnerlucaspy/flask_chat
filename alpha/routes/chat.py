from flask import Blueprint, render_template, request
from flask_socketio import emit, join_room, leave_room
from flask_login import login_required, current_user
from extensions import socketio, db
from models import Message, User

bp = Blueprint('chat', __name__)

@bp.route('/', endpoint='chat_home')
@login_required
def index():
    users = User.query.filter(User.id != current_user.id).all()
    return render_template('chat/chat.html',
                         username=current_user.username,
                         users=users)

def init_socketio_handlers():
    @socketio.on('send_message')
    def handle_message(data):
        try:
            message = Message(
                sender_id=current_user.id,
                receiver_id=data['receiver_id'],
                content=data['message']
            )
            db.session.add(message)
            db.session.commit()
            
            emit('receive_message', {
                'username': current_user.username,
                'message': data['message'],
                'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            }, room=str(data['receiver_id']))
            
        except Exception as e:
            db.session.rollback()
            emit('error', {'message': 'Failed to send message'})

    @socketio.on('join')
    def on_join(data):
        room = str(data.get('room'))
        join_room(room)
        emit('status', {
            'message': f'{current_user.username} has joined the chat',
            'username': current_user.username
        }, room=room)

    @socketio.on('leave')
    def on_leave(data):
        room = str(data.get('room'))
        leave_room(room)
        emit('status', {
            'message': f'{current_user.username} has left the chat',
            'username': current_user.username
        }, room=room)
