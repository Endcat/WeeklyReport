import functools
from flask import session, redirect
from models import Users

def authed(func):
    @functools.wraps(func)
    def _authed(*args, **kwargs):
        if 'id' not in session.keys():
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