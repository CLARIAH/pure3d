import os
from dispatcher import DispatcherMiddleware
from flask import Flask, render_template
from webdavapp import getWebdavApp


BASE = os.path.dirname(os.path.dirname(__file__))
ROOT_URL = "/data/"
RES_ROOT_URL = "/static/dist"
SCENE = "clanwilliam.json"
WIDTH = "1000px"
HEIGHT = "600px"
STATUS = os.environ["PILOT_MODE"]

app = Flask(__name__, static_folder=f"{BASE}/static")


@app.route("/")
def index():
    return render_template(
        "index.html", status=STATUS, scene=SCENE, height=HEIGHT, width=WIDTH
    )


@app.route("/voyager/<string:scene>")
def voyager(scene):
    ext = "min" if STATUS == "prod" else "dev"
    return render_template(
        "voyager.html",
        ext=ext,
        root=ROOT_URL,
        resourceRoot=RES_ROOT_URL,
        scene=scene,
    )


app.wsgi_app = DispatcherMiddleware(
    app.wsgi_app,
    {
        "/data/": getWebdavApp(),
    },
)
