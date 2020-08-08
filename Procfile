web: gunicorn wsgi:app
web: gunicorn -k eventlet app:main
worker: celery worker -A tasks.app -l INFO