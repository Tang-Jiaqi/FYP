from flask import Blueprint,render_template, request, session
from app.models.base import db
from app.models.member import Member
from sqlalchemy import and_, or_, not_
from app.models.contribution import Contribution
from app.models.student import Student
from app.models.team import Team
from app.models.assessment import Assessment

assessmentBP = Blueprint('assessment', __name__)


@assessmentBP.route('', methods=['GET','POST'])
def assessment_leader():
    _course_id = session.get('course_id')
    _email = session.get('email')
    student = Student.query.filter(Student.email == _email).first()
    team_id = Team.query.filter(and_(Team.course_id == _course_id, Team.student_email == _email)).first().team_id
    member = Member.query.filter(and_(Member.vote_number >= 2, Member.team_id == team_id)).first()
    method = Team.query.filter(Team.course_id == _course_id).first().method
    if request.method == 'GET':
        return render_template('assessment_leader.html', member=member, student=student,method=method)
    else:
        assessment_number = 0
        assessment_value = request.form.get('select2')
        if assessment_value == 'very_good':
            assessment_number = 2
        elif assessment_value == 'good':
            assessment_number = 1
        elif assessment_value == 'fair':
            assessment_number = 0
        elif assessment_value == 'bad':
            assessment_number = -1
        else:
            assessment_number = -2
        with db.auto_commit():
            assessment_number = Assessment(assessment_number, member.email)
            # 数据库的insert操作
            db.session.add(assessment_number)
        return render_template('assessment_leader.html', member=member, student=student,method=method)
