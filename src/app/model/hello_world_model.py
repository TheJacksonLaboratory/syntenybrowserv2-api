from . import Base
from sqlalchemy import *
from src import ma


class Hello(Base):
    __tablename__ = "hellos"

    id = Column(Integer, primary_key=True)
    when = Column(DateTime)
    who = Column(String)


class HelloSchema(ma.ModelSchema):
    class Meta:
        model = Hello
        strict = True
