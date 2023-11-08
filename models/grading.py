from sqlalchemy import Column, String, Integer, orm, Float
from sqlalchemy.orm import relationship
from app.models.base import Base,db


class Grading(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer)
    course_id = Column(Integer)
    rubric_id = Column(Integer)
    team_id = Column(Integer,default=0)
    submission_id = Column(Integer)
    grade = Column(Float)
    selectitem = Column(String(300),nullable=True)# used to save ABCD

    def __init__(self, student_id,team_id, course_id, rubric_id, submission_id):
        super().__init__()
        self.student_id = student_id
        self.team_id = team_id
        self.course_id = course_id
        self.rubric_id = rubric_id
        self.submission_id = submission_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.remove(self)
        db.session.commit()