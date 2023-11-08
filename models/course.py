from sqlalchemy import Column, String, Integer, orm
from app.models.base import Base


class Course(Base):
    course_name = Column(String(50), nullable=False)
    course_id = Column(Integer, primary_key=True,autoincrement=True)

    def __init__(self, course_name, course_id):
        self.course_id = course_id
        self.course_name = course_name

    def display_students(self):
        pass


    def get_course_name(self):
        return self.course_name

    def get_course_id(self):
        return self.course_id