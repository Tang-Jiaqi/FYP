from flask import Blueprint, render_template, request, session, url_for, redirect, jsonify
from app.models.base import db
from app.models.contribution import Contribution
from app.models.submissionitem import Submissionitem
from app.models.teacher import Teacher
from app.models.course import Course
from app.models.student import Student
from app.models.member import Member
from app.models.team import Team
from app.models.leader import Leader
from app.models.rubric import Rubric
from app.models.grading import Grading
from app.models.item import Item
import xlrd, xlwt, os, json
from xlutils.copy import copy

basedir = os.path.abspath(os.path.dirname(__file__))

teacherBP = Blueprint('teacher', __name__)


@teacherBP.route('', methods=['GET'])
def get_teacher():
    with db.auto_commit():
        teacher = Teacher('Ben', 'ben@uic.edu.hk', '123456', 'CST')
        # 数据库的insert操作
        db.session.add(teacher)

    return 'hello teacher'


@teacherBP.route('/courseshow', methods=['GET', 'POST'])
def courseshow():
    teacher = Teacher.query.filter(Teacher.email == session.get("email")).first()
    msg = ''
    if request.method == "POST":
        course = request.values.get('course')
        session["course_id"] = course
        print(course)
        if (course != None):
            return redirect(url_for("teacher.navigation"))
        else:
            msg = 'Please select a course'
            courses = []
            course = request.values.get('course')
            session["course_id"] = course
            if teacher.course_id:
                ids = teacher.course_id.split(",")
                for i in ids:
                    if i != "":
                        course = Course.query.filter(Course.course_id == int(i)).first()
                        courses.append(course)
            return render_template("teacher_course.html", teacher=teacher, courses=courses, msg=msg)
    else:
        courses = []
        course = request.values.get('course')
        session["course_id"] = course
        if teacher.course_id:
            ids = teacher.course_id.split(",")
            for i in ids:
                if i != "":
                    course = Course.query.filter(Course.course_id == int(i)).first()
                    courses.append(course)
        return render_template("teacher_course.html", teacher=teacher, courses=courses, msg=msg)


@teacherBP.route("/navigation", methods=['GET', 'POST'])
def navigation():
    teacher = Teacher.query.filter(Teacher.email == session.get("email")).first()
    return render_template("navigation2.html", teacher=teacher)


@teacherBP.route("/generate_account", methods=['GET', 'POST'])
def generate_account():
    teacher = Teacher.query.filter(Teacher.email == session.get("email")).first()
    _password = '0000'
    if request.method == 'GET':
        return render_template("acc_generate.html", teacher=teacher)
    else:
        name = request.form.get('name')
        email = request.form.get('email')
        id = request.form.get('id')
        gpa = request.form.get('gpa')
        course_id = session.get('course_id')
        student = Student.query.filter(Student.email == email).first()
        if student != None:
            student.course_id = student.course_id + ',' + course_id
            print(student.course_id)
            db.session.commit()
            student = Student.query.filter(Student.email == session.get("email")).first()
            return render_template("acc_generate.html", teacher=teacher)
        else:
            with db.auto_commit():
                student1 = Student(name, id, email, gpa, _password, course_id)
                db.session.add(student1)
            return render_template("acc_generate.html", teacher=teacher)


@teacherBP.route("/import_file", methods=['GET', 'POST'])
def import_file():
    teacher = Teacher.query.filter(Teacher.email == session.get("email")).first()
    _password = '0000'
    course_id = session.get('course_id')
    if request.method == 'POST':
        file = request.files['file']
        f = file.read()
        data = xlrd.open_workbook(file_contents=f)
        table = data.sheets()[0]
        for i in range(1, table.nrows):
            name = table.cell(i, 0).value
            id = table.cell(i, 1).value
            email = table.cell(i, 2).value
            gpa = table.cell(i, 3).value
            with db.auto_commit():
                db.session.add(Student(name, id, email, gpa, _password, course_id))
        else:
            return render_template("import_file.html", teacher=teacher)
    else:
        return render_template("import_file.html", teacher=teacher)


