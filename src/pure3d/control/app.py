from flask import Flask, redirect, abort, request

from control.messages import Messages
from control.config import Config
from control.mongo import Mongo
from control.viewers import Viewers
from control.content import Content
from control.users import Users
from control.pages import Pages
from control.editsessions import EditSessions
from control.authorise import Auth
from control.webdavapp import WEBDAV_METHODS

from control.helpers.generic import AttrDict

if True:
    Config = Config(Messages(None)).getConfig()
    Messages = Messages(Config)

    Mongo = Mongo(Config, Messages)

    Viewers = Viewers(Config, Mongo)

    Users = Users(Config, Messages, Mongo)
    Content = Content(Config, Viewers, Messages, Mongo)
    Auth = Auth(Config, Messages, Mongo, Users, Content)
    EditSessions = EditSessions(Mongo)

    Content.addAuth(Auth)
    Viewers.addAuth(Auth)

    Pages = Pages(Config, Messages, Content, Viewers, Auth, Users)
else:
    (Config, Messages, Mongo, Viewers, Users, Content, Auth, EditSessions, Pages) = (
        AttrDict(dict(secret_key=None)),
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
    )


# create and configure app


def appFactory():
    app = Flask(__name__, static_folder="../static")
    app.secret_key = Config.secret_key

    def redirectResult(url, good):
        code = 302 if good else 303
        return redirect(url, code=code)

    # app url routes start here

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

    @app.route("/")
    @app.route("/home")
    def home():
        return Pages.home()

    @app.route("/about")
    def about():
        return Pages.about()

    @app.route("/surpriseme")
    def surpriseme():
        return Pages.surprise()

    @app.route("/projects")
    def projects():
        return Pages.projects()

    @app.route("/projects/<string:projectId>")
    def project(projectId):
        return Pages.project(projectId)

    @app.route("/editions/<string:editionId>")
    def edition(editionId):
        return Pages.edition(editionId)

    @app.route(
        "/scenes/<string:sceneId>",
        defaults=dict(viewer="", version="", action=""),
    )
    @app.route(
        "/scenes/<string:sceneId>/<string:viewer>",
        defaults=dict(version="", action=""),
    )
    @app.route(
        "/scenes/<string:sceneId>/<string:viewer>/<string:version>",
        defaults=dict(action=""),
    )
    @app.route(
        "/scenes/<string:sceneId>/<string:viewer>/<string:version>/<string:action>",
    )
    def scene(sceneId, viewer, version, action):
        return Pages.scene(sceneId, viewer, version, action)

    @app.route(
        "/viewer/<string:viewer>/<string:version>/<string:action>/<string:sceneId>"
    )
    def viewerFrame(sceneId, viewer, version, action):
        return Pages.viewerFrame(sceneId, viewer, version, action)

    @app.route("/data/texts/<string:fileName>")
    def dataTexts(fileName):
        return Pages.dataTexts(fileName)

    @app.route(
        "/data/projects/<string:projectName>/",
        defaults=dict(editionName="", path=""),
    )
    @app.route(
        "/data/projects/<string:projectName>/<path:path>",
        defaults=dict(editionName=""),
    )
    @app.route(
        "/data/projects/<string:projectName>/editions/<string:editionName>/",
        defaults=dict(path=""),
    )
    @app.route(
        "/data/projects/<string:projectName>/editions/<string:editionName>/<path:path>",
    )
    def dataProjects(projectName, editionName, path):
        return Pages.dataProjects(projectName, editionName, path)

    @app.route(
        "/auth/webdav/projects/<string:projectName>/editions/<string:editionName>/",
        defaults=dict(path=""),
        methods=tuple(WEBDAV_METHODS),
    )
    @app.route(
        "/auth/webdav/projects/<string:projectName>/editions/<string:editionName>/"
        "<path:path>",
        methods=tuple(WEBDAV_METHODS),
    )
    def authwebdav(projectName, editionName, path):
        permitted = Auth.authorise(
            WEBDAV_METHODS[request.method],
            project=projectName,
            edition=editionName,
            byName=True,
        )
        Messages.info(
            logmsg=f"WEBDAV auth: {permitted=} {Auth.user=}"
            f" {projectName=} {editionName=} {path=}"
        )
        return permitted

    @app.route("/auth/webdav/<path:path>", methods=tuple(WEBDAV_METHODS))
    def webdavinvalid(path):
        Messages.info(logmsg=f"Invalid webdav access {path=}")
        return False

    @app.route("/no/webdav/<path:path>")
    def nowebdav(path):
        Messages.info(logmsg=f"Unauthorized webdav access {path=}")
        abort(404)

    return app
