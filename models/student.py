from sqlalchemy import Column, String, Integer, orm
from app.models.user import User


class Student(User):
    id = Column(Integer, primary_key=True, autoincrement=True)
    gpa = Column("GPA", String(50), nullable=True)
    course_id = Column(String(100), primary_key=True)

    def __init__(self, name, id, email, gpa, password, course_id):
        super(Student, self).__init__(name, email, password)
        self.id = id
        self.gpa = gpa
        self.course_id = course_id

    def jsonstr(self):
        jsondata = {
            'name': self.name,
            'email': self.email,
            'GPA': self.gpa,
            'password': self._password
        }
        return jsondata

