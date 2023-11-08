from sqlalchemy import Column, String, Integer, orm
from app.models.user import User

class Teacher(User):
    id = Column(Integer, primary_key=True, autoincrement=True)
    major = Column(String(50), nullable=False)
    course_id = Column(String(100), primary_key=True)

    def __init__(self, name, email, password,major):
        super(Teacher,self).__init__(name, email, password)
        self.major = major

