from markdown import markdown

from control.helpers.files import readYaml
from control.helpers.generic import AttrDict


COMPONENT = dict(
    me=(None, None, None, None),
    home=("texts/intro", "md", True, ""),
    about=("texts/about", "md", True, "## About\n\n"),
    intro=("texts/intro", "md", True, ""),
    usage=("texts/usage", "md", True, "## Guide\n\n"),
    description=("texts/description", "md", True, "## Description\n\n"),
    sources=("texts/sources", "md", True, "## Sources\n\n"),
    title=("meta/dc", "json", "dc.title", None),
    icon=("candy/icon", "png", None, None),
    list=(None, None, None, None),
)


class ContentError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class Content:
    def __init__(self, Config, Viewers, Messages, Mongo):
        self.Config = Config
        self.Viewers = Viewers
        self.Messages = Messages
        self.Mongo = Mongo

        yamlDir = Config.yamlDir
        self.projectStatus = readYaml(f"{yamlDir}/projectstatus.yaml")

    def addAuth(self, Auth):
        self.Auth = Auth

    def getText(self, name, projectId=None, editionId=None):
        Mongo = self.Mongo

        table = "texts"
        condition = {}

        if editionId is not None:
            table = "editions"
            condition = dict(editionId=editionId)
        elif projectId is not None:
            table = "projects"
            condition = dict(projectId=projectId)
        else:
            table = "texts"

        record = Mongo.execute(
            table, "find_one", dict(name=name, **condition), dict(_id=False, text=True)
        )
        return markdown(record.get("text", ""))

    def getSurprise(self):
        return "<h2>You will be surprised!</h2>"

    def getProjects(self):
        Mongo = self.Mongo
        Auth = self.Auth

        wrapped = []

        for row in Mongo.execute(
            "projects", "find", {}, dict(title=True, name=True, projectId=True)
        ):
            row = AttrDict(row)
            projectId = row._id
            permitted = Auth.authorise("read", projectId=projectId)
            if not permitted:
                continue

            title = row.title
            candy = row.candy

            projectUrl = f"/projects/{projectId}"
            projectName = row.name
            iconUrlBase = f"/data/projects/{projectName}/candy"
            caption = self.getCaption(title, candy, projectUrl, iconUrlBase)
            wrapped.append(caption)

        return "\n".join(wrapped)

    def getEditions(self, projectId):
        Mongo = self.Mongo
        Auth = self.Auth

        projectInfo = self.getRecord("projects", projectId)
        projectName = projectInfo.name

        wrapped = []

        for row in Mongo.execute(
            "editions",
            "find",
            dict(projectId=projectId),
            dict(title=True, name=True),
        ):
            row = AttrDict(row)
            editionId = row._id
            permitted = Auth.authorise("read", projectId=projectId, editionId=editionId)
            if not permitted:
                continue

            title = row.title
            candy = row.candy

            editionUrl = f"/editions/{editionId}"
            editionName = row.name
            iconUrlBase = f"/data/projects/{projectName}/editions/{editionName}/candy"
            caption = self.getCaption(title, candy, editionUrl, iconUrlBase)
            wrapped.append(caption)

        return "\n".join(wrapped)

    def getScenes(
        self,
        projectId,
        editionId,
        activeId=None,
        viewer=None,
        version=None,
        action="read",
    ):
        Mongo = self.Mongo
        Auth = self.Auth
        Viewers = self.Viewers

        projectInfo = self.getRecord("projects", projectId)
        projectName = projectInfo.name
        editionInfo = self.getRecord("projects", projectId)
        editionName = editionInfo.name

        wrapped = []

        permitted = Auth.authorise("read", projectId=projectId, editionId=editionId)
        if not permitted:
            return []

        action = Auth.checkModifiable(projectId, editionId, action)
        actions = ["read"]
        if Auth.isModifiable(projectId, editionId):
            actions.append("update")

        (viewer, version) = Viewers.check(viewer, version)

        wrapped = []

        for row in Mongo.execute(
            "scenes",
            "find",
            dict(editionId=editionId),
            dict(name=True, projectName=True, projectId=True),
        ):
            row = AttrDict(row)
            sceneId = row._id
            title = row.name
            candy = row.candy

            isSceneActive = sceneId == activeId
            (frame, buttons) = Viewers.getButtons(
                sceneId, actions, isSceneActive, viewer, version, action
            )

            frame = ""

            buttons = "\n".join(buttons)

            sceneUrl = f"/scenes/{sceneId}"
            iconUrlBase = f"/data/projects/{projectName}/editions/{editionName}/candy"
            caption = self.getCaption(
                title,
                candy,
                sceneUrl,
                iconUrlBase,
                active=activeId is None or isSceneActive,
                frame=frame,
                buttons=buttons,
            )
            wrapped.append(caption)

        return "\n".join(wrapped)

    def getRecord(self, table, itemId):
        Mongo = self.Mongo
        Auth = self.Auth

        record = AttrDict(Mongo.execute(table, "find_one", dict(_id=itemId), {}))
        projectId = itemId if table == "projects" else record.projectId
        editionId = (
            None
            if table == "projects"
            else itemId
            if table == "editions"
            else record.projectId
        )
        permitted = Auth.authorise("read", projectId=projectId, editionId=editionId)
        return AttrDict(record if permitted else {})

    def getCaption(
        self, title, candy, url, iconUrlBase, active=False, buttons="", frame=""
    ):
        icon = self.getIcon(candy)

        activeCls = "active" if active else ""
        start = f"""<div class="caption {activeCls}">"""
        visual = (
            f"""<img class="previewicon" src="{iconUrlBase}/{icon}">""" if icon else ""
        )
        heading = (
            f"""{frame}<a href="{url}">{title}</a>"""
            if frame
            else f"""<a href="{url}">{visual}{title}</a>"""
        )
        end = """</div>"""
        caption = f"""{start}{heading}{buttons}{end}"""
        return caption

    def getIcon(self, candy):
        first = [image for (image, isIcon) in candy.items() if isIcon]
        if first:
            return first[0]
        if candy:
            return list(candy)[0]
        return None
