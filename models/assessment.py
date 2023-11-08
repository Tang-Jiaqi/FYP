from flask import render_template, request
from sqlalchemy import Column, String, Integer, orm
from app.models.base import Base


class Assessment(Base):
    id = Column(Integer, autoincrement=True, primary_key=True)
    assessment_number = Column(Integer)
    leader_email = Column(String(50))

    def __init__(self, assessment_number, leader_email):
        self.assessment_number = assessment_number
        self.leader_email = leader_email
