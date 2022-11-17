import os
from cheroot import wsgi
from wsgidav.wsgidav_app import WsgiDAVApp

HOST = int(os.environ["PILOT_HOST"])
PORT = int(os.environ["PILOT_PORT"])

BASE = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = f"{BASE}/data/3d"

config = {
    "host": HOST,
    "port": PORT,
    "provider_mapping": {
        "/": DATA_DIR,
    },
    "simple_dc": {"user_mapping": {"*": True}},
    "verbose": 1,
}

app = WsgiDAVApp(config)
server_args = {
    "bind_addr": (config["host"], config["port"]),
    "wsgi_app": app,
}
server = wsgi.Server(**server_args)
server.start()
