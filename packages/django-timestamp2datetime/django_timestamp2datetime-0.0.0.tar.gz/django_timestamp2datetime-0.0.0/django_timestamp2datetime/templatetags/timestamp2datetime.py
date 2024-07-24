from datetime import datetime

from django.template import Library

register = Library()

@register.filter
def timestamp2datetime(timestamp):
    if timestamp:
        return datetime.fromtimestamp(timestamp)