@teacherBP.route('/export', methods=['POST', 'GET'])
def export():
    teacher = Teacher.query.filter(Teacher.email == session.get("email")).first()
    msg = ""
    if request.method == 'GET':
        return render_template("export.html", msg=msg, teacher=teacher)
    else:
        wb = xlwt.Workbook()
        ws = wb.add_sheet('Contribution File')

        first_col = ws.col(0)
        second_col = ws.col(1)
        third_col = ws.col(2)
        four_col = ws.col(3)

        # column width
        first_col.width = 128 * 20
        second_col.width = 230 * 20
        third_col.width = 230 * 20
        four_col.width = 128 * 20

        ws.write(0, 0, "name")
        ws.write(0, 1, "ID")
        ws.write(0, 2, "contribution")
        ws.write(0, 3, "bonus")

        data = Leader.query.filter(Leader.course_id == session.get("course_id")).all()
        if data is not None:
            for i in range(0, len(data)):
                stu = data[i]
                ws.write(i + 1, 0, stu.name)
                ws.write(i + 1, 1, stu.id)
                ws.write(i + 1, 2, stu.contribution)
                ws.write(i + 1, 3, stu.bonus)

                path = "/static/excel"
                fileName = "StudentInfo.xls"
                file_path = basedir + path

                if not os.path.exists(file_path):
                    os.makedirs(file_path)
                file_path = file_path + fileName

                try:
                    f = open(file_path, 'r')
                    f.close()
                except IOError:
                    f = open(file_path, 'w')
                    f.close()
                wb.save(file_path)
                msg = path + fileName
        return render_template("export.html", msg=msg, teacher=teacher)


@teacherBP.route("/add_rubric", methods=['GET', 'POST'])
def add_rubric():
    totalper = 0
    teacher = Teacher.query.filter(Teacher.email == session.get("email")).first()
    course_id = session.get('course_id')
    status = 0
    msg = "Add error"
    if request.method == 'GET':
        return render_template("add_rubric.html", teacher=teacher, msg=msg)
    else:
        # get form data
        rubric_name = request.form.get('rubric_name')
        item = request.form.get('item')
        per = request.form.get('per')
        # spilt data
        items = item.split("@#@")
        pers = per.split("@#@")
        for iper in pers:
            totalper += int(iper)
        # test the total percentage
        rubric = Rubric.query.filter(Rubric.rubric_name == rubric_name, Rubric.course_id == course_id).first()
        print(rubric)
        if totalper == 100:
            # add to database
            if rubric != None:
                msg = "The rubirc name has exsited."
            else:
                with db.auto_commit():
                    rubric = Rubric(rubric_name, course_id)
                    pi = 0
                    for iitem in items:
                        print(pers[pi])
                        tempitem = Item(iitem, pers[pi])
                        rubric.items.append(tempitem)
                        pi = pi + 1
                    db.session.add(rubric)
                status = 1
                msg = "Add successfully!"
        else:
            msg = "The total percentage must be 100%!"

        ret = {"status": status, "msg": msg}
        return json.dumps(ret)


@teacherBP.route("/rubric_file", methods=['GET', 'POST'])
def rubric_file():
    teacher = Teacher.query.filter(Teacher.email == session.get("email")).first()
    course_id = session.get('course_id')
    name = request.form.get('name')

    if request.method == 'POST':
        file = request.files['file']
        f = file.read()
        data = xlrd.open_workbook(file_contents=f)
        table = data.sheets()[0]
        rubric = Rubric(name, course_id)
        data = []
        for i in range(0, table.nrows):
            item = table.cell(i, 0).value
            per = table.cell(i, 1).value
            items = Item(item, per)
            temp = {'item_content': item, 'percentage': per}
            print(temp)
            data.append(temp)
            with db.auto_commit():
                rubric.items.append(items)
        else:
            with db.auto_commit():
                db.session.add(rubric)
            aJson = json.dumps(data)
            return redirect("/teacher/rubric_file?contents=" + aJson + "&name=" + name)
    else:
        contents = request.args.get('contents')
        name = request.args.get('name')
        check = 0
        if contents is not None:
            check = 1
            contents = json.loads(contents)
            return render_template("rubric_file.html", teacher=teacher, check=check, contents=contents, name=name)
        else:
            return render_template("rubric_file.html", teacher=teacher, check=check)


@teacherBP.route("/edit_rubric", methods=['GET', 'POST'])
def edit_rubric():
    if request.method == 'GET':
        rubric_id = request.args.get('rubric_id')

        teacher = Teacher.query.filter(Teacher.email == session.get("email")).first()
        items = []
        rubrics = Rubric.query.filter(Rubric.status == 1).all()

        if rubric_id != "" and rubric_id is not None:
            items = Item.query.filter(Item.status == 1, Item.rubric_id == rubric_id).all()
        return render_template("edit_rubric.html", teacher=teacher, items=items, rubrics=rubrics, rubric_id=rubric_id)


