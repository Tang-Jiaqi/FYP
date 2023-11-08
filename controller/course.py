from flask import Blueprint,render_template, request,session
from app.models.base import db
from app.models.course import Course
from app.models.teacher import Teacher


courseBP = Blueprint('course', __name__)


@courseBP.route('', methods=['GET','POST'])
def course_add():
    teacher = Teacher.query.filter(Teacher.email == session.get("email")).first()
    if request.method == 'GET':
        return render_template("course_add.html", teacher=teacher)
    else:
        id = request.form.get('id')
        name = request.form.get('name')
        teacher.course_id = teacher.course_id + ',' + id
        print(teacher.course_id)
        db.session.commit()
        with db.auto_commit():
                course = Course(name,id)
                db.session.add(course)
        return render_template("course_add.html", teacher=teacher)

