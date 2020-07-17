from flask import Flask, render_template, request, redirect, url_for
from tasks import hello

app = Flask(__name__)

@app.route("/")
def index():
    hello.delay()
    return render_template('index.html')

@app.route("/image", methods=["GET", "POST"])
def image():
    return render_template('image.html')


@app.route("/image/<task_id>")
def image_result(task_id):
    pass


@app.route("/pdp", methods=["GET", "POST"])
def prodpdp():
    return render_template('pdp.html')


@app.route("/pdp/<task_id>")
def pdp_result(task_id):
    pass

@app.route("/cdp", methods=["GET", "POST"])
def prodcdp():
    return render_template('cdp.html')