@teacherBP.route("/edit_rubric_item", methods=['GET', 'POST'])
def edit_rubric_item():
    if request.method == 'GET':
        rubric_id = request.args.get('rubric_id')
        teacher = Teacher.query.filter(Teacher.email == session.get("email")).first()
        rubric = Rubric.query.filter(Rubric.id == rubric_id).first()
        items = Item.query.filter(Item.rubric_id == rubric_id, Item.status == 1).all()
        return render_template("edit_rubric_item.html", teacher=teacher, rubric_id=rubric_id, rubric=rubric,
                               items=items)
    else:
        totalper = 0
        status = 0
        msg = "Edit error"
        item = request.form.get('item')
        per = request.form.get('per')
        item_id = request.form.get('item_id')
        rubric_id = request.form.get('rubric_id')
        # spilt data
        items = item.split("@#@")
        pers = per.split("@#@")
        item_ids = item_id.split("@#@")
        for iper in pers:
            totalper += int(iper)
        # test the total percentage
        if totalper == 100:
            # add to database
            with db.auto_commit():
                pi = 0
                allitems = Item.query.filter(Item.rubric_id == rubric_id).all()
                for allitem in allitems:
                    atemp = Item.query.get(allitem.item_id)
                    atemp.status = 0
                    db.session.commit()

                for iitem in items:
                    print(pers[pi])
                    temp = Item.query.get(item_ids[pi])
                    if temp is None:
                        tempitem = Item(iitem, pers[pi])
                        tempitem.item_id = item_ids[pi]
                        tempitem.rubric_id = rubric_id
                        tempitem.status = 1
                        db.session.commit()
                        db.session.add(tempitem)
                    else:
                        temp.item_id = item_ids[pi]
                        temp.item_content = iitem
                        temp.percentage = pers[pi]
                        temp.rubric_id = rubric_id
                        temp.status = 1
                        db.session.commit()
                    pi = pi + 1

            status = 1
            msg = "Edit successfully!"
        else:
            msg = "The total percentage must be 100%!"

        ret = {"status": status, "msg": msg}
        return json.dumps(ret)


@teacherBP.route("/delete_rubric", methods=['GET', 'POST'])
def delete_rubric():
    if request.method == 'GET':
        teacher = Teacher.query.filter(Teacher.email == session.get("email")).first()
        rubric = Rubric.query.all()
        return render_template("delete_rubric.html", teacher=teacher, rubric=rubric)
    else:
        rid = request.form.get('id')
        if rid:
            rubric = Rubric.query.filter(Rubric.id == int(rid)).first()
            if rubric:
                db.session.delete(rubric)
                db.session.commit()
                return jsonify({
                    'status': 1,
                    'data': {}
                })
    return jsonify({
        'status': 0,
        'data': {}
    })


@teacherBP.route("/edit_item", methods=['GET', 'POST'])
def edit_item():
    if request.method == 'GET':
        iid = request.args.get('id')
        item = Item.query.filter(Item.item_id == int(iid)).first()
        teacher = Teacher.query.filter(Teacher.email == session.get("email")).first()
        return render_template("edit_item.html", item=item, teacher=teacher)
    else:
        item_id = request.form.get('item_id')
        item_content = request.form.get('item_content')
        percentage = request.form.get('percentage')
        if item_id:
            item = Item.query.filter(Item.item_id == int(item_id)).first()
            if item_id:
                item.item_content = item_content
                item.percentage = percentage
                db.session.commit()
                return jsonify({
                    'status': 1,
                    'msg': "Edit Successfully"
                })
    return jsonify({
        'status': 0,
        'msg': "Fail"
    })


@teacherBP.route("/del_item", methods=['POST'])
def del_item():
    if request.method == 'POST':
        iid = request.form.get('id')
        if iid:
            item = Item.query.filter(Item.item_id == int(iid)).first()
            if item:
                db.session.delete(item)
                db.session.commit()
                return jsonify({
                    'status': 1,
                    'msg': "Delete Successfully,but the total perentage is not 1."
                })
    return jsonify({
        'status': 0,
        'msg': "Fail"
    })


