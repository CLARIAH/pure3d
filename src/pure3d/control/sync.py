class Sync:
    def __init__(self, Messages, Mongo, Projects):
        self.Messages = Messages
        self.Mongo = Mongo
        self.Projects = Projects

    def sync(self, allowRemove=False):
        # get projects, editions, scenes from file system
        # insert new entities in the db
        # remove superfluous entities from the db

        Messages = self.Messages
        Projects = self.Projects
        Mongo = self.Mongo

        (projectsFile, editionsFile, scenesFile) = Projects.getAllContent()

        Messages.info(logmsg=f"{scenesFile=}")

        Mongo.checkCollection("projects")
        Mongo.checkCollection("editions")
        Mongo.checkCollection("scenes")
        projectsDb = list(
            Mongo.execute("projects", "find", {}, dict(_id=True, fileName=True))
        )
        if len(projectsDb) == 0:
            testProjects = [
                dict(fileName="aap"),
                dict(fileName="noot"),
                dict(fileName="mies"),
            ]
            Mongo.execute("projects", "insert_many", testProjects)
        projectsDb = list(
            Mongo.execute("projects", "find", {}, dict(_id=True, fileName=True))
        )

        Messages.info(logmsg=f"{projectsDb=}")

        projectsFileSet = set(projectsFile)
        projectsDbByFile = {row["fileName"]: row["_id"] for row in projectsDb}

        projectNamesToRemove = []
        projectIdsToRemove = []

        for (fileName, mongoId) in projectsDbByFile.items():
            if fileName not in projectsFileSet:
                projectIdsToRemove.append(mongoId)
                projectNamesToRemove.append(fileName)
        if projectIdsToRemove:
            Messages.info(
                logmsg=f"PROJECTS to remove from DB: {', '.join(projectNamesToRemove)}"
            )
            if allowRemove:
                Mongo.execute(
                    "projects", "delete_many", {"_id": {"$in": projectIdsToRemove}}
                )
                Messages.info(logmsg="these projects have been removed from the DB")
            else:
                Messages.warning(logmsg="these projects are kept in the DB")
