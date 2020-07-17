import os
import redis

# ## Broker settings.
# broker_url = os.environ['REDIS_URL']

# # # List of modules to import when the Celery worker starts.
# # imports = ('myapp.tasks',)

# # ## Using the database to store task state and results.
# celery_result_backend = os.environ['REDIS_URL']

# # task_annotations = {'tasks.add': {'rate_limit': '10/s'}}

# celery_task_serializer = 'json'

broker_url = os.environ['REDIS_URL']
result_backend = os.environ['REDIS_URL']

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'Europe/Oslo'
enable_utc = True