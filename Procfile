web: gunicorn wsgi:app
gunicorn --worker-class eventlet -w 1 module:app
worker: celery worker -A tasks.app -l INFO