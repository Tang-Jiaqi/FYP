
from flask import Blueprint,render_template, request,session,redirect,url_for
from app.models.base import db
from app.models.student import Student
from app.models.course import Course
from app.models.team import Team
from sqlalchemy import or_,and_,all_,any_

studentBP = Blueprint('student',__name__)

@studentBP.route('/updatePassword',methods = ['GET','POST'])
def updatePassword():
    msg = ""
    _password = request.form.get('password')
    n_password = request.form.get('n_password')
    r_password = request.form.get('r_password')
    student = Student.query.filter(and_(Student.email == session.get("email"), Student._password == _password)).first()
    method = Team.query.filter(Team.course_id == session.get('course_id')).first()
    if request.method == 'GET':
        return render_template('updatepwd.html',student = student,msg = msg, method=method)
    else:
        if student:
            if len(n_password) < 11 and len(r_password) < 11:
                if _password != n_password:
                    if n_password == r_password:
                        msg = "Change successfully"
                        student._password = n_password
                        db.session.commit()
                        return  render_template('updatepwd.html', student=student,msg = msg,method=method)
                    else:
                        msg = "Not equal"
                        return  render_template('updatepwd.html', student = student,msg = msg,method=method)
                else:
                    msg = "wrong password"
                    return  render_template('updatepwd.html', student = student,msg = msg,method=method)
            else:
                msg = "New password over length."
                return render_template('updatepwd.html', student = student,msg = msg,method=method)
        else:
            msg = "wrong password"
            return  render_template('updatepwd.html', student = student,msg = msg,method=method)

@studentBP.route('/courseshow',methods = ['GET','POST'])
def courseshow():
    student = Student.query.filter(Student.email == session.get("email")).first()
    msg = ''
    if request.method == "POST":
        course = request.values.get('course')
        session["course_id"] = course
        print(course)
        if (course != None):
            return redirect(url_for("student.navigation"))
        else:
            msg = 'Please select a course'
            courses = []
            course = request.values.get('course')
            session["course_id"] = course
            if student.course_id:
                ids = student.course_id.split(",")
                for i in ids:
                    if i != "":
                        course = Course.query.filter(Course.course_id == int(i)).first()
                        courses.append(course)
            return render_template("student_course.html", student=student, courses=courses, msg=msg)
    else:
        courses = []
        course = request.values.get('course')
        session["course_id"] = course
        if student.course_id:
            ids = student.course_id.split(",")
            for i in ids:
                if i != "":
                    course = Course.query.filter(Course.course_id == int(i)).first()
                    courses.append(course)
        return render_template("student_course.html", student=student, courses=courses, msg=msg)

@studentBP.route('/navigation',methods = ['GET','POST'])
def navigation():
    course = session.get('course_id')
    print(course)
    student = Student.query.filter(Student.email == session.get("email")).first()
    method = Team.query.filter(Team.course_id == course).first()
    return render_template("navigation.html", method=method,student = student)