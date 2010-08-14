from django.conf import settings
import redis

class Client(object):
    def __init__(self, **kwargs):
        self.connection_settings = {'host': settings.REDIS_HOST, 'port': settings.REDIS_PORT, 'db': 0}

    def redis(self):
        return redis.Redis(**self.connection_settings)

client = Client()
connection = client.redis()
