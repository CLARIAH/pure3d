import typing as t

if t.TYPE_CHECKING:
    from _typeshed.wsgi import StartResponse
    from _typeshed.wsgi import WSGIApplication
    from _typeshed.wsgi import WSGIEnvironment


class DispatchWebdav:
    """Leave the url intact after dispatching.

    This is like DispatcherMiddleware,
    but after dispatching the full url is passed to
    the chosen app, instead of removing the prefix that
    corresponds with the selected mount.
    """

    def __init__(
        self,
        app: "WSGIApplication",
        webdavPrefix: str,
        webdavApp: "WSGIApplication",
    ) -> None:
        self.app = app
        self.webdavPrefix = webdavPrefix
        self.webdavApp = webdavApp

    def __call__(
        self, environ: "WSGIEnvironment", start_response: "StartResponse"
    ) -> t.Iterable[bytes]:
        app = self.app
        webdavPrefix = self.webdavPrefix
        webdavApp = self.webdavApp

        url = environ.get("PATH_INFO", "")
        aimedAtWebdav = url.startswith(webdavPrefix)

        theApp = app

        if aimedAtWebdav:
            environ["PATH_INFO"] = f"/auth{url}"
            with app.request_context(environ) as ctx:
                ctx.push()
                authorized = app.dispatch_request()
                ctx.pop()
            print(f"Dispatcher: {authorized=}")
            if authorized:
                environ["PATH_INFO"] = url
                theApp = webdavApp
            else:
                environ["PATH_INFO"] = f"/no{url}"

        print(f"{theApp=}")
        return theApp(environ, start_response)
