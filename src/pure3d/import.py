import os

from control.messages import Messages
from control.config import Config
from control.mongo import Mongo

from control.helpers.files import listFiles, listImages, readPath, readJson, readYaml
from control.helpers.generic import AttrDict


TEXTS = "texts"
PROJECTS = "projects"
EDITIONS = "editions"

VIEWER_DEFAULT = "voyager"

Config = Config(Messages(None, flask=False)).getConfig()
Messages = Messages(Config, flask=False)
Mongo = Mongo(Config, Messages)


def importFsContent():
    viewerDir = Config.viewerDir
    dataDir = Config.dataDir

    for table in (
        "texts",
        "projects",
        "editions",
        "scenes",
        "users",
        "projectusers",
        "viewers",
    ):
        Mongo.checkCollection(table, reset=True)

    with os.scandir(viewerDir) as vd:
        for entry in vd:
            if entry.is_dir():
                viewerName = entry.name
                viewerPath = f"{viewerDir}/{viewerName}"
                versions = []

                with os.scandir(viewerPath) as sd:
                    for entry in sd:
                        if entry.is_dir():
                            version = entry.name
                            versions.append(version)

                viewerInfo = AttrDict(
                    name=viewerName,
                    versions=versions,
                )
                if viewerName == VIEWER_DEFAULT:
                    viewerInfo.default = True
                Mongo.execute("viewers", "insert_one", viewerInfo)

    textPath = f"{dataDir}/{PROJECTS}"
    textFiles = listFiles(textPath, ".md")

    for textFile in textFiles:
        text = readPath(f"{textPath}/{textFile}.md")
        textInfo = dict(
            name=textFile,
            text=text,
        )
        result = Mongo.execute("texts", "insert_one", textInfo)
        textId = result.inserted_id if result is not None else None
        textId

    projectsPath = f"{dataDir}/{PROJECTS}"
    projectIdByName = {}

    with os.scandir(projectsPath) as pd:
        for entry in pd:
            if entry.is_dir():
                projectName = entry.name
                projectPath = f"{projectsPath}/{projectName}"

                meta = {}
                metaPath = f"{projectPath}/meta"
                metaFiles = listFiles(metaPath, ".json")

                for metaFile in metaFiles:
                    meta[metaFile] = readJson(f"{metaPath}/{metaFile}.json")

                title = meta.get("dc", {}).get("dc.title", projectName)

                texts = {}
                textPath = f"{projectPath}/texts"
                textFiles = listFiles(textPath, ".md")

                for textFile in textFiles:
                    texts[textFile] = readPath(f"{textPath}/{textFile}.md")

                candy = {}
                candyPath = f"{projectPath}/candy"

                for image in listImages(candyPath):
                    candy[image] = True if image.lower() == "icon.png" else False

                projectInfo = dict(
                    title=title,
                    name=projectName,
                    meta=meta,
                    texts=texts,
                    candy=candy,
                )

                result = Mongo.execute("projects", "insert_one", projectInfo)
                projectId = result.inserted_id if result is not None else None
                projectIdByName[projectName] = projectId

                editionsPath = f"{projectPath}/{EDITIONS}"

                with os.scandir(editionsPath) as ed:
                    for entry in ed:
                        if entry.is_dir():
                            editionName = entry.name
                            editionPath = f"{editionsPath}/{editionName}"

                            meta = {}
                            metaPath = f"{editionPath}/meta"
                            metaFiles = listFiles(metaPath, ".json")

                            title = meta.get("dc", {}).get("dc.title", editionName)

                            for metaFile in metaFiles:
                                meta[metaFile] = readJson(f"{metaPath}/{metaFile}.json")

                            texts = {}
                            textPath = f"{editionPath}/texts"
                            textFiles = listFiles(textPath, ".md")

                            for textFile in textFiles:
                                texts[textFile] = readPath(f"{textPath}/{textFile}.md")

                            scenes = listFiles(editionPath, ".json")
                            sceneSet = set(scenes)
                            sceneCandy = {scene: {} for scene in scenes}

                            candy = {}
                            candyPath = f"{editionPath}/candy"

                            for image in listImages(candyPath):
                                (baseName, extension) = image.rsplit(".", 1)
                                if baseName in sceneSet:
                                    sceneCandy[baseName][image] = extension.lower() == "png"
                                else:
                                    candy[image] = True if image.lower() == "icon.png" else False

                            editionInfo = dict(
                                title=title,
                                name=editionName,
                                projectId=projectId,
                                meta=meta,
                                texts=texts,
                                candy=candy,
                            )
                            result = Mongo.execute(
                                "editions", "insert_one", editionInfo
                            )
                            editionId = (
                                result.inserted_id if result is not None else None
                            )

                            for scene in scenes:
                                sceneInfo = dict(
                                    name=scene,
                                    editionId=editionId,
                                    projectId=projectId,
                                    candy=sceneCandy[scene],
                                )
                                result = Mongo.execute(
                                    "scenes", "insert_one", sceneInfo
                                )
                                sceneId = (
                                    result.inserted_id if result is not None else None
                                )
                                sceneId

    workflowPath = f"{dataDir}/yaml/workflow.yaml"
    workflow = readYaml(workflowPath)
    users = workflow["users"]
    projectUsers = workflow["projectUsers"]
    projectStatus = workflow["projectStatus"]

    userIdByName = {}

    for (userName, role) in users.items():
        userInfo = dict(
            name=userName,
            role=role,
        )
        result = Mongo.execute("users", "insert_one", userInfo)
        userId = result.inserted_id if result is not None else None
        userIdByName[userName] = userId

    for (projectName, isPublished) in projectStatus.items():
        Mongo.execute(
            "projects",
            "update_one",
            dict(_id=projectIdByName[projectName]),
            {"$set": dict(isPublished=isPublished)},
        )

    for (projectName, projectUsrs) in projectUsers.items():
        for (userName, role) in projectUsrs.items():
            xInfo = dict(
                userId=userIdByName[userName],
                projectId=projectIdByName[projectName],
                role=role,
            )
            Mongo.execute("projectusers", "insert_one", xInfo)


if __name__ == "__main__":
    importFsContent()