@teacherBP.route("/grading", methods=['GET', 'POST'])
def grading():
    submissionid = request.args.get('submissionid', "")
    rubricid = request.args.get('rubricid', "")
    # studentid = request.args.get('studentid', "")
    course_id = session.get('course_id')
    teamid = request.args.get('teamid', "")
    print(submissionid, rubricid, teamid, course_id)

    if teamid == "undefined":
        teacher = Teacher.query.filter(Teacher.email == session.get("email")).first()
        subms = Submissionitem.query.all()
        return render_template("homework_select.html", teacher=teacher, submission=subms)
    # student = Student.query.filter_by(id=int(studentid)).first()
    team = Team.query.filter_by(team_id=int(teamid)).first()

    if request.method == 'GET':
        teacher = Teacher.query.filter(Teacher.email == session.get("email")).first()
        g = Grading.query.filter_by(team_id=int(teamid), course_id=int(course_id), rubric_id=int(rubricid),
                                    submission_id=int(submissionid)).first()
        savevalue = ''
        if g:
            savevalue = g.selectitem  # used to save ABCD
            print(savevalue)
        if rubricid and rubricid != 'undefined':
            rubric = Rubric.query.filter_by(id=int(rubricid)).first()
            ritems = rubric.items
        else:
            ritems = Item.query.all()

        return render_template("grading_page.html", teacher=teacher, items=ritems, submissionid=submissionid,
                               rubricid=rubricid, teamid=teamid, team=team, savevalue=savevalue)
    else:
        rubricnum = request.form.get('rubricnum')
        data = request.form.get('data')
        grade = request.form.get('grade', 0)
        selectitem = request.form.get('selectitem')
        print(request.form)
        print(json.loads(data))

        submission = Submissionitem.query.filter_by(id=int(submissionid)).first()
        filename = "grading-" + submission.title + ".xls"
        rubric = Rubric.query.filter_by(id=int(rubricid)).first()

        contri = Contribution.query.filter_by(course_id=int(course_id), title=submission.title).all()

        if os.path.isfile(filename):
            grades = xlrd.open_workbook(filename)
            sheets = grades.sheet_by_index(0)
            # print(sheet.name, sheet.nrows, sheet.ncols)
            workbook = copy(grades)
            sheet = workbook.get_sheet(0)
            nrow = sheets.nrows
        else:
            workbook = xlwt.Workbook()
            sheet = workbook.add_sheet("Sheet1")
            # sheet.write(0, 0, "submission")
            # heet.write(0, 1, "rubric")
            sheet.write(0, 0, "team")
            sheet.write(0, 1, "student")
            sheet.write(0, 2, "grade")
            nrow = 1

        s_team = Team.query.filter_by(team_id=int(teamid)).all()
        for s_t in s_team:
            s_contri = Contribution.query.filter_by(s_email=s_t.student_email).first()
            if not s_contri:
                return jsonify({
                    "status": 0,
                    "msg": "you have not set contribution for the team"
                })
            contr = Contribution.query.filter_by(s_email=s_t.student_email,course_id=course_id,title=submission.title).first()
            if not contr:
                print("not found contr\n\n")
            student_ = Student.query.filter_by(email=s_t.student_email).first()
            s_grade = round(float(grade) * contr.contribution,2)
            sheet.write(nrow, 0, team.team_name)
            sheet.write(nrow, 1, student_.name)
            sheet.write(nrow, 2, str(s_grade))
            nrow = nrow + 1
            oldg = Grading.query.filter_by(team_id=int(teamid), course_id=int(course_id), rubric_id=int(rubricid),
                                           submission_id=int(submissionid),student_id=student_.id).first()
            if not oldg:
                g = Grading(student_id=student_.id,team_id=int(teamid), course_id=int(course_id), rubric_id=int(rubricid),
                            submission_id=int(submissionid))
                g.selectitem = selectitem
                g.grade = round(float(s_grade),2)
                g.save()
            else:
                oldg.selectitem = selectitem
                oldg.grade = round(float(s_grade),2)
                oldg.student_id = student_.id
                oldg.team_id = int(teamid)
                oldg.save()
        workbook.save(filename)
        return jsonify({
            'status': 1,
            'data': {}
        })


@teacherBP.route("/rubric_select", methods=['GET', 'POST'])
def rubric_select():
    submissionid = request.args.get('submissionid', "")
    teacher = Teacher.query.filter(Teacher.email == session.get("email")).first()
    rubric = Rubric.query.all()
    course_id = session.get('course_id')

    g = Grading.query.filter_by(course_id=int(course_id),
                                submission_id=int(submissionid)).first()
    select_rubric_id = -1
    if g:
        select_rubric_id = g.rubric_id

    return render_template("rubric_select.html", teacher=teacher, rubric=rubric, submissionid=submissionid,
                           select_rubric_id=select_rubric_id)


