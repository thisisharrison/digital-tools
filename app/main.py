from flask import Flask, render_template, request, redirect, url_for
from tasks import hello

app = Flask(__name__)

@app.route("/")
def index():
    hello.delay()
    # return "<h1>Successful</h1>"
    return render_template('new_index.html')
    # return render_template('index.html')
    # return redirect(url_for('index'))