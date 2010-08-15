# nope we're using redis :)
# mimic a django like model with some methods to fetch data

import time
from django.conf import settings
from connect_redis import get_client
from utils import to36
redis_ob = get_client()

class UrlNotSaved(Exception):
    pass

class DoesNotExist(Exception):
    pass

class UrlModel(object):
    key_prefix = "url:"
    key_counter = "counter:url"

    def __init__(self, url_data={}, url_id=None):
        self.id = url_id
        self.url = url_data.get('url', None)
        self.hits = url_data.get('hits', 0)
        self.created_at = url_data.get('created_at', time.time()+7*60*60)
        self.is_file = url_data.get('is_file', False)

    def set_counter_url(self):
        redis_ob.set(self.key_counter, 14000)
        return 14000

    @classmethod
    def get_by_id(self, url_id):
        url_data = redis_ob.hgetall(url_id)
        if not url_data: raise DoesNotExist
        url_data_id = int(url_id.lstrip("url:"))
        return self(url_data=url_data, url_id=url_data_id)

    def get_short_url(self, user=None):
        if not self.id: raise UrlNotSaved
        domain = None
        if user:
            domain = redis_ob.hget("user:%s" %str(user), "custom_domain")
        if not domain: domain = settings.SHORT_URL
        return '%s%s/' %(domain, to36(int(self.id)))

    def save(self, url_id=None):
        if not url_id: url_id = redis_ob.incr(self.key_counter)
        # if url id is less than 14000 set to 14000 so that they appear better
        if url_id < 14000: url_id = self.set_counter_url()
        while redis_ob.hexists(self.key_prefix+str(url_id), "url"):
            url_id = redis_ob.incr(self.key_counter)
        self.id = url_id
        redis_ob.hmset(self.key_prefix+str(url_id), {'url' : self.url, 
                                                    'hits' : self.hits,
                                                 'is_file' : self.is_file,
                                               'created_at': self.created_at})

