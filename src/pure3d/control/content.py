import os
from markdown import markdown

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


class Content:
    def __init__(self, Config, Viewers, Messages, Mongo):
        self.Config = Config
        self.Viewers = Viewers
        self.Messages = Messages
        self.Mongo = Mongo

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

        record = Mongo.getRecord(table, name=name, **condition)
        return markdown(record.text or "")

    def getSurprise(self):
        return "<h2>You will be surprised!</h2>"

    def getProjects(self):
        Mongo = self.Mongo
        Auth = self.Auth

        wrapped = []

        for row in Mongo.execute(
            "projects", "find", {}, dict(title=True, name=True, candy=True)
        ):
            row = AttrDict(row)
            self.Messages.debug(logmsg=f"{row.name=}")
            projectId = row._id
            permitted = Auth.authorise("view", project=projectId)
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

        projectInfo = Mongo.getRecord("projects", _id=projectId)
        projectName = projectInfo.name

        wrapped = []

        for row in Mongo.execute(
            "editions",
            "find",
            dict(projectId=projectId),
            dict(title=True, name=True, candy=True),
        ):
            row = AttrDict(row)
            editionId = row._id
            permitted = Auth.authorise("view", project=projectId, edition=editionId)
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
        sceneId=None,
        viewer="",
        version="",
        action="view",
    ):
        Mongo = self.Mongo
        Auth = self.Auth
        Viewers = self.Viewers

        projectInfo = Mongo.getRecord("projects", _id=projectId)
        projectName = projectInfo.name
        editionInfo = Mongo.getRecord("editions", _id=editionId)
        editionName = editionInfo.name

        wrapped = []

        permitted = Auth.authorise("view", project=projectId, edition=editionId)
        if not permitted:
            return []

        action = Auth.checkModifiable(projectId, editionId, action)
        actions = ["view"]
        if Auth.isModifiable(projectId, editionId):
            actions.append("edit")

        (viewer, version) = Viewers.check(viewer, version)

        wrapped = []

        for row in Mongo.execute(
            "scenes",
            "find",
            dict(editionId=editionId),
            dict(name=True, projectName=True, projectId=True),
        ):
            row = AttrDict(row)

            isSceneActive = row._id == sceneId
            (frame, buttons) = Viewers.getButtons(
                row._id, actions, isSceneActive, viewer, version, action
            )

            sceneUrl = f"/scenes/{row._id}"
            iconUrlBase = f"/data/projects/{projectName}/editions/{editionName}/candy"
            caption = self.getCaption(
                row.name,
                row.candy,
                sceneUrl,
                iconUrlBase,
                active=sceneId is None or isSceneActive,
                frame=frame,
                buttons=buttons,
            )
            wrapped.append(caption)

        return "\n".join(wrapped)

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
        if candy is None:
            return None
        first = [image for (image, isIcon) in candy.items() if isIcon]
        if first:
            return first[0]
        return None

    def getData(self, path, projectName="", editionName=""):
        Config = self.Config
        Messages = self.Messages
        Auth = self.Auth

        dataDir = Config.dataDir

        urlBase = (
            "texts"
            if projectName == "" and editionName == ""
            else f"projects/{projectName}"
            if editionName == ""
            else f"projects/{projectName}/editions/{editionName}"
        )

        dataPath = f"{dataDir}/{urlBase}/{path}"

        permitted = (
            True
            if urlBase == "texts"
            else Auth.authorise(
                "view", project=projectName, edition=editionName, byName=True
            )
        )

        exists = os.path.isfile(dataPath)
        if not permitted or not exists:
            logmsg = f"Issues in accessing {dataPath}: "
            if not permitted:
                logmsg = "not allowed. "
            if not exists:
                logmsg += "does not exist. "
            Messages.error(
                msg="Accessing a file",
                logmsg=logmsg,
            )

        with open(dataPath, "rb") as fh:
            textData = fh.read()

        return textData

    def getRecord(self, *args, **kwargs):
        return self.Mongo.getRecord(*args, **kwargs)
