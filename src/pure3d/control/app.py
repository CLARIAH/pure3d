import os

from flask import Flask, render_template, redirect, make_response, abort, request

from control.messages import Messages
from control.config import Config
from control.mongo import Mongo
from control.viewers import Viewers
from control.content import Content, ContentError
from control.users import Users
from control.pages import Pages
from control.editsessions import EditSessions
from control.authorise import Auth
from control.webdavapp import WEBDAV_METHODS

Config = Config(Messages(None)).getConfig()
Messages = Messages(Config)
Mongo = Mongo(Config, Messages)
Viewers = Viewers(Mongo)
Users = Users(Config, Messages)
Content = Content(Config, Viewers, Messages, Mongo)
Auth = Auth(Config, Messages, Users, Content)
Content.addAuth(Auth)
Viewers.addAuth(Auth)
Pages = Pages(Config, Messages, Content, ContentError, Auth)
EditSessions = EditSessions(Mongo)


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
    def projectPage(projectId):
        return Pages.projectPage(projectId)

    @app.route("/editions/<string:editionId>")
    def editionPage(editionId):
        return Pages.editionPage(editionId)

    @app.route("/scenes/<string:sceneId>")
    def scenePage(sceneId):
        return Pages.scenePage(sceneId)

    @app.route(
        "/projects/<string:projectId>/editions/<string:editionId>/<string:sceneName>/<string:viewerVersion>"
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
        "/projects/<string:projectId>/editions/<string:editionId>/<string:sceneName>/<string:viewerVersion>/<string:action>"
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
        "/viewer/<string:viewerVersion>/<string:action>/<string:projectId>/<string:editionId>/<string:sceneName>"
    )
    def voyager(viewerVersion, action, projectId, editionId, sceneName):
        try:
            (rootPath, rootUrl, rootExists) = Content.getLocation(
                projectId,
                editionId,
                None,
                None,
                None,
                action=action,
            )
            (scenePath, sceneUrl, sceneExists) = Content.getLocation(
                projectId,
                editionId,
                sceneName,
                None,
                None,
            )
        except ContentError as e:
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

    @app.route(
        "/auth/webdav/projects/<string:projectId>/editions/<string:editionId>/",
        defaults=dict(path=""),
        methods=tuple(WEBDAV_METHODS),
    )
    @app.route(
        "/auth/webdav/projects/<string:projectId>/editions/<string:editionId>/<path:path>",
        methods=tuple(WEBDAV_METHODS),
    )
    def authwebdav(projectId, editionId, path):
        permitted = Auth.authorise(
            WEBDAV_METHODS[request.method], projectId=projectId, editionId=editionId
        )
        Messages.debug(
            logmsg=f"WEBDAV auth: {permitted=} {Auth.user=} {projectId=} {editionId=} {path=}"
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


def decide(env):
    for (k, v) in env.items():
        Messages.plain(logmsg=f"{k} = {v}")
    return False
