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
        self.session_key = self._get_new_session_key()
        return self.save()

    def save(self):
        key = "s:%s" % self.session_key
        func = redis_ob.set
        result = func(key, self.encode(self._get_session(no_load=must_create)))
        redis_ob.expire(key, self.get_expiry_age())

    def delete(self):
        pass

