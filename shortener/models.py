# nope we're using redis :)
# mimic a django like model with some methods to fetch data

class UrlModel(object):
    key_prefix = "url:"
    key_counter = "counter:url"

    def __init__(self, url_data={}):
        self.url = url_data.get('url', None)
        self.hits = url_data.get('hits', 0)
        self.created_at = url_data.get('created_at', time.time()+7*60*60)
        self.is_file = url_data.get('is_file', False)


