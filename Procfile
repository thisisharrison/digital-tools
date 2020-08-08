web: gunicorn wsgi:app
web: gunicorn -k eventlet wsgi:app
worker: celery worker -A tasks.app -l INFO