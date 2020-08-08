web: gunicorn wsgi:app
web: gunicorn -k eventlet main
worker: celery worker -A tasks.app -l INFO