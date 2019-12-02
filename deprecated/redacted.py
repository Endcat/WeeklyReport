

@app.route("/view/user/<author_id>/<week>", methods=['GET'])
@app.route("/view/user/<author_id>", methods=['GET'])
@authed
def person_view(author_id, week=None):
    author = Users.query.filter_by(id=author_id).first()
    if not author:
        return "没有!"
    if week:
        report = Reports.query.filter_by(author_id=author_id, week=week).first()
    else:
        report = None
    all_reports = Reports.query.filter_by(author_id=author_id)
    return render_template('user_view.html', report=report, all_reports=all_reports, author=author)


@app.route("/view/week/<week>/<author_id>")
@app.route("/view/week/<week>")
@authed
def week_view(week, author_id=None):
    all_author = db.session.query(Users.id, Users.name).join(Reports).filter(
        Users.id == Reports.author_id,
        Reports.week == week
    )
    if not all_author:
        return "没有!"
    if author_id:
        report = Reports.query.filter_by(week=week, author_id=author_id).first()
        if not report:
            return "没有!"
        author = Users.query.filter_by(id=author_id).first()
    else:
        author = None
        report = None
    return render_template('week_view.html', all_author=all_author, report=report, author=author, week=week)


@app.route("/submit", methods=['GET', 'POST'])
@authed
def submit():
    if not submit_time():
        return 'only sunday'

    week = get_current_week()
    id = session['id']
    user = Users.query.filter_by(id=id).first()
    old_report = Reports.query.filter_by(author_id=id, week=week).first()

    if request.method == 'GET':
        content = ''
        if old_report:
            content = old_report.content
        return render_template('submit.html', user=user, content=content, week=week)

    if request.method == 'POST':
        content = request.form.get('content')
        is_valid = content_safe(content)
        if not is_valid:
            return 'invalid'
        if old_report:
            old_report.content = content
        else:
            report = Reports(author_id=id, week=week, content=content)
            db.session.add(report)
        db.session.commit()
        db.session.close()
        return redirect('/submit')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        info = ''
        return render_template('login.html', info=info)
    if request.method == 'POST':
        name = request.form.get('username')
        passwd = request.form.get('passwd')
        user = auth.simple_auth(name, passwd)
        if not user:
            info = "wrong!"
            return render_template('login.html', info=info)
        session['id'] = user.id
        session['name'] = user.name
        return redirect('/index')


@app.route("/index", methods=['GET'])
@app.route("/", methods=['GET'])
def index():
    reports = Reports.query.all()
    users = Users.query.filter_by(is_hidden=False).order_by(Users.direction, Users.level)
    users_report_stat = []
    for user in users:
        user_weeks = []
        user_reports_stat = []
        for report in reports:
            if user.id == report.author_id:
                user_weeks.append(report.week)
        for recent_week in get_recent_weeks():
            flag = False
            for report_week in user_weeks:
                if recent_week == report_week:
                    flag = report_week
                    break
            user_reports_stat.append(flag)
        users_report_stat.append({'info': user, 'stat': user_reports_stat})
    return render_template('index.html', users_report_stat=users_report_stat, recent_weeks=recent_weeks)


@app.route("/logout", methods=['GET'])
def logout():
    session.pop('name', None)
    session.pop('id', None)
    return redirect("/login")


@app.route("/manage_info")
@authed
@admin_only
def update_info():
    users = Users.query.filter_by().order_by(Users.direction, Users.level).all()
    configs = Configs.query.filter_by(id=1).first()
    return render_template('manage_info.html', users=users, configs=configs)


@app.route("/modify", methods=['POST'])
@authed
@admin_only
def modify():
    id = int(request.form['id'])
    name = request.form['name']
    direction = request.form['direction']
    level = request.form['level']
    token = request.form['token']
    hidden = int(request.form['is_hidden'])
    admin = int(request.form['is_admin'])
    banned = int(request.form['is_banned'])
    rs = db.session.query(Users).filter_by(id=id)
    rs.update({
        Users.name: name,
        Users.direction: direction,
        Users.level: level,
        Users.token: token,
        Users.is_hidden: hidden,
        Users.is_banned: banned,
        Users.is_admin: admin
    })
    db.session.commit()
    return redirect('/manage_info')


@app.route("/add", methods=['POST'])
@authed
@admin_only
def add():
    name = request.form['name']
    direction = request.form['direction']
    level = request.form['level']
    token = request.form['token']
    hidden = int(request.form['is_hidden'])
    admin = int(request.form['is_admin'])
    banned = int(request.form['is_banned'])
    new_user = Users(name=name, direction=direction, level=level, token=token,
                     is_hidden=hidden, is_banned=banned, is_admin=admin)
    rs = db.session.add(new_user)
    db.session.commit()
    return redirect('/manage_info')


@app.route("/modify_config", methods=['POST'])
@authed
@admin_only
def modify_config():
    begin_week = int(request.form['begin_week'])
    skip_weeks = request.form['skip_weeks']
    record = Configs.query.filter_by(id=1).first()
    if not record:
        record = Configs(id=1, begin_week=begin_week, skip_weeks=skip_weeks)
        db.session.add(record)
        db.session.commit()
    else:
        db.session.query(Configs).filter_by(id=1).update({Configs.begin_week: begin_week,
                                                          Configs.skip_weeks: skip_weeks})
        db.session.commit()
    return redirect('/manage_info')
