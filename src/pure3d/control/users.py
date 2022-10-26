from control.helpers.files import readYaml


class Users:
    def __init__(self, Config, Messages):
        self.Config = Config
        self.Messages = Messages

    def getTestUsers(self):
        Config = self.Config
        Messages = self.Messages
        yamlDir = Config.yamlDir

        testUsers = readYaml(f"{yamlDir}/testusers.yaml")
        userNameById = {}
        userRoleById = {}
        testUserIds = set()

        for (name, info) in testUsers.items():
            userId = info["id"]
            if userId in testUserIds:
                prevName = userNameById[userId]
                Messages.warning(
                    msg=f"duplicate test user {userId} = {name}, {prevName}"
                )
                continue
            testUserIds.add(userId)
            userNameById[userId] = name
            userRoleById[userId] = info["role"]

        return dict(
            testUserIds=testUserIds,
            userNameById=userNameById,
            userRoleById=userRoleById,
        )

    def getUserProject(self):
        Config = self.Config
        yamlDir = Config.yamlDir

        projectUsers = readYaml(f"{yamlDir}/projectusers.yaml")

        userProjects = {}
        for (project, users) in projectUsers.items():
            for (user, role) in users.items():
                userProjects.setdefault(user, {})[project] = role
        return dict(projectUsers=projectUsers, userProjects=userProjects)
