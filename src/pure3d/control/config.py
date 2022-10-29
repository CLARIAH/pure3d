import os
import sys
from textwrap import dedent

from control.helpers.files import readYaml, readPath
from control.helpers.generic import AttrDict


VERSION_FILE = "version.txt"


class Config:
    def __init__(self, Messages):
        """All configuration details of the app.

        It is instantiated by a singleton object.

        Parameters
        ----------
        Messages: object
            Singleton instance of `control.messages.Messages`.
        """
        self.Messages = Messages
        self.good = False
        self.config = AttrDict()
        self.checkEnv()

        if not self.good:
            Messages.error(logmsg="Check environment ...")
            sys.exit(1)

    def checkEnv(self):
        Messages = self.Messages

        repoDir = os.environ.get("repodir", None)
        if repoDir is None:
            Messages.error(
                logmsg=dedent(
                    """
                    Environment variable `repodir` not defined
                    Don't know where I must be running
                    """
                )
            )

        config = self.config
        config.repoDir = repoDir
        yamlDir = f"{repoDir}/src/pure3d/control/yaml"
        config.yamlDir = yamlDir
        staticDir = f"{repoDir}/src/pure3d/static"
        config.staticDir = staticDir
        viewerDir = f"{staticDir}/viewers"
        config.viewerDir = viewerDir

        versionPath = f"{repoDir}/src/{VERSION_FILE}"
        versionInfo = readPath(versionPath)
        if not versionInfo:
            Messages.error(logmsg=f"Cannot find version info in {versionPath}")

        config.versionInfo = versionInfo

        settings = readYaml(f"{yamlDir}/settings.yaml")

        if settings is None:
            Messages.error(logmsg="Cannot read settings.yaml in {yamlDir}")
            return

        for (k, v) in settings.items():
            config[k] = v

        authData = readYaml(f"{yamlDir}/authorise.yaml")
        if authData is None:
            Messages.error(logmsg="Cannot read authorise.yaml in {yamlDir}")
            return

        auth = AttrDict()
        config.auth = auth

        for (k, v) in authData.items():
            auth[k] = v

        viewerSettings = readYaml(f"{yamlDir}/viewers.yaml")
        if viewerSettings is None:
            Messages.error(logmsg="Cannot read viewers.yaml in {yamlDir}")
            return

        config.viewers = AttrDict(viewerSettings)

        secretFileLoc = os.environ.get("SECRET_FILE", None)

        if secretFileLoc is None:
            Messages.error(logmsg="Environment variable `SECRET_FILE` not defined")
            return

        if not os.path.exists(secretFileLoc):
            Messages.error(
                logmsg=dedent(
                    f"""
                    Missing secret file for sessions: {secretFileLoc}
                    Create that file with contents a random string like this:
                    fjOL901Mc3XZy8dcbBnOxNwZsOIBlul")
                    But do not choose this one.")
                    Use your password manager to create a random one.
                    """
                )
            )
            return

        dataDir = os.environ.get("DATA_DIR", None)
        if dataDir is None:
            Messages.error(logmsg="Environment variable `DATA_DIR` not defined")
            return

        config.dataDir = dataDir.rstrip("/")
        if not os.path.exists(dataDir):
            Messages.error(logmsg=f"Data directory does not exist: {dataDir}")
            return

        with open(secretFileLoc) as fh:
            config.secret_key = fh.read()

        config.testMode = os.environ["flasktest"] == "test"
        """With test mode enabled.

        This means that there is a row of test users on the interface,
        and that you can log in as one of these users with a single click,
        without any kind of authentication.
        """

        config.debugMode = os.environ["flaskdebug"] == "--debug"
        """With debug mode enabled.

        This means that the unminified, development versions of the javascript libraries
        of the 3D viewers are loaded, instead of the production versions.
        """

        config.mongoUser = os.environ["mongouser"]
        config.mongoPassword = os.environ["mongopassword"]

        self.good = True

    def getConfig(self):
        return self.config
