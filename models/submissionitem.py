from sqlalchemy import Column, String, Integer, orm, Float
from app.models.base import Base


class Submissionitem(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50))
    percentage = Column(Float)
    course_id = Column(String(100))

    def __init__(self, title, percentage, course_id):
        super(Submissionitem, self).__init__()
        self.title = title
        self.percentage = percentage
        self.course_id = course_id
