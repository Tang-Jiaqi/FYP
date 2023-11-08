from sqlalchemy import Column, String, Integer, orm
from app.models.base import Base

class User(Base):
    __abstract__ = True # 抽象类 不会生成表
    name = Column(String(50), nullable=False,unique=True)
    email = Column(String(24), unique=True, nullable=True,primary_key=True)
    _password = Column('password', String(10))


    def __init__(self, name,email, password):
        super(User,self).__init__()
        self.name = name
        self.email = email
        self._password = password

    def setPassword(self,password):
        super().set_attrs(password)

    def getPassword__(self, password):
        return super().__getitem__(password)