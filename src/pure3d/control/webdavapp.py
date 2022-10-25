import os

from wsgidav.wsgidav_app import WsgiDAVApp

from control.config import Config
from control.messages import Messages


Config = Config(Messages).getConfig()

BASE = os.path.dirname(os.path.dirname(__file__))

WEBDAV_METHODS = dict(
    HEAD="read",
    GET="read",
    PUT="update",
    POST="update",
    OPTIONS="read",
    TRACE="read",
    DELETE="update",
    PROPFIND="read",
    PROPPATCH="update",
    MKCOL="update",
    COPY="update",
    MOVE="update",
    LOCK="update",
    UNLOCK="update",
)


config = {
    "provider_mapping": {
        "/webdav/": {
            "root": Config.dataDir,
            "readonly": False,
        },
    },
    "simple_dc": {"user_mapping": {"*": True}},
    "verbose": 1,
}


def getWebdavApp():
    return WsgiDAVApp(config)
