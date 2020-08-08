web: gunicorn wsgi:app
web: gunicorn -k eventlet app:app
worker: celery worker -A tasks.app -l INFO