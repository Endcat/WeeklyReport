import functools
import time

from flask import session, redirect

from models import Users, Configs


def authed(func):
    @functools.wraps(func)
    def _authed(*args, **kwargs):
        if session.get('id') is None:
            return redirect('/login')
        return func(*args, **kwargs)

    return _authed


def admin_only(func):
    @functools.wraps(func)
    def _admin_only(*args, **kwargs):
        if Users.query.filter_by(id=session['id'], is_admin=1).first() is not None:
            return func(*args, **kwargs)
        return redirect('/index')

    return _admin_only


def submit_time():
    # return True
    return time.strftime('%w', time.localtime(time.time())) == '0'


def content_safe(content):
    return True


def get_recent_weeks():
    week_now = getweek()
    record = Configs.query.filter_by(id=1).first()
    try:
        begin_week = int(record.begin_week)
    except:
        begin_week = week_now
    try:
        skip_weeks = [int(i) for i in record.skip_weeks.split(',')]
    except:
        skip_weeks = []
    recent_weeks = []
    for week in range(begin_week, week_now + 1):
        if week in skip_weeks:
            continue
        recent_weeks.append(week)
    return recent_weeks[-6:]


def getweek():
    week = time.strftime('%Y%U', time.localtime(time.time()))
    return int(week)
