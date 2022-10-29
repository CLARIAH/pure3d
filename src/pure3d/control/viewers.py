from textwrap import dedent

from control.helpers.generic import AttrDict


class Viewers:
    def __init__(self, Config, Mongo):
        """Knowledge of the installed 3D viewers.

        This class knows which (versions of) viewers are installed,
        and has the methods to invoke them.

        It is instantiated by a singleton object.

        Parameters
        ----------
        Config: object
            Singleton instance of `control.config.Config`.
        Mongo: object
            Singleton instance of `control.mongo.Mongo`.
        """
        self.Config = Config
        self.Mongo = Mongo

        viewers = AttrDict()
        self.viewers = viewers
        self.default = None

        for v in Mongo.execute("viewers", "find"):
            v = AttrDict(v)
            viewer = v.name
            viewers[viewer] = AttrDict(versions=v.versions, config=AttrDict(v.config))
            if v.default:
                self.default = viewer

    def addAuth(self, Auth):
        self.Auth = Auth

    def check(self, viewer, version):
        viewers = self.viewers
        if viewer not in viewers:
            viewer = self.default
        versions = viewers[viewer].versions
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
                    "active"
                    if isSceneActive and isViewerActive and isVersionActive
                    else ""
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

        return (frame, "\n".join(buttons))

    def genHtml(self, urlBase, sceneName, viewer, version, action):
        Config = self.Config
        debugMode = Config.debugMode
        ext = "dev" if debugMode else "min"

        viewerStatic = f"/static/viewers/{viewer}/{version}"
        viewerRoot = self.getRoot(urlBase, action, viewer)

        if viewer == "voyager":
            element = "explorer" if action == "view" else "story"
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
                  root="{viewerRoot}"
                  document="{sceneName}.json"
                  resourceroot="{viewerStatic}"
                > </voyager-{element}>
                </body>
                """
            )
        else:
            return dedent(
                f"""
                <head>
                <meta charset="utf-8">
                </head>
                <body>
                <p>Unsupported viewer: {viewer}</p>
                </body>
                """
            )

    def getRoot(self, urlBase, action, viewer):
        viewers = self.viewers

        if viewer not in viewers:
            return None

        config = viewers[viewer].config

        prefix = config.edit if action == "edit" else config.view

        return f"{prefix}/{urlBase}"
