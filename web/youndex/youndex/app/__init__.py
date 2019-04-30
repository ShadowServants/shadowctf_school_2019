from flask import Flask
from flask_mongoengine import MongoEngine
from celery import Celery
from redis import Redis

app = Flask(__name__)

app.config.from_pyfile('settings.py')

db = MongoEngine()
db.init_app(app)

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

redis_client = Redis(
    host=app.config['REDIS_HOST'],
    port=app.config['REDIS_PORT'],
    db=app.config['REDIS_DB']
)

from app.views import core

app.register_blueprint(core)
