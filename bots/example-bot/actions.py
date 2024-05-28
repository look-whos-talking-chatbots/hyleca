"""
File contains the generic and common action functions.

The functions under this file should always expect "user" data as their input.
They should always return a single variable, but the type of the variable depends on your application.
"""

from datetime import datetime
from dateutil import parser


def get_on_hold(user):
    try:
        timedelta = datetime.now() - parser.isoparse(user['progress']['onhold']['start'])
        return user['progress']['onhold']['duration'] > timedelta.total_seconds()
    except:
        return False


def get_now_time(user):
    return datetime.now().isoformat()


def get_true(user):
    return True
