from flask import Flask, render_template


app1 = Flask(__name__)


def route(path):
    return render_template("index.html", route=path)

@app.route("/aap")
lambda x: route("/aap")

@app.route("/noot")
lambda x: route("/noot")
