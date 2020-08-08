web: gunicorn wsgi:app
worker: celery worker -A tasks.app -l INFO
web: gunicorn -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 wsgi:app