from textwrap import dedent


class Viewers:
    def __init__(self, Mongo):
        self.Mongo = Mongo

        viewers = {}
        self.viewers = viewers

        for v in Mongo.execute("viewers", "find"):
            viewers[v["name"]] = v["versions"]

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
