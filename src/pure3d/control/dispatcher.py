import typing as t

if t.TYPE_CHECKING:
    from _typeshed.wsgi import StartResponse
    from _typeshed.wsgi import WSGIApplication
    from _typeshed.wsgi import WSGIEnvironment


class DispatcherMiddleware:
    """Leave the url intact after dispatching.

    This is like DispatcherMiddleware,
    but after dispatching the full url is passed to
    the chosen app, instead of removing the prefix that
    corresponds with the selected mount.
    """

    def __init__(
        self,
        app: "WSGIApplication",
        mounts: t.Optional[t.Dict[str, "WSGIApplication"]] = None,
    ) -> None:
        self.app = app
        self.mounts = mounts or {}

    def __call__(
        self, environ: "WSGIEnvironment", start_response: "StartResponse"
    ) -> t.Iterable[bytes]:
        url = environ.get("PATH_INFO", "")

        app = None

        for mount in self.mounts:
            if url.startswith(mount):
                app = self.mounts[mount]
                break

        if app is None:
            app = self.app
        else:
            environ["PATH_INFO"] = f"/auth{url}"
            with self.app.request_context(environ) as ctx:
                ctx.push()
                authorized = self.app.dispatch_request()
                ctx.pop()
            print(f"Dispatcher: {authorized=}")
            if not authorized:
                environ["PATH_INFO"] = f"/no{url}"
                app = self.app

        return app(environ, start_response)
