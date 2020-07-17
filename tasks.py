from celery import Celery 
import os
import redis

app = Celery()
app.config_from_object("celery_settings")

@app.task
def hello():
    print 'hello'