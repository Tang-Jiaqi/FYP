from sqlalchemy import Column, String, Integer, orm, Float
from app.models.member import Member


class Leader(Member):
    bonus = Column(Float, default=0)

    def __init__(self, bonus, contribution, name, email, password, gpa, course_id, team_id):
        super(Leader, self).__init__(contribution, name, email, password, gpa, course_id, team_id)
        self.bonus = bonus

