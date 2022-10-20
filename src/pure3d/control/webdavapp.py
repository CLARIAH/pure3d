import os

from wsgidav.wsgidav_app import WsgiDAVApp

from control.config import Config
from control.messages import Messages


Config = Config(Messages).getConfig()

BASE = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = f"{BASE}/data/3d"

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

app = WsgiDAVApp(config)
