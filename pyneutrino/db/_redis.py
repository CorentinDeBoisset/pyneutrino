from flask import Flask
from redis import Redis


class RedisEngine:
    def __init__(self):
        self.connexion = None

    def init_app(self, app: Flask):
        uri = app.config["REDIS_URI"]
        if not uri:
            raise Exception("A REDIS_URI configuration key is required")

        self.connexion = Redis.from_url(uri)


redis = RedisEngine()
