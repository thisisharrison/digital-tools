import os 
# import psycopg2
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
import datetime
import time
from tasks import hello, imgstatus_task, pdpscrape_task
from helper import *

app = Flask(__name__)
app.config.from_object('config.ProdConfig')
Session(app)

DATABASE_URL = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.BigInteger, unique=True, nullable=False, index=True)
    style_desc = db.Column(db.String(120), nullable=False)
    style_option = db.Column(db.String(120), nullable=False, index=True)
    colour_name = db.Column(db.String(120), nullable=False)
    size_code = db.Column(db.String(120), nullable=False)
    department_name = db.Column(db.String(120))
    class_name = db.Column(db.String(120))
    subclass_name = db.Column(db.String(120))

    def __init__(self, sku, style_desc, style_option, colour_name, size_code, department_name, class_name, subclass_name):
        self.sku = sku
        self.style_desc = style_desc
        self.style_option = style_option
        self.colour_name = colour_name
        self.size_code = size_code
        self.department_name = department_name
        self.class_name = class_name
        self.subclass_name = subclass_name


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
    return

def updateUser(info):
    if not session.get('user'):    
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
        if session.get('user'):
            return render_template('pdp.html', user = session['user'])
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
    
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

@app.errorhandler(503)
def page_not_found(e):
    return render_template('503.html'), 503

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
    
