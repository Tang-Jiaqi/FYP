from flask import Blueprint,render_template, request, redirect, url_for, session
from app.models.base import db
from app.models.member import Member
from sqlalchemy import and_, or_, not_
from app.models.contribution import Contribution
from app.models.student import Student
from app.models.team import Team
from app.models.teacher import Teacher

memberBP = Blueprint('member', __name__, template_folder='templates', static_folder='static')


@memberBP.route('/', methods=['GET','POST'])
def calculate_contribution():
    _course_id = session.get('course_id')
    _email = session.get('email')
    teacher = Teacher.query.filter(Teacher.email == session.get("email")).first()
    students = Student.query.filter(Student.course_id == _course_id)
    if request.method == 'GET':
        return render_template('calculate_contribution.html', teacher=teacher)
    else:
        for student in students:
            submission_items = Contribution.query.filter(and_(Contribution.course_id == _course_id, Contribution.s_email == student.email))
            overall_contribution = 0
            for submission_item in submission_items:
                overall_contribution += submission_item.percentage * submission_item.contribution
            with db.auto_commit():
                member = Member.query.filter(Member.email == student.email).first()
                # 数据库的insert操作
                member.contribution = overall_contribution
                db.session.commit()
        return render_template('calculate_contribution.html', teacher=teacher)


@memberBP.route('/vote_leader', methods=['GET', 'POST'])
def vote_leader():
    _course_id = session.get('course_id')
    _email = session.get('email')
    student = Student.query.filter(Student.email == _email).first()
    _team_id = Team.query.filter(and_(Team.course_id == _course_id, Team.student_email == _email)).first().team_id
    members = Member.query.filter(and_(Member.team_id == _team_id, Member.course_id == _course_id))
    method = Team.query.filter(Team.course_id == _course_id).first().method
    if request.method == 'GET':
        print(members.all(),method)
        return render_template('vote_leader.html', members=members, student=student,method=method)
    else:
        name = request.form.get('check')
        member = Member.query.filter(and_(Member.team_id == _team_id, Member.name == name)).first()
        member.vote_number += 1
        db.session.commit()
        return render_template('vote_leader.html', members=members, student=student,method=method)


