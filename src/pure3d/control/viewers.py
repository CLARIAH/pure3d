import os
from textwrap import dedent


class Viewers:
    def __init__(self, Config):
        self.Config = Config

        staticDir = Config.staticDir

        viewers = {
            v: []
            for (v, enabled) in Config.viewers.items()
            if enabled and os.path.isdir(f"{staticDir}/{v}")
        }
        self.viewers = viewers

        for v in viewers:
            viewerDir = f"{staticDir}/{v}"
            with os.scandir(viewerDir) as vh:
                for entry in vh:
                    if entry.is_dir():
                        viewers[v].append(entry.name)

        self.makeLinkPrefixes()

    def addAuth(self, Auth):
        self.Auth = Auth

    def makeLinkPrefixes(self):
        viewers = self.viewers

        prefixes = []
        for (viewer, versions) in sorted(viewers.items()):
            for version in sorted(versions):
                prefixes.append(f"{viewer}-{version}")

        self.prefixes = prefixes

    def genHtml(self, viewerVersion, action, projectId, editionId, root, scene):
        Config = self.Config
        Auth = self.Auth
        debugMode = Config.debugMode
        ext = "dev" if debugMode else "min"

        (viewer, version) = viewerVersion.split("-", 1)

        action = Auth.checkModifiable(projectId, editionId, action)

        if viewer == "voyager":
            element = "explorer" if action == "read" else "story"
            return dedent(
                f"""
                <head>
                <link href="/static/dist/fonts/fonts.css" rel="stylesheet"/>
                <link
                  rel="shortcut icon"
                  type="image/png"
                  href="/static/dist/favicon.png"
                />
                <link
                  rel="stylesheet"
                  href="/static/{viewer}/{version}/css/voyager-{element}.{ext}.css"
                />
                <script
                  defer
                  src="/static/{viewer}/{version}/js/voyager-{element}.{ext}.js">
                </script>
                </head>
                <body>
                <voyager-{element}
                  root="{root}"
                  document="{scene}"
                  resourceroot="/static/{viewer}/{version}"
                > </voyager-{element}>
                </body>
                """
            )
