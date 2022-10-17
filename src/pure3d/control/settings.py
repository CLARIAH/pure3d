import os
import sys

from helpers.files import readYaml, readPath
from helpers.messages import error
from helpers.generic import AttrDict


VERSION_FILE = "version.txt"


class Settings:
    def __init__(self):
        self.good = False
        self.config = AttrDict()
        self.checkEnv()
        if not self.good:
            error("Aborting ...")
            sys.exit(1)

    def checkEnv(self):
        repoDir = os.environ.get("repodir", None)
        if repoDir is None:
            error("Environment variable `repodir` not defined")
            error("Don't know where I must be running")
            return

        config = self.config
        config.repoDir = repoDir
        yamlDir = f"{repoDir}/src/pure3d/control/yaml"
        config.yamlDir = yamlDir
        staticDir = f"{repoDir}/src/pure3d/static"
        config.staticDir = staticDir

        versionPath = f"{repoDir}/src/{VERSION_FILE}"
        versionInfo = readPath(versionPath)
        if not versionInfo:
            error(f"Cannot find version info in {versionPath}")
            return

        config.versionInfo = versionInfo

        settings = readYaml(f"{yamlDir}/settings.yaml")
        if settings is None:
            error("Cannot read settings.yaml in {yamlDir}")
            return
        for (k, v) in settings.items():
            config[k] = v

        secretFileLoc = os.environ.get("SECRET_FILE", None)
        if secretFileLoc is None:
            error("Environment variable `SECRET_FILE` not defined")
            return

        if not os.path.exists(secretFileLoc):
            error(f"Missing secret file for sessions: {secretFileLoc}")
            error("Create that file with contents a random string like this:")
            error("fjOL901Mc3XZy8dcbBnOxNwZsOIBlul")
            error("But do not choose this one.")
            error("Use your password manager to create a random one.")

        dataDir = os.environ.get("DATA_DIR", None)
        if dataDir is None:
            error("Environment variable `DATA_DIR` not defined")
            return

        config.dataDir = dataDir
        if not os.path.exists(dataDir):
            error(f"Data directory does not exist: {dataDir}")
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
        self.good = True

    def getConfig(self):
        return self.config
