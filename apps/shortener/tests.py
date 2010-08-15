"""
A few tests to check if basic functionalities are working properly
"""

import os
from django.conf import settings
from django.test import TestCase
from django.utils.hashcompat import md5_constructor
from connect_redis import get_client
redis_ob = get_client()

class FunctionalityTest(TestCase):
    # no fixtures to load

    def test_register(self):
        response = self.client.get('/')
        self.failUnlessEqual(response.status_code, 200)
        response = self.client.post('/_register/', {'email': 'yash888@gmail.com', 'password': '123456'}, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.redirect_chain, [('http://testserver/', 302)])
        self.assertEquals(True, redis_ob.exists("user:email:%s" %md5_constructor('yash888@gmail.com').hexdigest()))
        # cant assert the user:1 because redis might already have a user:1
        # and we dont clear redis data 

    def test_login(self):
        response = self.client.post('/_login/', {'email': 'yash888@gmail.com', 'password': '123456'}, follow=True)
        self.assertEquals(response.status_code, 200)
        # need to assure some text from logged in home
        self.assertContains(response, "")
        
    def test_shorten_url(self):
        response = self.client.get('/shorten_url/', {'url': 'http://www.google.com/'})
        self.assertEquals(response.status_code, 200)
        # need to check the db if write succeded
    
    def test_file_upload(self):
        f = open(os.path.join(settings.MEDIA_ROOT, 'facebox', 'stairs.jpg'))
        response = self.client.post('/file_upload/', {'file': f})
        f.close()
        self.assertEquals(response.status_code, 200)
        
    def test_settings(self):
        response = self.client.get('/_settings/')
        self.assertEquals(response.status_code, 404)
        