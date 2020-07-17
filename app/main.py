from flask import Flask
from tasks import hello

app = Flask(__name__)

@app.route("/")
def index():
    hello.delay()
    return "<h1>Successful</h1>"