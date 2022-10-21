import os

from flask import Flask, render_template, redirect, make_response, abort

from control.messages import Messages
from control.config import Config
from control.mongo import Mongo
from control.viewers import Viewers
from control.projects import Projects, ProjectError
from control.users import Users
from control.pages import Pages
from control.sync import Sync
from control.editsessions import EditSessions
from control.authorise import Auth

Config = Config(Messages).getConfig()
Messages = Messages(Config)
Viewers = Viewers(Config)

# create and configure app


Mongo = Mongo(Config, Messages)
Users = Users(Config, Messages)
Projects = Projects(Config, Viewers, Messages)
Auth = Auth(Config, Messages, Users, Projects)
Projects.addAuth(Auth)
Viewers.addAuth(Auth)
Pages = Pages(Config, Messages, Projects, ProjectError, Auth)
Sync = Sync(Messages, Mongo, Projects)
EditSessions = EditSessions(Mongo)


def prepare():
    Sync.sync(allowRemove=not Config.testMode)


def appFactory():
    app = Flask(__name__, static_folder="../static")
    app.secret_key = Config.secret_key

    def redirectResult(url, good):
        code = 302 if good else 303
        return redirect(url, code=code)

    # app url routes start here

    @app.route("/")
    @app.route("/home")
    def home():
        return Pages.base("home", left=("home",))

    @app.route("/about")
    def about():
        return Pages.base("about", left=("home",), right=("about",))

    @app.route("/surpriseme")
    def surpriseme():
        content = "<h2>You will be surprised!</h2>"
        return Pages.base("surpriseme", left=("home",), content=content)

    @app.route("/login")
    def login():
        if Auth.authenticate(login=True):
            good = True
        else:
            good = False
        return redirectResult("/", good)

    @app.route("/logout")
    def logout():
        Auth.deauthenticate()
        return redirectResult("/", True)

    @app.route("/projects")
    def projects():
        title = """<h2>Scholarly projects</h2>"""

        return Pages.base("projects", left=("list",), title=title)

    @app.route("/projects/<int:projectId>")
    def projectPage(projectId):
        title = """<h2>Editions in this project</h2>"""

        return Pages.base(
            "projects",
            projectId=projectId,
            left=("list",),
            right=(
                "title",
                "home",
                "about",
                "description",
            ),
            title=title,
        )

    @app.route("/projects/<int:projectId>/editions/<int:editionId>")
    def editionPage(projectId, editionId):
        title = """<h2>Scenes in this edition</h2>"""

        return Pages.base(
            "projects",
            projectId=projectId,
            editionId=editionId,
            left=("list",),
            right=(
                "title",
                "about",
                "sources",
            ),
            title=title,
        )

    @app.route("/projects/<int:projectId>/editions/<int:editionId>/<string:sceneName>")
    def scenePage(projectId, editionId, sceneName):
        return Pages.base(
            "projects",
            projectId=projectId,
            editionId=editionId,
            sceneName=sceneName,
            left=("list",),
            right=(
                "about",
                "sources",
            ),
        )

    @app.route(
        "/projects/<int:projectId>/editions/<int:editionId>/<string:sceneName>/<string:viewerVersion>"
    )
    def sceneViewer(projectId, editionId, sceneName, viewerVersion):
        return Pages.base(
            "projects",
            projectId=projectId,
            editionId=editionId,
            sceneName=sceneName,
            viewerVersion=viewerVersion,
            left=("list",),
            right=(
                "about",
                "sources",
            ),
        )

    @app.route(
        "/projects/<int:projectId>/editions/<int:editionId>/<string:sceneName>/<string:viewerVersion>/<string:action>"
    )
    def sceneWorker(projectId, editionId, sceneName, viewerVersion, action):
        return Pages.base(
            "projects",
            projectId=projectId,
            editionId=editionId,
            sceneName=sceneName,
            viewerVersion=viewerVersion,
            action=action,
            left=("list",),
            right=(
                "about",
                "sources",
            ),
        )

    @app.route(
        "/viewer/<string:viewerVersion>/<string:action>/<int:projectId>/<int:editionId>/<string:sceneName>"
    )
    def voyager(viewerVersion, action, projectId, editionId, sceneName):
        try:
            (rootPath, rootUrl, rootExists) = Projects.getLocation(
                projectId,
                editionId,
                None,
                None,
                None,
                action=action,
            )
            (scenePath, sceneUrl, sceneExists) = Projects.getLocation(
                projectId,
                editionId,
                sceneName,
                None,
                None,
            )
        except ProjectError as e:
            msg = f"Voyager viewer: {e}"
            Messages.error(msg=msg, logmsg=msg)

        viewerCode = Viewers.genHtml(
            viewerVersion,
            action,
            projectId,
            editionId,
            f"{rootUrl}/",
            f"{sceneName}.json",
        )

        return render_template(
            "voyager.html",
            viewerCode=viewerCode,
        )

    @app.route("/data/<path:path>")
    def data(path):
        dataDir = Config.dataDir

        dataPath = f"{dataDir}/{path}"
        if not os.path.isfile(dataPath):
            Messages.error(
                msg="Accessing a file",
                logmsg=f"File does notexist: {dataPath}",
            )

        with open(dataPath, "rb") as fh:
            textData = fh.read()

        return make_response(textData)

    @app.route("/auth/webdav/<path:path>")
    def authwebdav(path):
        authenticated = Auth.authenticate()
        if authenticated:
            Messages.info(logmsg=f"User = {Auth.user} {path=}")
            return True
        else:
            Messages.info(logmsg=f"Unauthenticated {path=}")
            return False

    @app.route("/no/webdav/<path:path>")
    def nowebdav(path):
        Messages.info(logmsg=f"Unauthorized webdav access {path=}")
        abort(404)

    return app


def decide(env):
    for (k, v) in env.items():
        Messages.plain(logmsg=f"{k} = {v}")
    return False


prepare()
