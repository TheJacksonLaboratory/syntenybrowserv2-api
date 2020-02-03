from sqlalchemy import *
from . import BASE


class CytogeneticBand(BASE):
    """ This class represents the 'cytogenetic_band' table. """

    __tablename__ = 'cytogenetic_band'

    id = Column(String, primary_key=True)
    taxon_id = Column(Integer, primary_key=True)
    chr = Column(String)
    source = Column(String)
    type = Column(String)
    start = Column(Integer)
    end = Column(Integer)
    location = Column(String)
    color = Column(String)
