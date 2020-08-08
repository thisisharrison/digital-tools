web: gunicorn wsgi:app
worker: celery worker -A tasks.app -l INFO
web: gunicorn --worker-class socketio.sgunicorn.GeventSocketIOWorker --log-file=- main:app