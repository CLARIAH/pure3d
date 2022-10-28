from flask import request, session

from control.helpers.generic import AttrDict


class Auth:
    def __init__(self, Config, Messages, Mongo, Users, Content):
        self.Config = Config
        self.Messages = Messages
        self.Mongo = Mongo
        self.Users = Users
        self.Content = Content
        self.user = AttrDict()

    def clearUser(self):
        user = self.user
        user.clear()

    def getUser(self, userId):
        Messages = self.Messages
        Mongo = self.Mongo
        user = self.user

        user.clear()
        record = Mongo.getRecord("users", _id=userId)
        if record:
            user.id = userId
            user.name = record.name
            user.role = record.role
            result = True
        else:
            Messages.warning(msg="Unknown user", logmsg=f"Unknown user {userId}")
            result = False
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

    def authenticate(self, login=False):
        user = self.user

        if login:
            session.pop("userid", None)
            if self.checkLogin():
                session["userid"] = user.id
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
            self.clearUser()
            Messages.plain(msg="logged out", logmsg=f"LOGOUT successful: user {userId}")
        else:
            Messages.warning(msg="You were not logged in")

        session.pop("userid", None)

    def authorise(self, action, project=None, edition=None, byName=False):
        Config = self.Config
        Mongo = self.Mongo

        user = self.user

        if project is not None:
            projectId = (
                Mongo.getRecord("projects", name=project).projectId
                if byName
                else project
            )
        if edition is not None:
            editionId = (
                Mongo.getRecord("editions", name=edition).editionId
                if byName
                else edition
            )

        if projectId is None:
            projectId = Mongo.getRecord("editions", _id=editionId).projectId

        projectRole = Mongo.getRecord(
            "projectUsers", projectId=projectId, userId=user._id
        ).role

        projectPub = Mongo.getRecord("projects", _id=projectId).isPublished

        projectRules = Config.auth.projectrules[projectPub]
        condition = (
            projectRules[user.role] if user.role in projectRules else projectRules[None]
        ).get(action, False)
        permission = condition if type(condition) is bool else projectRole in condition
        return permission

    def isModifiable(self, projectId, editionId):
        return self.authorise("edit", project=projectId, edition=editionId)

    def checkModifiable(self, projectId, editionId, action):
        if action != "view":
            if not self.isModifiable(projectId, editionId):
                action = "view"
        return action
