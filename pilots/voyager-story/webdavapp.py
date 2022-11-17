import os

# from cheroot import wsgi
from wsgidav.wsgidav_app import WsgiDAVApp


BASE = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = f"{BASE}/data/3d"

config = {
    "provider_mapping": {
        "/data/": {
            "root": DATA_DIR,
            "readonly": False,
        },
    },
    "simple_dc": {"user_mapping": {"*": True}},
    "verbose": 1,
}


def getWebdavApp():
    return WsgiDAVApp(config)
