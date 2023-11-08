from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from app.models.base import db
from app.models.student import Student
from app.models.teacher import Teacher
from app.models.course import Course
from sqlalchemy import or_, and_, all_, any_
import re

userBP = Blueprint('user', __name__)


@userBP.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form.get('email')
        _password = request.form.get('password')
        if re.match(r'[0-9a-zA-Z_]{0,19}@mail.uic.edu.hk', email):  # test email account
            result = Student.query.filter(and_(Student.email == email, Student._password == _password)).first()
            session["email"] = email
            if result == None:
                return render_template('login.html', msg='Login fail')
            else:
                return redirect(url_for("student.courseshow"))
        elif re.match(r'[0-9a-zA-Z_]{0,19}@uic.edu.hk', email):
            result = Teacher.query.filter(and_(Teacher.email == email, Teacher._password == _password)).first()
            session["email"] = email
            if result == None:
                return render_template('login.html', msg='Login fail')
            else:
                return redirect(url_for("teacher.courseshow"))
        else:
            return 'invalid email'


@userBP.route('/logout', methods=["GET"])
def logout():
    # set the session empty
    session["emial"] = ""
    # jump to the login page
    return redirect(url_for("user.login"))













