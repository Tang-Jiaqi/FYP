from sqlalchemy import Column, String, Integer, orm
from app.models.base import Base


class Team(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    team_name = Column(String(50), nullable=True)
    team_id = Column(Integer, nullable=False)
    student_id = Column(Integer)
    course_id = Column(Integer, nullable=True)
    student_email = Column(String(24), nullable=True)
    method = Column(String(50))

    def __init__(self, team_name, team_id, student_id, course_id, student_email, method):
        self.team_name = team_name
        self.team_id = team_id
        self.student_id = student_id
        self.course_id = course_id
        self.student_email = student_email
        self.method = method

    def display_students(self):
        pass

    def set_team_name(self, team_name):
        self.team_name = team_name

    def get_team_name(self):
        return self.team_name

    def get_team_id(self):
        return self.team_id
