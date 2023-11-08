from sqlalchemy import Column, String, Integer, orm
from app.models.base import Base

class Divide(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id =  Column(Integer, nullable=True)
    method_id = Column(Integer, nullable=True)

    def __init__(self,course_id,method_id):
        self.course_id = course_id
        self.method_id = method_id