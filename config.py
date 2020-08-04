"""Flask config."""
# from os import environ, path
# from dotenv import load_dotenv
import os
import redis
import secrets
import datetime
# from datetime import datetime, timedelta

# basedir = path.abspath(path.dirname(__file__))
# load_dotenv(path.join(basedir, '.env'))
key = secrets.token_urlsafe(16)

class Config:
    """Base config."""
    SECRET_KEY = os.environ.get('SECRET_KEY', key)
    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.from_url(os.environ.get('REDIS_URL','redis://localhost:6379/0'))
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=1)


class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    


class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    
    