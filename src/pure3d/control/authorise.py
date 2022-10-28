from flask import request, session


class Auth:
    def __init__(self, Config, Messages, Users, Projects):
        self.Config = Config
        self.Messages = Messages
        self.Users = Users
        self.Projects = Projects
        self.authData = Users.getPermissions()
        userData = Users.getTestUsers() if Config.testMode else {}
        self.testUserIds = userData.get("testUserIds", set())
        self.userNameById = userData.get("userNameById", {})
        self.userRoleById = userData.get("userRoleById", {})
        userProjectData = Users.getUserProject()
        self.userProjects = userProjectData["userProjects"]
        self.projectUsers = userProjectData["projectUsers"]
        self.user = {}

    def clearUser(self):
        user = self.user
        user.clear()

    def getUser(self, userId):
        Messages = self.Messages
        user = self.user
        userNameById = self.userNameById
        userRoleById = self.userRoleById

        user.clear()
        result = userId in userNameById
        if result:
            user["id"] = userId
            user["name"] = userNameById[userId]
            user["role"] = userRoleById[userId]
            Messages.debug(
                msg=f"Existing user {userId} = {user['role']}: {user['name']}"
            )
        else:
            Messages.debug(msg=f"Unknown user {userId}")
        return result

    def checkLogin(self):
        Config = self.Config
        Messages = self.Messages
        self.clearUser()
        if Config.testMode:
            userId = request.args.get("userid", None)
            result = self.getUser(userId)
            if result:
                Messages.plain(msg=f"LOGIN successful: user {userId}")
            else:
                Messages.warning(msg=f"LOGIN: user {userId} does not exist")
            return result

        Messages.warning(msg="User management is only available in test mode")
        return False

    def wrapTestUsers(self):
        Config = self.Config

        if not Config.testMode:
            return ""

        user = self.user
        testUserIds = self.testUserIds
        userNameById = self.userNameById
        userRoleById = self.userRoleById

        html = []
        me = "active" if user.get("id", None) is None else ""
        html.append(
            f"""<a
                    href="/logout"
                    class="button small {me}"
                >logged out</a>"""
        )
        for uid in sorted(testUserIds, key=lambda u: userNameById[u]):
            me = "active" if uid == user.get("id", None) else ""
            uname = userNameById[uid]
            urole = userRoleById[uid]
            html.append(
                f"""<a
                        title="{urole}"
                        href="/login?userid={uid}"
                        class="button small {me}"
                    >{uname}</a>"""
            )
        return "\n".join(html)

    def authenticate(self, login=False):
        user = self.user

        if login:
            session.pop("userid", None)
            if self.checkLogin():
                session["userid"] = user["id"]
                return True
            return False

        userId = session.get("userid", None)
        if userId:
            if not self.getUser(userId):
                self.clearUser()
                return False
            return True

        self.clearUser()
        return False

    def authenticated(self):
        user = self.user
        return "id" in user

    def deauthenticate(self):
        Messages = self.Messages
        userId = session.get("userid", None)
        if userId:
            self.getUser(userId)
            self.clearUser()
            Messages.plain(msg=f"LOGOUT successful: user {userId}")
        else:
            Messages.warning(msg="You were not logged in")

        session.pop("userid", None)

    def authorise(self, projectId, editionId, action):
        PROJECTS = self.Projects
        user = self.user
        userId = user.get("id", None)
        authData = self.authData
        userRoleById = self.userRoleById
        projectStatus = PROJECTS.projectStatus
        userProjects = self.userProjects

        userRole = userRoleById.get(userId, None)
        projectRole = (
            None
            if userRole is None
            else userProjects.get(userId, {}).get(projectId, None)
        )
        projectPub = (
            "published" if projectStatus.get(projectId, False) else "unpublished"
        )

        projectRules = authData["projectrules"][projectPub]
        condition = (
            projectRules[userRole] if userRole in projectRules else projectRules[None]
        ).get(action, False)
        permission = condition if type(condition) is bool else projectRole in condition
        return permission

    def isModifiable(self, projectId, editionId):
        return self.authorise(projectId, editionId, "update")

    def checkModifiable(self, projectId, editionId, action):
        if action != "read":
            if not self.isModifiable(projectId, editionId):
                action = "read"
        return action
