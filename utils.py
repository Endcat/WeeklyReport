import time

from flask import session

from models import Configs, Users


class ApiError(Exception):
    def __init__(self, message):
        super().__init__()
        self.message = message


def content_safe(content):
    return True


def get_recent_weeks():
    week_now = get_current_week()
    record = Configs.query.filter_by(id=1).first()
    begin_week = int(record.begin_week)
    skip_weeks = [int(i) for i in record.skip_weeks.split(',')]
    for week in range(begin_week, week_now + 1):
        if week in skip_weeks:
            continue
        yield week


def get_current_week():
    week = time.strftime('%Y%U', time.localtime(time.time()))
    return int(week)


def is_visible(author_id, week):
    author = Users.query.filter_by(id=author_id).first()
    if not author:
        return False
    if author.is_hidden and Users.query.filter_by(
            id=session['id'], is_admin=1
    ).first() is None:
        return False
    #TODO: only present reports that are created recently
    return True
