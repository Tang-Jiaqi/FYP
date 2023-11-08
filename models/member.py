from sqlalchemy import Column, String, Integer, orm, Float
from app.models.student import Student


class Member(Student):
    contribution = Column(Float, nullable=False)
    team_id = Column(Integer)
    vote_number = Column(Integer, default=0)

    def __init__(self, contribution, name,  email, password, gpa, course_id, team_id):
        super(Member, self).__init__(name,  email, password, gpa, course_id)
        self.contribution = contribution
        self.team_id = team_id

