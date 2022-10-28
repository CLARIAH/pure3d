from control.helpers.generic import AttrDict


class Users:
    def __init__(self, Config, Messages, Mongo):
        self.Config = Config
        self.Messages = Messages
        self.Mongo = Mongo

    def wrapTestUsers(self, userActive):
        Config = self.Config
        Mongo = self.Mongo

        if not Config.testMode:
            return ""

        def wrap(title, href, cls, text):
            return (
                f'<a title="{title}" href="{href}" class="button small {cls}">'
                f'{text}</a>'
            )

        active = "active" if userActive is None else ""

        html = []
        html.append(wrap("if not logged in", "/logout", active, "logged out"))

        for user in sorted(Mongo.execute("users", "find"), key=lambda r: r["name"]):
            user = AttrDict(user)

            active = "active" if str(user._id) == userActive else ""
            html.append(wrap(user.role, f"/login?userid={user._id}", active, user.name))

        return "\n".join(html)
