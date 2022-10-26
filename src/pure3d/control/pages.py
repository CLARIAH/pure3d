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
    def __init__(self, Config, Messages, Projects, ProjectError, Auth):
        self.Config = Config
        self.Messages = Messages
        self.Projects = Projects
        self.ProjectError = ProjectError
        self.Auth = Auth

    def home(self):
        Projects = self.Projects
        intro = Projects.getText("intro")
        return self.base(left=(intro,))

    def about(self):
        Projects = self.Projects
        intro = Projects.getText("intro")
        surpriseMe = Projects.getSurprise()
        return self.base(left=(intro,), right=(surpriseMe,))

    def surprise(self):
        Projects = self.Projects
        intro = Projects.getText("intro")
        about = Projects.getText("about")
        return self.base(left=(intro,), right=(about,))

    def backLink(projectId):
        projectUrl = f"/projects/{projectId}"
        return f"""<p><a class="button" href="{projectUrl}">back to editions</a></p>"""

    def base(
        self,
        url,
        projectId=None,
        editionId=None,
        action="read",
        left=(),
        right=(),
        back="",
        title="",
        content="",
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
            materialLeft=back + title + "\n".join(left),
            materialRight="\n".join(right) + content,
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
