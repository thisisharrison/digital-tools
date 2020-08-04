from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
# import secrets
# import os
# import redis
# from datetime import datetime
import datetime
import pytz
from tzlocal import get_localzone
import uuid
from tasks import hello, imgstatus_task, pdpscrape_task
from helper import *

app = Flask(__name__)
app.config.from_object('config.DevConfig')
Session(app)


# key = secrets.token_urlsafe(16)
# SESSION_TYPE = 'redis'
# SESSION_REDIS = redis.from_url(os.environ.get('REDIS_URL','redis://localhost:6379/0'))
# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)



@app.route("/")
def index():
    hello.delay()
    session.clear()

    if not session.get('testing'):
        session['testing'] = 'TESTING'
    print (session['testing'])
    
    return render_template('index.html')



@app.route("/image", methods=["GET", "POST"])
def image():
    if request.method == 'POST':
        query = request.form.get('style_colors')
        queryset = query_edit(query)
        
        # send style colors to check status
        task = imgstatus_task.apply_async(args=[queryset])
        task_id = task.id
        
        now = datetime.now()
        now_s = now.strftime("%D %H:%M:%S")

        # TO-DO
        # add task queue page

        # {task_id:
        #   {time: time,
        #   status: status,
        #   finished: finished}
        # }

        if not session.get('uuid'):
            session['uuid'] = uuid.uuid4()
            session['imageTasks'] = {task_id: {'started_at': now_s}}
        else:
            session['imageTasks'][task_id] = {'started_at': now_s}
            
        print(session['uuid'])
        print(session['imageTasks'])
        
        return redirect(url_for('image_result', task_id=task_id))

    else:

        if session.get('uuid'):
            image_tasks = session['imageTasks']
            tasks = hash_update(imgstatus_task, 'imageTasks', image_tasks)
            return render_template('image.html', tasks = tasks)
        else: 
            return render_template('image.html')

def hash_update(task_type, session_type, tasks):
    print('-------- ATTENTION --------')
    print(task_type)
    print(tasks)
    for task_id in tasks:
        task = task_type.AsyncResult(task_id)
        finished_at = str(task.date_done)
        finished_at = datetime.strptime(finished_at, '%Y-%m-%d %H:%M:%S.%f')
        print(finished_at)

        print('-------- TIMEZONE --------')
        local_tz = get_localzone()
        print(local_tz)
        
        
        # local_timezone = datetime.now(datetime.timetz).astimezone().tzinfo
        # local_time = local_timezone.localize(finished_at)
        
        # print(local_time)
        # print(local_time.tzinfo)
        finished_at = finished_at.strftime("%D %H:%M:%S")
        state = task.state

        print('-------- TASKS --------')
        print(task)
        print(finished_at)
        print(state)

        session_task = session[session_type][task.id]
        
        started_at = session_task['started_at']

        session_task['finished_at'] = finished_at
        session_task['state'] = state
    return tasks
        


@app.route("/image/<task_id>")
def image_result(task_id):
    # call result 
    task = imgstatus_task.AsyncResult(task_id)
    results = task.get()
    # render result page
    return render_template('image.html', results=results)
    


@app.route("/pdp", methods=["GET", "POST"])
def prodpdp():
    if request.method == 'POST':
        query = request.form.get('masters')
        site = request.form.get('site')
        siteEnv = request.form.get('siteEnv')
        email = request.form.get('email')
        password = request.form.get('password')
        date = request.form.get('date')
        queryset = query_edit(query)

        info = {'site': site, 'siteEnv': siteEnv, 'email': email, 'password': password, 'date': date}

        # send master/skus to check pdps
        task = pdpscrape_task.apply_async(args=[queryset, info])
        task_id = task.id
        return redirect(url_for('pdp_result', task_id=task_id))

        # TO-DO
        # add task queue page

    else:
        return render_template('pdp.html')
        


@app.route("/pdp/<task_id>")
def pdp_result(task_id):
    # call result 
    task = pdpscrape_task.AsyncResult(task_id)
    results = task.get()
    
    # Gets back finished time in UTC format 
    # print(task.date_done)

    # info and results are identical
    # print(task.info)
    # print(task.result)

    # render result page
    return render_template('pdp.html', results=results)



@app.route("/cdp", methods=["GET", "POST"])
def prodcdp():
    if request.method == 'POST':
        query = request.form.get('cdp_url')
        siteEnv = request.form.get('siteEnv')
        email = request.form.get('email')
        password = request.form.get('password')
        date = request.form.get('date')

        info = {'siteEnv': siteEnv, 'email': email, 'password': password, 'date': date}
        
        results = cdp_scrape(query, info)
        return render_template('cdp.html', results=results)
    else:
        return render_template('cdp.html')
    return render_template('cdp.html')