@teacherBP.route("/homework_select", methods=['GET', 'POST'])
def homework_select():
    teacher = Teacher.query.filter(Teacher.email == session.get("email")).first()
    subms = Submissionitem.query.filter(Submissionitem.course_id == session.get("course_id"))
    teams = Team.query.filter(Team.course_id == session.get("course_id")).order_by(Team.team_id.desc()).first()
    course_id = int(session.get('course_id'))
    team_cnt = teams.team_id + 1
    
    newsubms = []
    for sub in subms:
        tmp = {
            "id": sub.id,
            "title": sub.title,
            "percentage": sub.percentage,
            "course_id": sub.course_id,
            "status": 0  # 0 is not start  1 is processing 2 is finish
        }
        g_teams = Grading.query.filter_by(course_id=course_id, submission_id=sub.id).all()
        # teams filter
        team_ids = set()
        
        for t in g_teams:
            team_ids.add(t.team_id)
        
        g_teams_cnt = len(team_ids)
        print(g_teams_cnt)
        print(team_cnt)
        if (g_teams_cnt == 0):  # 没有打分
            tmp["status"] = 0
        elif g_teams_cnt == team_cnt:  # finish
            tmp["status"] = 2
        else:
            tmp["status"] = 1
        newsubms.append(tmp)
    return render_template("homework_select.html", teacher=teacher, submission=newsubms)

@teacherBP.route("/team_select", methods=['GET', 'POST'])
def team_select():
    submissionid = request.args.get('submissionid', "")
    rubricid = request.args.get('rubricid', "")
    course_id = session.get('course_id')
    print(submissionid, rubricid, course_id)
    if not course_id or not submissionid or not rubricid:
        return "error session 失效，重新登录"
    teacher = Teacher.query.filter(Teacher.email == session.get("email")).first()
    # student = Student.query.all()
    teams_ids = set()
    teams = Team.query.filter_by(course_id=int(course_id)).all()
    # filter team's ids
    for t in teams:
        teams_ids.add(t.team_id)
    # filter team
    newteams = []
    for tid in teams_ids:
        t = Team.query.filter_by(team_id=tid).first()
        newteams.append(t)
    data = []
    for s in newteams:
        g = Grading.query.filter_by(team_id=s.team_id, course_id=int(course_id), rubric_id=int(rubricid),
                                    submission_id=int(submissionid)).first()
        if g:
            disable = True
        else:
            disable = False
        tmp = {"id": s.team_id, "name": s.team_name, "disable": False}  # True change to allow change
        data.append(tmp)
    return render_template("team_select.html", teacher=teacher, team=data, submissionid=submissionid,
                           rubricid=rubricid)


@teacherBP.route("/showtotal", methods=['GET', 'POST'])
def showtotal():
    course_id = session.get('course_id')
    course_id = int(course_id)
    print(course_id)
    all_submission = Submissionitem.query.filter_by(course_id=course_id).all()
    student = Member.query.all()
    student_cnt = len(student)
    if len(all_submission) == 0:
        return jsonify({
            "status": 0,
            "msg": "dont have a submission"
        })
    for submiss in all_submission:
        # total_grade = 0
        g = Grading.query.filter_by(course_id=course_id, submission_id=submiss.id).all()
        if len(g) == student_cnt:
            continue
        else:
            return jsonify({
                "status": 0,
                "msg": "not finish the grading process"
            })

    if os.path.isfile("student_grad.xls"):
        grades = xlrd.open_workbook("student_grad.xls")
        sheets = grades.sheet_by_index(0)
        # print(sheet.name, sheet.nrows, sheet.ncols)
        workbook = copy(grades)
        sheet = workbook.get_sheet(0)
        nrow = sheets.nrows
    else:
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet("Sheet1")
        sheet.write(0, 0, "course")
        sheet.write(0, 1, "student")
        sheet.write(0, 2, "team")
        sheet.write(0, 3, "grade")
        nrow = 1

    for s in student:
        course_grade = 0
        g = Grading.query.filter_by(course_id=course_id, student_id=s.id).all()
        for grade in g:
            sub = Submissionitem.query.filter_by(id=grade.submission_id).all()
            for su in sub:
                course_grade = round(course_grade + grade.grade * su.percentage,2)
        course_name = Course.query.filter_by(course_id=course_id).first().course_name
        sheet.write(nrow, 0, course_name)
        sheet.write(nrow, 1, s.name)
        sheet.write(nrow, 2, str(s.team_id))
        sheet.write(nrow, 3, str(course_grade))
        nrow = nrow + 1
    workbook.save("student_grad.xls")

    return jsonify({
        "status": 1,
        "data": ''
    })
