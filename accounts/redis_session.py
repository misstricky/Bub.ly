# since redis is the only datastore writing a sessionStore class 
# to store sessions in redis

from django.conf import settings
from django.utils.encoding import force_unicode
from django.contrib.sessions.backends.base import SessionBase, CreateError
from connect_redis import get_client

class SessionStore(SessionBase):
    """
    store user session in redis with key prefix s:
    """
    def load(self):
        pass

    def create(self):
        pass

    def save(self):
        pass

    def delete(self):
        pass

