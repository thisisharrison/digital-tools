from flask import Flask, render_template, request, redirect, url_for
from tasks import hello, imgstatus_task, pdpscrape_task
from helper import *

app = Flask(__name__)

@app.route("/")
def index():
    hello.delay()
    return render_template('index.html')



@app.route("/image", methods=["GET", "POST"])
def image():
    if request.method == 'POST':
        query = request.form.get('style_colors')
        queryset = query_edit(query)
        
        # send style colors to check status
        task = imgstatus_task.apply_async(args=[queryset])
        task_id = task.id
        return redirect(url_for('image_result', task_id=task_id))

        # TO-DO
        # add task queue page

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
        queryset = query_edit(query)

        # send master/skus to check pdps
        task = pdpscrape_task.apply_async(args=[queryset])
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
    # render result page
    return render_template('pdp.html', results=results)



@app.route("/cdp", methods=["GET", "POST"])
def prodcdp():
    if request.method == 'POST':
        query = request.form.get('cdp_url')
        results = cdp_scrape(query)
        return render_template('cdp.html', results=results)
    else:
        return render_template('cdp.html')
    return render_template('cdp.html')