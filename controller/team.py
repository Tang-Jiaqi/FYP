from flask import Blueprint,render_template, request,session,redirect,url_for
import numpy as np
from app.models.base import db
from app.models.team import Team
from app.models.dividein import Divide
from app.models.teacher import Teacher
from app.models.student import Student
from app.models.member import Member
from sqlalchemy import or_,and_,all_,any_,func, not_

teamBP = Blueprint('team',__name__)


@teamBP.route('/form_team', methods=['GET', 'POST'])
def form_team():
    teacher = Teacher.query.filter(Teacher.email == session.get("email")).first()
    if request.method == 'GET':
        return render_template('form_team.html', teacher=teacher)
    else:
        members = Member.query.all()
        _course_id = session.get('course_id')
        _email = session.get('email')
        num = request.form.get('num')
        method = request.form.get('option')
        consider_gpa = request.form.get('option2')
        students = Student.query.filter(Student.course_id==_course_id)
        gpa = []
        offset_gpa = request.form.get('gpa')
        k = 0
        for student in students:
            k += 1
        group_number = k / int(num)
        if k % int(num) != 0:
            return redirect(url_for('.form_team_wrong', group_number=int(group_number), member_number=int(num), course_id=_course_id, method=method))
        else:
            if method == 'method2':
                if consider_gpa == 'consider':
                    for student in students:
                        temp = float(student.gpa)
                        gpa.append(temp)
                    class_gpa = np.mean(gpa)
                    count = 0
                    for i in range(int(group_number)):
                        for j in range(int(num)):
                            with db.auto_commit():
                                team = Team(i+1, i+1, students[count].id, _course_id, students[count].email, method)
                                members[count].team_id = i+1
                                db.session.commit()
                                # 数据库的insert操作
                                db.session.add(team)
                            count += 1
                else:
                    count = 0
                    for i in range(int(group_number)):
                        for j in range(int(num)):
                            with db.auto_commit():
                                team = Team(i, i, students[count].id, _course_id, students[count].email, method)
                                members[count].team_id = i
                                db.session.commit()
                                # 数据库的insert操作
                                db.session.add(team)
                            count += 1
            else:
                count = 0
                for i in range(int(group_number)):
                    for j in range(int(num)):
                        with db.auto_commit():
                            team = Team(i + 1, i + 1, students[count].id, _course_id, students[count].email, method)
                            members[count].team_id = i + 1
                            db.session.commit()
                            # 数据库的insert操作
                            db.session.add(team)
                        count += 1
        return render_template('form_team.html', teacher=teacher)


@teamBP.route('/?<int:group_number>?<int:member_number>?<int:course_id>?<string:method>', methods=['GET','POST'])
def form_team_wrong(group_number, member_number, course_id, method):
    teacher = Teacher.query.filter(Teacher.email == session.get("email")).first()
    if request.method == 'GET':
        return render_template('form_team_warning.html', group_number=group_number)
    else:
        students = Student.query.all()
        members = Member.query.all()
        member_number_list = request.form.getlist('member_num')
        team_id = 1
        count = 0
        for number in member_number_list:
            if number:
                for i in range(int(number)):
                    with db.auto_commit():
                        team = Team(team_id, team_id, students[count].id, course_id, students[count].email, method)
                        members[count].team_id = team_id
                        db.session.commit()
                        # 数据库的insert操作
                        db.session.add(team)
                        count += 1
                team_id += 1
            else:
                for i in range(int(member_number)):
                    with db.auto_commit():
                        team = Team(team_id, team_id, students[count].id, course_id, students[count].email, method)
                        members[count].team_id = team_id
                        db.session.commit()
                        # 数据库的insert操作
                        db.session.add(team)
                        count += 1
                team_id += 1
        return render_template('form_team.html', teacher=teacher)


@teamBP.route('/choose_team_member', methods=['GET', 'POST'])
def choose_team_member():
    _course_id = session.get('course_id')
    _email = session.get('email')
    him = Student.query.filter(Student.email == session.get("email")).first()
    good = Student.query.filter(Student.email==_email).first().name
    students = Student.query.filter(and_(Student.course_id==_course_id, not_(Student.email==_email)))
    if request.method == 'GET':
        return render_template('choose_team_member.html', students=students, good=good, him=him)
    else:
        return render_template('choose_team_member.html', students=students, good=good, him=him)
