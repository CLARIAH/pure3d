from pymongo import MongoClient

from control.helpers.generic import AttrDict


class Mongo:
    def __init__(self, Config, Messages):
        self.Config = Config
        self.Messages = Messages
        self.client = None
        self.mongo = None
        self.database = Config.database

    def connect(self):
        Config = self.Config
        Messages = self.Messages
        client = self.client
        mongo = self.mongo
        database = self.database

        if mongo is None:
            try:
                Messages.debug(logmsg=f"{Config.mongoHost=} {Config.mongoPort=}")
                client = MongoClient(Config.mongoHost, Config.mongoPort, username=Config.mongoUser, password=Config.mongoPassword)
                mongo = client[database]
            except Exception as e:
                self.Messages.error(
                    msg="Could not connect to the database",
                    logmsg=f"Mongo connection: `{e}`",
                )
            self.client = client
            self.mongo = mongo

    def disconnect(self):
        client = self.client

        if client:
            client.close()

        self.client = None
        self.mongo = None

    def checkCollection(self, table, reset=False):
        Messages = self.Messages

        self.connect()
        client = self.client
        mongo = self.mongo

        if mongo[table] is None:
            try:
                client.create_collection(table)
            except Exception as e:
                Messages.error(
                    msg="Database action",
                    logmsg=f"Cannot create collection: `{table}`: {e}",
                )
        if reset:
            try:
                self.execute(table, "delete_many", {})
            except Exception as e:
                Messages.error(
                    msg="Database action",
                    logmsg=f"Cannot clear collection: `{table}`: {e}",
                )

    def getRecord(self, table, **criteria):
        result = self.execute(table, "find_one", criteria, {})
        if result is None:
            result = {}
        return AttrDict(result)

    def execute(self, table, command, *args, **kwargs):
        Messages = self.Messages

        self.connect()
        mongo = self.mongo

        method = getattr(mongo[table], command, None)
        result = None

        if method is None:
            Messages.error(
                msg="Database action", logmsg=f"Unknown Mongo command: `{method}`"
            )
        try:
            result = method(*args, **kwargs)
        except Exception as e:
            Messages.error(
                msg="Database action",
                logmsg=f"Executing Mongo command db.{table}.{command}: {e}",
            )
            result = None

        return result
