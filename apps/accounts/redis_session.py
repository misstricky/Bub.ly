# since redis is the only datastorewe use, writing a sessionStore class 
# to store sessions in redis
# inspired from http://hg.gomaa.us/agdj/file/tip/agdj/lib/redis_session_backend.py

from django.conf import settings
from django.utils.encoding import force_unicode
from django.contrib.sessions.backends.base import SessionBase, CreateError
from connect_redis import get_client
redis_ob = get_client()

class SessionStore(SessionBase):
    """
    store user session in redis with key prefix s:
    """
    def load(self):
        session_data = redis_ob.get("s:"+self.session_key)
        if session_data is not None:
            return self.decode(force_unicode(session_data))
        self.create()
        return {}

    def create(self):
        while True:
            self.session_key = self._get_new_session_key()
            try:
                self.save(must_create=True)
            except CreateError:
                # Would be raised if the key wasn't unique
                continue
            self.modified = True
            return

    def save(self, must_create=False):
        if must_create:
            func = redis_ob.setnx
        else:
            func = redis_ob.set
        key = "s:%s" % self.session_key
        result = func(key, self.encode(self._get_session(no_load=must_create)))
        if must_create and result is None:
            raise CreateError
        redis_ob.expire(key, self.get_expiry_age())
        self.modified = False

    def exists(self, session_key):
        if redis_ob.exists("s:%s" % session_key):
            return True
        return False

    def delete(self, session_key=None):
        if session_key is None:
            if self._session_key is None:
                return
            session_key = self._session_key
        redis_ob.delete("s:"+session_key)


