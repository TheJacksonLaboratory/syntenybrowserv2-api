from sqlalchemy import *
from sqlalchemy.orm import relationship
from . import BASE

on_pairs = Table(
    'on_pairs', BASE.metadata,
    Column('parent', String, ForeignKey('on_terms.id'), primary_key=True),
    Column('child', String, ForeignKey('on_terms.id'), primary_key=True))


class OntologyTerm(BASE):
    """ This class represents the 'on_terms' table. """

    __tablename__ = 'on_terms'

    id = Column(String, primary_key=True)
    name = Column(String)
    namespace = Column(String)
    definition = Column('def', String)

    descendants = relationship('OntologyTerm', secondary='on_pairs',
                               primaryjoin='OntologyTerm.id == on_pairs.c.parent',
                               secondaryjoin='OntologyTerm.id == on_pairs.c.child')
