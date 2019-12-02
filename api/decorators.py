import functools

from flask import session, redirect

from models import Users, db
from utils import ApiError


def is_authed():
    return 'id' in session.keys()


def api_response(func):
    @functools.wraps(func)
    def _api_response(*args, **kwargs):
        result = "success"
        message = ""
        data = None
        try:
            data = func(*args, **kwargs)
        except ApiError as e:
            result = "failed"
            message = e.message
        # except:
        #     result = "error"
        return {
            "result": result,
            "message": message,
            "data": data
        }

    return _api_response


def authed(func):
    @functools.wraps(func)
    def _authed(*args, **kwargs):
        if not is_authed():
            raise ApiError("Unauthorized")
        return func(*args, **kwargs)
    return _authed


def admin_only(func):
    @functools.wraps(func)
    def _admin_only(*args, **kwargs):
        if Users.query.filter_by(
                id=session['id'], is_admin=1
        ).first() is None:
            raise ApiError("Unauthorized")
        return func(*args, **kwargs)

    return _admin_only


def make_serializable(model: db.Model):
    def _make_serializable(func):
        @functools.wraps(func)
        def __make_serializable(*args, **kwargs):
            keys = [
                i for i in
                set(dir(model)) - set(dir(db.Model))
                if not i.startswith('_')
            ]
            result = func(*args, **kwargs)
            if not result:
                return None
            result = [{i: str(getattr(o, i)) for i in keys} for o in result] \
                if type(result) == list else \
                {i: str(getattr(result, i)) for i in keys}
            return result

        return __make_serializable

    return _make_serializable
