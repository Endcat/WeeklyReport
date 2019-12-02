from flask import (
    Blueprint,
    request,
    session,
)
from flask_restful import Api, Resource

from utils import *
from models import *
from .decorators import *

import time
api_users = Blueprint('api_users', __name__)
api = Api(api_users)


@api.resource('/report')
class Report(Resource):
    @api_response
    @authed
    @make_serializable(Reports)
    def get(self):
        args = request.args
        author, week = [args.get(i) for i in ['author', 'week']]
        if not author:
            author = session['id']
        if not week:
            week = get_current_week()
        if not is_visible(author, week):
            raise ApiError("Invisible")
        f = (Reports.author_id == author) & (Reports.week == week)
        return Reports.query.filter(f).first()

    @api_response
    @authed
    def post(self):
        if time.strftime('%w', time.localtime(time.time())) != '0':
            raise ApiError("Only Sunday")
        author = session['id']
        content = request.form.get('content')
        if not content_safe(content):
            raise ApiError("Unsafe Content Detected")
        week = get_current_week()
        report = Reports.query.filter_by(author_id=author, week=week).first()
        if not report:
            db.session.add(Reports(
                author_id=author, week=week
            ))
        report.content = content
        db.session.commit()
        db.session.close()
        return None
