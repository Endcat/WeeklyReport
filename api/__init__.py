from flask import request, Blueprint
from flask_restful import Api

from .decorators import *
from models import *
from utils import *

from .admin import api_admin
from .users import api_users

api_root = Blueprint('_api_root', __name__)
_api_root = Api(api_root)


@api_root.route('/login')
def api_login():
    username = request.form.get('username') or request.args.get('username')
    password = request.form.get('passwd') or request.args.get('passwd')
    if not username or not password:
        return _api_root.make_response({
            'result': 'failed',
            'message': 'username={}&passwd={}',
            'data': None
        }, 200)
    user = make_serializable(Users)(
        lambda: Users.query.filter_by(name=username, token=password).first()
    )()
    if not user:
        return _api_root.make_response({
            'result': 'failed',
            'message': 'Username or Password incorrect',
            'data': None
        }, 200)
    if user['is_banned'] == '1':
        return _api_root.make_response({
            'result': 'failed',
            'message': 'User banned',
            'data': None
        })
    user.pop('token')
    session['id'] = user['id']
    session['name'] = user['name']
    return _api_root.make_response({
        'result': 'success', 'message': None, 'data': user
    }, 200)


@api_root.route('/logout')
def api_logout():
    session.pop('id')
    session.pop('name')
    return _api_root.make_response({
        'result': 'success', 'message': None, 'data': None
    }, 200)
