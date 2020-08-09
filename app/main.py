from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
import datetime
import time
# import eventlet
# from flask_socketio import SocketIO, emit
from tasks import hello, imgstatus_task, pdpscrape_task
from helper import *

app = Flask(__name__)
app.config.from_object('config.ProdConfig')
Session(app)
# eventlet.monkey_patch()
# socketio = SocketIO(app, cors_allowed_origins="*", logger=True, engineio_logger=True, manage_session=False)

@app.route("/")
def index():
    hello.delay()
    session.clear()

    if not session.get('testing'):
        session['testing'] = 'TESTING'
    print (session['testing'])
    
    return render_template('index.html')


def updateSession(taskName, task_object):
    if not session.get(taskName):
        session[taskName] = [task_object]
    else:
        # only keep last 5 tasks
        if len(session[taskName]) > 4:
            session[taskName].pop(0)    
            session[taskName].append(task_object)
        else:
            session[taskName].append(task_object)            
    print(session[taskName])
    return

def updateUser(info):
    if session.get('user'):
        if not session['user']['date'] == info['date']:
            session['user']['date'] = info['date']
        
    else: 
        email = info['email']
        password = info['password']
        date = info['date']
        session['user'] = {'email': email, 'password': password, 'date': date}
    return
        


@app.route("/image", methods=["GET", "POST"])
def image():
    if request.method == 'POST':
        query = request.form.get('style_colors')
        queryset = query_edit(query)
        
        # send style colors to check status
        task = imgstatus_task.apply_async(args=[queryset])
        task_id = task.id
        # update session
        task_object = takeSnapshot(task_id)
        updateSession('imageTasks', task_object)
        
        return redirect(url_for('image'))

    else:
        return render_template('image.html')
        
        
@app.route("/queue/<task>")
def queue(task):
    if task == 'pdp':
        task_type = pdpscrape_task
        session_name = 'pdpTasks'
        # tasks = session['pdpTasks']
        
    elif task == 'image':
        task_type = imgstatus_task
        session_name = 'imageTasks'
        # tasks = session['imageTasks']
    
    if session.get(session_name):
        tasks = session[session_name]
    else:
        tasks = None
    
    if tasks != None:
        tasks = task_update(task_type, session_name, tasks)
        return render_template('queue.html', tasks = tasks[::-1], action = task)
    else:
        return render_template('queue.html')
    


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

        # update session for this task
        task_object = takeSnapshot(task_id)
        updateSession('pdpTasks', task_object)
        updateUser(info)

        return redirect(url_for('prodpdp'))
        # return redirect(url_for('pdp_result', task_id=task_id))

    else:
        return render_template('pdp.html')
        


@app.route("/pdp/<task_id>")
def pdp_result(task_id):
    # call result 
    task = pdpscrape_task.AsyncResult(task_id)
    results = task.get()
    
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
        updateUser(info)

        results = cdp_scrape(query, info)
        return render_template('cdp.html', results=results, user = session['user'])
    else:
        if session.get('user'):
            return render_template('cdp.html', user = session['user'])
        else:
            return render_template('cdp.html')
    

# @socketio.on('check status')
# def check_status(data):
#     pending_tasks = data['ids']
#     path = data['task']
#     print('======= SOCKET CHECKING =======')
#     print("Checking IDS: ",pending_tasks)
#     print("Checking TASK TYPE: ",path)
    
#     complete = []
#     if path == 'pdp':
#         task_type = pdpscrape_task
#     elif path == 'image':
#         task_type = imgstatus_task

#     for i in pending_tasks:
#         task = task_type.AsyncResult(i)
#         status = task.state
#         if status == "SUCCESS":
#             complete.append(i)
#             socketio.emit('update complete', {'ID': complete})
    
