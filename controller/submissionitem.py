from flask import Blueprint,render_template, request, url_for, redirect,session,flash,jsonify
from app.models.base import db
from app.models.submissionitem import Submissionitem
from app.models.teacher import Teacher
from app.models.contribution import Contribution

submissionitemBP = Blueprint('submissionitem', __name__, template_folder='templates', static_folder='static')


@submissionitemBP.route('/', methods=['GET', 'POST'])
def display_submission():
    teacher = Teacher.query.filter(Teacher.email == session.get("email")).first()
    submission_items = Submissionitem.query.filter(Submissionitem.course_id == session.get("course_id"))
    total = 0
    for item in submission_items:
        total = total + item.percentage
    if total < 1:
        flash('tip:total percentage < 1 !!!! ,plz check ur input! ')
    if request.method == 'GET':
        return render_template("submission.html", submission_items=submission_items, teacher=teacher)
    else:
        return redirect(url_for('.edit_submission'))


@submissionitemBP.route('/edit_submission', methods=['GET', 'POST'])
def edit_submission():
    teacher = Teacher.query.filter(Teacher.email == session.get("email")).first()
    course_id = session.get('course_id')
    submission_items = Submissionitem.query.filter(Submissionitem.course_id == session.get("course_id"))

    if request.method == 'GET':
        total = 0
        for item in submission_items:
            total = total + item.percentage
        if total < 1:
            flash('tip:total percentage < 1 !!!! ,plz check ur input! ')
        return render_template("edit_submission.html", teacher=teacher,submission_items=submission_items)
    else:
        title = request.form.get('title')
        percentage = request.form.get('percentage')
        total = float(percentage)
        for item in submission_items:
            total = total + item.percentage
        if total > 1:
            flash('tip:total percentage excessed 1 !!!! ,plz check ur input! ')
            return redirect(url_for('.display_submission'))
        with db.auto_commit():
            submission_item = Submissionitem(title, percentage,course_id)
            # 数据库的insert操作
            db.session.add(submission_item)
        return redirect(url_for('.display_submission'))

@submissionitemBP.route('/change_submission', methods=['GET', 'POST'])
def change_submission():
    sid = request.form.get("id")
    title = request.form.get("title")
    percent = request.form.get("percent")

    if not sid or not title or not percent:
        return jsonify({
            "status":0,
            "msg":"no params"
        })


    sid = int(sid)
    submissionitem = Submissionitem.query.filter_by(id=sid).first()
    submission_items = Submissionitem.query.filter(Submissionitem.course_id == session.get("course_id"))
    total = float(percent)
    for item in submission_items:
        if item.id == submissionitem.id:
            continue
        total = total + item.percentage
    if total > 1:
        return jsonify({
            "status": 0,
            "msg": "total percent  >1 "
        })

    submissionitem.title = title
    submissionitem.percentage = percent

    db.session.add(submissionitem)
    db.session.commit()
    return jsonify({
        "status":1
    })