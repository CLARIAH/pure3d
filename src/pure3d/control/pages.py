from textwrap import dedent
from flask import render_template, make_response

TABS = (
    ("home", "Home", True),
    ("about", "About", True),
    ("projects", "3D Projects", True),
    ("directory", "3D Directory", False),
    ("surpriseme", "Surprise Me", False),
    ("advancedsearch", "Advanced Search", False),
)


class Pages:
    def __init__(self, Config, Messages, Content, Viewers, Auth, Users):
        self.Config = Config
        self.Messages = Messages
        self.Content = Content
        self.Auth = Auth
        self.Users = Users
        self.Viewers = Viewers

    def home(self):
        Content = self.Content
        intro = Content.getText("intro")
        left = (intro,)
        return self.page("home", left=left)

    def about(self):
        Content = self.Content
        intro = Content.getText("intro")
        about = Content.getText("about")
        left = (intro,)
        right = (about,)
        return self.page("about", left=left, right=right)

    def surprise(self):
        Content = self.Content
        intro = Content.getText("intro")
        surpriseMe = Content.getSurprise()
        left = (intro,)
        right = (surpriseMe,)
        return self.page("surpriseme", left=left, right=right)

    def projects(self):
        Content = self.Content
        title = """<h2>Scholarly projects</h2>"""
        projects = Content.getProjects()
        left = (
            title,
            projects,
        )
        return self.page("projects", left=left)

    def project(self, projectId):
        Content = self.Content
        projectInfo = Content.getRecord("projects", _id=projectId)
        editions = Content.getEditions(projectId)
        title = f"<h1>{projectInfo.title}</h1>"
        left = (title, editions)
        right = tuple(
            Content.getText(item, projectId=projectId)
            for item in ("intro", "about", "description")
        )
        return self.page("projects", left=left, right=right, projectId=projectId)

    def edition(self, editionId):
        Content = self.Content
        editionInfo = Content.getRecord("editions", _id=editionId)
        projectId = editionInfo.projectId
        back = self.backLink(projectId)
        title = f"<h2>{editionInfo.title}</h2>"
        scenes = Content.getScenes(projectId, editionId)
        left = (back, title, scenes)
        right = tuple(
            Content.getText(item, editionId=editionId) for item in ("about", "sources")
        )
        return self.page(
            "projects", left=left, right=right, projectId=projectId, editionId=editionId
        )

    def scene(self, sceneId, viewer, version, action):
        Content = self.Content
        sceneInfo = Content.getRecord("scenes", _id=sceneId)
        projectId = sceneInfo.projectId
        editionId = sceneInfo.editionId
        back = self.backLink(projectId)
        title = f"<h3>{sceneInfo.name}</h3>"
        scenes = Content.getScenes(
            projectId,
            editionId,
            sceneId=sceneId,
            viewer=viewer,
            version=version,
            action=action,
        )
        left = (back, title, scenes)
        right = tuple(
            Content.getText(item, editionId=editionId) for item in ("about", "sources")
        )
        return self.page(
            "projects",
            left=left,
            right=right,
            projectId=projectId,
            editionId=editionId,
            action=action,
        )

    def viewerFrame(self, sceneId, viewer, version, action):
        Content = self.Content
        Viewers = self.Viewers
        Auth = self.Auth

        sceneInfo = Content.getRecord("scenes", _id=sceneId)
        sceneName = sceneInfo.name

        projectId = sceneInfo.projectId
        projectName = Content.getRecord("projects", _id=projectId).name

        editionId = sceneInfo.editionId
        editionName = Content.getRecord("editions", _id=editionId).name

        urlBase = f"projects/{projectName}/editions/{editionName}/"

        action = Auth.checkModifiable(projectId, editionId, action)

        viewerCode = Viewers.genHtml(urlBase, sceneName, viewer, version, action)
        return render_template("viewer.html", viewerCode=viewerCode)

    def dataTexts(self, fileName):
        Content = self.Content

        data = Content.getData(fileName)
        return make_response(data)

    def dataProjects(self, projectName, editionName, path):
        Content = self.Content

        data = Content.getData(path, projectName=projectName, editionName=editionName)
        return make_response(data)

    def page(
        self,
        url,
        projectId=None,
        editionId=None,
        action="view",
        left=(),
        right=(),
    ):
        Config = self.Config
        Messages = self.Messages
        Auth = self.Auth
        Users = self.Users

        userActive = Auth.user._id
        action = Auth.checkModifiable(projectId, editionId, action)

        navigation = self.navigation(url)
        testUsers = Users.wrapTestUsers(userActive) if Config.testMode else ""

        return render_template(
            "index.html",
            versionInfo=Config.versionInfo,
            navigation=navigation,
            materialLeft="\n".join(left),
            materialRight="\n".join(right),
            messages=Messages.generateMessages(),
            testUsers=testUsers,
        )

    def navigation(self, url):
        search = dedent(
            """
            <span class="search-bar">
                <input
                    type="search"
                    name="search"
                    placeholder="search item"
                    class="button disabled"
                >
                <input type="submit" value="Search" class="button disabled">
            </span>
            """
        )
        html = ["""<div class="tabs">"""]

        for (tab, label, enabled) in TABS:
            active = "active" if url == tab else ""
            elem = "a" if enabled else "span"
            href = f""" href="/{tab}" """ if enabled else ""
            cls = active if enabled else "disabled"
            html.append(
                dedent(
                    f"""
                    <{elem}
                        {href}
                        class="button large {cls}"
                    >{label}</{elem}>
                    """
                )
            )
        html.append(search)
        html.append("</div>")
        return "\n".join(html)

    def backLink(projectId):
        projectUrl = f"/projects/{projectId}"
        cls = """ class="button" """
        href = f""" href="{projectUrl}" """
        text = """back to the project page"""
        return f"""<p><a {cls} {href}>{text}</a></p>"""
