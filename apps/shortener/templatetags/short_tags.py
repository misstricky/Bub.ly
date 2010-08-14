import datetime
from django.template import Library, Node, TemplateSyntaxError, Variable

register = Library()

""" convert timestamp into python datetime 2008-07-17T09:24:17Z """
@register.filter
def to_datetime(timestamp):
    return datetime.datetime.fromtimestamp(float(timestamp)).strftime("%Y-%m-%dT%H:%M:%SZ")
