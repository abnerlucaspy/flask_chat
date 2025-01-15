import os
from datetime import timedelta

class Config:
    # Config basica Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev'
    
    # SQLAlchemy config
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///chat.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Flask-Login config
    REMEMBER_COOKIE_DURATION = timedelta(days=30)
    SESSION_PROTECTION = 'strong'
