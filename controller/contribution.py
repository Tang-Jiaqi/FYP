from flask import Blueprint,render_template, request, url_for, redirect, session
from app.models.base import db
from sqlalchemy import and_, or_, not_, null
from app.models.submissionitem import Submissionitem
from app.models.contribution import Contribution
from app.models.team import Team
from app.models.member import Member
from app.models.student import Student

contributionBP = Blueprint('contribution', __name__, template_folder='templates', static_folder='static')


@contributionBP.route('/', methods=['GET', 'POST'])
def set_contribution():
    _course_id = session.get('course_id')
    _email = session.get('email')
    student = Student.query.filter(Student.email == _email).first()
    submission_items = Submissionitem.query.filter(Submissionitem.course_id == _course_id)
    _team_id = Team.query.filter(Team.student_email == _email).first().team_id
    members = Member.query.filter(and_(Member.course_id == _course_id, Member.team_id == _team_id))
    method = Team.query.filter(Team.course_id == _course_id).first()
    if request.method == 'GET':
        return render_template("set_contribution.html", submission_items=submission_items, members=members, student=student,method=method)
    else:
        contributions = request.form.getlist('select2')
        count = 0
        for submission in submission_items:
            for member in members:
                if contributions[count] == 'full':
                    contribution = 1.0
                elif contributions[count] == 'fair':
                    contribution = 0.67
                elif contributions[count] == 'little':
                    contribution = 0.33
                else:
                    contribution = 0
                with db.auto_commit():
                    submission_item_contribution = Contribution(contribution, submission.title, submission.percentage, _course_id, _team_id, member.email)
                    # insert into database
                    db.session.add(submission_item_contribution)
                count += 1
        return render_template("set_contribution.html", submission_items=submission_items, members=members, student=student,method=method)



