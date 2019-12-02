from flask import request, Blueprint
from flask_restful import Resource, Api

from utils import *
from models import *
from .decorators import *

api_admin = Blueprint(
    'api_admin', __name__
)
_api_admin = Api(api_admin)

@_api_admin.resource('/user')
class Administrate(Resource):
    @staticmethod
    def extract_user(form):
        return {
            "name": form['name'],
            "direction": form['direction'],
            "level": form['level'],
            "token": form['token'],
            "hidden": int(form['is_hidden']),
            "admin": int(form['is_admin']),
            "banned": int(form['is_banned']),
        }

    @api_response
    @authed
    @admin_only
    @make_serializable(Users)
    def get(self):
        return Users.query.filter_by(
            #TODO: filters
        ).order_by(Users.direction, Users.level).all()

    @api_response
    @authed
    @admin_only
    def update(self):
        try:
            user = self.extract_user(request.form)
        except IndexError:
            raise ApiError("Insufficient Arguments")
        user_id = request.form.get('id')
        user_row = db.session.query(Users).filter_by(id=user_id)
        if not user_row:
            raise ApiError("User Doesn't Exist")
        user_row.update({getattr(Users, k): user[v] for k, v in user.items()})
        return None

    @api_response
    @authed
    @admin_only
    def put(self):
        try:
            user = self.extract_user(request.form)
        except IndexError:
            raise ApiError("Insufficient Arguments")
        user_row = db.session.query(Users).filter_by(name=user['name'], level=user['level']).first()
        if user_row:
            raise ApiError(f"A user named {user['name']} of grade {user['level']} already existed")
        db.session.add(Users(**{getattr(Users, k): user[v] for k, v in user.items()}))
        db.session.commit()

    @api_response
    @authed
    @admin_only
    def delete(self):
        user_id = request.form.get('id')
        token = request.form.get('token')
        user_row = db.session.query(Users).filter_by(id=user_id, token=token).first()
        if not user_row:
            raise ApiError("User_id or Token Error")
        db.session.delete(user_row)
        db.session.commit()
        return None


@_api_admin.resource('/config')
class Configure(Resource):
    @api_response
    @authed
    @admin_only
    @make_serializable(Configs)
    def get(self):
        return Configs.query.filter_by(id=1).first()

    @api_response
    @authed
    @admin_only
    def post(self):
        begin_week = int(request.form['begin_week'])
        skip_weeks = request.form['skip_weeks']
        record = Configs.query.first()
        if not record:
            db.session.add(Configs(
                begin_week=begin_week, skip_weeks=skip_weeks
            ))
            db.session.commit()
        else:
            Configs.query.update({
                Configs.begin_week: begin_week,
                Configs.skip_weeks: skip_weeks
            })
            db.session.commit()
        return None
