from flask import Flask, redirect, url_for, render_template
from config import Config
from extensions import db, socketio, login_manager
from routes import auth, chat
from flask_login import current_user
from models import User

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Iniciação Banco de Dados 
    db.init_app(app)
    socketio.init_app(app)
    login_manager.init_app(app)

    # Config msg
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Registro 
    app.register_blueprint(auth.bp, url_prefix='/auth')
    app.register_blueprint(chat.bp, url_prefix='/chat')

    # Root route
    @app.route('/')
    def index():
        if current_user.is_authenticated:
            return redirect(url_for('chat.chat_home'))
        return redirect(url_for('auth.login'))

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500

    # Iniciação do Socket.IO event handlers
    with app.app_context():
        chat.init_socketio_handlers()
        # Criação tabela de Db
        db.create_all()

    return app

# Creação da instancia
app = create_app()

if __name__ == '__main__':
    socketio.run(app, debug=True)
