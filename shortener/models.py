# nope we're using redis :)
# mimic a django like model with some methods to fetch data

import time
from connect_redis import get_client
redis_ob = get_client()

class DoesNotExist(Exception):
    pass

class UrlModel(object):
    key_prefix = "url:"
    key_counter = "counter:url"

    def __init__(self, url_data={}):
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

    def save(self):
        url_id = redis_ob.incr(self.key_counter)
        # if url id is less than 6000 set to 6000 so that they appear better
        if url_id < 14000: url_id = self.set_counter_url()
        while redis_ob.hexists(self.key_prefix+str(url_id), "url"):
            url_id = redis_ob.incr(self.key_counter)
        self.id = url_id
        redis_ob.hmset(self.key_prefix+str(url_id), {'url' : self.url, 
                                                    'hits' : self.hits,
                                                 'is_file' : self.is_file,
                                               'created_at': self.created_at})

