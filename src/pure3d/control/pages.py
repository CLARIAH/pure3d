from textwrap import dedent
from flask import abort, render_template

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

    def base(
        self,
        url,
        projectId=None,
        editionId=None,
        sceneName=None,
        viewerVersion=None,
        action="read",
        left=(),
        right=(),
        title=None,
        content=None,
    ):
        Config = self.Config
        M = self.Messages
        Projects = self.Projects
        ProjectError = self.ProjectError
        Auth = self.Auth
        action = Auth.checkModifiable(projectId, editionId, action)

        back = ""

        try:
            if projectId is not None and editionId is not None:
                (projectPath, projectUrl, exists) = Projects.getLocation(
                    projectId, None, None, None, None, api=True
                )
                back = dedent(
                    f"""
                        <p>
                            <a
                                class="button"
                                href="{projectUrl}"
                            >back to editions</a>
                        </p>
                        """
                )
                if sceneName is not None:
                    (editionPath, editionUrl, exists) = Projects.getLocation(
                        projectId, editionId, None, None, None, api=True
                    )
                    back += dedent(
                        f"""
                            <p>
                                <a
                                    class="button"
                                    href="{editionUrl}"
                                >back to scenes</a>
                            </p>
                            """
                    )
            projectData = Projects.getInfo(
                projectId,
                editionId,
                sceneName,
                viewerVersion,
                action,
                *left,
                *right,
                missingOk=True,
            )
        except ProjectError as e:
            M.error(e)
            abort(404)

        navigation = self.navigation(url)
        material = dict(left=[], right=[])

        for (comps, side) in ((left, "left"), (right, "right")):
            sideMaterial = material[side]
            for comp in comps:
                sideMaterial.append(
                    dedent(
                        f"""
                <div class="comp-{comp}">
                    {projectData[comp][2]}
                </div>
                """
                    )
                )

            material[side] = "\n".join(sideMaterial)

        title = title or ""
        content = content or ""

        return render_template(
            "index.html",
            versionInfo=Config.versionInfo,
            navigation=navigation,
            materialLeft=back + title + material["left"],
            materialRight=material["right"] + content,
            messages=M.generateMessages(),
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
