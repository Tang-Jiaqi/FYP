from sqlalchemy import Column, String, Integer, orm
from sqlalchemy.orm import relationship
from app.models.base import Base


class Rubric(Base):
    id = Column(Integer, primary_key=True,autoincrement=True)
    course_id = Column(String(100))
    rubric_name = Column(String(50), nullable=False)
    items = relationship('Item', backref='rubric', cascade="all, delete-orphan")

    def __init__(self, rubric_name,course_id):
        self.rubric_name = rubric_name
        self.course_id = course_id


    def get_id(self):
        return self.id

    def get_rubric_name(self):
        return self.rubric_name



