from textwrap import dedent

from control.helpers.generic import AttrDict


class Viewers:
    def __init__(self, Mongo):
        self.Mongo = Mongo

        viewers = AttrDict()
        self.viewers = viewers
        self.default = None

        for v in Mongo.execute("viewers", "find"):
            v = AttrDict(v)
            viewer = v.name
            viewers[viewer] = v.versions
            if v.get("default", None):
                self.default = viewer

        self.makeLinkPrefixes()

    def addAuth(self, Auth):
        self.Auth = Auth

    def check(self, viewer, version):
        viewers = self.viewers
        if viewer not in viewers:
            viewer = self.default
        versions = viewers[viewer]
        if version not in versions:
            version = versions[-1]
        return (viewer, version)

    def getButtons(
        self, sceneId, actions, isSceneActive, viewerActive, versionActive, actionActive
    ):
        viewers = self.viewers

        buttons = []
        frame = ""

        for viewer in viewers:
            isViewerActive = viewer == viewerActive
            vwActive = "active" if isSceneActive and isViewerActive else ""
            buttons.append(
                dedent(
                    f"""<span class="vw"><span class="vwl {vwActive}">{viewer}</span>
                        <span class="vwv">
                    """
                )
            )

            for version in viewers[viewer].versions:
                isVersionActive = version == versionActive
                vsActive = (
                    "active" if isSceneActive and isViewerActive and isVersionActive else ""
                )
                buttons.append(
                    f"""<span class="vv"><span class="vvl {vsActive}">{version}</span>"""
                )
                for action in actions:
                    isActionActive = action == actionActive
                    btActive = (
                        "active"
                        if isSceneActive
                        and isViewerActive
                        and isVersionActive
                        and isActionActive
                        else ""
                    )

                    elem = "a"
                    attStr = ""

                    if btActive:
                        frame = dedent(
                            f"""
                            <div class="model">
                                <iframe
                                    class="previewer"
                                    src="/viewer/{viewer}/{version}/{action}/{sceneId}"/>
                                </iframe>
                            </div>
                            """
                        )
                        elem = "span"
                    else:
                        attStr = (
                            f' href="/scenes/{sceneId}/{viewer}/{version}/{action}" '
                        )

                    cls = f"button {btActive} vwb"
                    begin = f"""<{elem} class="{cls}" {attStr}>"""
                    end = f"</{elem}>"
                    buttons.append(f"{begin}{action}{end}")
                buttons.append("""</span> """)
            buttons.append("""</span></span> """)

        return (frame, buttons)

    def genHtml(self, viewer, version, action, projectId, editionId, root, scene):
        Config = self.Config
        Auth = self.Auth
        debugMode = Config.debugMode
        ext = "dev" if debugMode else "min"

        action = Auth.checkModifiable(projectId, editionId, action)

        viewerStatic = f"/static/viewers/{viewer}/{version}"

        if viewer == "voyager":
            element = "explorer" if action == "read" else "story"
            return dedent(
                f"""
                <head>
                <meta charset="utf-8">
                <link
                  href="{viewerStatic}/fonts/fonts.css"
                  rel="stylesheet"
                />
                <link
                  rel="shortcut icon"
                  type="image/png"
                  href="{viewerStatic}/favicon.png"
                />
                <link
                  rel="stylesheet"
                  href="{viewerStatic}/css/voyager-{element}.{ext}.css"
                />
                <script
                  defer
                  src="{viewerStatic}/js/voyager-{element}.{ext}.js">
                </script>
                </head>
                <body>
                <voyager-{element}
                  root="{root}"
                  document="{scene}"
                  resourceroot="{viewerStatic}"
                > </voyager-{element}>
                </body>
                """
            )
