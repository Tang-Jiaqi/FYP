from sqlalchemy import Column, String, Integer, orm,ForeignKey
from app.models.base import Base
from sqlalchemy.orm import relationship


# rubric item
class Item(Base):
    item_id = Column(Integer, primary_key=True,autoincrement=True)
    item_content = Column(String(50), nullable=False)
    percentage = Column(String(50), nullable=False)
    rubric_id = Column(Integer,ForeignKey('rubric.id', ondelete='CASCADE'))

    def __init__(self, item_content,percentage):
        self.item_content = item_content
        self.percentage = percentage


    def get_item_id(self):
        return self.item_id

    def get_item_content(self):
        return self.item_content