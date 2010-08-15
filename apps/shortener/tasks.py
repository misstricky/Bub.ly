import os, sys
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CURRENT_PATH.rstrip('apps/shortener/'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import datetime
from django.conf import settings

class FileUpload(object):
    queue="fileupload"

    @staticmethod
    def perform():
        pass

