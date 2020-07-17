import os
import redis

## Broker settings.
broker_url = os.environ.get('REDIS_URL','redis://localhost:6379/0')

# # List of modules to import when the Celery worker starts.
# imports = ('myapp.tasks',)

# ## Using the database to store task state and results.
result_backend = 'REDIS_URL'

# task_annotations = {'tasks.add': {'rate_limit': '10/s'}}