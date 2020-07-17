import os
import redis


broker_url = os.environ.get('REDIS_URL','redis://localhost:6379/0')
result_backend = os.environ.get('REDIS_URL','redis://localhost:6379/0')

# broker_url = os.environ['REDIS_URL']
# result_backend = os.environ['REDIS_URL']

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'Europe/Oslo'
enable_utc = True