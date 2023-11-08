from sqlalchemy import Column, String, Integer, orm, Float
from app.models.base import Base



class Contribution(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50))
    percentage = Column(Float)
    course_id = Column(String(100))
    contribution = Column(Float, default=0)
    team_id = Column(Integer)
    s_email = Column(String(24))

    def __init__(self, contribution, title, percentage, course_id,team_id, s_email):
        self.title = title
        self.percentage = percentage
        self.course_id = course_id
        self.contribution = contribution
        self.team_id = team_id
        self.s_email = s_email

