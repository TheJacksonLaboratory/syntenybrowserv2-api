from sqlalchemy import *
from . import BASE


class Feature(BASE):
    __tablename__ = 'feature'

    taxon_id = Column('taxon_id', Integer)
    seq_id = Column('seq_id', String)
    source = Column('soource', String)
    type = Column('type', String)
    start = Column('start', Integer)
    end = Column('end', Integer)
    score = Column('score', Float)
    strand = Column('strand', String)
    phase = Column('phase', Integer)
    id = Column('id', String)
    name = Column('name', String)
    dbxref = Column('dbxref', String)
    bio_type = Column('bio_type', String)
    status = Column('status', String)
    parent = Column('parent', String)
