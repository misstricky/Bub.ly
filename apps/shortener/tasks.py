import os, sys
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CURRENT_PATH.rstrip('apps/shortener/'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import datetime, boto
from django.conf import settings
from models import *
from connect_redis import get_client
redis_ob = get_client()

from boto.s3.connection import S3Connection
from boto.s3.key import Key

conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
bucket = conn.get_bucket(settings.AMAZON_MEDIA_BUCKET)
k = Key(bucket)

class FileUpload(object):
    queue="fileupload"

    @staticmethod
    def perform(url_id):
        # pass a url_id and the file associated with that entry will be 
        # uploaded to S3
        url_object = UrlModel.get_by_id(url_id=int(url_id))
        file_c = settings.MEDIA_ROOT+"static/files/"+url_object.file_name
        k.key = url_object.file_name
        k.set_contents_from_filename(file_c, policy='public-read')

class FileDelete(object):
    queue = "filedelete"

    @staticmethod
    def perform(url_id):
        url_object = UrlModel.get_by_id(url_id=int(url_id))
        bucket.delete_key(url_object.filename)

