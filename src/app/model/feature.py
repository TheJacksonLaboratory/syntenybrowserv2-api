from sqlalchemy import *
from . import BASE


class Feature(BASE):
    __tablename__ = 'feature'

    taxon_id = Column(Integer)
    seq_id = Column(String)
    source = Column(String)
    type = Column(String)
    start = Column(Integer)
    end = Column(Integer)
    score = Column(Float)
    strand = Column(String)
    phase = Column(Integer)
    id = Column(String, primary_key=True)
    name = Column(String)
    dbxref = Column(String)
    bio_type = Column(String)
    status = Column(String)
    parent = Column(String)
