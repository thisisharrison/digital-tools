web: gunicorn wsgi:app
worker: celery worker -A tasks.app -l INFO