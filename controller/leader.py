from flask import Blueprint, render_template, request, session
from app.models.base import db
from app.models.leader import Leader
from sqlalchemy import and_, or_, not_
from app.models.student import Student
from app.models.assessment import Assessment
from app.models.teacher import Teacher
from app.models.member import Member

leaderBP = Blueprint('leader', __name__)


@leaderBP.route('', methods=['GET', 'POST'])
def calculate_bonus():
    _course_id = session.get('course_id')
    _email = session.get('email')
    teacher = Teacher.query.filter(Teacher.email == session.get("email")).first()
    members = Member.query.filter(Member.vote_number >= 2)
    if request.method == 'POST':
        for member in members:
            average = 0
            count = 0
            assessments_leader = Assessment.query.filter(Assessment.leader_email == member.email)
            for assessment_leader in assessments_leader:
                average += assessment_leader.assessment_number
                count += 1
            average = average / count
            with db.auto_commit():
                leaders = Leader.query.filter(and_(Leader.email == member.email, Leader.course_id == _course_id)).first()
                # 数据库的insert操作
                leaders.bonus = average
                db.session.commit()
            return render_template('calculate_bonus.html', teacher=teacher)
    else:
        return render_template('calculate_bonus.html', teacher=teacher)