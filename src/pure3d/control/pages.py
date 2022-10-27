from textwrap import dedent
from flask import render_template

TABS = (
    ("home", "Home", True),
    ("about", "About", True),
    ("projects", "3D Projects", True),
    ("directory", "3D Directory", False),
    ("surpriseme", "Surprise Me", False),
    ("advancedsearch", "Advanced Search", False),
)


class Pages:
    def __init__(self, Config, Messages, Content, ContentError, Auth):
        self.Config = Config
        self.Messages = Messages
        self.Content = Content
        self.ContentError = ContentError
        self.Auth = Auth

    def home(self):
        Content = self.Content
        intro = Content.getText("intro")
        left = (intro,)
        return self.page(left=left)

    def about(self):
        Content = self.Content
        intro = Content.getText("intro")
        surpriseMe = Content.getSurprise()
        left = (intro,)
        right = (surpriseMe,)
        return self.page(left=left, right=right)

    def surprise(self):
        Content = self.Content
        intro = Content.getText("intro")
        about = Content.getText("about")
        left = (intro,)
        right = (about,)
        return self.page(left=left, right=right)

    def projects(self):
        Content = self.Content
        title = """<h2>Scholarly projects</h2>"""
        projects = Content.getProjects()
        left = (title, projects,)
        return self.page(left=left)

    def projectPage(self, projectId):
        Content = self.Content
        projectInfo = Content.getRecord("projects", projectId)
        editions = Content.getEditions(projectId)
        title = f"<h1>{projectInfo.title}</h1>"
        left = (title, editions)
        right = tuple(
            Content.getText(item, projectId=projectId)
            for item in ("intro", "about", "description")
        )
        return self.page(left=left, right=right)

    def editionPage(self, editionId):
        Content = self.Content
        editionInfo = Content.getRecord("editions", editionId)
        projectId = editionInfo.projectId
        back = self.backLink(projectId)
        title = f"<h2>{editionInfo.title}</h2>"
        scenes = Content.getScenes(projectId, editionId)
        left = (back, title, scenes)
        right = tuple(
            Content.getText(item, editionId=editionId)
            for item in ("about", "sources")
        )
        return self.page(left=left, right=right)

    def scenePage(self, sceneId):
        Content = self.Content
        sceneInfo = Content.getRecord("scenes", sceneId)
        projectId = sceneInfo.projectId
        editionId = sceneInfo.editionId
        back = self.backLink(projectId)
        title = f"<h3>{sceneInfo.name}</h3>"
        scenes = Content.getScenes(projectId, editionId, sceneId=sceneId)
        left = (back, title, scenes)
        right = tuple(
            Content.getText(item, editionId=editionId)
            for item in ("about", "sources")
        )
        return self.page(left=left, right=right)

    def backLink(projectId):
        projectUrl = f"/projects/{projectId}"
        return f"""<p><a class="button" href="{projectUrl}">back to the project page</a></p>"""

    def page(
        self,
        url,
        projectId=None,
        editionId=None,
        action="read",
        left=(),
        right=(),
    ):
        Config = self.Config
        Messages = self.Messages
        Auth = self.Auth
        action = Auth.checkModifiable(projectId, editionId, action)

        navigation = self.navigation(url)

        return render_template(
            "index.html",
            versionInfo=Config.versionInfo,
            navigation=navigation,
            materialLeft="\n".join(left),
            materialRight="\n".join(right),
            messages=Messages.generateMessages(),
            testUsers=Auth.wrapTestUsers(),
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
