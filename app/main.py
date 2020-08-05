from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
# import secrets
# import os
# import redis
# from datetime import datetime
import datetime
import time
# from dateutil.tz import tzlocal
# from tzlocal import get_localzone
# import pytz
from flask_socketio import SocketIO, emit
import uuid
from tasks import hello, imgstatus_task, pdpscrape_task
from helper import *

app = Flask(__name__)
app.config.from_object('config.ProdConfig')
Session(app)
# socketio = SocketIO(app)


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
        
        now = datetime.datetime.now()
        now_s = now.strftime("%D %H:%M:%S")

        #  session[task_name] = [
        # {task_id: id, start: start, finish: finish, status: status},
        #   ...
        # ]

        task_object = {'task_id': task_id, 'start_at': now_s, 'finish_at': '', 'status': ''}

        if not session.get('uuid'):
            session['uuid'] = uuid.uuid4()
            session['imageTasks'] = [task_object]
        else:
            if len(session['imageTasks']) > 4:
                session['imageTasks'].pop(0)    
            session['imageTasks'].append(task_object)
            
        print(session['uuid'])
        print(session['imageTasks'])
        
        # return redirect(url_for('image_result', task_id=task_id))
        return redirect(url_for('image'))
        

    else:

        if session.get('uuid'):
            image_tasks = session['imageTasks']
            tasks = task_update(imgstatus_task, 'imageTasks', image_tasks)
            return render_template('image.html', tasks = tasks[::-1])
        else: 
            return render_template('image.html')
        


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

# @socketio.on('check status')
# def check_status(data):
#     tasks = data['data']
#     print(f"Total IDS: {tasks}")
    # pending = []
    # complete = []
    # for i in tasks:
    #     task = imgstatus_task.AsyncResult(i)
    #     status = task.state
    #     if status != "SUCCESS" and status != "FAILURE":
    #         pending.append(i)
    #     else:
    #         complete.append(i)
    #         socketio.emit('update complete', {'ID': complete})
    # time.sleep(5)
    # socketio.emit('update pending', {'ID': pending})
